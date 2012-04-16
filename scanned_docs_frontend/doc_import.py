#!/usr/bin/python
# -*- coding: utf-8 -*-

from five import grok
from logging import getLogger
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.statusmessages.interfaces import IStatusMessage
from urllib import urlopen as url
from zope.interface import Interface
import json
import transaction

list_service = \
    u'http://localhost:6547/doc?page=%(page)i&filter=%(filter)s'
doc_service = u'http://localhost:6547/doc?id=%(id)s'

logger = getLogger(__name__)


class DocImport(grok.View):

    grok.context(Interface)
    grok.require('zope2.View')

    def update(self):
        msgs = IStatusMessage(self.request)
        if 'id' in self.request.form:
            try:
                return self.handle_import(self.request.form['id'])
            except (ValueError, IOError), e:
                msgs.addStatusMessage('Error: %s' % str(e), type='error'
                        )
                transaction.abort()

        start = int(self.request.get('b_start', 0))
        self.filter = self.request.get('filter', '')
        try:
            reply = url(list_service % dict(page=start / 10,
                        filter=self.filter))
            reply_data = reply.read()
            data = json.loads(reply_data)
        except ValueError, e:
            msgs.addStatusMessage('Error: %s' % str(e), type='error')
            self.results = []
            logger.error(reply_data)
            return
        except IOError, e:
            msgs.addStatusMessage('Error: %s' % str(e), type='error')
            self.results = []
            return
        self.totals = data['total']
        size = 10
        results = [None for x in range(start)] + data['results'] \
            + [None for x in range(min(max(0, self.totals - size),
               self.totals - start + size))]
        self.results = Batch(results, size, start)

    def handle_import(self, id):
        reply = url(doc_service % dict(id=id))
        reply_data = reply.read()
        data = json.loads(reply_data)['results'][0]
        user = self.getUser(data['owner_mail'])
        new_ob = self.createObject(data['title'])
        new_ob.setDescription(data['description'])
        new_ob.setTitle(data['title'])
        new_ob.setFile(url(data['resource_url']).read())
        new_ob.setFilename(data['filename'].encode('utf-8'))
        for (group, roles) in json.loads(data['local_roles']).items():
            new_ob.manage_setLocalRoles(group, roles)
        new_ob.changeOwnership(user)
        new_ob.setCreators(tuple(user.getUserId()))
        return self.request.response.redirect(new_ob.absolute_url()
                + '/view')

    def createObject(self, title):
        new_id = self.context.invokeFactory('File', title)
        return self.context[new_id]

    def getUser(self, email):
        user_tool = getToolByName(self.context, 'acl_users')
        member_tool = getToolByName(self.context, 'portal_membership')

        search_results = user_tool.searchUsers(email=email)
        if len(search_results) > 1:
            raise ValueError('More than one person has the email "%s"'
                             % email)
        if not search_results:
            return member_tool.getAuthenticatedMember()
        else:
            return user_tool.getUserById(search_results[0]['id'])

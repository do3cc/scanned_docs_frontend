from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IScannedDocsFrontend(Interface):

    list_service = schema.TextLine(title=u"Listing URL",
         description=u"The url to call for getting a document listing.", 
         default=u'http://localhost:6547/doc?page=%(page)i&filter=%(filter)s')
    doc_service = schema.TextLine(title=u"Document URL",
        description=u"The url to call for getting a document.", 
        default=u'http://localhost:6547/doc?id=%(id)s')


class ScannedDocsPanelForm(RegistryEditForm):
    schema = IScannedDocsFrontend

ScannedDocsPanelView = layout.wrap_form(ScannedDocsPanelForm, ControlPanelFormWrapper)
ScannedDocsPanelView.label = u"Scanned Docs Frontend settings"

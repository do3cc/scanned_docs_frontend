"""

	Plone views overrides.

	For more information see

	* http://collective-docs.readthedocs.org/en/latest/views/browserviews.html

"""

# Zope imports
from zope.interface import Interface
from five import grok
from Products.CMFCore.interfaces import ISiteRoot

# Local imports
from scanned_docs_frontend.interfaces import IAddonSpecific, IThemeSpecific

grok.templatedir("templates")
grok.layer(IThemeSpecific)

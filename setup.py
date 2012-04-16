from setuptools import setup

setup(name = "scanned_docs_frontend",
    version = "0.1",
    description = "A plone frontend to the scanned docs web service",
    author = "Patrick Gerken",
    author_email = "gerken@patrick-gerken.de",
    url = "",
    install_requires = ["five.grok",
        "Products.CMFCore",
        "Products.CMFPlone",
        "Products.statusmessages",
        "plone.app.layout",
        "plone.theme",
        "zope.component",
        "zope.interface",
        "zope.schema",
        "plone.z3cform",
        "plone.app.registry"],
    packages = ['scanned_docs_frontend'],
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],     
    license="BSD",
    include_package_data = True,
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,        
) 

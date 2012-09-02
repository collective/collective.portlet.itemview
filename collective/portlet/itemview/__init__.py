from zope.i18nmessageid import MessageFactory

messageFactory = MessageFactory("collective.portlet.itemview")

from Products.CMFCore.permissions import setDefaultRoles
setDefaultRoles('collective.portlet.itemview: Add itemview portlet',
                ('Manager', 'Site Administrator', 'Owner',))

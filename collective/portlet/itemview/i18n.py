from zope.i18nmessageid import MessageFactory
messageFactory = MessageFactory('collective.portlet.itemview')
_ = messageFactory

portlet_title          = _(u"portlet_title", default=u"Item portlet view")
portlet_description    = _(u"portlet_description", default=u"A portlet which can render an item.")
portlet_target_title   = _(u"Item")
portlet_target_desc    = _(u"portlet_target_desc", default=u"Find an item to display")
portlet_viewname_title = _(u"View")
portlet_viewname_desc  = _(u"portlet_viewname_desc", default=u"view used to render this item")

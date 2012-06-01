from plone.portlets.interfaces import IPortletDataProvider
from zope import component
from zope import schema
from zope import interface
from zope.formlib import form
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.itemview import i18n

import logging
logger = logging.getLogger('collective.portlet.itemview')

class IItemViewPortlet(IPortletDataProvider):

    target = schema.Choice(
        title=i18n.portlet_target_title,
        description=i18n.portlet_target_desc,
        required=True,
        source=SearchableTextSourceBinder(
            {},
            default_query='path:'))

    viewname = schema.Choice(
        title=i18n.portlet_viewname_title,
        description=i18n.portlet_viewname_desc,
        required=True,
        default="itemview_portlet",
        vocabulary="collective.portlet.itemview.vocabulary.templateview")

def getTarget(portal, target_path):
    if not target_path:
        return None

    if target_path.startswith('/'):
        target_path = target_path[1:]

    if not target_path:
        return None

    if isinstance(target_path, unicode):
        #restrictedTraverse accept only strings
        target_path = str(target_path)
    return portal.restrictedTraverse(target_path, default=None)

class Assignment(base.Assignment):
    interface.implements(IItemViewPortlet)

    viewname = "itemview_portlet"
    target = None

    def __init__(self,target=None, viewname="itemview_portlet"):
        self.target = target
        self.viewname = viewname
    
    @property
    def title(self):
        if self.target:
            portal = component.getSiteManager()
            try:
                target = getTarget(portal, self.target)
            except AttributeError:
                #TODO: need to work out why we can't always get the portal
                if isinstance(self.target, basestring):
                    title = self.target
                    if title.startswith('/'):
                        title = title[1:]
                    return title
                else:
                    target = None
            if target:
                return target.Title()
        return i18n.portlet_title

class Renderer(base.Renderer):

    def render(self):
        viewname = self.data.viewname
        if not viewname: viewname="itemview_portlet"

        target = self.target()
        if target is None:
            return ""

        try:
            view = component.getMultiAdapter((target, self.request),
                                        name=viewname)
            return view()
        except component.ComponentLookupError, e:
            logger.error('no %s for %s'%(viewname, target.portal_type))

        return ""

    @memoize
    def target(self):
        """ get the collection the portlet is pointing to"""

        target_path = self.data.target
        portal_state = component.getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        return getTarget(portal, target_path)


class AddForm(base.AddForm):
    form_fields = form.Fields(IItemViewPortlet)
    form_fields['target'].custom_widget = UberSelectionWidget

    label = i18n.portlet_addform_title
    description = i18n.portlet_addform_desc

    def create(self, data):
        return Assignment( target=data.get("target"), 
                viewname=data.get("viewname", "itemview_portlet") )

class EditForm(base.EditForm):
    form_fields = form.Fields(IItemViewPortlet)
    form_fields['target'].custom_widget = UberSelectionWidget

    label = i18n.portlet_editform_title
    description = i18n.portlet_editform_desc

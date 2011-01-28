from plone.portlets.interfaces import IPortletDataProvider
from zope import component
from zope import schema
from zope import interface
from zope.formlib import form
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.itemview import vocabulary

class IItemViewPortlet(IPortletDataProvider):
    header = schema.TextLine(
        title=u"Portlet header",
        description=u"Title of the rendered portlet",
        required=True)

    target = schema.Choice(
        title=u"Target Item",
        description=u"Find the collection which provides the items to list",
        required=True,
        source=SearchableTextSourceBinder(
            {},
            default_query='path:'))

    templateview = schema.Choice(
        title=u"Template View",
        description=u"Template used to render this item",
        required=True,
        vocabulary="collective.portlet.itemview.vocabulary.templateview")

class Assignment(base.Assignment):
    interface.implements(IItemViewPortlet)


    header = u""
    target = None
    templateview = base

    def __init__(self, header=u"", target=None, templateview="base"):
        self.header = header
        self.target = target
        self.templateview = templateview

class Renderer(base.Renderer):

    index = ViewPageTemplateFile('itemview.pt')

    def render(self):
        import pdb;pdb.set_trace()
        template = component.getUtility(vocabulary.ITemplateView,
                                        name=self.data.templateview)
        if template is None:
            return index()
        return xhtml_compress(template())

class AddForm(base.AddForm):
    form_fields = form.Fields(IItemViewPortlet)
    form_fields['target'].custom_widget = UberSelectionWidget
    label = u"Add Item View portlet"
    description = u"This portlet displays an item with a selected view"

    def create(self, data):
        return Assignment()

class EditForm(base.EditForm):
    form_fields = form.Fields(IItemViewPortlet)
    form_fields['target'].custom_widget = UberSelectionWidget
    label = u"Edit Item View Portlet"
    description = u"This portlet displays an item with a selected view."

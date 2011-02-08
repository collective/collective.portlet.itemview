from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.site.hooks import getSite
from zope import component
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope import interface

class ITemplateView(interface.Interface):

    id = schema.ASCIILine(title=u"id")
    name = schema.TextLine(title=u"title")

class DefaultTemplate(object):
    interface.implements(ITemplateView)

    id = "itemview_portlet"
    name = u"Default template"

class Vocabulary(object):
    """    """
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        templates = component.getUtilitiesFor(ITemplateView)
        items = [SimpleTerm(item[1].id, item[1].id, item[1].name) for item in templates]
        return SimpleVocabulary(items)

VocabularyFactory = Vocabulary()

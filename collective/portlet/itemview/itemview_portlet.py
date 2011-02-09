from plone.memoize.instance import memoize
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class DefaultItemView(BrowserView):
    """default view"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def title(self):
        return self.context.Title()

    def description(self):
        return self.context.Description()
    
    def url(self):
        return self.context.absolute_url()
    
class TopicItemView(DefaultItemView):

    @memoize
    def results(self):
        results = self.context.queryCatalog()
        if len(results)>5:
            results = results[:4]
        return results

class FolderItemView(DefaultItemView):

    @memoize
    def results(self):
        results = self.context.getFolderContents()
        if len(results)>5:
            results = results[:4]
        return results

class FileItemView(DefaultItemView):

    def content_type(self):
        return self.context.get_content_type()

    def size(self):
        size = self.context.get_size()
        return '%s kb (%s bytes)'%(size/1024, size)

    def icon_url(self):
        return self.context.portal_url() +'/'+ self.context.getIcon()

    def filename(self):
        return self.context.getFilename()

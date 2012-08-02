from datetime import datetime

from Products.Five.browser import BrowserView

from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.layout.navigation.root import getNavigationRootObject

from collective.suggestions import SuggestionsMessageFactory as _
from ..interfaces import ISuggestionsStorage
from Products.CMFCore.interfaces._content import IContentish, IFolderish


class SuggestActions(BrowserView):

    def add(self):
        request = self.request
        view = request.get('view', '')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        ISuggestionsStorage(site).add_suggestion(
                id=IUUID(self.context),
                type='uid',
                view=view,
                date=datetime.now())

        if IFolderish(self.context):
            IStatusMessage(self.request).addStatusMessage(
                        _("The folder has been added to suggestions"))
        elif IContentish(self.context):
            IStatusMessage(self.request).addStatusMessage(
                        _("The document has been added to suggestions"))
        else:
            IStatusMessage(self.request).addStatusMessage(
                        _("The element has been added to suggestions"))

        self.request.response.redirect(self.context.absolute_url() + '/' + view)

    def remove(self):
        request = self.request
        view = request.get('view', '')
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        ISuggestionsStorage(site).remove_suggestion(id=IUUID(self.context))
        IStatusMessage(self.request).addStatusMessage(
                    _("The element has been removed from suggestions"))
        self.request.response.redirect(self.context.absolute_url() + '/' + view)
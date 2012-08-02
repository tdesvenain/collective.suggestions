from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ..interfaces import ISuggestionsStorage


class SwitchSuggest(ViewletBase):

    index = ViewPageTemplateFile('switchsuggest.pt')

    def update(self):
        super(SwitchSuggest, self).update()
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        self.template = self.request.steps[-1]
        self.issuggestion = ISuggestionsStorage(site).is_suggestion(
                                                             IUUID(self.context))
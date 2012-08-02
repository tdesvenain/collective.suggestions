from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.formlib import form

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.portlets.portlets import base

from collective.suggestions import SuggestionsMessageFactory as _
from collective.suggestions.interfaces import ISuggestionsStorage
from Products.CMFPlone.utils import normalizeString


class ISuggestionsPortlet(IPortletDataProvider):

    pass


class Assignment(base.Assignment):
    implements(ISuggestionsPortlet)

    @property
    def title(self):
        return _(u"Suggested content")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('suggestions.pt')

    title = _("Suggestions")

    @property
    def anonymous(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.anonymous()

    @property
    def available(self):
        return not self.anonymous and len(self._data())

    def suggestions_items(self):
        return self._data()

    def get_suggestions_infos(self, context, suggestions_list):
        """Return content infos
        """
        suggestions_dict = dict([(f['id'], f) for f in suggestions_list])
        ctool = getToolByName(context, 'portal_catalog')
        portal_url = getToolByName(context, 'portal_url')()
        brains = ctool.unrestrictedSearchResults(UID=[f['id'] for f in suggestions_list])

        infos = []
        for brain in brains:
            uid = brain.UID
            icon_url = brain.getIcon and "%s/%s" % (portal_url, brain.getIcon) or None
            info = {'url': brain.getURL() + '/' + suggestions_dict[uid].get('view', ''),
                    'description': brain.Description,
                    'title': brain.Title,
                    'icon': icon_url,
                    'class': 'contenttype-%s' % brain.portal_type.lower(),
                    'index': '%s-%s' % (brain.portal_type,
                                        normalizeString(brain.Title,
                                                        context=context))
                    }
            infos.append(info)

        return infos

    @memoize
    def _data(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        suggestions_list = ISuggestionsStorage(site).list_suggestions()

        suggestions_infos = self.get_suggestions_infos(self.context, suggestions_list)
        suggestions_infos.sort(key=lambda x: x['index'])
        return suggestions_infos


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ISuggestionsPortlet)
    label = _(u"Add Suggestions Portlet")
    description = _(u"This portlet displays the documents webmasters have suggested.")

    def create(self):
        return Assignment()
from persistent.dict import PersistentDict
from persistent.list import PersistentList

from zope.interface import implements
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations

from plone.app.layout.navigation.interfaces import INavigationRoot

from .interfaces import ISuggestionsStorage


SUGGESTIONS_KEY = 'collective.suggestions'

class SuggestionsStorage(object):

    adapts(INavigationRoot)
    implements(ISuggestionsStorage)

    def __init__(self, context):
        self.annotations = IAnnotations(context)

    def add_suggestion(self, id, type, **kwargs):
        value = PersistentDict(type=type,
                               id=id,
                               **kwargs)

        if self.is_suggestion(id):
            self.remove_suggestion(id)

        self.annotations[SUGGESTIONS_KEY].append(value)

    def remove_suggestion(self, id):
        suggestions_list = self.list_suggestions()
        for num, value in enumerate(suggestions_list):
            if value['id'] == id:
                break
        else:
            raise KeyError, "No value for %s in suggestions" % (id,)

        suggestions_list.remove(suggestions_list[num])
        self.annotations[SUGGESTIONS_KEY] = suggestions_list

    def is_suggestion(self, id):
        suggestions_list = self.list_suggestions()
        for num, value in enumerate(suggestions_list):
            if value['id'] == id:
                return True
        else:
            return False

    def list_suggestions(self):
        if not SUGGESTIONS_KEY in self.annotations:
            self.annotations[SUGGESTIONS_KEY] = PersistentList()

        return self.annotations[SUGGESTIONS_KEY]

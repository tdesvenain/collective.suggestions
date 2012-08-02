from zope.interface import Interface


class ISuggestionsStorage(Interface):
    """Adapts view, context and request to get
    """

    def add_suggestion(type, id, date, **kwargs):
        """Add a suggestion of a certain type
        """

    def remove_suggestion(id, **kwargs):
        """Remove a suggestion
        """

    def list_suggestions():
        """List all suggestions
        """
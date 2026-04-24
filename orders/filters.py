from rest_framework import filters

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.user.is_staff:
            return ['id', 'email']
        return ['id']

from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 2

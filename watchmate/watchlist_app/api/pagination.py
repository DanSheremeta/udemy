from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 7
    page_query_param = 'p'
    page_size_query_param = 'page_size'
    max_page_size = 50
    last_page_strings = 'end'


class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 7
    max_limit = 15
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCursorPagination(CursorPagination):
    page_size = 7
    ordering = '-avg_rating'
    # cursor_query_param = 'record'

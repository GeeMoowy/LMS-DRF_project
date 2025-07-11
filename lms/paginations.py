from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомный пагинатор для отображения количества сущностей на странице"""

    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

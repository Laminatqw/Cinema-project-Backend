from rest_framework.pagination import PageNumberPagination

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']

    # 'DEFAULT_PARSER_CLASSES': [
    #     'rest_framework.parsers.JSONParser',
    # ]
}
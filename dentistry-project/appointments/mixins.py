from rest_framework import mixins, viewsets


class ListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    pass

from rest_framework import viewsets, mixins


class ListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    pass

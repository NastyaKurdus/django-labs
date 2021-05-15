from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import FilterSet, DjangoFilterBackend, CharFilter
from .models import MyUser, OnlineUser
from .serializers import MyUserSerializer, OnlineUserSerializer


class MyUserFilter(FilterSet):
    regex = CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = MyUser
        fields = ('regex', )


class MyUserReadViewSet(ReadOnlyModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MyUserFilter


class OnlineUserReadViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows to view online users
    """
    queryset = OnlineUser.objects.all()
    serializer_class = OnlineUserSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django_filters.rest_framework import FilterSet, NumberFilter
from .serializers import CalculatorSerializer, HistorySerializer
from .models import Calculator, History
from rest_framework.pagination import PageNumberPagination


class CalculatorPaginator(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'per_page'
    max_page_size = 100


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user == obj.owner)


class IsCalculatorOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user == obj.calculator.owner)


class BaseModelViewSet(ModelViewSet):
    pagination_class = CalculatorPaginator
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {

    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get('permission_classes')
            else:
                permission_classes = None
            return [permission() for permission in (permission_classes or self.permission_classes)]


class CalculatorViewSet(BaseModelViewSet):
    """
    API endpoint that allows users to create, update, view and remove calculators.
    """
    serializer_class = CalculatorSerializer
    permission_classes_by_action = {
        'update': [IsOwner],
        'partial_update': [IsOwner],
        'destroy': [IsAdminUser | IsOwner]
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Calculator.objects.all()
        return Calculator.objects.filter(owner=self.request.user)


class HistoryFilter(FilterSet):
    calculator = NumberFilter(field_name='calculator__id')

    class Meta:
        model = History
        fields = ('calculator', )


class HistoryViewSet(BaseModelViewSet):
    """
    API endpoint that allows users to create, update, view and remove expressions to calculate.
    """
    serializer_class = HistorySerializer
    filterset_class = HistoryFilter
    permission_classes_by_action = {
        'update': [IsCalculatorOwner],
        'partial_update': [IsCalculatorOwner],
        'destroy': [IsAdminUser | IsCalculatorOwner]
    }

    def get_queryset(self):
        if self.request.user.is_superuser:
            return History.objects.all()
        return History.objects.filter(calculator__owner=self.request.user)

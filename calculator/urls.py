from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvitationEmailsView, InfoView, CalculatorViewSet, HistoryViewSet

router = DefaultRouter()
router.register(r'calculators', CalculatorViewSet, basename='calculator')
router.register(r'calculations', HistoryViewSet, basename='calculation')

urlpatterns = [
    path('', include(router.urls)),
    path('emails/', InvitationEmailsView.as_view()),
    path('info/', InfoView.as_view())
]

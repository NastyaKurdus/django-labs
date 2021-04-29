from rest_framework.routers import DefaultRouter
from .views import CalculatorViewSet, HistoryViewSet

router = DefaultRouter()
router.register(r'calculators', CalculatorViewSet, basename='calculator')
router.register(r'calculations', HistoryViewSet, basename='calculation')

urlpatterns = router.urls

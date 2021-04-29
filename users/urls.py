from rest_framework.routers import DefaultRouter
from .views import MyUserReadViewSet

router = DefaultRouter()
router.register(r'users', MyUserReadViewSet, basename='user')

urlpatterns = router.urls
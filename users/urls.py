from rest_framework.routers import DefaultRouter
from .views import MyUserReadViewSet, OnlineUserReadViewSet

router = DefaultRouter()
router.register(r'users', MyUserReadViewSet, basename='user')
router.register(r'online-users', OnlineUserReadViewSet, basename='online-user')

urlpatterns = router.urls

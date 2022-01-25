# users/urls.py

from rest_framework import routers

from user.views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')

urlpatterns = router.urls
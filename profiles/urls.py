from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin

from .views import ProfileViewSet, FollowingViewSet


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()

profiles_router = router.register('profiles', ProfileViewSet)

profiles_router.register(
    'follow',
    FollowingViewSet,
    basename='follow',
    parents_query_lookups=['following']
)

urlpatterns = [
    path('', include(router.urls))
]

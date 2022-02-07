from django.urls import path, include
# from .views import PostAPIView, PostAPIDetail
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PostViewSet, CommentViewSet, LikeViewSet, FeedViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()

router.register('feed', FeedViewSet, basename='feed')

posts_router = router.register('posts', PostViewSet)

posts_router.register(
    'comments',
    CommentViewSet,
    basename='comments',
    parents_query_lookups=['post']
)

posts_router.register(
    'likes',
    LikeViewSet,
    basename='likes',
    parents_query_lookups=['post']
)

urlpatterns = [
    path('', include(router.urls))
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])

from rest_framework import status, filters, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Post, Comment, Like
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from profiles.models import Profile, FollowRelation


class PostViewSet(NestedViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.prefetch_related('comments').prefetch_related('likes')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["content"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(NestedViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.get_parents_query_dict()['post'])


class LikeViewSet(NestedViewSetMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def create(self, request, *args, **kwargs):
        request_data = request
        request_data.data['post'] = self.get_parents_query_dict()['post']
        request_data.data['user'] = request.user.pk
        return super().create(request_data)


class FeedViewSet(ModelViewSet, mixins.ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        profile = Profile.objects.filter(user=self.request.user).first()
        following = FollowRelation.objects.filter(follower=profile).values_list('following', flat=True)
        print(following)
        return Post.objects.filter(user__in=following)

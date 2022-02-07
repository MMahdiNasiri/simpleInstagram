from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import Profile, FollowRelation
from .permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer, FollowingSerializer


class ProfileViewSet(NestedViewSetMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.prefetch_related('following').prefetch_related('followers')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["username"]



class FollowingViewSet(NestedViewSetMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowingSerializer
    queryset = FollowRelation.objects.all()

    def get_queryset(self):
        follower = self.request.user.profile
        return FollowRelation.objects.filter(following=self.get_parents_query_dict()['following'], follower=follower)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('Field Already Exists')
        serializer.save(follower=self.request.user.profile, following_id=self.get_parents_query_dict()['following'])

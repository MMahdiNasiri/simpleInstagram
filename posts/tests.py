from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate
from rest_framework.test import APIRequestFactory
from .views import PostViewSet, CommentViewSet, LikeViewSet
from .models import Post, Comment, Like


class TestPosts(APITestCase):
    def setUp(self):
        self.uri = '/posts/'
        self.create_credentials = {'content': 'create test'}
        self.update_credentials = {'content': 'update test'}
        self.factory = APIRequestFactory()
        self.view = PostViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'put': 'update',
            'delete': 'destroy',
        })
        self.detail_view = PostViewSet.as_view(actions={'get': 'retrieve'})

        self.test_user = User(username='admin', password='admin')
        self.test_user.save()
        Post.objects.create(content='test created post', user=self.test_user)

    def test_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_create(self):
        request = self.factory.post(self.uri, self.create_credentials)
        force_authenticate(request, user=self.test_user, token=self.test_user.auth_token)
        response = self.view(request)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_retrieve(self):
        request = self.factory.get(f'{self.uri}/1')
        response = self.detail_view(request, pk=1)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_update(self):
        request = self.factory.put(self.uri+'1/', self.update_credentials)
        force_authenticate(request, user=self.test_user, token=self.test_user.auth_token)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))

    def test_delete(self):
        request = self.factory.delete(self.uri+'1/')
        force_authenticate(request, user=self.test_user, token=self.test_user.auth_token)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))




from django.test import TestCase

from django.contrib.auth.models import User

from .models import Post


class ForumTests(TestCase):
    def test_can_see_posts(self):
        user = self._create_user(login=True)
        self._create_post(user=user)

        response = self.client.get('/')
        self.assertContains(response, 'Test Message')

    def test_can_filter_posts_by_user(self):
        self._create_post()
        user = self._create_user(username='zoe', login=True)

        response = self.client.get('/?user=alice')
        self.assertContains(response, 'Test Message')
        response = self.client.get('/?user=zoe')
        self.assertNotContains(response, 'Test Message')

    def test_can_make_posts(self):
        user = self._create_user(login=True)

        num_before = Post.objects.count()
        self.client.post('/', {'message': 'Another Message'})
        self.assertEqual(num_before + 1, Post.objects.count())

    def test_redirected_after_posting(self):
        user = self._create_user(login=True)

        response = self.client.post('/', {'message': 'Another Message'})
        self.assertRedirects(response, '/')

    def test_sees_message_after_posting(self):
        user = self._create_user(login=True)

        response = self.client.post('/', {'message': 'Another Message'}, follow=True)
        self.assertContains(response, 'Thanks for posting')

    def test_can_sign_out(self):
        user = self._create_user(login=True)

        response = self.client.get('/accounts/logout/?next=/', follow=True)
        self.assertContains(response, 'Sign in')

    def test_cannot_see_posts_when_not_signed_in(self):
        response = self.client.get('/', follow=True)
        self.assertNotContains(response, 'Test Message')

    def test_cannot_make_posts_when_not_signed_in(self):
        num_before = Post.objects.count()
        self.client.post('/', {'message': 'Another Message'})
        self.assertEqual(num_before, Post.objects.count())

    def test_can_sign_in_when_not_signed_in(self):
        user = self._create_user()

        response = self.client.post(
            '/accounts/login/?next=/',
            {'username': 'alice', 'password': 'password'},
            follow=True,
        )
        self.assertContains(response, 'Hi, alice')

    def test_can_sign_up_when_not_signed_in(self):
        response = self.client.post(
            '/accounts/signup/',
            {'username': 'zoe', 'password1': 'password', 'password2': 'password'},
            follow=True,
        )
        self.assertContains(response, 'Hi, zoe')

    def _create_user(self, username='alice', login=False):
        user = User.objects.create_user(username, password='password')
        if login:
            self.client.login(username=username, password='password')
        return user

    def _create_post(self, user=None, message='Test Message'):
        user = user or self._create_user()
        return Post.objects.create(owner=user, message=message)

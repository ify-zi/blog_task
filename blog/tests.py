from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Post


# Create your tests here.
class BlogTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password= "password",
        )
        self.Post= Post.objects.create(
            title= "corruption",
            author=self.user,
            body="God is going to help this country",
        )

    def test_string_representation(self):
        post = Post(title='corruption')
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.Post.get_absolute_url(), '/post/1/')


    def test_post_content(self):
        self.assertEqual(f'{self.Post.title}', "corruption")
        self.assertEqual(f'{self.Post.author}', "testuser")
        self.assertEqual(f'{self.Post.body}',"God is going to help this country")
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "God is going to help this country")
        self.assertTemplateUsed(response, "home.html")
    def test_post_detail_view(self):
        response= self.client.get('/post/1/')
        no_response= self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "corruption")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),{
            'title' : 'New Blog',
            'body' : 'new blog text',
            'author' : self.user.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'New Blog')
        self.assertEqual(Post.objects.last().body, 'new blog text')
    def test_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'),{
            'title' : 'Updated title',
            'body' : 'Updated body',
        })
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)

    




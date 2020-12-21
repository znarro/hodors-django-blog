from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogTests(TestCase):
    def setUp(self):
        """
        We add a sample blog post to test
        """
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret",
        )

        self.post = Post.objects.create(
            title="A good title",
            body="Nice body content",
            author=self.user,
        )

    def test_string_representation(self):
        """
        Confirm that its string representation is correct
        """
        post = Post(title="A sample title")
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_post_content(self):
        """
        Confirm that its content is correct
        """
        self.assertEqual(f"{self.post.title}", "A good title")
        self.assertEqual(f"{self.post.author}", "testuser")
        self.assertEqual(f"{self.post.body}", "Nice body content")

    def test_post_list_view(self):
        """
        Confirm that our homepage returns a 200 HTTP status code, contains our
        body text, and uses the correct home.html template
        """
        response = self.client.get(reverse("home"))
        print(response)
        self.assertEqual(response.status_code, 200)  # 200: OK
        self.assertContains(response, "Nice body content")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detail_view(self):
        """
        Confirm that detail page works as expected and that an incorrect page
        returns a 404
        """
        response = self.client.get("/post/1/")
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)  # 404: Not found
        self.assertContains(response, "A good title")
        self.assertTemplateUsed(response, "post_detail.html")

    def test_post_create_view(self):
        response = self.client.post(
            reverse("post_new"),
            {
                "title": "New title",
                "body": "New text",
                "author": self.user,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New title")
        self.assertContains(response, "New text")

    def test_post_update_view(self):
        response = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title": "Updated title",
                "body": "Updated text",
            },
        )
        self.assertEqual(response.status_code, 302)  # 302: Found, redirect

    def test_post_delete_view(self):
        response = self.client.post(reverse("post_delete", args="1"))
        self.assertEqual(response.status_code, 302)
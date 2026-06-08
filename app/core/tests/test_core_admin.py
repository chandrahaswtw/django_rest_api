from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Used to login to the django admin console
from django.test import Client


class AdminTests(TestCase):

    #  setUp is called automatically immediately before running each individual test method within a test case class - unittest specific
    def setUp(self):

        # Client() is Django's test browser. It lets you simulate requests without opening a real browser.
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="Admin@789"
        )

        # force_login is a Django test utility that logs in a user without going through the login form or password authentication process.
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="User@789", name="testname"
        )

    def test_users_list(self):

        # We can admin URL's as mentioned here. https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        # Syntax is {{ app_label }}_{{ model_name }}_changelist as specified in above URL.
        url = reverse("admin:core_user_changelist")

        # This returns HTML page
        res = self.client.get(url)

        # assertContains looks for string within another string. BTW assertContains is Django specific not part of unittest.
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_users_change(self):

        # We can admin URL's as mentioned here. https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        # Syntax is {{ app_label }}_{{ model_name }}_change as specified in above URL.
        url = reverse("admin:core_user_change")

        # This returns HTML page
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_users_change(self):

        # We can admin URL's as mentioned here. https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#reversing-admin-urls
        # Syntax is {{ app_label }}_{{ model_name }}_add as specified in above URL.
        url = reverse("admin:core_user_add")

        # This returns HTML page
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

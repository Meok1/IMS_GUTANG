from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Student


class StudentDeleteTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="test-user",
            password="test-password-123",
        )
        self.client.force_login(self.user)
        self.student = Student.objects.create(
            student_id="DELETE-TEST",
            first_name="Test",
            last_name="Student",
            age=20,
            gender="Prefer not to say",
            course="BSIT",
            year_level="1",
            email="delete-test@example.com",
            contact_number="0000000000",
        )

    def test_delete_confirmation_is_separate_and_shows_student(self):
        response = self.client.get(reverse("student_delete", args=[self.student.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="card delete-confirmation"')
        self.assertContains(response, "Student ID: DELETE-TEST")
        self.assertContains(response, "Cancel and return to directory")

    def test_confirming_delete_removes_student_and_returns_to_directory(self):
        response = self.client.post(
            reverse("student_delete", args=[self.student.pk]),
            follow=True,
        )

        self.assertEqual(response.redirect_chain[-1][0], reverse("student_list"))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
        self.assertContains(response, "Student record removed successfully.")

    def test_adding_student_shows_success_message(self):
        response = self.client.post(
            reverse("student_create"),
            {
                "student_id": "ADD-TEST",
                "first_name": "Added",
                "last_name": "Student",
                "age": 19,
                "gender": "Prefer not to say",
                "course": "BSIT",
                "year_level": "1",
                "email": "added-test@example.com",
                "contact_number": "1111111111",
            },
            follow=True,
        )

        self.assertEqual(response.redirect_chain[-1][0], reverse("student_list"))
        self.assertContains(response, "Student record added successfully.")

    def test_student_list_search_matches_name_and_student_id(self):
        response = self.client.get(reverse("student_list"), {"q": "DELETE-"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Student, Test")
        self.assertContains(response, "DELETE-TEST")
        self.assertContains(response, "1 matching student")

    def test_student_list_search_shows_no_results_message(self):
        response = self.client.get(reverse("student_list"), {"q": "not-found"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No students matched")
        self.assertNotContains(response, "No student records yet.")


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="login-user",
            password="login-password-123",
        )

    def test_home_redirects_to_login_when_user_is_anonymous(self):
        response = self.client.get(reverse("student_list"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('student_list')}",
        )

    def test_login_redirects_to_student_directory(self):
        response = self.client.post(
            reverse("login"),
            {"username": "login-user", "password": "login-password-123"},
        )

        self.assertRedirects(response, reverse("student_list"))

    def test_invalid_login_offers_account_creation(self):
        response = self.client.post(
            reverse("login"),
            {"username": "unregistered-user", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your username or password was incorrect.")
        self.assertContains(response, 'href="/signup/">create an account</a>')

    def test_logout_ends_session_and_redirects_to_login(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        protected_response = self.client.get(reverse("student_list"))
        self.assertRedirects(
            protected_response,
            f"{reverse('login')}?next={reverse('student_list')}",
        )

    def test_signup_creates_account_logs_in_and_opens_directory(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "new-user",
                "password1": "Secure-test-password-8462",
                "password2": "Secure-test-password-8462",
            },
        )

        self.assertRedirects(response, reverse("student_list"))
        self.assertTrue(get_user_model().objects.filter(username="new-user").exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signup_rejects_password_mismatch(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "new-user",
                "password1": "Secure-test-password-8462",
                "password2": "different-password-8462",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username="new-user").exists())
        self.assertContains(response, "The two password fields didn’t match")

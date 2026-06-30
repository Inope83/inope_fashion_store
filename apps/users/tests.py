from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from apps.users.models import Kliente, Admin
from apps.dashboard.forms import DashboardKlienteForm, DashboardAdminForm
from django.core.exceptions import ValidationError


class SecurityAuthTestCase(TestCase):
    def setUp(self):
        # Create an initial Admin with an email-like username because LoginForm uses EmailField
        self.admin = Admin.objects.create(username="admin_test@example.com", password="InitialPassword123")

    def test_admin_password_hashing(self):
        # Verify initial admin password is encrypted
        self.assertTrue(self.admin.password.startswith('pbkdf2_'))
        self.assertTrue(self.admin.check_password("InitialPassword123"))

    def test_login_sync_to_kliente(self):
        # Post to login_view with admin credentials
        response = self.client.post(
            reverse('kliente_login'),
            {'email': 'admin_test@example.com', 'password': 'InitialPassword123'}
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success

        # Verify a Kliente record was created for the admin
        kliente = Kliente.objects.get(email="admin_test@example.com")
        self.assertTrue(kliente.is_staff)
        self.assertTrue(check_password("InitialPassword123", kliente.password))

    def test_admin_password_rotation_sync(self):
        # Simulate initial login to create Kliente
        self.client.post(
            reverse('kliente_login'),
            {'email': 'admin_test@example.com', 'password': 'InitialPassword123'}
        )
        kliente = Kliente.objects.get(email="admin_test@example.com")

        # Admin changes password in Admin table
        self.admin.password = "NewSecretPassword99"
        self.admin.save()

        # Try logging in with the OLD password - should fail
        response = self.client.post(
            reverse('kliente_login'),
            {'email': 'admin_test@example.com', 'password': 'InitialPassword123'}
        )
        # Should stay on page/show error message
        self.assertContains(response, 'Email ka password la los', status_code=200)

        # Log in with the NEW password - should succeed and sync the Kliente record
        response = self.client.post(
            reverse('kliente_login'),
            {'email': 'admin_test@example.com', 'password': 'NewSecretPassword99'}
        )
        self.assertEqual(response.status_code, 302)

        # Verify Kliente record has been updated with the new hash
        kliente.refresh_from_db()
        self.assertTrue(check_password("NewSecretPassword99", kliente.password))

    def test_custom_password_validation(self):
        # Validate RegistForm password requirements (minimum 8 chars + 1 digit)
        base = {'naran': 'Test Client', 'email': 'test@inopestore.com'}
        # Short password
        response = self.client.post(
            reverse('kliente_regist'),
            {**base, 'password': 'short', 'confirm_password': 'short'}
        )
        self.assertContains(response, 'Liafuan-pase tenke minimu karakter 8.', status_code=200)

        # No digits
        response = self.client.post(
            reverse('kliente_regist'),
            {**base, 'password': 'NoDigitsPassword', 'confirm_password': 'NoDigitsPassword'}
        )
        self.assertContains(response, 'Liafuan-pase tenke iha numeru ida (0-9).', status_code=200)

        # Valid password
        response = self.client.post(
            reverse('kliente_regist'),
            {**base, 'password': 'ValidPassword123', 'confirm_password': 'ValidPassword123'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Kliente.objects.filter(email='test@inopestore.com').exists())

    def test_dashboard_forms_do_not_expose_password_hashes(self):
        kliente = Kliente.objects.create(naran="Kliente Uno", email="uno@inopestore.com", password="SecurePassword1")
        original_hash = kliente.password

        # Instantiate update form
        form = DashboardKlienteForm(instance=kliente)
        # Password field should be optional on update and not contain the hash
        self.assertFalse(form.fields['password'].required)
        self.assertEqual(form.fields['password'].initial, '')

        # Save form without providing password -> password should not change
        form = DashboardKlienteForm(data={'naran': 'Kliente Uno Modified', 'email': 'uno@inopestore.com', 'password': ''}, instance=kliente)
        self.assertTrue(form.is_valid(), form.errors)
        saved_kliente = form.save()
        self.assertEqual(saved_kliente.naran, 'Kliente Uno Modified')
        self.assertEqual(saved_kliente.password, original_hash)  # Unchanged hash

        # Save form with new password -> password should update and hash
        form = DashboardKlienteForm(data={'naran': 'Kliente Uno Modified', 'email': 'uno@inopestore.com', 'password': 'NewPassword888'}, instance=saved_kliente)
        self.assertTrue(form.is_valid())
        saved_kliente = form.save()
        self.assertNotEqual(saved_kliente.password, original_hash)
        self.assertTrue(check_password('NewPassword888', saved_kliente.password))

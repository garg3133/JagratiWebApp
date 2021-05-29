from django.test import TestCase
# from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Profile,User
from apps.volunteers.models import Volunteer

class LoginSignupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user
        test_user1 = User.objects.create_user(email='testuser1@gmail.com', password='1X<ISRUkw+tuK')

        test_user1.save()

        # Complete profile of first user
        test_user1.first_name = 'test'
        test_user1.last_name = 'user'
        test_user1.is_active = False
        test_user1.auth = True
        test_user1.save()
        test_user1_profile = Profile.objects.create(
            user = test_user1,
            gender = 'M',
            alt_email = 'alt@gmail.com',
            profile_image = 'fesse.JPEG',
            street_address1 = 'awdwdawd',
            street_address2 = 'awdawdawd',
            contact_no = '9999999999',
            city = 'Montreal',
            state = 'Quebec',
            pincode = 98743
        )

        test_user2 = User.objects.create_user(email='testuser2@gmail.com', password='2HJ1vRV0Z&3iD')

        test_user2.save()

        # Complete profile of first user
        test_user2.first_name = 'test1'
        test_user2.last_name = 'user1'
        test_user2.is_active = True
        test_user2.auth = True
        test_user2.save()
        test_user2_profile = Profile.objects.create(
            user = test_user2,
            gender = 'M',
            alt_email = 'altemail@gmail.com',
            profile_image = 'fessea.JPEG',
            street_address1 = 'awdwdaadswd',
            street_address2 = 'awdaasdawdawd',
            contact_no = '99999999999',
            city = 'Paris',
            state = 'France',
            pincode = 98798
        )
        test_user2_volunteer = Volunteer.objects.create(
            profile = test_user2_profile,
            roll_no = 18100123,
            dob = '2021-01-01',
            batch = 12,
            programme = 'awdaasdawdawd'
        )


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
           
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('accounts:login_signup'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        response = self.client.get(reverse('accounts:login_signup'))
        self.assertTemplateUsed(response, 'accounts/login_signup.html')

    def test_view_login_with_correct_data(self):
        response = self.client.post(reverse('accounts:login_signup'), {
            'email' : 'testuser2@gmail.com',
            'password' : '2HJ1vRV0Z&3iD',
            'submit' : 'login'
        })
        # Check it redirects correctly to login_signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/dashboard/')

    def test_view_login_with_incorrect_username(self):
        response = self.client.post(reverse('accounts:login_signup'), {
            'email' : 'fakeemail@email.com',
            'password' : '1X<ISRUkw+tuK',
            'submit' : 'login'
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login_signup.html')
        self.assertEqual(response.context['login_error'], 'Invalid credentials')

    def test_view_login_with_incorrect_password(self):
        response = self.client.post(reverse('accounts:login_signup'), {
            'email' : 'testuser1@gmail.com',
            'password' : '1X<8229821guiequiueui+tuK',
            'submit' : 'login'
        })

        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login_signup.html')
        self.assertEqual(response.context['login_error'], 'Invalid credentials')

    def test_view_signup_with_valid_data(self):
        response = self.client.post(reverse('accounts:login_signup'), {
            'email' : 'testuser99@gmail.com',
            'password1' : '1X<ISRUkw+tuK',
            'password2' : '1X<ISRUkw+tuK',
            'submit' : 'sign_up'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'accounts/email/account_activation_email.html')
        self.assertRedirects(response, reverse('accounts:signup_success'))

    def test_view_signup_with_existing_user(self):
        response = self.client.post(reverse('accounts:login_signup'), {
            'email' : 'testuser1@gmail.com',
            'password1' : '1X<ISRUkw+tuK',
            'password2' : '1X<ISRUkw+tuK',
            'submit' : 'sign_up'
        })
        # Check it renders correct template with correct error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login_signup.html')
        self.assertEqual(response.context['signup_error'], 'Account with entered email already exists')

    def test_view_signup_with_mismatching_password(self):
        response = self.client.post(reverse('accounts:login_signup'), {
            'email' : 'testuser3@gmail.com',
            'password1' : '1X<ISRUkw+tuK',
            'password2' : '1X<ISRUkw+tu',
            'submit' : 'sign_up'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login_signup.html')
        self.assertEqual(response.context['signup_error'], "Passwords don't match")

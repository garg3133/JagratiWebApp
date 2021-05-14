from django.test import SimpleTestCase,TestCase,Client
from django.urls import reverse,resolve
from accounts.models import User
class TestViews(TestCase):
    @classmethod
    def setUp(self):
        User.objects.create_superuser(
            'user101@example.com',
            'pswdt2gbjbuh',
        )
        self.client=Client()
        self.client.login(username="user101@example.com", password="pswdt2gbjbuh")
        self.un_auth_user=User.objects.create_user("user100@gmail.com","pswdt2gb")
         
    def tearDown(self):
        self.client.logout()
        
    
    def test_new_student(self):
        payload_data ={
               'first_name': "first_name",
               'last_name':"last_name",
               'gender':'M',
               'school_class':4,
               'village':'G',
               'guardian_name': "guardian_name",
            }
            
        response_post=self.client.post(reverse('students:add_student'),kwargs=payload_data,follow=True) 
        response_get=self.client.get(reverse('students:add_student'),follow=True)
        
        redirected_response_get=self.client.get(reverse('students:add_student'))
        redirected_response_post=self.client.post(reverse('students:add_student'),kwargs=payload_data)
        
        # Checking for unauthenticated users, to get redirected to correct url
        # Getting correct status code for redirection
        self.assertEquals(redirected_response_get.status_code,302)
        self.assertEquals(redirected_response_post.status_code,302)
        self.assertEquals(redirected_response_get.url,"/accounts/login/?next=/students/add/")
        
        # This is authenticated user so resp code 200
        self.assertEquals(response_post.status_code,200)
        self.assertEquals(response_get.status_code,200)   
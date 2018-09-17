from django.db import models
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    phone = models.CharField(max_length=50)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return 'Profile for {}'.format(self.user)


class Home(models.Model):
    faderimage1 = models.ImageField(upload_to='home')
    faderimage2 = models.ImageField(upload_to='home', blank=True)
    faderimage3 = models.ImageField(upload_to='home', blank=True)
    cake1_image = models.ImageField(upload_to='home', blank=True)
    cake1_title = models.CharField(max_length=50)
    cake1_description = models.CharField(max_length=75)
    cake2_image = models.ImageField(upload_to='home', blank=True)
    cake2_title = models.CharField(max_length=50)
    cake2_description = models.CharField(max_length=75)
    cake3_image = models.ImageField(upload_to='home', blank=True)
    cake3_title = models.CharField(max_length=50)
    cake3_description = models.CharField(max_length=75)
    banner_image = models.ImageField(upload_to='home')
    cart_banner_image = models.ImageField(upload_to='home')

    class Meta:
        verbose_name = 'Home'

    def __str__(self):
        return 'Home Configuration'


class About(models.Model):
    banner_image = models.ImageField(upload_to='about')
    banner_image2 = models.ImageField(upload_to='about')
    mission = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'About'

    def __str__(self):
        return 'About Configuration'


class Team(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='team')
    description = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Team'

    def __str__(self):
        return self.name


class Review(models.Model):
    name = models.CharField(max_length=100)
    body = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, validators=[validate_email])
    phone = models.CharField(max_length=35)
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def send_client_email(self):
        mail = EmailMessage(to=[
            {
                'address': self.email,
                'substitution_data': {
                    'name': self.name,
                    'subject': self.subject,
                    'message': self.message,
                    'phone': self.phone
                }
            }
        ], from_email='contact@flower-flour.com')
        mail.template = 'contact-email'
        mail.send()

    def send_admin_emails(self):
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            mail = EmailMessage(to=[
                {
                    'address': admin.email,
                    'substitution_data': {
                        'name': admin.first_name,
                        'client_name': self.name,
                        'subject': self.subject,
                        'message': self.message,
                        'phone': self.phone
                    }
                }
            ], from_email='contact@flower-flour.com')
            mail.template = 'contact-confirm-admin'
            mail.send()

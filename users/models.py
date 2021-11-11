from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.timezone import now

NULL_INSTALL = {'null':True, 'blank':True}

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', blank=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.CharField(max_length=128, **NULL_INSTALL)

    activation_key_created = models.DateTimeField(auto_now_add=True, **NULL_INSTALL)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_created + timedelta(hours=48):
            return False
        return True


class UserProfile(models.Model):

    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOICES = ((MALE, 'M'),(FEMALE,'Ж'))
    RU = '0'
    UK = '1'
    BE = '2'
    EN = '3'
    LANGUAGE_CHOICES = ((RU, 'Русский'),(UK, 'Українська'), (BE, 'Беларуская'), (EN, 'English'))

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='тэги', max_length=128, blank=True)
    about = models.TextField(verbose_name='о себе', blank=True, null=True)
    gender = models.CharField(verbose_name='пол', choices=GENDER_CHOICES, blank=True, max_length=5)
    lang = models.CharField(verbose_name='язык', choices=LANGUAGE_CHOICES, blank=True, max_length=10)
    photo = models.ImageField(blank=True)


    # Это два сигнала, которые мы обрабатываем в зависмости от того, что происходит во views в профайле (create или update)
    @receiver(post_save, sender=User) # Этот сигнал позволит создавать информацию в модели в рез-тате создания в основной модели
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
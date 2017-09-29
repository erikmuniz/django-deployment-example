from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User)

    # Just some additional fields
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    # (blank=True) means no error if field is NOT filled in
    # profile_pics is folder under media

    # Just method for printing
    def __str__(self):
        return self.user.username

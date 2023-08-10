from django.db import models

from django.contrib.auth.models import User

from content.models import course

# Create your models here.

class UserData(models.Model):
    banned = models.BooleanField(default=False)
    allow_profile_change = models.BooleanField(default=True)
    address = models.CharField(max_length=255,null=True)

    last_updated = models.DateField(auto_now=True)

    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Additional User Data"

    def __str__(self):
        return str(self.owner)

class UserSubscriptions(models.Model):
    course = models.ForeignKey(course.Course, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    premium_member = models.BooleanField(default=True)

    active = models.BooleanField(default=False)

    subscription_date = models.DateField(null=True)
    subscription_expiration_date = models.DateField(null=True)

    class Meta:
        verbose_name_plural = "Customer Subscriptions"

    def __str__(self):
        return str(self.owner)

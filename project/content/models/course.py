from django.db import models
import uuid
import os

# Create your models here.
def get_banner_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('courses/banners', filename)

def get_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('courses/logos', filename)

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    in_public = models.BooleanField(default=True)
    description = models.TextField()
    content = models.TextField()
    banner = models.ImageField(upload_to=get_banner_path,null=True)
    logo = models.ImageField(upload_to=get_logo_path,null=True)

    assessment_limit = models.PositiveSmallIntegerField(default=0, null=True)

    arrangement = models.IntegerField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['arrangement']
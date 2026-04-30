import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class File(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='files')
    size = models.FloatField(help_text="Hajmi (MB)")
    is_public = models.BooleanField(default=False)
    download_limit = models.IntegerField(default=0, help_text="0 bo'lsa cheksiz")
    expire_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def is_expired(self):
        if self.expire_date and timezone.now() > self.expire_date:
            return True
        return False



class SharedLink(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE,related_name='links')
    token = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)




    def save(self, *args, **kwargs):
            if self.expire_date and timezone.now() > self.expire_date:
                self.is_active = False
            super().save(*args, **kwargs)
    def __str__(self):
        return f"Link for ({self.file.title})"
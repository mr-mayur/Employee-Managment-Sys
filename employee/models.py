from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    designation = models.CharField(max_length=20,null=True, blank=False)
    salary = models.BigIntegerField(null=True, blank=False)

    class Meta:
        ordering = ('-salary',)

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

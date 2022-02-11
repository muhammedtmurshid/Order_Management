from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from staff.models import Staff


@receiver(post_save, sender=User)
def create_user_staff(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_staff(sender, instance, **kwargs):
    instance.staff.save()
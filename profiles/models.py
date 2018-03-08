from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# from catalog.models import Ad

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True, help_text="City")
    birth_date = models.DateField(null=True, blank=True, help_text="Enter in format YYYY-DD-MM")
    # favourites = models.ManyToManyField(Ad, related_name='favourited_by')

    def __str__(self):
        return self.user.username

    # Returns the url to access a user profile based on user_id.
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.user.user_id)])

# Define signals to create/update Profile model when User model is created/updated
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

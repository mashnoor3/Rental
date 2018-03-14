from django.db import models
import uuid # To create unique ad instances
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

from django.contrib.auth.models import User
from django.contrib import admin

from profiles.models import Profile

# Model representing category for tool (e.g. Moving, Gardening, Home Renovation, etc.)
class Category(models.Model):
    CATEGORY_CHOICES = (
        ('Other', 'Other'),
        ('Home Renovation', 'Home Renovation'),
        ('Gardening', 'Gardening'),
        ('Power Tools', 'Power Tools'),
        ('Moving', 'Moving'),
        ('Garage', 'Garage'),
        ('Washroom', 'Washroom'),
    )

    category_name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, default='Other', help_text="Choose a cateogry (e.g. Moving, Gardening etc.)", unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'

# Model representing Ads that users can create
class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    renter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='my_ads')
    #borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrower')


    location = models.CharField(max_length=100)
    # By design an Ad can only belong to one category. Later change to ManyToManyField to allow one ad to have multiple categories
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('o', 'On loan'),
        ('r', 'Reserved'),
    )
    loan_status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Tool availability')

    loan_duration = models.IntegerField(help_text="Loan duration in days")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    favourites = models.ManyToManyField(Profile, blank=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for the ad")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('ad_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('ad_delete', args=[str(self.id)])

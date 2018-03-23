from django.db import models
import uuid # To create unique ad instances
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

from django.contrib.auth.models import User
from django.contrib import admin

from profiles.models import Profile

# Model representing category for tool (e.g. Moving, Gardening, Home Renovation, etc.)
class Category(models.Model):
    CATEGORY_CHOICES = (
        ('Home Renovation', 'Home Renovation'),
        ('Gardening', 'Gardening'),
        ('Power Tools', 'Power Tools'),
        ('Moving', 'Moving'),
        ('Garage', 'Garage'),
        ('Washroom', 'Washroom'),
        ('Kitchen', 'Kitchen'),
        ('Automobile', 'Automobile'),
        ('Other', 'Other'),
    )

    category_name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, default='Other', help_text="Choose a cateogry (e.g. Moving, Gardening etc.)", unique=True)

    category_img = models.ImageField(upload_to="catalog_images", blank=True, null=True,  default="catalog_images/no_img.png")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = 'Categories'

# Model representing Ads that users can create
class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    renter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=False, related_name='my_ads')

    ad_img = models.ImageField(upload_to="ad_images", blank=True, null=True,  default="ad_images/no_img.png")

    # Multiple people can request to borrow
    add_requestor = models.BooleanField(default=False)
    borrow_requests = models.ManyToManyField(Profile, blank=True,  related_name='borrow_requests')
    # Only one person can be borrower
    borrower = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrower')

    location = models.CharField(max_length=100)
    # By design an Ad can only belong to one category. Later change to ManyToManyField to allow one ad to have multiple categories
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('o', 'On loan'),
        ('c', 'Completed'),
    )
    loan_status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='Tool availability')

    loan_duration = models.IntegerField(help_text="Loan duration in days")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    favourites = models.ManyToManyField(Profile, null=True, blank=True, related_name='favs')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for the ad")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('ad_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('ad_delete', args=[str(self.id)])

    def update_fav_url(self):
        return reverse('update_fav', args=[str(self.id)])

    def request_ad_url(self):
        return reverse('request_ad', args=[str(self.id)])

    def cancel_request(self):
        return reverse('cancel_request', args=[str(self.id)])

    def manage_requests(self):
        return reverse('manage_requests', args=[str(self.id)])

    def accept_request(self):
        return reverse('accept_request', kwargs={"ad_pk":str(self.id)})

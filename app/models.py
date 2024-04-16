from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)


class User(AbstractUser):
    ADMIN = 1
    LANDLORD = 2
    TERNANT = 3
    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (LANDLORD, 'Landlord'),
        (TERNANT, 'Ternant'),
    )

    role = models.IntegerField(choices=ROLE_CHOICES, default=TERNANT)
    avatar = models.ImageField(upload_to="users/%Y/%m/", null=True)

    def save(self, *args, **kwargs):
        if self.role == self.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == self.LANDLORD:
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
    # is_superuser = None
    # is_staff = None
    pass
    # package = models.ForeignKey(Package, on_delete=models.CASCADE, default=None)
    # package_end_date = models.DateField(null=True, blank=True)
    #
    # def update_package_end_date(self):
    #     if self.package_id:
    #         duration = self.package.duration
    #         if duration:
    #             self.package_end_date = timezone.now().date() + timezone.timedelta(days=duration)
    #         else:
    #             self.package_end_date = None
    #     else:
    #         self.package_end_date = None
    #     self.save()


class Package(models.Model):
    name = models.CharField(max_length=255)
    turn = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    VNPAY = 1
    CASH = 2
    TYPE_CHOICES = (
        (VNPAY, 'Vnpay'),
        (CASH, 'Cash'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, default=VNPAY)
    status = models.TextField(default='pending')


class Remain(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    remain = models.IntegerField()


class House(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_houses')
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    room_count = models.PositiveIntegerField()
    description = models.TextField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    verified = models.BooleanField(default=False)
    is_rented = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='houses')


class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    content = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    status = models.TextField(default='pending')


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set', default=None)  # Người theo dõi
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set', default=None)  # Người được theo dõi


class Image(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_images')
    image = CloudinaryField('image', null=True)

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


class UserRole(Enum):
    ADMIN = 'admin'
    LANDLORD = 'landlord'
    TERNANT = 'ternant'


# class Package(models.Model):
#     name = models.CharField(max_length=255)
#     turn_post = models.PositiveIntegerField()
#     package_price = models.DecimalField(max_digits=10, decimal_places=2)
#     duration = models.PositiveIntegerField(help_text="Duration in days")


class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    role = models.CharField(max_length=20, choices=[(role.value, role.name) for role in UserRole],
                            default=UserRole.TERNANT.value)
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
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set', default=None)  # Người được theo dõi


class Image(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='house_images')
    image = CloudinaryField('image', null=True)

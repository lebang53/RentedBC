from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import Category, User, House, Post, Comment, Follow


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name', 'id']


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()


class UserSerializer(ModelSerializer):
    # permission_classes = [IsAuthenticated] # khi cần authentication thì sử dụng

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar'] = instance.avatar.url

        return rep

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'role']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            raise serializers.ValidationError(
                'username and password is required!'
            )

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError(
                'Incorrect username or password!'
            )

        token = RefreshToken.for_user(user)

        return {
            'success': True,
            'refresh': str(token),
            'access': str(token.access_token),
            'user': UserSerializer(user).data
        }


class HouseSerializer(ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = House
        fields = ['id', 'owner', 'address', 'phone_number', 'description', 'created_date', 'rent_price', 'room_count']


class PostSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'house', 'created_date', 'status']


class CommentSerializer(ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = ['user', 'content', 'post']


class FollowSerializer(ModelSerializer):
    following = UserSerializer()

    class Meta:
        model = Follow
        fields = ['following']


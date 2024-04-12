from rest_framework import viewsets, permissions, generics, parsers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from app import serializers, perms
import cloudinary.uploader

from app.models import Category, User, House, Post, Follow, Comment
from app.serializers import CategorySerializer, UserSerializer, HouseSerializer, PostSerializer, CommentSerializer, \
    FollowSerializer, LoginSerializer, ImageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(viewsets.ViewSet):
    serializer_class = ImageSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            url = cloudinary.uploader.upload(image)
            return Response({'url': url['secure_url']})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    # parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action in ['get_current_user', 'update_info', 'follow']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(UserSerializer(user).data)

    @action(methods=['post'], url_path='login', detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=['post', 'get'], url_path='get_token', detail=False)
    def refresh_token(self, request):
        refresh_token = request.data.get('refresh', None)

        if not refresh_token:
            return Response({'error': 'refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'access': access_token
                         }, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False, url_path='update_info', permission_classes=IsAuthenticated)
    def update_info(self, request):
        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='follow')
    def follow(self, request, pk):
        user = self.get_object()

        follow, created = Follow.objects.get_or_create(following=user, follower=request.user)

        if not created:
            return Response({'message': 'You are already following this user'}, status=status.HTTP_200_OK)

        return Response(serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.filter(active=True)
    serializer_class = HouseSerializer

    def get_queryset(self):
        queryset = self.queryset
        # rent_price, room_count, address
        if self.action == 'list':
            address = self.request.query_params.get('address')
            if address:
                queryset = House.objects.filter(address__icontains=address)

            room_count = self.request.query_params.get('room_count')
            if room_count:
                queryset = House.objects.filter(room_count=room_count)

            rent_price = self.request.query_params.get('rent_price')
            if rent_price:
                queryset = House.objects.filter(rent_price=rent_price)

        return queryset

    @action(methods=['get'], url_path='posts', detail=True)
    def get_post(self, request, pk):
        posts = self.get_object().post_set.filter(active=True)

        return Response(serializers.PostSerializer(posts, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['put'], url_path='verify', detail=True, permission_classes=[IsAdminUser])
    def verify_house(self, request, pk):
        house = self.get_object()

        if house.verified:
            return Response({
                'errors': 'This house has verified!'
            }, status=status.HTTP_400_BAD_REQUEST)

        house.verified = True
        house.save()

        serializer = serializers.PostSerializer(house)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['create_post', 'add_comment']:
            return [permissions.IsAuthenticated()]
        return [perms.PostOwner()]

    @action(methods=['post'], detail=False, url_path='create_post')
    def create_post(self, request):
        user = request.user
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        content = request.data.get('content')

        if content is None:
            return Response({
                'errors': 'Content is required!'
            })

        comment = self.get_object().comment_set.create(content=content, user=request.user)

        return Response(serializers.CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @action(methods=['put'], url_path='approve', detail=True, permission_classes=[IsAdminUser])
    def approve_post(self, request, pk):
        post = self.get_object()

        if post.status != 'pending':
            return Response({
                'errors': 'This post is not pending!'
            }, status=status.HTTP_400_BAD_REQUEST)

        post.status = 'approved'
        post.save()

        serializer = serializers.PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = CommentSerializer
    permission_classes = [perms.CommentOwner]


class FollowViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

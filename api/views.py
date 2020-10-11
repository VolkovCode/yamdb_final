from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, serializers, status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from .permissions import (
    IsSuperUser, IsAdminOrReadOnly, IsAdminOrSuperUser,
    IsAuthorOrAdminOrModerator,
)
from .models import Genre, Title, Category, User, Review
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    UserSerializer, ReviewSerializer, CommentSerializer,
    EmailSerializer, ConfirmCodeSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def retrieve(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]

    def retrieve(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser]


class UserMeViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsSuperUser]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        title = Title.objects.get(pk=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def rating_calc(self, title):
        reviews = Review.objects.filter(title=title)
        rating_average = reviews.aggregate(Avg('score'))['score__avg']
        title.rating = rating_average
        title.save()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        if Review.objects.filter(
            title=title,
            author=self.request.user
        ).exists():
            raise serializers.ValidationError('Отзыв уже оставлен')
        serializer.save(author=self.request.user, title=title)
        self.rating_calc(title)

    def perform_update(self, serializer):
        serializer.save()
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        self.rating_calc(title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
def get_confirmation_code(request):
    username = request.data.get('username')
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid() is not True:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email')
    if Review.objects.filter(username=username).exists() is False:
        User.objects.create_user(username=username, email=email)
    user = get_object_or_404(User, email=email)
    confirm_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Код подтверждения {confirm_code}',
        'praktikum@yandex.ru',
        [email],
        fail_silently=False,
    )
    return Response({'Success': 'Проверь почту'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = ConfirmCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_token(request):
    serializer = ConfirmCodeSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

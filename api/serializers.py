from rest_framework import serializers
from .models import Category, Genre, Title, User, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'bio',
            'role',
            'username',
            'email',
            'first_name',
            'last_name',
        )
        model = User
        lookup_field = 'username'


class CategoryReprField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class GenreReprField(serializers.SlugRelatedField):

    def to_representation(self, value):
        return {'name': value.name, 'slug': value.slug}


class TitleSerializer(serializers.ModelSerializer):
    category = CategoryReprField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = GenreReprField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)

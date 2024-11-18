from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from A_B_test.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_active = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'user_permissions', 'groups']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user


class VariantAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantAssignment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['user']


class ItemSerializer(serializers.Serializer):
    adult = serializers.BooleanField(read_only=True)
    backdrop_path = serializers.CharField(read_only=True)
    genres = serializers.ListField(read_only=True)
    id = serializers.CharField(read_only=True)
    original_language = serializers.CharField(read_only=True)
    original_title = serializers.CharField(read_only=True)
    overview = serializers.CharField(read_only=True)
    poster_path = serializers.CharField(read_only=True)
    release_date = serializers.DateField(read_only=True)
    title = serializers.CharField(read_only=True)
    video = serializers.BooleanField(read_only=True)

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Role.objects.all()
    )
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Role.objects.all()
    )

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User not found")
        return value


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="role.name")

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active"]


class UserListSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="role.name")

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active"]


class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Role.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ["email", "role", "is_active"]

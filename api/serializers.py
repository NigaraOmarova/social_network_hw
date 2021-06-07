from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, DisLike


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ("owner", "likes_number")


class DisLikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = DisLike
        fields = ("owner", "dislikes_number",)


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    likes = LikeSerializer(many=True, read_only=True)
    dislikes = DisLikeSerializer(many=True, read_only=True)
    likes_number = LikeSerializer(many=False, read_only=True)
    dislikes_number = DisLikeSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ['id','title', 'body', 'owner', 'likes','dislikes',"likes_number", "dislikes_number"]


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True, required=True)
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'password','password2'
        )



    def validate_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Name must start with uppercase")
        return value


    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs['password'] != password2:
            raise serializers.ValidationError("Password didn't match")
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



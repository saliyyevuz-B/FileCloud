from rest_framework import serializers
from .models import File, SharedLink
from django.contrib.auth import get_user_model

User = get_user_model()

class FileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    size_display = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'title', 'file', 'owner', 'size', 'size_display', 'views', 'created_at')
        read_only_fields = ('owner', 'size', 'views', 'created_at')

    def get_size_display(self, obj):
        if obj.size is None:
            return "0 KB"
        if obj.size < 1024:
            return f"{obj.size:.2f} KB"
        return f"{obj.size / 1024:.2f} MB"

class SharedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedLink
        fields = '__all__'













class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user') # Default holatda 'user'
        )
        return user
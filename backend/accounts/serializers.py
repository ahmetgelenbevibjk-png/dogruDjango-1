from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from .models import CustomUser, UserProfile, Company, Address
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    location = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'name',
            'username',
            'email',
            'password',
            'phone',
            'website',
            'company',
            'address',
            'location',
            'role',  # <-- 1. BURAYA EKLENDİ
        )

    def create(self, validated_data):
        company_name = validated_data.pop('company', None)
        address_val = validated_data.pop('address', None) or validated_data.pop('location', None)

        # Rol verisini alıyoruz (gelmezse modeldeki default değer geçerli olur)
        user_role = validated_data.pop('role', 'user')

        address_obj = None
        if address_val:
            address_obj = Address.objects.create(street=address_val)

        company_obj = None
        if company_name:
            company_obj, _ = Company.objects.get_or_create(name=company_name)

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            phone=validated_data.get('phone', ''),
            website=validated_data.get('website', ''),
            address=address_obj,
            company=company_obj,
            role=user_role,  # <-- 2. BURADA create_user içine veriliyor
        )
        UserProfile.objects.get_or_create(user=user)

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)
    company = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'name',
            'phone',
            'website',
            'avatar',
            'company',
            'address',
            'location',
            'role',  # <-- 3. BURAYA EKLENDİ (Listeleme/Detayda görünmesi için)
        ]

    def get_company(self, obj):
        if obj.company:
            return obj.company.name
        return None

    def get_address(self, obj):
        if hasattr(obj, 'address') and obj.address:
            if hasattr(obj.address, 'street'):
                return obj.address.street
            return str(obj.address)
        return ''

    def get_location(self, obj):
        return self.get_address(obj)


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', required=False)
    company = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    location = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'name',
            'phone',
            'website',
            'avatar',
            'company',
            'address',
            'location',
            'role',  # <-- 4. BURAYA EKLENDİ (Güncellenebilmesi için)
        ]
        read_only_fields = ['username']

    def update(self, instance, validated_data):
        company_name = validated_data.pop('company', None)
        address_val = validated_data.pop('address', None) or validated_data.pop('location', None)

        profile_data = validated_data.pop('profile', {})
        avatar = profile_data.get('avatar')

        if address_val is not None:
            if instance.address:
                instance.address.street = address_val
                instance.address.save()
            else:
                addr_obj = Address.objects.create(street=address_val)
                instance.address = addr_obj

        # 'role' alanı validated_data içinde kaldığı için bu döngü (for)
        # onu otomatik olarak güncelleyip instance'a atayacaktır.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if company_name is not None:
            if company_name.strip() == "":
                instance.company = None
            else:
                company_obj, _ = Company.objects.get_or_create(name=company_name)
                instance.company = company_obj

        instance.save()

        if avatar is not None:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            profile.avatar = avatar
            profile.save()

        return instance
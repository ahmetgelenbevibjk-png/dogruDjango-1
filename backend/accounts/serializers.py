from rest_framework import serializers
from .models import CustomUser, UserProfile, Company


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # Vue'dan gelen şirket bilgisini karşılamak için ekledik:
    company = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

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
        )

    def create(self, validated_data):
        # Şirket verisini validated_data'dan ayırıyoruz
        company_name = validated_data.pop('company', None)

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            phone=validated_data.get('phone', ''),
            website=validated_data.get('website', ''),
        )
        UserProfile.objects.get_or_create(user=user)

        # Eğer şirket adı girildiyse Company tablosuna da kaydediyoruz
        if company_name:
            Company.objects.get_or_create(user=user, defaults={'name': company_name})

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)

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
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'name',
            'phone',
            'website',
            'avatar',
        ]
        read_only_fields = ['username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        avatar = profile_data.get('avatar')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if avatar is not None:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            profile.avatar = avatar
            profile.save()

        return instance

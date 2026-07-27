from rest_framework import serializers
from .models import CustomUser, UserProfile, Company, Address


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
        )

    def create(self, validated_data):
        company_name = validated_data.pop('company', None)
        # address veya location hangisi dolu geldiyse onu alıyoruz
        address_val = validated_data.pop('address', None) or validated_data.pop('location', None)

        address_obj = None
        if address_val:
            address_obj = Address.objects.create(street=address_val)

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            phone=validated_data.get('phone', ''),
            website=validated_data.get('website', ''),
            address=address_obj,
        )
        UserProfile.objects.get_or_create(user=user)

        if company_name:
            Company.objects.get_or_create(user=user, defaults={'name': company_name})

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', read_only=True)
    company = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()  # Frontend 'location' okuyorsa patlamasın diye

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
        ]

    def get_company(self, obj):
        if hasattr(obj, 'company_detail') and obj.company_detail:
            return obj.company_detail.name
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
        ]
        read_only_fields = ['username']

    def update(self, instance, validated_data):
        company_name = validated_data.pop('company', None)
        # Frontend'den gelen 'address' veya 'location' verisini yakalıyoruz
        address_val = validated_data.pop('address', None) or validated_data.pop('location', None)

        profile_data = validated_data.pop('profile', {})
        avatar = profile_data.get('avatar')

        # Adres bilgisi güncelleniyor veya oluşturuluyor
        if address_val is not None:
            if instance.address:
                instance.address.street = address_val
                instance.address.save()
            else:
                addr_obj = Address.objects.create(street=address_val)
                instance.address = addr_obj

        # Temel kullanıcı alanları güncelleniyor
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Şirket bilgisi güncelleniyor
        if company_name is not None:
            Company.objects.update_or_create(
                user=instance,
                defaults={'name': company_name}
            )

        # Avatar güncelleniyor
        if avatar is not None:
            profile, _ = UserProfile.objects.get_or_create(user=instance)
            profile.avatar = avatar
            profile.save()

        return instance
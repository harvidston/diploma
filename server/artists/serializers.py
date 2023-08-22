from rest_framework import fields, serializers
from django.contrib.auth.models import User
from publications.models import PublicationCategory, Publication, Follower
from artists.models import Artist
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class NewArtistSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = Artist
        fields = ('email', 'username', 'first_name', 'last_name', 'description', 'password', 'token',)

        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)



    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.id,
            'token': user.token
        }


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Artist
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'image', 'username', 'password', 'token']

    def create(self, validated_data):
        user = Artist.objects.create_user(**validated_data)
        
        return {
            'email': user.email,
            'username': user.id,
            'token': user.token
        }

class UserSerializerName(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [ 'username']

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.username

        return name

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only= True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'isAdmin', 'name', 'last_name']

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.username

        return name



class ArtistSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Artist
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image','description']


class ArtistSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Artist
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'image','description', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)

        return str(token.access_token)

class UserSerializerWithToken(ArtistSerializer):
    token = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Artist
        fields = ['id', 'username', 'email', 'isAdmin', 'first_name', 'last_name', 'image', 'description', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)

        return str(token.access_token)

class ListFollowersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = "subscriber.username", read_only = True)
    first_name = serializers.CharField(source = "subscriber.first_name", read_only = True)
    last_name = serializers.CharField(source = "subscriber.last_name", read_only = True)
    user_id = serializers.IntegerField(source = "subscriber.id", read_only = True)
    image = serializers.ImageField(source = "subscriber.image", read_only = True)

    class Meta:
        model = Follower
        fields = ['id', 'image', 'user_id', 'username', 'first_name', 'last_name']


class ListFollowingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = "user.username", read_only = True)
    first_name = serializers.CharField(source = "user.first_name", read_only = True)
    last_name = serializers.CharField(source = "user.last_name", read_only = True)
    user_id = serializers.IntegerField(source = "user.id", read_only = True)
    image = serializers.ImageField(source = "user.image", read_only = True)

    class Meta:
        model = Follower
        fields = ['id', 'image', 'user_id', 'username', 'first_name', 'last_name']

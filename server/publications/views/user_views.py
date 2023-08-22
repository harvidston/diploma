from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters import rest_framework as rest_filters, CharFilter
from rest_framework import filters, response
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.models import User
from publications.models import Publication, PublicationCategory, Order, OrderItem, OrderAddress, Artist, Follower
from publications.serializers import PublicationCategorySerializer, PublicationSerializer, 
from artists.serializers import UserSerializer, UserSerializerWithToken, ArtistSerializer, ArtistSerializerWithToken, UserSerializerName, ListFollowersSerializer, ListFollowingSerializer

from django.contrib.auth.hashers import make_password
from publications.service import PublicationFilter
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework import generics, permissions, views, response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def followArtist(request, pk):
    data = request.data
    subscriber = data['subscriber_id']
    try:
        user = User.objects.get(id=pk)
        subscriber = User.objects.get(id=subscriber)
    except Follower.DoesNotExist:
        return response.Response(status=404)
    Follower.objects.create(subscriber=subscriber, user=user)
    return response.Response(status=201)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def unfollowArtist(request, pk):
    data = request.data
    subscriber = data['subscriber_id']
    try:
        subscriber = User.objects.get(id=subscriber)
        subscription = Follower.objects.get(subscriber=subscriber, user_id=pk)
    except Follower.DoesNotExist:
        return response.Response(status=404)
    subscription.delete()
    return response.Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFollowersArtist(request,pk):
    user = User.objects.get(id=pk)
    followers = Follower.objects.filter(user=user)

    serializer = ListFollowersSerializer(followers, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFollowingArtist(request,pk):
    user = User.objects.get(id=pk)
    following = Follower.objects.filter(subscriber=user)

    serializer = ListFollowingSerializer(following, many = True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateArtistDetails(request):
    artist = request.artist
    
    data = request.data
    artist.description = data['description']

    artist.save()

    return Response('Description was uploaded')

@api_view(['POST'])
def uploadArtistImage(request):
    data = request.data

    artist_id = data['artist_id']
    artist = Artist.objects.get(user=artist_id)

    artist.image = request.FILES.get('image')
    artist.save()

    return Response('Image was uploaded')

@api_view(['GET'])
def getArtist(request, pk):
    user = request.user
    artist = Artist.objects.filter(user=pk)
    serializer = ArtistSerializer(artist, many= True)
    return Response(serializer.data)

@api_view(['GET'])
def getArtists(request):
    user = request.user
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many= True)
    return Response(serializer.data)

@api_view(['GET'])
def getUsers(request):
    user = Artist.objects.all()
    serializer = ArtistSerializer(user, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getUserUsername(request):
    user_id = request.user_id
    user = User.objects.get(id = user_id)
    username = user.username
    serializer = UserSerializerName(user, many = False)
    return Response(serializer.data)

@api_view(['GET'])
def getUserProfile(request, pk):
    user = request.user
    user_publications = Publication.objects.filter(user=pk).order_by('-created_at')

    user_publications_amount = len(user_publications)
    serializer = PublicationSerializer(user_publications, many= True)

    return Response(serializer.data)

@api_view(['GET'])
def getUserPublicationsAmount(request, pk):
    user_publications = Publication.objects.filter(user=pk)
    user_publications_amount = len(user_publications)
    
    data ={
        'amount': user_publications_amount,
    }

    return Response(data)

@api_view(['GET'])
def getUserSettings(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserSettings(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    
    data = request.data
    user.first_name = data['name']
    user.last_name = data['last_name']
    user.username = data['username']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            username = data['username'],
            email = data['email'],
            password = make_password(data['password'])
        )
        user_model = User.objects.get(username = data['username'])
        new_artist = Artist.objects.create(user = user_model)
        new_artist.save()
 
        serializer = UserSerializerWithToken(user, many= False)
        return Response(serializer.data)
    except: 
        message = {'detail': 'User with this email already exists'}
        return Response(message, status = status.HTTP_400_BAD_REQUEST)




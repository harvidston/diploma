from django.shortcuts import render
from publications.models import Publication, PublicationCategory, Artist, Follower
from django_filters import rest_framework as rest_filters, CharFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as rest_filters, CharFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from publications.models import Publication, PublicationCategory, Review
from publications.serializers import PublicationCategorySerializer, PublicationSerializer, ListPostSerializer

from django.contrib.auth.hashers import make_password
from publications.service import PublicationFilter
from rest_framework.views import APIView
from rest_framework import generics

from django.contrib.auth.models import User

from rest_framework import status

from rest_framework import permissions, viewsets, response

from ..service import feed_service
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

class FeedView(viewsets.GenericViewSet):
    serializer_class = ListPostSerializer

    def list(self, request, *args, **kwargs):
        data = request.data
        user_id = data['user_id']
        user = Artist.objects.get(id=user_id)

        queryset = feed_service.get_post_list(user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getFeed(request, pk):
    artist = Artist.objects.get(id=pk)

    queryset = feed_service.get_post_list(artist)
    serializer = ListPostSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createPublication(request, pk):
    artist = Artist.objects.get(id=pk)
    category = PublicationCategory.objects.get(id=9)
    publication = Publication.objects.create(
                artist = artist,
                name = 'Publication Name',
                category = category,
                description = '',
            )
    serializer = PublicationSerializer(publication, many= False)
    return Response(serializer.data)

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    publication_id = data['publication_id']
    publication = Publication.objects.get(id=publication_id)

    publication.image = request.FILES.get('image')
    publication.save()

    return Response('Image was uploaded')

@api_view(['PUT'])
def updatePublication(request, pk):
    data = request.data
    publication = Publication.objects.get(id=pk)
    category = PublicationCategory.objects.get(id=data['category'])

    publication.name = data['name']
    publication.category = category
    publication.description = data['description']

    publication.save()

    serializer = PublicationSerializer(publication, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getPublications(request, category__id=None):
    #publications = Publication.objects.filter(category__id=category__id) if category__id else Publication.objects.all()
    publications = Publication.objects.all()
    serializer = PublicationSerializer(publications, many= True)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PublicationFilter

    return Response(serializer.data)

@api_view(['GET'])
def getPublication(request, pk):
    data = request.data
    publication = Publication.objects.get(id = pk)
    serializer = PublicationSerializer(publication, many = False)

    return Response(serializer.data)

class PublicationListView(generics.ListAPIView):
    serializer_class = PublicationSerializer
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = PublicationFilter
    paginate_by = 2

    search_fields = ['name']

    def get_queryset(self):
        publications = Publication.objects.all().order_by('-created_at')

        return publications

@api_view(['POST'])
def createPublicationReview(request, pk):
    data = request.data
    artist = Artist.objects.get(id = data['artist_id'])
    publication = Publication.objects.get(id=pk)
    
    review = Review.objects.create(
            artist = artist,
            publication = publication,
            comment = data['comment'],
    )

    publication.reviews_amount += 1
    publication.save()

    return Response('Review Added')

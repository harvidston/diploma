from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from publications.models import Publication, PublicationCategory
from publications.serializers import PublicationCategorySerializer, PublicationSerializer


@api_view(['GET'])
def getCategories(request):
    categories = PublicationCategory.objects.all()
    serializer = PublicationCategorySerializer(categories, many= True)
    return Response(serializer.data)

@api_view(['GET'])
def getCategory(request, pk):
    category = None

    pass 


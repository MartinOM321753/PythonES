from users.models import User
from rest_framework import status

from rest_framework.response import Response
from rest_framework import viewsets #conjunto de vistas
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Menu
from .serializers import MenuSerializer

# Create your views here.
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
class findMenusByRestaurant(APIView):
    permission_classes = [AllowAny]

    def get(self, request, restaurant_id, *args, **kwargs):
        menus = Menu.objects.filter(restaurants_id=restaurant_id)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data, status=200)

class MenusByUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        menus = Menu.objects.filter(restaurants__user=user)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
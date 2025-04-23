from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny

from .models import Foods
from .serializers import FoodSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Foods
from restaurants.models import Restaurant

from users.models import User  # Asegúrate de importar el modelo User
from rest_framework.exceptions import NotFound


class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Foods.objects.all().prefetch_related('image')
    serializer_class = FoodSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class FindFoodsByMenu(APIView):
    permission_classes = [AllowAny]

    def get(self, request, menu_id, *args, **kwargs):
        foods = Foods.objects.filter(menu_id=menu_id)
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data, status=200)


class UserFoodsView(generics.ListAPIView):
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Obtener el ID de usuario desde la URL
        user_id = self.kwargs['user_id']

        # Verificar si el usuario existe
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound("Usuario no encontrado")

        # Obtener todos los restaurantes asociados al usuario
        restaurants = Restaurant.objects.filter(user=user)

        # Obtener todos los alimentos asociados a esos restaurantes
        return Foods.objects.filter(menu_restaurants_in=restaurants)
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsRA, IsResident, IsSuperuser
from .serializers import UserSerializer

# Create your views here.

User = get_user_model()

class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class RADashboardView(APIView):
    permission_classes = [IsAuthenticated, IsRA]

    def get(self, request):
        return Response({"message": "Welcome RA, you can manage resident check-ins."})


from rest_framework import permissions, status, views, generics
from rest_framework.response import Response
from users.serializers import RegisterSerializer, MeSerializer
from django.contrib.auth import login
from users.models import CustomUser

class API_Register(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class ProfileAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        return user

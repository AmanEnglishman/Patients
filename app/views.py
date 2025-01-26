from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Patient
from .serializers import PatientSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Добавление конкретных полей в сообщение об ошибке
        if not username or not password:
            return Response({'username': 'This field is required.', 'password': 'This field is required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        # Проверяем учетные данные пользователя
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            # Refresh-токен для обновления access-токена
            access_token = str(refresh.access_token)
            # Access-токен для авторизации
            return Response({"access": access_token, "refresh": str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Проверяем, что пользователь состоит в группе "doctor"
        if not request.user.groups.filter(name='doctor').exists():
            return Response({'detail': 'Access denied: only doctors are allowed.'}, status=status.HTTP_403_FORBIDDEN)

        # Получаем всех пациентов из базы данных
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


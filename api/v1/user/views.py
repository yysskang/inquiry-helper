from django.contrib.auth import authenticate, login, logout

from apps.contract.models import Contract
from apps.user.service.registration import UserRegistrationService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'email': request.data.get('email'),
            'subscription_consent': request.data.get('subscription_consent'),
            'marketing_consent': request.data.get('marketing_consent'),
            'personal_info_consent': request.data.get('personal_info_consent')
        }
        service = UserRegistrationService(user_data=user_data)
        data, error = service.run()

        if error:
            return Response({'error': str(error.message)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            contract = Contract.objects.filter(user=user).first()
            if contract:
                request.session['contract_id'] = contract.id
                request.session['api_key'] = contract.api_key
            return Response({'message': '로그인에 성공했습니다.'}, status=status.HTTP_200_OK)
        return Response({'error': '유저 정보를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):

    def get(self, request):
        logout(request)
        return Response({'message': '정상적으로 로그아웃 되었습니다.'}, status=status.HTTP_200_OK)

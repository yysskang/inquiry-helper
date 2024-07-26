from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.v1.contract.serializers import ContractSerializer
from apps.contract.models import Contract

User = get_user_model()


class ContractViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if Contract.objects.filter(user=user.id).exists():
            return Response({'error': '이미 계약이 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        self.request.session['contract_id'] = serializer.data.get('id')
        self.request.session['api_key'] = serializer.data.get('api_key')
        return Response({'message': '계약이 생성되었습니다.'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response({'message': '정보가 수정되었습니다.'}, status=status.HTTP_200_OK)

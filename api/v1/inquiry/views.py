import json
import os
import boto3
from typing import Optional
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils.timezone import now
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.v1.inquiry.serializers import InquiryManagementSerializer, InquirySerializer
from apps.contract.models import Contract
from apps.inquiry.models import InquiryManagement, Inquiry
from apps.inquiry.service.inquiry import UpdateInquiryService


class InquiryManagementViewSet(mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = InquiryManagementSerializer
    queryset = InquiryManagement.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        contract_id = self.request.session.get('contract_id', None)
        if not contract_id:
            return InquiryManagement.objects.none()
        return self.queryset.filter(contract=contract_id)

    def create(self, request, *args, **kwargs):
        contract_id = self.request.session.get('contract_id')
        if not contract_id:
            return Response({"error": "계약이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        contract = get_object_or_404(Contract, id=contract_id)
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(contract=contract)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_inquiry_types(self, request, pk=None):
        inquiry_management = self.get_object()
        service = UpdateInquiryService(type_data=request.data, inquiry_management=inquiry_management)
        data, error = service.run()

        if error:
            return Response({"error": error.message}, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = InquiryManagementSerializer(data.get("inquiry_management")).data
        return Response(serialized_data, status=status.HTTP_200_OK)


class InquiryViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        contract_id = self.request.session.get('contract_id')
        if not contract_id:
            return Inquiry.objects.none()
        return Inquiry.objects.filter(contract=contract_id)

    def create(self, request, *args, **kwargs):
        api_key = request.META.get('HTTP_APIKEY', "")
        if not api_key:
            return Response({'detail': 'HTTP_APIKEY not found'}, status=status.HTTP_400_BAD_REQUEST)
        contract = Contract.objects.filter(api_key=api_key).first()
        if contract:
            request.data['contract'] = contract.id
            user_email = contract.user.email

            file_url = self.handle_file_upload(request.FILES.get('file'), api_key)
            if file_url:
                request.data['file'] = file_url.replace(" ", "_")

            # 객체 저장
            response = super().create(request, *args, **kwargs)
            if response.status_code == status.HTTP_201_CREATED and user_email:
                self.send_message_to_sqs(request.data, user_email)

            return response
        else:
            return Response({'detail': 'Contract not found'}, status=status.HTTP_400_BAD_REQUEST)

    def handle_file_upload(self, file_obj: Optional[UploadedFile], api_key: str):
        from datetime import datetime
        if file_obj:
            formatted_date = datetime.now().strftime("%Y%m%d")
            original_file_name, file_extension = os.path.splitext(file_obj.name)
            safe_file_name = f"{original_file_name}_{now().strftime('%Y%m%d%H%M%S')}{file_extension}"

            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_key = f"{api_key}/{formatted_date}/{safe_file_name}"
            s3_client.upload_fileobj(
                file_obj,
                bucket_name,
                file_key,
                ExtraArgs={'ContentType': file_obj.content_type, 'ACL': 'private'}
            )
            return f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_key}"
        return None

    def send_message_to_sqs(self, inquiry_data, user_email):
        message = {
            'inquiry': inquiry_data,
            'user_email': "iiomko@naver.com",
        }

        sqs = boto3.client(
            'sqs',
            region_name=settings.AWS_S3_REGION_NAME,
            aws_access_key_id=settings.SQS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.SQS_SECRET_ACCESS_KEY
        )
        queue_url = settings.QUEUE_URL
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message),
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
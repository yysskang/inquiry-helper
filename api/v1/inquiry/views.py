from django.db.models import When, Case, IntegerField
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.pagination import StandardPagination
from api.v1.inquiry.serializers import InquiryManagementSerializer, InquirySerializer
from apps.contract.models import Contract
from apps.inquiry.models import InquiryManagement, Inquiry
from apps.inquiry.service.inquiry import UpdateInquiryService
from util.fileupload import S3Client
from util.sqs_client import SQSClient


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
        contract_id = self.request.session.get('contract_id')
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
                     mixins.ListModelMixin):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    permission_classes = []
    authentication_classes = []
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        contract_id = self.request.session.get('contract_id')
        if not contract_id:
            return Inquiry.objects.none()
        return Inquiry.objects.filter(contract=contract_id).order_by(
            Case(
                When(status=False, then=0),
                default=1,
                output_field=IntegerField()
            ),
            '-created_at'
        )

    def create(self, request, *args, **kwargs):
        api_key = request.META.get('HTTP_APIKEY', "")
        if not api_key:
            return Response({'detail': 'HTTP_APIKEY not found'}, status=status.HTTP_400_BAD_REQUEST)
        contract = Contract.objects.filter(api_key=api_key).first()
        if contract:
            data = request.data.copy()
            data['contract'] = contract.id
            user_email = contract.user.email
            if request.FILES.get('file', ""):
                file_url = self.handle_file_upload(request.FILES.get('file'), api_key)
                if file_url:
                    data['file'] = file_url.replace(" ", "_")

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = Response(serializer.data, status=status.HTTP_201_CREATED)

            if response.status_code == status.HTTP_201_CREATED and user_email:
                self.send_message_to_sqs(request.data, user_email)
            return response

        else:
            return Response({'detail': 'Contract not found'}, status=status.HTTP_400_BAD_REQUEST)

    def handle_file_upload(self, file_obj, api_key: str):
        print("test1")
        if file_obj:
            s3_client = S3Client()
            file_path = s3_client.file_upload(file_obj, api_key)
            return file_path
        return ""

    def send_message_to_sqs(self, inquiry_data, user_email):
        message = {
            'inquiry': inquiry_data,
            'user_email': user_email,
        }

        sqs = SQSClient()
        sqs.send_message(message, 'send_email')

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.authentication_classes = [SessionAuthentication]
        self.pagination_class = StandardPagination
        return super().list(request, *args, **kwargs)
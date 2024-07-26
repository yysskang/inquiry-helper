from django.shortcuts import get_object_or_404

from api.v1.inquiry.serializers import InquiryTypeSerializer, InquiryManagementSerializer
from apps.base.base_class import BaseService, ServiceError, ServiceDataValidationError
from apps.inquiry.models import InquiryType
from typing import Dict, Tuple, Optional, List


class UpdateInquiryService(BaseService):
    permission_classes = []
    data_validation_classes = []

    def __init__(self, type_data: Dict[str, Optional[bool]], inquiry_management):
        self.type_data = type_data
        self.inquiry_management = inquiry_management

    def check_data_validation(self) -> Tuple[bool, Optional[ServiceError]]:
        is_valid, error = super().check_data_validation()
        if not is_valid:
            return is_valid, error

        inquiry_types = self.type_data.get('inquiry_types')

        if not isinstance(inquiry_types, list):
            return False, ServiceError("데이터에 문제가 발생했습니다.")

        if not inquiry_types:
            return False, ServiceError("데이터에 문제가 발생했습니다.")
        return True, None

    def __update_inquiry_type(self, item: Dict) -> InquiryType:
        inquiry_type = get_object_or_404(InquiryType, id=item.get('id'))
        inquiry_type.name = item.get('name', inquiry_type.name)
        inquiry_type.save()
        return inquiry_type

    def __create_inquiry_type(self, item: Dict) -> InquiryType:
        inquiry_type = InquiryType.objects.filter(name=item.get('name')).first()
        if not inquiry_type:
            serializer = InquiryTypeSerializer(data=item)
            if not serializer.is_valid():
                raise ServiceError(serializer.errors)
            inquiry_type = serializer.save()
        return inquiry_type

    def __handle_inquiry_types(self) -> List[InquiryType]:
        new_inquiry_types = []
        for item in self.type_data.get('inquiry_types'):
            if item.get('id'):
                inquiry_type = self.__update_inquiry_type(item)
            else:
                inquiry_type = self.__create_inquiry_type(item)
            new_inquiry_types.append(inquiry_type)
        return new_inquiry_types

    def __remove_deleted_inquiry_types(self, new_inquiry_types: List[InquiryType]):
        current_ids = {inquiry_type.id for inquiry_type in new_inquiry_types}
        for inquiry_type in self.inquiry_management.inquiry_types.all():
            if inquiry_type.id not in current_ids:
                self.inquiry_management.inquiry_types.remove(inquiry_type)

    def _handle_data(self, **kwargs) -> Tuple[Optional[dict], Optional[ServiceError]]:
        new_inquiry_types = self.__handle_inquiry_types()
        self.__remove_deleted_inquiry_types(new_inquiry_types)
        self.inquiry_management.inquiry_types.set(new_inquiry_types)
        self.inquiry_management.save()
        return {"inquiry_management": self.inquiry_management}, None

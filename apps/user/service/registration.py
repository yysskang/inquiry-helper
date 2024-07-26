from apps.base.base_class import BaseService, ServiceError, ServiceDataValidationError
from apps.user.models import UserAgreement
from django.contrib.auth import get_user_model
from typing import Dict, Tuple, Optional

User = get_user_model()


class UserRegistrationService(BaseService):
    permission_classes = []
    data_validation_classes = []

    def __init__(self, user_data: Dict[str, Optional[bool]]):
        self.user_data = user_data

    def check_data_validation(self) -> Tuple[bool, Optional[ServiceError]]:
        is_valid, error = super().check_data_validation()
        if not is_valid:
            return is_valid, error
        if User.objects.filter(username=self.user_data.get("username")).exists():
            return False, ServiceDataValidationError('사용할 수 없는 계정입니다.');

        if not self.user_data.get('personal_info_consent'):
            return False, ServiceDataValidationError('개인 정보 동의는 필수입니다.')

        return True, None

    def _handle_data(self, **kwargs) -> Tuple[Optional[dict], Optional[ServiceError]]:

        user = User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            email=self.user_data['email'],
        )

        UserAgreement.objects.create(
            user=user,
            subscription_consent=self.user_data.get('subscription_consent', False),
            marketing_consent=self.user_data.get('marketing_consent', False),
            personal_info_consent=self.user_data.get('personal_info_consent')
        )
        return {'user_id': user.id}, None

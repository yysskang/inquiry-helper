import logging
from typing import Tuple, Optional
from django.db import transaction as db_transaction


logger = logging.getLogger(__name__)


class ServiceError:
    def __init__(self, message: str = '서비스 오류', data: dict = None, exception=None):
        self.message = message
        self.data = data
        self.exception = exception


class ServiceUnknownError(ServiceError):
    def __init__(self, message: str = '고객센터에 문의가 필요합니다.',
                 data: dict = None,
                 exception=None):
        super().__init__(
            message=message,
            data=data,
            exception=exception
        )


class ServiceDataValidationError(ServiceError):
    def __init__(self, message: str = '입력 값에 문제가 있습니다.', data: dict = None, exception=None):
        super().__init__(
            message=message,
            data=data,
            exception=exception
        )


class BaseService:
    permission_classes = None
    data_validation_classes = None

    def _get_permission_context(self):
        return {}

    def _get_data_validation_context(self):
        return {}

    def check_permission(self) -> Tuple[bool, Optional[ServiceError]]:
        """
            권한체크 영역
        """
        if self.permission_classes:
            context = self._get_permission_context()
            for permission_class in self.permission_classes:
                has_permission, error = permission_class().check(context)
                if not has_permission:
                    return False, error

        return True, None

    def check_data_validation(self) -> Tuple[bool, Optional[ServiceError]]:
        """
            밸리데이션 체크
        """
        if self.data_validation_classes:
            context = self._get_data_validation_context()
            for data_validation_class in self.data_validation_classes:
                is_valid, error = data_validation_class().check(context)
                if not is_valid:
                    return False, error

        return True, None

    def check_runnable(self) -> Tuple[bool, Optional[ServiceError]]:
        """
            권한 / 밸리데이션 체크 실행 부분
        """
        has_permission, permission_error = self.check_permission()
        if not has_permission:
            return has_permission, permission_error

        is_valid, data_error = self.check_data_validation()
        if not is_valid:
            return is_valid, data_error

        return True, None

    def _handle_data(self, **kwargs) -> Tuple[Optional[dict], Optional[ServiceError]]:
        """
            Data DDL
        """
        raise NotImplementedError

    def _setup_in_atomic_block(self):
        pass

    def _handle_exception(self, exception):
        """
            exception 
        """
        logger.error(f'{self.__class__.__name__} failed to run {exception}', exc_info=True)

    def _post_handle_data_success(self, **kwargs):
        """
            Data DDL 성공 시
        """
        pass

    def _post_handle_data_error(self, **kwargs):
        pass

    def run(self, **kwargs) -> Tuple[Optional[dict], Optional[ServiceError]]:
        try:
            with db_transaction.atomic():
                self._setup_in_atomic_block()

                runnable, runnable_error = self.check_runnable()
                if not runnable:
                    return None, runnable_error

                data, error = self._handle_data(**kwargs)

            if error:
                kwargs['error'] = error
                self._post_handle_data_error(**kwargs)
                return None, error
            else:
                kwargs['data'] = data
                try:
                    self._post_handle_data_success(**kwargs)
                except Exception as e:
                    logger.error(f'{self.__class__.__name__} failed to _post_handle_data_success {e}', exc_info=True)

            return data, None

        except BaseException as e:
            self._handle_exception(exception=e)
            return None, ServiceUnknownError(exception=e)


class BasePermission:
    def check(self, context=None) -> Tuple[bool, Optional[ServiceError]]:
        raise NotImplementedError

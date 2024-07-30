## 1. CDK를 통한 인프라 구성
- **AWS CDK/CloudFormation**
  - VPC, 권한, S3 구성
  - ECS Fargate 구성을 통해 Container Orchestration의 용이성과 서버 관리에 대한 리소스 감소
  - ECR 구성
  - 헬스체크, 확장성, 가용성를 고려하여 ALB 구성
  - Autoscaling 구성
  - CPU 80% Scale Up, CPU 20% Scale In

## 2. Github Action
- **CI/CD 파이프라인**
  - **Docker Test Build**: 도커 이미지 테스트 빌드
  - **ECR Push**: 도커 이미지를 AWS ECR에 푸시
  - **ECS Deploy Pipeline**: ECS로 배포 파이프라인 구성

## 3. 활용한 기술 스택
### 클라우드 서비스
- **AWS ECS Fargate, ECR, ALB**
- **AWS CloudWatch**: 로그 연동 및 관리
- **AWS Secrets Manager**: 보안 데이터 관리
- **AWS SQS, Lambda, Amazon EventBridge**: 비동기 및 스케줄링 프로세스 처리
- **AWS S3**: 파일 스토리지 활용

### 프로그래밍 언어 및 프레임워크
- **Python 3.10**, **Django 4.2.4**, **DRF API**
- **MySQL**
- **Docker**
- **JavaScript**, **Jquery**, **Django Template**

- **GenericAPIView**: mixins 클래스를 활용하여 특정 기능만을 구성할 때 사용합니다.
- **ModelViewSet**: 간단한 CRUD 구성이 필요할 때 사용합니다.
- **APIView**: 복잡한 비즈니스 로직이나 외부 서비스와의 통합이 필요한 구성이 필요할 때 사용합니다.
- **Routers 및 Serializers** 활용
- **ServiceLayer**: 복잡한 비즈니스 로직은 구성해둔 BaseService(Permission, Validation, Translations, DML 실행)를 상속받아 가독성 및 에러 추적을 쉽게 합니다.

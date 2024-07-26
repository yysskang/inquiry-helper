import random
import string
from apps.contract.models import Contract
from rest_framework import serializers


def generate_unique_api_key():
    while True:
        api_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        if not Contract.objects.filter(api_key=api_key).exists():
            return api_key


class ContractSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    api_key = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    expiration_date = serializers.DateField()

    class Meta:
        model = Contract
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('view').action == 'update':
            self.fields['expiration_date'].read_only = True

    def create(self, validated_data):
        validated_data['api_key'] = generate_unique_api_key()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for data in ['api_key', 'is_active', 'expiration_date']:
            if data in validated_data:
                raise serializers.ValidationError({data: '수정이 불가능한 항목입니다.'})
        return super().update(instance, validated_data)

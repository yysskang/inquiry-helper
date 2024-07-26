from rest_framework import serializers

from apps.inquiry.models import InquiryType, InquiryManagement, Inquiry


class InquiryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryType
        fields = ['id', 'name']


class InquiryManagementSerializer(serializers.ModelSerializer):
    inquiry_types = InquiryTypeSerializer(many=True, read_only=True)

    class Meta:
        model = InquiryManagement
        fields = ['id', 'contract', 'name', 'phone', 'email', 'attachment', 'link', 'date_time', 'time_placeholder',
                  'address', 'inquiry_types']
        read_only_fields = ['contract']


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

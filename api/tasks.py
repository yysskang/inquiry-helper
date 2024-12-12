from __future__ import absolute_import, unicode_literals
from celery import shared_task
from premailer import transform
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

"""
배포 전 엔진 정보를 반드시 확인해 주세요.
"""


@shared_task
def my_test_add(x, y):
    print(x)
    print(y)
    return x + y


def send_inquiry_email(inquiry_data, user_email):
    try:
        html_content = render_to_string('mail/form.html', {'inquiry_data': inquiry_data})
        inline_html = transform(html_content)
        subject = f"[문의메일] {inquiry_data.get('title', '[확인] 고객의 문의가 등록되었습니다.')}"

        email = EmailMultiAlternatives(
            subject=subject,
            body=inline_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        email.attach_alternative(inline_html, "text/html")
        email.send()
        return {"status": "success", "message": "이메일 전송 성공"}
    except Exception as e:
        return {"status": "error", "message": f"이메일 전송 실패: {e}"}

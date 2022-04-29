from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import Context
from django.conf import settings 


def send_review_email(username, email, url):

    context = {
        'name': username, 
        'url': url
    }
    email_subject = 'Thank you for your review'
    email_body = render_to_string('email_message.txt', context)

    email = EmailMessage(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [email,]
    )
    return email.send(fail_silently=False)
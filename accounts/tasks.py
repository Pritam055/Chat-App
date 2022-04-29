# Create your tasks here 

from celery import shared_task

from accounts.utils import send_review_email


@shared_task
def send_mail_task(username, email,url):
    send_review_email(username, email, url)
from celery.decorators import task
from PIL import Image
from django.core.mail import send_mail


@task
def resize_image(path=None, size=(500, 300)):
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    image.save(path, quality=100)
    return "OK"


@task
def mail_sender(subject, message, sender, recipients, fail=True):
    send_mail(subject=subject,
              message=message,
              from_email=sender,
              recipient_list=recipients,
              fail_silently=fail)
    return "OK"


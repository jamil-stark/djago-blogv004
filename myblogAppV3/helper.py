from django.conf import settings
from django.core.mail import send_mail
from django.utils.text import slugify
import string
import random


def generate_random_string(N):
    res = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return res


def generate_slug(text):
    new_slug = slugify(text)

    from myblogAppV3.models import BlogModel

    if BlogModel.objects.filter(slug=new_slug).first():
        return generate_slug(text + generate_random_string(5))
    return new_slug


def send_mail_to_user(token, email):
    subject = f"Your Account Needs to be Verified."
    message = f"Hello, {email} Paste the link to verify your account.http://127.0.0.1:8000/login/verify/{token}".form
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True

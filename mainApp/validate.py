from api.models import user
from django.contrib import messages

def validate_register(request,user_name,email):

    if user.objects.filter(user_name=user_name).exists():
        messages.error(request,"Username already exists")

    if user.objects.filter(email=email).exists():
        messages.error(request,"Email has been used already")

    if len(messages.get_messages(request))!=0:
        return True
    else:
        return False



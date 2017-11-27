from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token


User = get_user_model()

def delete_token(user):
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except:
        pass


def generate_token(user):
    delete_token(user)
    token = Token.objects.create(user=user)
    return token.key


def logout_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        delete_token(user)
    except:
        raise ValueError

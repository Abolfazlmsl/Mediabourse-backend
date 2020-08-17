"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""
import django
import jwt
from bourse.models import TutorialOwner, TutorialFile
from mediabourse.settings import SECRET_KEY

if django.VERSION >= (1, 10):
    def allow_authenticated(private_file):
        return private_file.request.user.is_authenticated


    def allow_staff(private_file):
        request = private_file.request
        return request.user.is_authenticated and request.user.is_staff


    def allow_superuser(private_file):
        request = private_file.request
        return request.user.is_authenticated and request.user.is_superuser


    def allow_owner(private_file):
        request = private_file.request
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token[7:]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        tutorial_file = TutorialFile.objects.filter(file=private_file.relative_name)
        print(tutorial_file[0].tutorial)
        print(user_id)
        tutorial_owner = TutorialOwner.objects.filter(user_id=user_id, tutorial=tutorial_file[0].tutorial).exists()
        return tutorial_owner

else:
    def allow_authenticated(private_file):
        return private_file.request.user.is_authenticated()


    def allow_staff(private_file):
        request = private_file.request
        return request.user.is_authenticated() and request.user.is_staff


    def allow_superuser(private_file):
        request = private_file.request
        return request.user.is_authenticated() and request.user.is_superuser

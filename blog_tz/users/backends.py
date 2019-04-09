# from django.contrib.auth.models import User
#
#
# class EmailBackend(object):
#
#     def authenticate(self, username = None, password = None, **kwargs):
#         try:
#             user = User.objects.get(email = username)
#         except User.MultipleObjectsReturned:
#             user = User.objects.filter(email = username).order_by('id').first()
#         except User.DoesNotExist:
#             return None
#
#         if getattr(user, 'is_active') and user.check_password(password):
#             return user
#         return None
#
#     def get_user(self, user_id):
#         try:
#             User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):

  def authenticate(self, username=None, password=None, **kwargs):
    UserModel = get_user_model()
    if username is None:
        username = kwargs.get(UserModel.USERNAME_FIELD)
    try:
        if '@' in username:
            UserModel.USERNAME_FIELD = 'email'
        else:
            UserModel.USERNAME_FIELD = 'username'

        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        UserModel().set_password(password)
    else:
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
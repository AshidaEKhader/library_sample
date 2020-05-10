from rest_framework.permissions import BasePermission
from .models import User


class IsLibraryStaff(BasePermission):
    """
    Custom Permission class for checking if the requesting user is admin/library staff
    """

    def has_permission(self, request, view):
        """
        Function to check user is library staff or not
        :param request:
        :param view:
        :return: True if user is a library staff else false
        """
        #: normally users will have a token after login and the user will be accessible from self.request.user. Since
        # don't have any values to identify user, user_uid is explicitly passed with each request. It is passed as a
        #         param "uid"
        user_uid = request.GET.get('user')
        user = User.objects.get(uid=user_uid)

        return user.is_admin


class IsUser(BasePermission):
    """
    Custom Permission class for checking if the requesting user is web user
    """

    def has_permission(self, request, view):
        """
        Function to check user is user or not
        :param request:
        :param view:
        :return: True if user is awe user else false

        #: normally users will have a token after login and the user will be accessible from self.request.user. Since
        # don't have any values to identify user, user_uid is explicitly passed with each request.It is passed as a
        param "uid"
        """
        user_uid = request.GET.get('user')
        user = User.objects.get(uid=user_uid)

        return not user.is_admin
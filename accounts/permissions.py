
# ✅ STEP 1: Create Permission (VERY IMPORTANT)


from rest_framework.permissions import BasePermission
from .models import User

class IsPrincipal(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and
            request.user.role == User.PRINCIPAL
        )
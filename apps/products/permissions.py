from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    اجازه ویرایش و حذف فقط به Owner محصول داده شود.
    بقیه کاربران فقط می‌توانند مشاهده کنند.
    """
    def has_object_permission(self, request, view, obj):
        # دسترسی خواندن برای همه
        if request.method in permissions.SAFE_METHODS:
            return True
        # دسترسی ویرایش و حذف فقط برای Owner
        return obj.owner == request.user
#_____________________________________________________________________________________________
class IsProductOwnerOrReadOnly(permissions.BasePermission):
    """
    اجازه ویرایش و حذف فقط به مالک محصول داده شود.
    کاربران دیگر فقط می‌توانند مشاهده کنند.
    """
    def has_object_permission(self, request, view, obj):
        # دسترسی خواندن برای همه
        if request.method in permissions.SAFE_METHODS:
            return True
        # دسترسی ویرایش و حذف فقط برای مالک محصول
        return obj.product.owner == request.user

from rest_framework.permissions import BasePermission, SAFE_METHODS


# # پرمیشن‌های سفارشی (Custom Permissions)
# class IsFromSpecificCountry(BasePermission):  # پرمیشن سطح کلی (Global Permission)
#     def has_permission(self, request, view):
#         user_country = request.user.profile.country  # فرض کنید Profile به User لینک شده
#         return user_country == "Iran"

# class IsBookAuthorOrAdmin(BasePermission):  # پرمیشن سطح شی (Object-level Permission)
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
#             return True
#         return obj.author == request.user.author or request.user.is_staff

# class IsBookAuthor(BasePermission):  # فقط نویسنده کتاب بتواند آن را حذف کند
#     def has_object_permission(self, request, view, obj):
#         return obj.author == request.user.author  # فرض کنید User به Author لینک شده


class IsAuthorOrAdmin(BasePermission):  # ویرایش کتاب فقط توسط نویسنده یا ادمین
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author.user == request.user or request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    """
    اجازهٔ خواندن برای همه، اما اجازهٔ تغییر فقط برای کاربر مالک پروفایل.
    تنها خود کاربر بتواند اطلاعات پروفایلش را تغییر دهد.
    """

    def has_object_permission(self, request, view, obj):
        # اجازه دسترسی درصورت درخواست‌های امن (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # برای متدهای تغییر، فقط مالک پروفایل دسترسی دارد
        return obj.user == request.user


class OnlyAdminCanEdit(BasePermission):
    """
    اگر درخواست مربوط به تغییر (POST, PUT, PATCH, DELETE) باشد،
    تنها به ادمین‌ها اجازه اعمال تغییر داده می‌شود.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # اجازه خواندن برای همه
            return True
        # برای متدهای تغییر فقط اگر کاربر احراز هویت شده و ادمین است
        return request.user and request.user.is_staff

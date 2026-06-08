from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipe, Tag


# For users specifically, we use UserAdmin. We imported admin.ModelAdmin for other models if we remember.
class UserAdmin(UserAdmin):
    ordering = ["id"]
    list_display = ["email", "name", "is_active"]

    # Here we've use field sets. There are 2 reasons for it:
    #    As we see in User model we have inherited a few classes. Few fields will come from there. Also when we use "UserAdmin" here, it brings up all the
    #    fields within it which are not available in our user model. It internally uses fields tag to show a specific set of fields. If we use the same
    #    fields tag, it will not override the old fields tag.  But fieldsets override.

    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Personal Info", {"fields": ("name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
    )

    # Just like fieldsets for editing, add_fieldset helps us to override the fields when we are trying to add user.
    # password1 and passord2 are django admin specific. Untimately they make it to password field as specified in model.

    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        ("Personal Info", {"fields": ("name",)}),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
admin.site.register(Tag)

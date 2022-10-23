from django.contrib import admin

from .models import User, ExtraInfoMentor


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """ Организация """
    list_display = ('get_full_name', 'email', 'user_type', 'created_at', 'updated_at')
    search_fields = ['get_full_name', 'email']
    list_filter = ('user_type',)


@admin.register(ExtraInfoMentor)
class AdminExtraInfoMentor(admin.ModelAdmin):
    """ Организация """
    list_display = ('mentor', 'type_of_experience', 'audience')
    list_filter = ('type_of_experience', 'audience')

from django.contrib import admin
from main.models import Review, Contact, Home, About, Team, Profile
from menu.models import Menu
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.TabularInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
admin.site.unregister(model_or_iterable=User)
admin.site.register(model_or_iterable=User, admin_class=CustomUserAdmin)


class HomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'faderimage1', 'faderimage2', 'faderimage3',
                    'cake1_image', 'cake2_image', 'cake3_image', 'banner_image', 'cart_banner_image')
admin.site.register(Home, HomeAdmin)


class AboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'mission', 'banner_image', 'banner_image2')
admin.site.register(About, AboutAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'image', 'description')
admin.site.register(Team, TeamAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'published', 'created', 'updated')
    list_editable = ('published',)
    search_fields = ('name', 'body')
admin.site.register(Review, ReviewAdmin)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'banner_image',)
admin.site.register(Menu, MenuAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'date')
    search_fields = ('name', 'email', 'phone', 'subject', 'message', 'date')
admin.site.register(Contact, ContactAdmin)

admin.site.site_header = "Flower-Flour Administration"
admin.site.site_title = "Flower-Flour"
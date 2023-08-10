from django.contrib import admin
from .models import *
from datetime import datetime, date

from django.contrib.auth.models import User, Group

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import GroupAdmin

from .forms.admin import *

admin.site.unregister(User)
admin.site.unregister(Group)

class SubscriptionInline(admin.StackedInline):
    # template = "codelines-admin/edit_inline/stacked.html"
    model = UserSubscriptions
    extra = 0

class UserDataInline(admin.StackedInline):
    # template = "codelines-admin/edit_inline/stacked.html"
    model = UserData

class PopulationAdmin(UserAdmin):
    inlines = (UserDataInline,SubscriptionInline,)
    list_display = (
        'name',
        'email',
        'is_active',
        'is_staff',
        'status',
        'subscriptions',
    )

    # add_form = PopulationCreateAdminForm
    # form = PopulationChangeAdminForm

    # add_form_template = "codelines-admin/change_form.html"

    def name(self, obj):
        return obj.last_name+", "+obj.first_name
    def sub_date(self, obj):
        return obj.userdata.subscription_date.strftime("%d %B, %Y")
    
    def expires(self, obj):
        return obj.userdata.subscription_expiration_date.strftime("%d %B, %Y")
    
    def remaining(self, obj):
        delta = obj.userdata.subscription_expiration_date - obj.userdata.subscription_date
        return str(delta.days) + " day/s"

    def status(self, obj):
        if obj.userdata.banned:
            return "BANNED"
        else:
            return "NORMAL"
  
    def subscriptions(self, obj):
        return obj.usersubscriptions_set.count()

class PopulationGroupAdmin(GroupAdmin):
    pass
  
class SubscriptionAdmin(admin.ModelAdmin):
    model = UserSubscriptions

    add_form = SubscriptionAdminChangeAdmin
    form = SubscriptionAdminChangeAdmin

    add_form_template = "codelines-admin/change_form.html"
    change_list_template = "codelines-admin/change_list.html"

    list_display = (
        'subscriber',
        'course',
        'subscription_date',
        'subscription_expiration_date',
    )
    def subscriber(self, obj):
        return str(obj.owner.last_name) + ", " + str(obj.owner.first_name)

admin.site.register(User, PopulationAdmin)
admin.site.register(Group, PopulationGroupAdmin)
admin.site.register(UserSubscriptions, SubscriptionAdmin)



from django.contrib import admin
from reversion.admin import VersionAdmin
from payments.models import Plan, Subscription
class YourModelAdmin(VersionAdmin):
    """Admin settings go here."""


class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('user', 'plan', 'projects', 'revenue')

class PlanAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'is_active', 'free_trial_days', 'created', 'number_of_subscriptions', 'revenue')
    list_filter = ('is_active', 'price')
    
    prepopulated_fields = {"slug": ("name",)}

    def queryset(self, request):
        qs = super(PlanAdmin, self).queryset(request)
        #qs = list(qs)
        #qs.append(Plan())
        return qs


admin.site.register(Plan, PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

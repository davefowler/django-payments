
from django.conf.urls.defaults import *


from payments.views import form_view




urlpatterns = patterns('',
    ('^form/(?P<plan_slug>.*)/$', form_view, {}, 'payments_form'),
    ('^edit/(?P<subscription_id>\d+)/$', form_view, {}, 'payments_edit_form'),
                       
    )

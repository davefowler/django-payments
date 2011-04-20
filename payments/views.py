
from payments.forms import SubscriptionForm
from payments.models import Plan, Subscription, SUCCESS_REDIRECT_URL
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect


from django.contrib.auth.decorators import login_required

@login_required
def form_view(request, plan_slug = "", subscription_id = ""):
    subscription = None
    
    if plan_slug != "":
        plan = get_object_or_404(Plan, slug=plan_slug)
    else:
        subscription = Subscription.objects.get(id = int(subscription_id))
        plan = subscription.plan
    
    if request.method=="POST":
        form = SubscriptionForm(request.POST, instance = subscription or Subscription(plan = plan))
        form.request = request
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(SUCCESS_REDIRECT_URL)

    else:
        form = SubscriptionForm(instance = Subscription(plan = plan))

    return render_to_response('payments/subscription_form.html', {'form': form, 'plan': plan }, context_instance=RequestContext(request))

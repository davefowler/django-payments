
__test__ = {
"Payment Form": """

>>> from django.test.client import Client
>>> from django.core.urlresolvers import reverse
>>> from django.contrib.auth.models import User

# Create an Authenticated User
>>> user = User.objects.create_user("payment@form.com", "payment@form.com", "pass")
>>> user.is_staff = True; user.is_superuser = True; user.save();
>>> c = Client()

>>> from django.conf import settings
>>> r = c.post(reverse(settings.LOGIN_URL), {'email': user.username, "password": "pass"})
>>> r.status_code # should redirect if login worked
302

# Create a few plans
>>> from payments.models import Plan, Subscription
>>> Plan.objects.all().delete(); Subscription.objects.all().delete();
>>> basic = Plan(slug='basic', name="basic", price=2000, free_trial_days = 30, per="month", limits={'users': 2})
>>> basic.save()
>>> advanced = Plan(slug='advanced', name="advanced", price=4000, free_trial_days = 30, per="month", limits={'users': 2})
>>> advanced.save()

# Bad Year
>>> r = c.post(reverse('payments_form', args=['basic']), {'exp_month': '10', 'exp_year': '2009', 'number': 4242424242424242, 'plan': basic.id })
>>> r.status_code
200
>>> r.context['form'].errors 
{'__all__': [u"Your card's expiration year is invalid"]}

# Bad Month
>>> r = c.post(reverse('payments_form', args=['basic']), {'exp_month': 'a9', 'exp_year': '2011', 'number': 4242424242424242, 'plan': basic.id })
>>> r.status_code
200
>>> r.context['form'].errors
{'__all__': [u'exp_month should be an int (is None)']}

# Bad Number
>>> r = c.post(reverse('payments_form', args=['basic']), {'exp_month': 'a9', 'exp_year': '2011', 'number': "asdf", 'plan': basic.id })
>>> r.status_code
200
>>> r.context['form'].errors
{'number': [u'Enter a whole number.'], '__all__': [u'exp_month should be an int (is None)']}

>>> r = c.post(reverse('payments_form', args=['basic']), {'exp_month': 10, 'exp_year': 2011, 'number': 4242424242424242, 'plan': basic.id })
>>> r.status_code
302

# Ensure that the user is in the subscription
>>> Subscription.objects.all().count()
1
>>> sub = Subscription.objects.all()[0]
>>> sub.user.id == user.id
True
>>> sub.plan
<Plan: basic>

# Edit the subscription from the Basic plan to the Advanced
>>> r = c.post(reverse('payments_edit_form', args=[sub.id]), {'exp_month': 10, 'exp_year': 2011, 'number': 4242424242424242, 'plan': advanced.id })
>>> r.status_code
302


>>> Subscription.objects.all().count()
1
>>> sub = Subscription.objects.get(id = sub.id)
>>> sub.plan
<Plan: advanced>

""",

"Payment": """

# NOTE!  Make sure your API key is not in livemode when you do these tests!
Documentation on that is here http://eta.devpayments.com/api

>>> from payments.models import Plan, Subscription, User

# Make a 20/mo plan with a 30 day free trial
>>> plan = Plan(price=2000, free_trial_days = 30, per="month", limits={'users': 2})
>>> plan.save()

# Make an example user and an Subscription for them with this plan
>>> user = User.objects.create_user("devpaymentstest", "dev@payments.com", "pass")

# Sample card credentials
>>> number = 4242424242424242; exp_month = 10; exp_year = 2011

>>> nsubs = Subscription.objects.all().count()
>>> subscription = Subscription.objects.new(plan, user, number, exp_month, exp_year)
>>> subscription.active_card
True

# Ensure that a subscription was saved.
>>> Subscription.objects.all().count() - nsubs 
1
>>> len(subscription.devpayments_id) > 2
True



####  Now lets deal with crappy/invalid payments. ####


# Expiration date is already passed...
>>> from devpayments import *
>>> try:
...   badsub = Subscription.objects.new(plan, user, number, exp_month, 2008)
... except CardException, e:
...   print e
Your card's expiration year is invalid


# Month is not 0-11
>>> try:
...   badsub = Subscription.objects.new(plan, user, number, 18, exp_year)
... except CardException, e:
...   print e
Your card's expiration month is invalid





"""}


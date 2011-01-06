
__test__ = {"New Project with User Limits": """

The following example creates a payment plan with a limit of 1 user.
It then adds a user to it, and runs into the limit when adding another.


>>> from payments.models import Subscription, Plan, QuotaException

# Make a plan and note that you can create an arbitrary dict of limits: limits={'users': 1}
>>> plan = Plan(name='Single User', slug='single', price='3000', per='month', limits={'users': 1}); 
>>> plan.save()

>>> from demo.projects.models import User, Project

# create a new project
>>> project = Project(name='example'); project.save()

# create a new user and subscription
>>> user = User.objects.create_user('projtester', 'projtester@chart.io', 'pass')
>>> subscription = Subscription.objects.new(plan = plan, user = user, card_number = 4242424242424242, exp_month = 10, exp_year = 2015)

# add the subscription to the project
>>> project.subscription = subscription
>>> project.save()

# We should be able to add 1 user
>>> project.add_user(user)
>>> project.users.all().count()
1

# But not the second!
>>> another_user = User.objects.create_user('another', 'another@chart.io', 'pass')
>>> try: 
...   project.add_user(another_user)
... except QuotaException, e:
...   print "QuotaException: ", e
QuotaException: You have reached your limit of users.  Please Upgrade!


"""}


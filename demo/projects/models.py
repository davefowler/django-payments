from django.db import models

from django.contrib.auth.models import User
from payments.models import Subscription, QuotaException

class Project(models.Model):

    name = models.CharField(max_length = 40)
    
    users = models.ManyToManyField(User, related_name = 'projects', editable=False)

    # The link to the payment.
    subscription = models.ForeignKey(Subscription, null=True, blank=True)
    
    
    def add_user(self, user):
        """
        Wrapper to add a user to the project.  

        Note: You could do this with signals the pre-save of the many2many relationship and then still 
        be able to do project.users.add( someuser ) the same way you normally would but as of writing this
        that's a very new feature for django1.2 only. http://docs.djangoproject.com/en/dev/ref/signals/#m2m-changed
        """
        

        # Raise an exception if their plan doesn't allow this many users...
        # They need to upgrade!
        if self.subscription.plan.limits.get('users', 0) < self.users.all().count() + 1:
            raise QuotaException("You have reached your limit of users.  Please Upgrade!")

        return self.users.add(user)


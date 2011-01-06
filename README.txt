=========================================
Django Payments
=========================================
A Plans, Subcriptions and payment processing library using Stripe.com as the payment processor.

WARNING: The following libary requires you to get private beta access to the stripe.com api.  Don't try this if you don't have it.


Created by Dave Fowler dave@chart.io


Setup:

Include the following in your urls.py

    (r'^payments/', include('payments.urls')),


in payments/models.py edit the configurable options at the top including your STRIPE_API_KEY that you obtain from stripe.com

STRIPE_API_KEY = "YOURKEYHERE"


---- More to come on this later  ---

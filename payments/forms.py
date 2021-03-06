from django import forms
from payments.models import Plan, Subscription


PLAN_CHOICES = tuple([(plan.id, plan.name) for plan in Plan.objects.filter(is_active=True)])


from datetime import datetime
year = datetime.now().year
YEAR_CHOICES = tuple([(y, y) for y in range(year, year+15)])
MONTH_CHOICES = tuple([(m, m) for m in range(1, 13)])

class SubscriptionForm(forms.ModelForm):

    number = forms.IntegerField(label="Credit Card Number")
    exp_month = forms.ChoiceField(label="Expiration Month", choices = MONTH_CHOICES)
    
    exp_year = forms.ChoiceField(label="Expiration Year", choices = YEAR_CHOICES)
    
    #plan = forms.ChoiceField(label="Plan", choices = PLAN_CHOICES)
    
    class Meta:
        model = Subscription
        fields = ('plan', )


    def clean_exp_month(self):
        try:
            return int(self.cleaned_data['exp_month'])
        except:
            #raise forms.ValidationError("The Expiration Month is invalid.")
            pass # The dev payments API handles this warning
        
    def clean_exp_year(self):
        try:
            return int(self.cleaned_data['exp_year'])
        except:
            raise forms.ValidationError("The Expiration Year is invalid.")
        
    def clean_number(self):
        try:
            return int(self.cleaned_data['number'])
        except:
            raise forms.ValidationError("Your Credit Card Number is invalid")
        
    
    def clean(self):
        from stripe import StripeException

        self.instance.user = self.request.user

        # Ensure that the card is valid
        try:
            paid = self.instance.pay(self.cleaned_data.get('number'), self.cleaned_data.get('exp_month'), self.cleaned_data.get('exp_year'))
        except StripeException, e: 
            raise forms.ValidationError(e)
        

        return self.cleaned_data

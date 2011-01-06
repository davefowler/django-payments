from django import forms
from payments.models import Plan, Subscription


PLAN_CHOICES = tuple([(plan.id, plan.name) for plan in Plan.objects.filter(is_active=True)])

class SubscriptionForm(forms.ModelForm):

    number = forms.IntegerField(label="Credit Card Number")
    exp_month = forms.CharField(label="Expiration Month", max_length = 2)
    
    exp_year = forms.CharField(label="Expiration Year", max_length = 4)
    
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
        from devpayments import DevPayException

        self.instance.user = self.request.user

        # Ensure that the card is valid
        try:
            paid = self.instance.pay(self.cleaned_data.get('number'), self.cleaned_data.get('exp_month'), self.cleaned_data.get('exp_year'))
        except DevPayException, e: 
            raise forms.ValidationError(e)
        

        return self.cleaned_data

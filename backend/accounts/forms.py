from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import OrgUser, Organization

class OrgUserSignupForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        required=False,
        empty_label="Select existing organization",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    new_organization = forms.CharField(
        max_length=255,
        required=False,
        help_text="Enter a new organization name if you are not joining an existing one",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    class Meta:
        model = OrgUser
        fields = ('username', 'email', 'organization', 'new_organization', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        org = cleaned_data.get("organization")
        new_org = cleaned_data.get("new_organization")

        if not org and not new_org:
            self.add_error('organization', "Select an existing organization or enter a new one.")
            self.add_error('new_organization', "Select an existing organization or enter a new one.")
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        org = self.cleaned_data.get('organization')
        new_org_name = self.cleaned_data.get('new_organization')

        if new_org_name:
            org, created = Organization.objects.get_or_create(name=new_org_name)

        user.organization = org
        user.set_password(self.cleaned_data["password"])  # hash password properly

        if commit:
            user.save()
        return user

class OrgUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

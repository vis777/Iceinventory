from django import forms
from django.contrib.auth.models import User
from .models import ShopOwner
from django.contrib.auth.forms import AuthenticationForm

class ShopOwnerRegistrationForm(forms.ModelForm):
    """Form for registering and editing ShopOwner details."""
    
    email = forms.EmailField(required=True)
    owner_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    shop_name = forms.CharField(required=True)
    location = forms.CharField(required=True)
    shop_image = forms.ImageField(required=False)  # Optional
    
    # Fields only required for registration
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = ShopOwner
        fields = ["owner_name", "phone", "shop_name", "location", "shop_image", "email"]

    def __init__(self, *args, **kwargs):
        """Dynamically remove password fields when editing a profile."""
        super().__init__(*args, **kwargs)

        if self.instance.pk:  # If instance exists, it's an edit, so remove password fields
            self.fields.pop("password", None)
            self.fields.pop("confirm_password", None)

    def clean_email(self):
        """Ensure email is unique for other users."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(id=self.instance.user.id if self.instance.pk else None).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone(self):
        """Ensure phone number is unique."""
        phone = self.cleaned_data.get("phone")
        if ShopOwner.objects.filter(phone=phone).exclude(id=self.instance.id if self.instance.pk else None).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone

    def clean(self):
        """Check if passwords match (only during registration)."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class ShopOwnerLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    class Meta:
        model = ShopOwner
        fields = ('username', 'password', 'remember_me')
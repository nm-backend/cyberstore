import re

from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this field.
    website = forms.CharField(required=False)

    class Meta:
        model = Lead
        fields = ["name", "phone", "wants_installment", "comment"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = re.sub(r"\D", "", phone)
        if not 9 <= len(digits) <= 15:
            raise forms.ValidationError("Введите номер телефона, например +996 555 123 456.")
        return phone

    def clean_name(self):
        return self.cleaned_data["name"].strip()

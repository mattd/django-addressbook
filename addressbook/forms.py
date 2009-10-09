from django.forms import ModelForm

from addressbook.models import Person, Organization


class PersonForm(ModelForm):
    class Meta:
        model = Person


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

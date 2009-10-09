from django.forms import ModelForm

from addressbook.models import Person, Organization


class PersonForm(ModelForm):
    class Meta:
        model = Person
        exclude = ('date_added', 'date_modified')


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ('date_added', 'date_modified')

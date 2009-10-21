from datetime import datetime

from django import forms
from django.forms import ModelForm

from addressbook.models import Person, Organization


class PersonForm(ModelForm):
    """A model form for Person objects.

    One twist: instead of displaying a standard ModelChoiceField for the
    Person's related Organization, use a CharField and pick the correct
    Organization from user input.

    """
    organization = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Person
        exclude = ('organization', 'date_added', 'date_modified')

    def save(self, force_insert=False, force_update=False, commit=True):
        """Override the default ModelForm ``save()`` method.
        
        Check if an organization with the given name exists. If so, attach the
        person. If not, create the organization and then attach the person.

        """
        instance = super(PersonForm, self).save(commit=False)
        # No blank Organization names, please.
        org_name = self.cleaned_data['organization'].strip()
        if org_name:
            try:
                organization = Organization.objects.get(name__iexact=org_name)
            except Organization.DoesNotExist:
                organization = Organization(name=org_name, 
                                            date_added=datetime.now())
                organization.save()
            instance.organization = organization
        if commit:
            instance.save()

        return instance


class OrganizationForm(ModelForm):
    """A model form for Organization objects."""
    class Meta:
        model = Organization
        exclude = ('date_added', 'date_modified')

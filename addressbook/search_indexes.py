from haystack import indexes
from haystack import site 

from addressbook.models import Person, EmailAddress, IMAccount, Note, \
    Organization, PhoneNumber, StreetAddress, Website


class PersonIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def prepare_name(self, object):
        """Populate a Person object's name field in a sort friendly manner.

        This is needed for sorting the results of a combined search on Person and 
        Organization objects as it provides a common field name to order_by.

        """
        return "%s %s %s" % (object.last_name, object.first_name,
                             object.middle_name)
    

site.register(Person, PersonIndex)
site.register(EmailAddress)
site.register(IMAccount)
site.register(Note)
site.register(Organization)
site.register(PhoneNumber)
site.register(StreetAddress)
site.register(Website)

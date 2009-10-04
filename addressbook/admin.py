from django.contrib import admin
from django.contrib.contenttypes import generic

from addressbook.models import Person, Organization, EmailAddress, \
    StreetAddress, PhoneNumber, Website, IMAccount, Note

class StreetAddressInline(generic.GenericTabularInline):
    model = StreetAddress 

class EmailAddressInline(generic.GenericTabularInline):
    model = EmailAddress

class PhoneNumberInline(generic.GenericTabularInline):
    model = PhoneNumber 

class WebsiteInline(generic.GenericTabularInline):
    model = Website 

class IMAccountInline(generic.GenericTabularInline):
    model = IMAccount

class NoteInline(generic.GenericTabularInline):
    model = Note

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        StreetAddressInline,
        EmailAddressInline,
        PhoneNumberInline,
        WebsiteInline,
        IMAccountInline,
        NoteInline,
    ]

class PersonAdmin(admin.ModelAdmin):
    inlines = [
        StreetAddressInline,
        EmailAddressInline,
        PhoneNumberInline,
        WebsiteInline,
        IMAccountInline,
        NoteInline,
    ]

admin.site.register(Person, PersonAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(StreetAddress)
admin.site.register(EmailAddress)
admin.site.register(PhoneNumber)
admin.site.register(Website)
admin.site.register(IMAccount)
admin.site.register(Note)

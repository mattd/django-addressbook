from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class GenericRelationshipMixin(models.Model):
    """A mixin for adding generic relationship fields to a model."""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class DateMixin(models.Model):
    """A mixin for adding created and modified dates to a model."""
    date_added = models.DateTimeField(_('date added'), default=datetime.now)
    date_modified = models.DateTimeField(_('date modified'), null=True, 
                                         blank=True)

    class Meta:
        abstract = True

    def save(self):
        self.date_modified = datetime.now()
        super(DateMixin, self).save()


class EmailAddress(GenericRelationshipMixin, DateMixin):
    """A generically related email address model."""
    TYPE_CHOICES = (
        ('main', _('Main')),
        ('personal', _('Personal')),
        ('work', _('Work')),
        ('other', _('Other')),
    )
    address = models.EmailField(_('address'), max_length=100, blank=True, 
                                null=True)
    type = models.CharField(_('type'), max_length=15, choices=TYPE_CHOICES, 
                            blank=True, null=True)

    class Meta:
        verbose_name = _('email address')
        verbose_name_plural = _('email addresses')

    def __unicode__(self):
        return u'%s' % self.address


class StreetAddress(GenericRelationshipMixin, DateMixin):
    """A generically related street address model."""
    TYPE_CHOICES = (
        ('main', _('Main')),
        ('home', _('Home')),
        ('work', _('Work')),
        ('other', _('Other')),
    )
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, blank=True,
                            null=True)

    class Meta:
        verbose_name = _('street address')
        verbose_name_plural = _('street addresses')

    def __unicode__(self):
        return u'%s, %s, %s %s' % (self.address, self.city, self.state,
                                   self.zip)


class PhoneNumber(GenericRelationshipMixin, DateMixin):
    """A generically related phone number model."""
    TYPE_CHOICES = (
        ('main', _('Main')),
        ('home', _('Home')),
        ('work', _('Work')),
        ('mobile', _('Mobile')),
        ('fax', _('Fax')),
        ('other', _('Other')),
    )
    number = models.CharField(_('number'), max_length=20, blank=True, 
                              null=True)
    type = models.CharField(_('type'), max_length=15, choices=TYPE_CHOICES, 
                            blank=True, null=True)

    class Meta:
        verbose_name = _('phone number')
        verbose_name_plural = _('phone numbers')

    def __unicode__(self):
        return u'%s' % self.number


class Website(GenericRelationshipMixin, DateMixin):
    """A generically related website model."""
    TYPE_CHOICES = (
        ('work', _('Work')),
        ('personal', _('Personal')),
        ('other', _('Other')),
    )
    name = models.CharField(_('name'), max_length=200, blank=True, null=True)
    url = models.URLField(_('url'), max_length=100, blank=True, null=True)
    type = models.CharField(_('type'), max_length=15, choices=TYPE_CHOICES, 
                            blank=True, null=True)

    class Meta:
        verbose_name = _('website')
        verbose_name_plural = _('websites')

    def __unicode__(self):
        return u'%s' % self.url


class IMAccount(GenericRelationshipMixin, DateMixin):
    """A generically related IM model."""
    SERVICE_CHOICES = (
        ('aim', _('AIM')),
        ('msn', _('MSN')),
        ('icq', _('ICQ')),
        ('jabber', _('Jabber')),
        ('yahoo', _('Yahoo')),
        ('skype', _('Skype')),
        ('qq', _('QQ')),
        ('sametime', _('Sametime')),
        ('gadu-gadu', _('Gadu-Gadu')),
        ('google-talk', _('Google Talk')),
        ('other', _('Other'))
    )
    TYPE_CHOICES = (
        ('work', _('Work')),
        ('personal', _('Personal')),
        ('other', _('Other')),
    )
    username = models.CharField(_('username'), max_length=100)
    service = models.CharField(_('service'), max_length=15, 
                               choices=SERVICE_CHOICES, blank=True, null=True)
    type = models.CharField(_('type'), max_length=15, choices=TYPE_CHOICES, 
                            blank=True, null=True)

    class Meta:
        verbose_name = _('IM account')
        verbose_name_plural = _('IM accounts')

    def __unicode__(self):
        return u'%s (%s)' % (self.username, self.get_service_display())


class Note(GenericRelationshipMixin, DateMixin):
    """A generic note model."""
    content = models.TextField(_('content'))
    reference_date = models.DateTimeField(_('reference date'), null=True, 
                                          blank=True)

    class Meta:
        verbose_name = _('note')
        verbose_name_plural = _('notes')

    def __unicode__(self):
        return u'%s' % self.content


class ContactInfoMixin(models.Model):
    """An abstract base class providing common contact information."""
    street_addresses = generic.GenericRelation(StreetAddress, blank=True, 
                                               null=True)
    phone_numbers = generic.GenericRelation(PhoneNumber, blank=True, null=True)
    email_addresses = generic.GenericRelation(EmailAddress, blank=True, 
                                              null=True)
    websites = generic.GenericRelation(Website, blank=True, null=True)
    im_accounts = generic.GenericRelation(IMAccount, blank=True, null=True)
    notes = generic.GenericRelation(Note, blank=True, null=True)

    class Meta:
        abstract = True


class Organization(ContactInfoMixin, DateMixin):
    """Organization Model

    Organizations are institutions to which contacts may be associated. 

    """
    name = models.CharField(_('name'), max_length=200)

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        ordering = ('name',)
    
    def __unicode__(self):
        return u'%s' % self.name

    @permalink
    def get_absolute_url(self):
        return ('addressbook_organization_detail', (), {
            'organization_id': self.id,
        })


class Person(ContactInfoMixin, DateMixin):
    """Person Model

    A person is an individual that may be associated with an Organization. Note
    that the name field is blank on each record. It exists solely to provide a
    consistent way of sorting Person and Organization results via haystack.

    """
    organization = models.ForeignKey(Organization, blank=True, null=True)
    title = models.CharField(_('title'), max_length=100, blank=True)
    first_name = models.CharField(_('first name'), max_length=50)
    middle_name = models.CharField(_('middle name'), max_length=50, blank=True, 
                                   null=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True, 
                                 null=True)
    name = models.CharField(_('name'), max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('people')
        ordering = ('last_name', 'first_name',)

    def __unicode__(self):
        return u'%s' % self.full_name
        
    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @permalink
    def get_absolute_url(self):
        return ('addressbook_person_detail', (), {
            'person_id': self.id,
        })
        

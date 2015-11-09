__author__ = "Jonathan Carlton"
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# The type of user
USER_TYPE = (
    ('1', 'Staff'),
    ('2', 'Student')
)

# Level in which the communication relates too
LEVEL = (
    ('N/A', 'N/A'),
    ('UG', 'Undergraduate'),
    ('PGT', 'Postgraduate Taught'),
    ('PGR', 'Postgraduate Research'),
    ('ST', 'Staff')
)

class Audience(models.Model):
    """
    Audience model describes the type internal or external
    media format the communication has been published on
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return "%s %s" % (self.name, self.description)

class Sources(models.Model):
    """
    Describes the source of the data, where/who it has
    come from
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return "%s" % self.name

class UserProfile(models.Model):
    """
    User profile for those that are a member of the site
    """
    user = models.OneToOneField(User)
    username = models.CharField(max_length=255)
    title = models.CharField(max_length=35)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=1, choices=USER_TYPE)
    email = models.EmailField()
    smart_card = models.CharField(max_length=255)
    login_count = models.IntegerField()
    last_login = models.DateField(auto_now_add=False, auto_now=True)
    unit = models.CharField(max_length=255)
    known_as = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __unicode__(self):
        return "%s" % self.user

class Tags(models.Model):
    """
    Tags relate to the type of Communication that is being stored,
    allows for faster searching on the jQueryTables
    """
    name = models.CharField(max_length=255)
    history = HistoricalRecords()

    def __unicode__(self):
        return "%s" % self.name

class Notes(models.Model):
    """
    Notes are defined by the user entering the communication,
    generally small comments in relation to the communication
    """
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    created_on = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey('UserProfile', blank=True, null=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return "%s, %s: %s" % (self.title, self.created_on, self.created_by)

class Communication(models.Model):
    """
    Main bulk of the models, this defines the communication that is
    being added by the users.
    """
    short_desc = models.CharField(max_length=140)
    full_desc = models.CharField(max_length=3000)
    bh_number = models.CharField(max_length=255, null=True, blank=True)
    value_of_award = models.IntegerField(default=0)
    value_awarded_to_ncl = models.IntegerField(default=0, null=True, blank=True)
    project_start_date = models.DateField()
    duration = models.IntegerField(default=0)
    individuals = models.ManyToManyField(UserProfile, related_name="communication_individuals", null=True, blank=True)
    external = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(UserProfile, null=True)
    created_on = models.DateField(null=True)
    source = models.ForeignKey(Sources, null=True)
    admin_checked = models.BooleanField(default=False)
    level = models.CharField(max_length=3, choices=LEVEL)
    tags = models.ManyToManyField(Tags, related_name="communication_tags", null=True, blank=True)
    notes = models.ManyToManyField(Notes, related_name="communication_notes", null=True, blank=True)
    flag = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return "%s" % self.short_desc

class CommsAudit(models.Model):
    """
    Records when the data has been communicated out and by whom
    """
    sent = models.ForeignKey(Communication, null=True)
    sent_by = models.ForeignKey(UserProfile, null=True, blank=True)
    # TODO Should really be a many to many field
    audience = models.ForeignKey(Audience, null=True)
    from_date = models.DateField(null=True)
    to_date = models.DateField(null=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return "%s" % self.sent

class Newsletter(models.Model):
    audit = models.ForeignKey(CommsAudit)
    
    # Twitter will only allow a maximum length of 23, including https://
    # see: https://dev.twitter.com/rest/reference/get/help/configuration
    link = models.CharField(max_length=23)

    def __unicode__(self):
        return "%s" % self.audit.sent.short_desc

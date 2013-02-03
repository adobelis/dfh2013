from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _

class Workspace(models.Model):
    """
    A shared permission 'space', users with access to items in a workspace
    can see all projects/samples/content related to that workspace.
    """
    workspace_name = models.CharField(max_length=150)
    dt_created = models.DateTimeField(default=datetime.utcnow, editable=False)
    def __unicode__(self):
        return u'%s' % self.workspace_name
    

class UserProfile(models.Model):
    """
    Any person using the system
    """
    user                = models.OneToOneField(User, primary_key=True)
    full_name           = models.CharField(max_length=100)
    workspace           = models.ManyToManyField(Workspace, through="WorkspaceMembership", 
                                                 related_name="wkspace")
    email            = models.EmailField(_('Email'),
                                            max_length=100, null=True, blank=True)
    country             = models.CharField(max_length=2, blank=True, null=True) 
                                            # choices=COUNTRIES, 
    city                = models.CharField(_('city'),
                                            max_length=128,
                                            null=True, blank=True)
    address_1           = models.CharField(_('address_1'),
                                            max_length=128,
                                            null=True, blank=True)
    address_2           = models.CharField(_('address_2'),
                                            max_length=128,
                                            null=True, blank=True)
    zip                 = models.CharField(_('zip code'),
                                            max_length=25,
                                            null=True, blank=True)
    url                 = models.URLField(_('url'),
                                            verify_exists=False,
                                            max_length=256,
                                            null=True, blank=True)
    picture             = models.ImageField(_('picture'),
                                            upload_to="images/pictures/%Y/%m/%d/",
                                            max_length=128,
                                            null=True, blank=True)
    skype_id            = models.CharField(_('skype id'),
                                            max_length=35,
                                            null=True, blank=True)
    phone_land          = models.CharField(_('phone land'),
                                            max_length=25,
                                            null=True, blank=True)
    phone_mobile        = models.CharField(_('phone mobile'),
                                            max_length=25,
                                            null=True, blank=True)
    phone_fax           = models.CharField(_('phone fax'),
                                            max_length=25,
                                            null=True, blank=True)
    dt_created    = models.DateTimeField(_('datetime created'),
                                            db_index=True,
                                            default=datetime.utcnow, editable=False)
    is_active           = models.BooleanField(_('is active'),
                                            default=True, editable=True)
    def __unicode__(self):
        return u'%s (%s)' % (self.full_name, self.user.username)

class WorkspaceMembership(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    workspace    = models.ForeignKey(Workspace)

class SampleProject(models.Model):
    sampleproject_name = models.CharField(max_length=100)
    workspace = models.ForeignKey(Workspace)
    dt_created = models.DateTimeField(default=datetime.utcnow, editable=False)
    def __unicode__(self):
        return u'%s' % self.sampleproject_name

class SamplePresentation(models.Model):
    """
    A set of media items presenting the latest iteration of a product sample.
    The producer creates this to send to the designer and receive comments
    on the latest iteration.
    """
    workspace = models.ForeignKey(Workspace)
    sample_project = models.ForeignKey(SampleProject)
    samplepreso_name = models.CharField(max_length=100)
    creator_up = models.ForeignKey(UserProfile, related_name="creator")
    primary_recipient_up = models.ForeignKey(UserProfile, related_name="primary_recip")
    def __unicode__(self):
        return u'%s' % self.samplepreso_name

class MediaItem(models.Model):
    """
    The video (or other media item) that the producer adds to their sample presentation
    and the designer tags/comments on
    """
    workspace = models.ForeignKey(Workspace)
    sample_presentation = models.ForeignKey(SamplePresentation)
    url                 = models.URLField(_('url'),
                                            verify_exists=False,
                                            max_length=256,
                                            null=True, blank=True)

class VideoFrameContext(models.Model):
    """
    The video frame that the designer adds tags/comments to
    """
    workspace           = models.ForeignKey(Workspace)
    media_item          = models.ForeignKey(MediaItem)
    frame_time          = models.FloatField(default=datetime.utcnow, editable=False)
    
class VisualTag(models.Model):
    """
    The video frame that the designer adds tags/comments to
    """
    workspace           = models.ForeignKey(Workspace)
    video_frame_context = models.ForeignKey(VideoFrameContext)
    commenter_up        = models.ForeignKey(UserProfile)
    dt_created          = models.DateTimeField(default=datetime.utcnow)
    tag_index           = models.IntegerField()
    top                 = models.IntegerField()
    left                = models.IntegerField()
    height              = models.IntegerField()
    width               = models.IntegerField()
    comment_type        = models.IntegerField(default=0)
    comment_urgency     = models.IntegerField(default=0)
    


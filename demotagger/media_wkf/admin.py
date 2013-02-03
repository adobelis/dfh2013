from django.contrib import admin
from media_wkf import models as mw_models


class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('workspace_name', 'dt_created',)
admin.site.register(mw_models.Workspace, WorkspaceAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'dt_created')
admin.site.register(mw_models.UserProfile, UserProfileAdmin)

class WorkspaceMembershipAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'workspace')
admin.site.register(mw_models.WorkspaceMembership, WorkspaceMembershipAdmin)

class SampleProjectAdmin(admin.ModelAdmin):
    list_display = ('sampleproject_name', 'workspace', 'dt_created')
admin.site.register(mw_models.SampleProject, SampleProjectAdmin)

class SamplePresentationAdmin(admin.ModelAdmin):
    list_display = ('samplepreso_name', 'workspace', 'sample_project', 
                  'creator_up', 'primary_recipient_up')
admin.site.register(mw_models.SamplePresentation, SamplePresentationAdmin)

class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('workspace', 'sample_presentation', 'url')
admin.site.register(mw_models.MediaItem, MediaItemAdmin)

class VideoFrameContextAdmin(admin.ModelAdmin):
    list_display = ('workspace', 'media_item', 'frame_time')
admin.site.register(mw_models.VideoFrameContext, VideoFrameContextAdmin)
    
class VisualTagAdmin(admin.ModelAdmin):
    list_display = ('workspace', 'video_frame_context', 'commenter_up',
                    'dt_created', 'tag_index', 
                    'top', 'left', 'height', 'width',
                    'comment_type', 'comment_urgency')
admin.site.register(mw_models.VisualTag, VisualTagAdmin)    


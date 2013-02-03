from django.http import HttpResponse
from utilities.decorators import render_with
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json
import media_wkf.models as mw_models

from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login

@render_with('auth.html')
def login_user(request):
    posted = False
    logged_in = False
    username = password = ''
    user_exists=True
    if request.POST:
        posted = True
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        user_exists = True
        logged_in = False
        if user is not None:
            if user.is_active:
                login(request, user)
                logged_in=True
        else:
            user_exists = False

    return {'posted': posted,'logged_in':logged_in, 'username': username, 'user_exists': user_exists}



@render_with('index.html')
def index(request):
    return {
        "workspace_id": 0,
        "user_id": 0,
        "visual_tags": [
          {
            "x": 100,
            "y": 100,
            "time": 10.104,
            "comments":
                [{"content":"Make it redder",
                  "datetime": datetime.utcnow(),
                  "author":"Grant Kot",
                  "author_id":10,
                  },
                  {"content":"Why?",
                  "datetime": datetime.utcnow() + timedelta(hours = 5),
                  "author":"Arthur Dobelis",
                  "author_id":10,
                  }
    
                ]
          }
          ]
      }

@render_with('sample_preso2.html')
def sample_preso(request, workspace_index, preso_index):
    user_profile = request.user.get_profile()
    member = mw_models.WorkspaceMembership.objects.filter(user_profile=user_profile, workspace=workspace_index)
    if not len(member):
        return HttpResponse("Not your workspace")
    sample_preso = mw_models.SamplePresentation.objects.get(workspace=workspace_index,
                                                            pk=preso_index)
    media_items = mw_models.MediaItem.objects.filter(sample_presentation=preso_index)

    media_item = media_items[0]

    frame_times = mw_models.VideoFrameContext.objects.filter(media_item=media_item)
    frame_times = json.dumps([{"id": frame_time.id, "time": frame_time.frame_time} \
                    for frame_time in frame_times])

    return {
        "workspace_id": workspace_index,
        "user_id": user_profile,
        "sample_preso": sample_preso,
        "media_items": media_items,
        "frame_times": frame_times
    }

@render_with('media_item.html')
def media_item(request, workspace_index, mi_index):
    user_profile = request.user.get_profile()
    member = mw_models.WorkspaceMembership.objects.filter(user_profile=user_profile, workspace=workspace_index)
    if not len(member):
        return HttpResponse("Not your workspace")
    media_item = mw_models.MediaItem.objects.get(pk=mi_index)
    sample_preso = media_item.sample_presentation

    frames = mw_models.VideoFrameContext.objects.filter(media_item=media_item)
    frame_times = json.dumps([{"id": frame_time.id, "time": frame_time.frame_time} \
                    for frame_time in frames])

    comment_hash = {}
    #for frame in frames:
      #comment_hash[]

    return {
        "workspace_id": workspace_index,
        "user_id": user_profile,
        "sample_preso": sample_preso,
        "media_item": media_item,
        "frame_times": frame_times,
        "frames": frames
    }




@csrf_exempt
def add_comment(request):
    request_data        = json.loads(request.POST['data'])
    workspace_id        = request_data.get('workspace_id', None)
    media_item_id      = request_data.get('media_item_id', None)
    video_frame_ctxt_id = request_data.get('video_frame_ctxt_id', None)
    frame_time          = request_data.get('frame_time', None)
    commenter_id        = request_data.get('commenter_id', None)
    top                 = request_data.get('top', None)
    left                = request_data.get('left', None)
    height              = request_data.get('height', None)
    width               = request_data.get('width', None)
    comment_type        = request_data.get('comment_type', 0)
    comment_urgency     = request_data.get('comment_urgency', 0)
    comment_text        = request_data.get('comment_text', None)

    #tag_index           = models.IntegerField()
    if not video_frame_ctxt_id:
      workspace = mw_models.Workspace.objects.get(pk=workspace_id)
      media_item = mw_models.MediaItem.objects.get(pk=media_item_id)
      frame_context = mw_models.VideoFrameContext(workspace=workspace, media_item=media_item, frame_time=frame_time)
      frame_context.save()
      video_frame_ctxt_id = frame_context.id
    
    new_note = mw_models.VisualTag(workspace_id=workspace_id, video_frame_context_id=video_frame_ctxt_id, commenter_up_id=commenter_id, top=top, left=left, width=width, height=height, comment_type=comment_type, comment_urgency=comment_urgency, tag_index=0)
    new_note.save()

    #new_comment = mw_models.Commment(visual_tag=new_note, text=comment_text)

    return HttpResponse(
      json.dumps({"video_frame_ctxt_id": video_frame_ctxt_id, "tag_id": new_note.id}),
      mimetype='application/json'
    );
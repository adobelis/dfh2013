from django.http import HttpResponse
from utilities.decorators import render_with
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json
import media_wkf.models as mw_models

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
    comment_type        = request_data.get('comment_type', None)
    comment_urgency     = request_data.get('comment_urgency', None)

    #tag_index           = models.IntegerField()
    if not video_frame_ctxt_id:
      frame_context = mw_models.VideoFrameContext(workspace_id=workspace_id, media_item_id=media_item_id, frame_time=frame_time)
      frame_context.save()
      video_frame_ctxt_id = frame.id
    
    new_note = mw_models.VisualTag(workspace_id=workspace_id, video_frame_context_id=video_frame_ctxt_id, commenter_up_id=commenter_id, top=top, left=left, width=width, height=height, comment_type=comment_type, comment_urgency=comment_urgency)
    new_note.save()

    return HttpResponse(
      json.dumps({"frame_id": 0}),
      mimetype='application/json'
    );
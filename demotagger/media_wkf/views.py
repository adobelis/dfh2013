from django.http import HttpResponse
from utilities.decorators import render_with
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json

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
    #video_frame_ctxt_id = request_data.get('video_id', None)
    frame_time          = request_data.get('frame_time', None)
    commenter_id        = request_data.get('commenter_id', None)
    top                 = request_data.get('top', None)
    left                = request_data.get('left', None)
    height              = request_data.get('height', None)
    width               = request_data.get('width', None)
    #comment_type        = request_data.get('comment_type', None)
    #comment_urgency     = request_data.get('comment_urgency', None)

    #tag_index           = models.IntegerField()
    
    return HttpResponse(
      json.dumps({"frame_id": 0}),
      mimetype='application/json'
    );
from django.http import HttpResponse
from utilities.decorators import render_with
from datetime import datetime, timedelta

@render_with('index.html')
def index(request):
    return {
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

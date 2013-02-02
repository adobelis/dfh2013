from django.contrib.auth import authenticate, login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages
from django.utils.http import urlquote
from django.utils.functional import wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse, resolve


def render_with(template_name):
    """
    Renders the view wrapped by this decorator with the given template.  The
    view should return the context to be used in the template, or an
    HttpResponse.
    
    If the view returns an HttpResponseRedirect, the decorator will redirect
    to the given URL, or to request.REQUEST['next'] (if it exists).
    """
    def renderer(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            output = function(request, *args, **kwargs)

            if isinstance(output, HttpResponse):
                if isinstance(output, HttpResponseRedirect) and 'next' in request.REQUEST:
                    return HttpResponseRedirect(request.REQUEST['next'])
                else:
                    return output
            else:
                template = output.pop('TEMPLATE', template_name)
                return render_to_response(template, output, \
                    context_instance=RequestContext(request))
        return wrapper
    return renderer

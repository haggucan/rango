from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
import sys,json
from myrango.views import get_category_list, get_page_list
from dropbox import get_authorization_url


def about(request):
    context = RequestContext(request)

    context_variables = {}
    context_variables["ps_message"] = "Yeeey"
    context_variables["categories"] = get_category_list()
    context_variables["pages"] = get_page_list()
    if "last_visit" in request.session:
        visits = request.session.get("visits")
        context_variables["count"] = visits + 1
        context_variables["last_visit"] = request.session.get("last_visit")
    else:
        context_variables["count"] = 0
        context_variables["last_visit"] = datetime.now()

    return render_to_response("test.html", context_variables, context)


@csrf_protect
def upload(request):
    context = RequestContext(request)
    if request.method == 'POST':
        data = {}
        data['name'] = request.POST['name']
        data['value'] = request.POST['value']
        data['successful'] = True



    return HttpResponse(json.dumps(data), mimetype="application/json")

def drop_box_welcome(request):
    context = RequestContext(request)

    context_variables = {}

    if request.method == "GET":
        return render_to_response("dropbox.html",context_variables,context)

def auth(request):

    auth_url = get_authorization_url()
    return HttpResponse(auth_url,mimetype="application/json")


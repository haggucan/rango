from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from myrango.views import get_category_list, get_page_list


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

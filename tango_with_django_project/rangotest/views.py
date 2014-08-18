from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
import sys, json
from myrango.views import get_category_list, get_page_list
from dropbox_api import get_authorization_url, get_client, finish_auth, get_dropbox_session


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
        return render_to_response("dropbox.html", context_variables, context)


def auth(request):
    auth_url = get_authorization_url()
    return HttpResponse(auth_url, mimetype="application/json")


def finish(request):
    context = RequestContext(request)
    client_info = False
    if request.method == 'POST':
        if 'code' in request.POST:
            code = request.POST['code'].strip()
            access_token, user_id = finish_auth(code, context)
            if not access_token:
                access_token = "TIb6-fAkIJEAAAAAAAAA_7k1hMiM-OkyJeg3_BNkVuX9jUPq1_gu1STIKOg6ag1f"
                user_id = 252893107
            dropBox_client = get_client(access_token)
            root_folder_meta = dropBox_client.metadata("/")

            if root_folder_meta['contents']:
                content_depth = 0
                dropbox_context = root_folder_meta['contents']
                structured_folder = get_folder_struct(dropBox_client, dropbox_context, content_depth)
    return HttpResponse(prepare_list_for_template(structured_folder))


def get_folder_struct(dropBox_client, folder, depth):
    structured_folder = []
    for single_folder in folder:
        if single_folder["is_dir"]:
            subs_of_single_folder = dropBox_client.metadata(single_folder["path"])
            sub_doc = {}
            sub_doc["is_dir"] = True
            if subs_of_single_folder['contents']:
                sub_folders = get_folder_struct(dropBox_client, subs_of_single_folder['contents'], depth + 1)
                sub_doc["sub_folders"] = sub_folders
        else:
            sub_doc = {}
            sub_doc["sub_folders"] = None
            sub_doc["is_dir"] = False
        sub_doc["depth"] = depth
        sub_doc['path'] = single_folder["path"]
        sub_doc["size"] = single_folder["size"]
        if "last_modified" in single_folder:
            sub_doc["last_modified"] = single_folder["last_modified"]

        structured_folder.append(sub_doc)
    return structured_folder


def prepare_list_for_template(structured_folder):
    html = ""
    return get_doc_tree_as_html(html, structured_folder)


def get_doc_tree_as_html(html, structured_folder):
    html += "<ul>"
    for folder in structured_folder:
        if folder["sub_folders"]:
            html += "<li class=dir>"
            html += folder["path"]
            html += "</li>"

            for sub_folder in folder["sub_folders"]:

                if sub_folder["sub_folders"]:
                    html += "<li class=dir>"
                    html += sub_folder["path"]
                    html += "</li>"
                    html = get_doc_tree_as_html(html, sub_folder["sub_folders"])
                else:
                    html += "<ul><li class=file>"
                    html += sub_folder["path"]
                    html += "</li></ul>"
        else:
            html += "<li class=file>"
            html += folder["path"]
            html += "</li>"

    html += "</ul>"
    return html

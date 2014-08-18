from dropbox import client, rest, session
from django.http import HttpResponse
import json
from  dropbox.rest import ErrorResponse
from django.shortcuts import render_to_response


app_key = 'x2itss80z06yx7i'
app_secret = 'sqiby4k0590xiiq'
ACCESS_TYPE = "Full Dropbox"
AUTH_TOKEN = "TIb6-fAkIJEAAAAAAAAA_7k1hMiM-OkyJeg3_BNkVuX9jUPq1_gu1STIKOg6ag1f"
ACCESS_TYPE = 'app_folder'

flow = client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)


def get_authorization_url():
    authorize_url = flow.start()

    context_variables = {'authorize_url': authorize_url}
    response = json.dumps(context_variables)
    return HttpResponse(response, mimetype='application/json')


def finish_auth(code, context):
    try:
        access_token, user_id = flow.finish(code)
    except ErrorResponse as e:
        print e
        return None, None

    return access_token, user_id


def get_client(access_token):
    cl = client.DropboxClient(access_token)
    return cl


def get_dropbox_session():
    return session.DropboxSession(app_key, app_secret, ACCESS_TYPE)

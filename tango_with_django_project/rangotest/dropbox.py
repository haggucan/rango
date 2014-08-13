__author__ = 'hakanyildiz'
import dropbox

app_key = 'x2itss80z06yx7i'
app_secret = 'sqiby4k0590xiiq'
ACCESS_TYPE = "Full Dropbox"

def get_authorization_url():

    print ''
    ACCESS_TYPE = "Full Dropbox"
    sess = dropbox.session.DropboxSession(app_key,app_secret,ACCESS_TYPE)
    request_token = sess.obtain_request_token()
    url = sess.build_authorize_url(request_token)



    return url


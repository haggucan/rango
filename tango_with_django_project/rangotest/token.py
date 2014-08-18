import dropbox_api

access_token = 'KzDOzQ6Y8JkAAAAAAAAAAU_Ey3ENFaZ5dXWqXwSxegEvCnYAsQR1V9dn6AqXOn9z'
user_id = '13738484'

client = dropbox_api.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

app_key = '5xfbszi9zdc1eu9'
app_secret = 'q06tgbyfuhu98xu'

flow = dropbox_api.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()
access_token, user_id = flow.finish(code)

print 'PUT FOLLOWING CODE TO helpers.py'
print access_token


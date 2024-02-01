import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
creds = None

# The file token.json stores the user's access and refresh tokens and is created automatically when the authorization flow completes for the first time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Build your APK - replace this line with your actual build command
os.system('./gradlew assembleRelease')

# Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# Upload the APK to Google Drive
file_metadata = {
    'name': 'YourAppRelease.apk',  # Change this to your APK file name
    'parents': ['YourFolderID'],  # Change this to the folder ID where you want to save the APK
}

media = MediaFileUpload('app/build/outputs/apk/release/app-release.apk', mimetype='application/vnd.android.package-archive')

file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

print('File ID:', file.get('id'))

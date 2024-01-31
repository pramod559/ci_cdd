import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def upload_to_google_drive(credentials_path):
    # Authenticate with Google Drive API
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(credentials_path)
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile(credentials_path)

    drive = GoogleDrive(gauth)

    # Upload APK to Google Drive
    apk_path = 'build/app/outputs/flutter-apk/app-release.apk'  # Update path if necessary
    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    file = drive.CreateFile({'parents': [{'id': folder_id}]})
    file.SetContentFile(apk_path)
    file.Upload()

if __name__ == '__main__':
    credentials_path = sys.argv[1]
    upload_to_google_drive(credentials_path)
  

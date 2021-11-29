
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging
   
import os
   
class Upload_GDrive:
    def __init__(self):
        logging.debug('Upload_GDrive instance initialized')
        self.scope = ['https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', self.scope)
        self.service = build('drive', 'v3', credentials=self.credentials)
   
    def upload_file(self, file_path, file_name):
        logging.debug(f"Method called: upload_file, args: {{self, file_path, file_name}}")

        logging.info(f'Uploading {file_name} to Google Drive...')
        try:
            file_metadata = {
                'name': file_name, 
                "parents": ["11BnyVeHDuFHvlXGqY4r8bNdGlc7k7jmt"]} # folder id

            media = MediaFileUpload(file_path, mimetype='text/csv')

            file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            logging.info(f'File {file_name} successfully uploaded to Google Drive!')
            logging.debug(f"File ID: {file.get('id')}")

        except Exception as e:
            logging.exception(f'Unexpected error')

    def upload_folder(self, folder_path):
        for file in os.listdir(folder_path):
            self.upload_file(os.path.join(folder_path, file), file)
   

# # Below code does the authentication
# # part of the code
# gauth = GoogleAuth()
  
# # Creates local webserver and auto
# # handles authentication.
# gauth.LocalWebserverAuth()       
# drive = GoogleDrive(gauth)
   
# # replace the value of this variable
# # with the absolute path of the directory
# path = r"C:\Games\Battlefield"   
   
# # iterating thought all the files/folder
# # of the desired directory
# for x in os.listdir(path):
   
#     f = drive.CreateFile({'title': x})
#     f.SetContentFile(os.path.join(path, x))
#     f.Upload()
  
#     # Due to a known bug in pydrive if we 
#     # don't empty the variable used to
#     # upload the files to Google Drive the
#     # file stays open in memory and causes a
#     # memory leak, therefore preventing its 
#     # deletion
#     f = None
"""Google Drive API Helper Class"""

import httplib2
import googleapiclient.discovery
import googleapiclient.http
import googleapiclient.errors
import oauth2client.client


class DriveClient:
    """Google Drive API Wrapper"""

    def __init__(self):
        self.oauth2_scope = 'https://www.googleapis.com/auth/drive'
        self.client_secrets = '../misc/client_secrets.json'
        self.mimetype = 'text/plain'
        self.flow = self.set_flow()
        self.drive_service = self.get_drive_service()

    def set_flow(self):
        """Create a flow object for the Google API."""

        flow = oauth2client.client.flow_from_clientsecrets(self.client_secrets,
                                                           self.oauth2_scope)
        flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
        return flow

    def get_drive_service(self):
        """Create a drive_service to perform Drive operations on."""

        authorize_url = self.flow.step1_get_authorize_url()
        print('Go to the following link in your browser: ' + authorize_url)
        code = input('Enter verification code: ').strip()
        credentials = self.flow.step2_exchange(code)

        http = httplib2.Http()
        credentials.authorize(http)
        drive_service = googleapiclient.discovery.build('drive', 'v2',
                                                        http=http)
        return drive_service

    def push_file(self, file_src, title, description=''):
        """Creates a file to post on the main Drive documents page.

        :param file_src: The document file to use when creataing the Google Doc
        page.
        :param title: The title of the Google Doc.
        :param description: A description of the Google Doc.
        """

        media_body = googleapiclient.http.MediaFileUpload(
            file_src, mimetype=self.mimetype, resumable=True)
        body = {
            'title': title,
            'description': description
        }
        try:
            self.drive_service.files().insert(
                body=body, media_body=media_body, convert=True).execute()
        except googleapiclient.errors.HttpError as error:
            print('An error occured: %s' % error)

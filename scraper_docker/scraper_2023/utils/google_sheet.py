from __future__ import print_function
import os.path
import traceback

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from input.config import ZONES_FOLDER_ID, test_properties, COLUMNS_NEEDED, PATH_SHARED_DOCKER
import pandas as pd
from .logger import logger


PATH_CREDS_FOLDER = os.path.join(PATH_SHARED_DOCKER, 'creds')
PATH_CREDS_JSON = os.path.join(PATH_CREDS_FOLDER, 'credentials.json')
PATH_TOKEN_JSON = os.path.join(PATH_CREDS_FOLDER, 'token.json')


class GoogleSheet:
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self):
        self.sheet_obj = None
        self.drive_obj = None
        self.creds = None

    def auth(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(PATH_TOKEN_JSON):
            self.creds = Credentials.from_authorized_user_file(PATH_TOKEN_JSON, GoogleSheet.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            logger.info('not self.creds or not self.creds.valid')
            if self.creds and self.creds.expired and self.creds.refresh_token:
                logger.info('Refresh token')
                logger.info(f'self.creds {self.creds}')
                logger.info(f'self.creds.expired {self.creds.expired}')
                logger.info(f'self.creds.refresh_token {self.creds.refresh_token}')
                self.creds.refresh(Request())
            else:
                logger.info('InstalledAppFlow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    PATH_CREDS_JSON, GoogleSheet.SCOPES)
                self.creds = flow.run_local_server(port=0)
                logger.info('Credentials created')
            # Save the credentials for the next run
            with open(PATH_TOKEN_JSON, 'w') as token:
                logger.info('write token.json for next run')
                token.write(self.creds.to_json())
        else:
            logger.info('Authenticated Successfully!')

        self.drive_obj = build('drive', 'v3', credentials=self.creds)
        self.sheet_obj = build('sheets', 'v4', credentials=self.creds)

    def create_sheet(self, title, folder_id=None):
        """
        Creates the Sheet the user has access to.
        Load pre-authorized user credentials from the environment.
        for guides on implementing OAuth2 for the application.
            """
        # pylint: disable=maybe-no-member
        try:
            if not self.creds:
                self.auth()

            if folder_id:
                file_metadata = {
                    'name': title,
                    'parents': [folder_id],
                    'mimeType': 'application/vnd.google-apps.spreadsheet',
                }
                spreadsheet = self.drive_obj.files().create(body=file_metadata).execute()
                logger.info(f"Spreadsheet ID: {(spreadsheet.get('id'))}")
                logger.info(f"spreadsheet: {spreadsheet}")

                return spreadsheet.get('id')

            else:
                spreadsheet = {
                    'properties': {
                        'title': title
                    }
                }

                spreadsheet = self.sheet_obj.spreadsheets().create(body=spreadsheet,
                                                                   fields='spreadsheetId') \
                    .execute()

                logger.info(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
                logger.info(f"spreadsheet: {spreadsheet}")

                return spreadsheet.get('spreadsheetId')

        except HttpError as error:
            logger.info(f"An error occurred: {error}")
            return error

    def move_file_to_folder(self, file_id, folder_id):
        """Move specified file to the specified folder.
        Args:
            file_id: Id of the file to move.
            folder_id: Id of the folder
        Print: An object containing the new parent folder and other meta data
        Returns : Parent Ids for the file
        Load pre-authorized user credentials from the environment.
        for guides on implementing OAuth2 for the application.
        """

        try:
            if not self.creds:
                self.auth()

            # call drive api client

            # pylint: disable=maybe-no-member
            # Retrieve the existing parents to remove
            file = self.drive_obj.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            # Move the file to the new folder
            file = self.drive_obj.files().update(fileId=file_id, addParents=folder_id,
                                          removeParents=previous_parents,
                                          fields='id, parents').execute()
            return file.get('parents')

        except HttpError as error:
            logger.info(F'An error occurred: {error}')
            return None

    def create_folder(self, folder_name, parents=ZONES_FOLDER_ID):
        """ Create a folder and prints the folder ID
        Returns : Folder Id
        Load pre-authorized user credentials from the environment.
        for guides on implementing OAuth2 for the application.
        """

        try:
            if not self.creds:
                self.auth()

            # pylint: disable=maybe-no-member
            # Retrieve the existing parents to remove
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parents]

            }

            # pylint: disable=maybe-no-member
            file = self.drive_obj.files().create(body=file_metadata, fields='id'
                                          ).execute()
            logger.info(F'Folder ID: "{file.get("id")}".')
            logger.info(F'folder_name: "{folder_name}", Created Successfully')
            return file.get('id')

        except HttpError as error:
            logger.info(F'An error occurred: {error}')
            return None

    def update_values(self, spreadsheet_id, values, range_name='Sheet1'):
        """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.
        for guides on implementing OAuth2 for the application.
            """
        logger.info('update_values')
        logger.info(str(values))

        try:

            body = {
                'values': values
            }
            result = self.sheet_obj.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body
                ).execute()
            logger.info(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            logger.info(f"An error occurred: {error}")
            return error

    def convert_to_df(self, list_of_dicts):

        def extract_nbrhd(dictionary):
            value = dictionary['value']
            return value

        df_ = pd.DataFrame(list_of_dicts)
        logger.info(df_)
        try:
            # df_[['neighborhood']] = df_['neighborhood'].apply(lambda x: pd.Series(extract_nbrhd(x)))
            df_ = df_.loc[:, COLUMNS_NEEDED]

        except:
            traceback.print_exc()

        # print(df)
        logger.info(df_.columns.values.tolist())
        logger.info(df_.values.tolist())
        return [df_.columns.values.tolist()] + df_.values.tolist()

    def get_or_create(self, folder_name, parent_id):
        is_exists, folder_id_ = self.is_folder_exist(folder_name, parent_id)
        if is_exists:
            logger.info(f'Folder: {folder_name} already exists with id: {folder_id_}')
        else:
            folder_id_ = self.create_folder(folder_name, parent_id)
            logger.info(f'Folder: {folder_name} is Created Successfully with id: {folder_id_}')
        return folder_id_

    def is_folder_exist(self, folder_name, parent_id):
            """Search file in drive location

            Load pre-authorized user credentials from the environment.
            for guides on implementing OAuth2 for the application.
            """
            is_exists = False
            folder_id = None
            try:

                if not self.creds:
                    self.auth()

                # create drive api client
                page_token = None
                while True:
                    # pylint: disable=maybe-no-member
                    response = self.drive_obj.files().list(
                                                    q=f"name='{folder_name}' and trashed=false and "
                                                      f" mimeType='application/vnd.google-apps.folder'",
                                                    spaces='drive',
                                                    fields='nextPageToken, '
                                                           'files(id, name, mimeType, size, parents, modifiedTime)',
                                                    pageToken=page_token).execute()

                    for file in response.get('files', []):
                        print(file)
                        parent = file.get("parents")[0]
                        folder_id = file.get("id")
                        if parent == parent_id:
                            print(f'This Folder: {folder_name}, is already exists in Parent_id: {parent_id}')
                            is_exists = True
                            break
                    if is_exists:
                        break
                    page_token = response.get('nextPageToken', None)
                    if page_token is None:
                        break

            except HttpError as error:
                print(F'An error occurred: {error}')

            return is_exists, folder_id

    # def get_parent_id(self, id):
    #     items = self.drive_obj.files().list(pageSize=5, fields="nextPageToken, files(id, name, mimeType, size, parents, modifiedTime)").execute()
    #
    #     # results = self.drive_obj.files().list(q="'" + id + "' in parents", pageSize=10,
    #     #                              ).execute()
    #     # items = results.get('files', [])
    #     print(items)


if __name__ == '__main__':

    sh = GoogleSheet()
    sh.auth()

    # df = sh.convert_to_df(test_properties)
    #
    # sh_id = sh.create_sheet('Test Zak', ZONES_FOLDER_ID)
    # sh.update_values(sh_id, df)
    # folder_id = sh.get_or_create('Bosecke_11', ZONES_FOLDER_ID)
    # print(folder_id)
    # sh.get_parent_id(id_1)
    # auth()
    # main()
    # sprd_id = create("mysheet2")
    # move_file_to_folder(file_id=sprd_id,
    #                     folder_id='1Yw_w_-xbmUanwRs7yQkIbP3fTmEk3U5c')

    # gc = gspread.service_account(filename='adam-scraping-606173fe1ee9.json')
    #
    # sh = gc.create('A new spreadsheet')
    # sh.share('zak.omer.90@gmail.com', perm_type='user', role='writer')

# if __name__ == '__main__':
#     main()

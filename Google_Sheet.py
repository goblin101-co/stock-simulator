import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES=["https://googleapis.com/auth/spreadsheets"]

SPREATSHEET_ID="1EPYXbsuPgbFXJoghnMkAWnreqN253hXlf7uSXcebO-M"


def main():
    credentials=None
    if os.path.exists("token.json"):
        crendetials=Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.exprired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        with open("token.json", "w") as token:
            token.write(credentials.to.json())
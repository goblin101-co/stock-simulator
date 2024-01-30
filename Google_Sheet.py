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
        crendetials=Credentials.from_authorized_user_file("token.json", SCOPE)
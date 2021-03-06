from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    with open('december_results.csv', 'r') as f:
        next(f)
        for line in f:
            data = line.strip('\n').split('\t')
            event_name = data[0]
            venue_name = data[1]
            start_date = data[16]
            end_date = data[17]
            site_link = data[10]
            address = data[11]
            description = data[14]

            # print('start date: ' + start_date)
            # print('end date: ' + end_date)
            # print(description)
            # exit()

            event = {
              'summary': event_name,
              'location': venue_name + ', ' + address,
              'description': description + '\n\n' + site_link,
              'start': {
                # 'dateTime': '2015-05-28T09:00:00-07:00',
                'dateTime': start_date,
                'timeZone': 'America/New_York',
              },
              'end': {
                'dateTime': end_date,
                'timeZone': 'America/New_York',
              },
              'recurrence': [
                # 'RRULE:FREQ=DAILY;COUNT=2'
              ],
              'attendees': [
                # {'email': 'lpage@example.com'},
                # {'email': 'sbrin@example.com'},
              ],
              'reminders': {
                'useDefault': True,
                # 'overrides': [
                #   {'method': 'email', 'minutes': 24 * 60},
                #   {'method': 'popup', 'minutes': 10},
                # ],
              },
            }

            event = service.events().insert(calendarId='brain-arts.org_cs2ruvhpnv1d0cp12isfushun8@group.calendar.google.com', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')) + '\n')


if __name__ == '__main__':
    main()
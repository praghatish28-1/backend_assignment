import unittest
from unittest.mock import patch, MagicMock
from src.services.gmail_service import GmailService

class TestGmailService(unittest.TestCase):
    @patch('src.services.gmail_service.build')
    @patch('src.services.gmail_service.pickle.load')
    @patch('src.services.gmail_service.os.path.exists')
    def test_authenticate_gmail(self, mock_exists, mock_pickle_load, mock_build):
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_pickle_load.return_value = mock_creds
        gmail_service = GmailService('credentials.json', 'token.pickle', ['scope'])
        self.assertEqual(gmail_service.service, mock_build.return_value)
        mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_creds)

    @patch('src.services.gmail_service.GmailService.authenticate_gmail')
    def test_fetch_emails(self, mock_authenticate_gmail):
        mock_service = MagicMock()
        mock_authenticate_gmail.return_value = mock_service
        mock_service.users().messages().list().execute.return_value = {
            'messages': [{'id': '1'}]
        }
        mock_service.users().messages().get().execute.return_value = {
            'id': '1',
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'sender@example.com'},
                    {'name': 'Subject', 'value': 'Subject'}
                ],
                'parts': [{'mimeType': 'text/plain', 'body': {'data': 'Body'}}]
            },
            'internalDate': '1234567890'
        }
        gmail_service = GmailService('credentials.json', 'token.pickle', ['scope'])
        emails = gmail_service.fetch_emails()
        self.assertEqual(emails, [
            ('1', 'sender@example.com', 'Subject', 'Body', '1234567890')
        ])

    @patch('src.services.gmail_service.GmailService.authenticate_gmail')
    def test_modify_email_labels(self, mock_authenticate_gmail):
        mock_service = MagicMock()
        mock_authenticate_gmail.return_value = mock_service
        gmail_service = GmailService('credentials.json', 'token.pickle', ['scope'])
        gmail_service.modify_email_labels('1', ['INBOX'], ['UNREAD'])
        mock_service.users().messages().modify.assert_called_once_with(
            userId='me', id='1', body={'addLabelIds': ['INBOX'], 'removeLabelIds': ['UNREAD']}
        )

    @patch('src.services.gmail_service.GmailService.authenticate_gmail')
    def test_get_label_id(self, mock_authenticate_gmail):
        mock_service = MagicMock()
        mock_authenticate_gmail.return_value = mock_service
        mock_service.users().labels().list().execute.return_value = {
            'labels': [{'id': '1', 'name': 'INBOX'}]
        }
        gmail_service = GmailService('credentials.json', 'token.pickle', ['scope'])
        label_id = gmail_service.get_label_id('INBOX')
        self.assertEqual(label_id, '1')

if __name__ == '__main__':
    unittest.main()
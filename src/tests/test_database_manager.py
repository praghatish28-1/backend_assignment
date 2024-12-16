import unittest
from unittest.mock import patch, MagicMock
from src.services.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    @patch('src.services.database_manager.sqlite3.connect')
    def test_create_tables(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_manager = DatabaseManager('test.db')
        db_manager.create_tables()
        mock_conn.cursor().execute.assert_called_once_with('''
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                sender TEXT,
                subject TEXT,
                body TEXT,
                received_at TEXT
            )
        ''')
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.services.database_manager.sqlite3.connect')
    def test_store_email(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_manager = DatabaseManager('test.db')
        db_manager.store_email('1', 'sender@example.com', 'Subject', 'Body', '1234567890')
        mock_conn.cursor().execute.assert_called_once_with('''
            INSERT OR IGNORE INTO emails (id, sender, subject, body, received_at) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('1', 'sender@example.com', 'Subject', 'Body', '1234567890'))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.services.database_manager.sqlite3.connect')
    def test_get_emails(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('1', 'sender@example.com', 'Subject', 'Body', '1234567890')
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        db_manager = DatabaseManager('test.db')
        emails = db_manager.get_emails()
        self.assertEqual(emails, [{
            'id': '1',
            'From': 'sender@example.com',
            'Subject': 'Subject',
            'Body': 'Body',
            'Date received': 1234567890
        }])
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import MagicMock, patch

from cli import create_connection, get_schema


class TestGetSchema(unittest.TestCase):
    @patch('mysql.connector.connect')
    def test_create_connection(self, mock_connect):
        # Define the mock behavior for mysql.connector.connect
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        # Input text
        text = "connect --user test_user --password test_password --host test_host --port 3306"

        # Call the function
        connection = create_connection(text)

        # Check if mysql.connector.connect was called with the correct parameters
        mock_connect.assert_called_once_with(
            user='test_user', 
            passwd='test_password', 
            host='test_host', 
            port=3306
        )

        # Check if the returned connection is the mock connection
        self.assertEqual(connection, mock_connection)

    def test_get_schema(self):
         # Create a mock connection and cursor
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Define the behavior of the mock cursor
        mock_cursor.fetchall.return_value = [('table1',), ('table2',)]
        mock_cursor.fetchone.side_effect = [
            ('table1', 'CREATE TABLE table1 (id INT)'),
            ('table2', 'CREATE TABLE table2 (name VARCHAR(255))')
        ]

        # Expected schema
        expected_schema = "CREATE TABLE table1 (id INT);\nCREATE TABLE table2 (name VARCHAR(255));\n"

        # Call the function with the mock connection
        schema = get_schema(mock_connection, 'test_db')

        # Check if the result is as expected
        self.assertEqual(schema, expected_schema)
        

if __name__ == '__main__':
    unittest.main()

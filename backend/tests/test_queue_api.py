"""
Tests for the queue API endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from psycopg2.extras import RealDictRow


class TestQueueAPI:
    """Test suite for /api/queue endpoint."""

    @patch('backend.api.queue.db_connection')
    def test_get_queue_success(self, mock_db, client, mock_db_connection):
        """Test successful retrieval of queue items."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        # Mock queue data
        mock_row = MagicMock(spec=RealDictRow)
        mock_row.__getitem__ = lambda self, key: {
            'github_id': 12345,
            'priority': 5,
            'created_at': '2024-01-01T00:00:00'
        }.get(key)
        mock_row.keys.return_value = ['github_id', 'priority', 'created_at']
        mock_cursor.fetchall.return_value = [mock_row]

        response = client.get('/api/queue')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        mock_cursor.execute.assert_called_once()
        # Verify ORDER BY created_at was used
        assert 'ORDER BY' in str(mock_cursor.execute.call_args).upper()

    @patch('backend.api.queue.db_connection')
    def test_get_queue_empty(self, mock_db, client, mock_db_connection):
        """Test queue endpoint with empty queue."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = []

        response = client.get('/api/queue')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

    @patch('backend.api.queue.db_connection')
    def test_get_queue_database_error(self, mock_db, client):
        """Test error handling when database connection fails."""
        mock_db.side_effect = Exception("Database connection failed")

        response = client.get('/api/queue')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

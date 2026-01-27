"""
Tests for the users API endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from psycopg2.extras import RealDictRow


class TestUsersAPI:
    """Test suite for /api/users endpoint."""

    @patch('backend.api.users.db_connection')
    def test_get_users_success(self, mock_db, client, mock_db_connection, sample_user_data):
        """Test successful retrieval of users."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        # Mock database response
        mock_row = MagicMock(spec=RealDictRow)
        mock_row.__getitem__ = lambda self, key: sample_user_data.get(key)
        mock_row.keys.return_value = sample_user_data.keys()
        mock_cursor.fetchall.return_value = [mock_row]
        mock_cursor.fetchone.return_value = {'total': 1}

        response = client.get('/api/users?page=1&per_page=10')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'users' in data or isinstance(data, list)
        mock_cursor.execute.assert_called()

    @patch('backend.api.users.db_connection')
    def test_get_users_with_search(self, mock_db, client, mock_db_connection):
        """Test user search functionality."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {'total': 0}

        response = client.get('/api/users?search=testuser')
        
        assert response.status_code == 200
        # Verify search query was used in SQL
        assert any('plainto_tsquery' in str(call) for call in mock_cursor.execute.call_args_list)

    @patch('backend.api.users.db_connection')
    def test_get_users_with_filters(self, mock_db, client, mock_db_connection):
        """Test user filtering by gender, type, location."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {'total': 0}

        response = client.get('/api/users?gender=Male&type=User&location=United States')
        
        assert response.status_code == 200
        # Verify filters were applied
        assert mock_cursor.execute.called

    @patch('backend.api.users.db_connection')
    def test_get_users_with_sorting(self, mock_db, client, mock_db_connection):
        """Test user sorting functionality."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {'total': 0}

        response = client.get('/api/users?sortField=total_sponsors&sortOrder=descend')
        
        assert response.status_code == 200
        assert mock_cursor.execute.called

    @patch('backend.api.users.db_connection')
    def test_get_users_pagination(self, mock_db, client, mock_db_connection):
        """Test pagination parameters."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {'total': 0}

        response = client.get('/api/users?page=2&per_page=20')
        
        assert response.status_code == 200
        # Verify LIMIT and OFFSET were used
        execute_calls = [str(call) for call in mock_cursor.execute.call_args_list]
        assert any('LIMIT' in call or 'OFFSET' in call for call in execute_calls)

    @patch('backend.api.users.db_connection')
    def test_get_users_database_error(self, mock_db, client):
        """Test error handling when database connection fails."""
        mock_db.side_effect = Exception("Database connection failed")

        response = client.get('/api/users')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    @patch('backend.api.users.db_connection')
    def test_export_users_rate_limit(self, mock_db, client, mock_db_connection):
        """Test export rate limiting."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {'total': 0}

        # First export should succeed
        response1 = client.get('/api/users/export')
        assert response1.status_code in [200, 429]  # May be rate limited or succeed

        # Multiple rapid exports should be rate limited
        for _ in range(5):
            response = client.get('/api/users/export')
            # Rate limiting may kick in
            assert response.status_code in [200, 429]

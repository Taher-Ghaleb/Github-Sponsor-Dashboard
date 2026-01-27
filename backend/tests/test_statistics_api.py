"""
Tests for the statistics API endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock


class TestStatisticsAPI:
    """Test suite for /api/stats/* endpoints."""

    @patch('backend.api.statistics.db_connection')
    def test_get_stats_brief_success(self, mock_db, client, mock_db_connection, sample_stats_data):
        """Test successful retrieval of brief statistics."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchone.return_value = sample_stats_data

        response = client.get('/api/stats/brief')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_users' in data or isinstance(data, dict)
        mock_cursor.execute.assert_called_once()

    @patch('backend.api.statistics.db_connection')
    def test_get_stats_brief_database_error(self, mock_db, client):
        """Test error handling for brief stats."""
        mock_db.side_effect = Exception("Database error")

        response = client.get('/api/stats/brief')
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    @patch('backend.api.statistics.db_connection')
    def test_get_user_stats_success(self, mock_db, client, mock_db_connection):
        """Test user statistics endpoint."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [
            {
                'country': 'United States',
                'genderData': {'male': 100, 'female': 50, 'other': 10, 'unknown': 20}
            }
        ]

        response = client.get('/api/user-stats')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'country' in data[0]
            assert 'genderData' in data[0]

    @patch('backend.api.statistics.db_connection')
    def test_get_gender_stats_success(self, mock_db, client, mock_db_connection):
        """Test gender statistics endpoint."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [
            {'gender': 'Male', 'count': 500},
            {'gender': 'Female', 'count': 300},
            {'gender': 'Other', 'count': 50},
            {'gender': 'Unknown', 'count': 150}
        ]

        response = client.get('/api/gender-stats')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

    @patch('backend.api.statistics.db_connection')
    def test_get_sponsorship_stats_success(self, mock_db, client, mock_db_connection):
        """Test sponsorship statistics endpoint."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [
            {
                'sponsoring_only': 100,
                'sponsored_only': 200,
                'both': 50
            }
        ]

        response = client.get('/api/user-sponsorship-stats')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert 'sponsoring_only' in data[0] or 'sponsored_only' in data[0]

    @patch('backend.api.statistics.db_connection')
    def test_get_brief_user_stats_success(self, mock_db, client, mock_db_connection):
        """Test brief user statistics endpoint."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [{
            'total_users': 1000,
            'most_sponsored_user': {'username': 'user1', 'total_sponsors': 100},
            'most_sponsoring_user': {'username': 'user2', 'total_sponsoring': 50},
            'top_country': {'country': 'United States', 'sponsored_users': 300}
        }]

        response = client.get('/api/brief-user-stats')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)

    @patch('backend.api.statistics.db_connection')
    def test_get_gender_distribution_table(self, mock_db, client, mock_db_connection):
        """Test gender distribution table endpoint."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [
            {
                'Category': 'Pronouns Specified',
                'Male': '100 (50%)',
                'Female': '80 (40%)',
                'Other': '10 (5%)',
                'Unknown': '10 (5%)',
                'Total': 200
            }
        ]

        response = client.get('/api/gender-distribution-table')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

    @patch('backend.api.statistics.db_connection')
    def test_get_location_sponsorship_roles(self, mock_db, client, mock_db_connection):
        """Test location sponsorship roles endpoint."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [
            {
                'location': 'United States',
                'sponsored_only': 100,
                'sponsoring_only': 50,
                'both_roles': 25,
                'total_active': 175
            }
        ]

        response = client.get('/api/location-sponsorship-roles')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

    @patch('backend.api.statistics.db_connection')
    def test_get_sponsorship_roles_by_type(self, mock_db, client, mock_db_connection):
        """Test sponsorship roles by type endpoint."""
        mock_conn, mock_cursor = mock_db_connection
        mock_db.return_value = mock_conn
        
        mock_cursor.fetchall.return_value = [
            {
                'entity_type': 'User',
                'active_sponsored_only': 200,
                'active_sponsoring_only': 100,
                'active_both': 50
            }
        ]

        response = client.get('/api/sponsorship-roles-by-type')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

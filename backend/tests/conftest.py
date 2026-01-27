"""
Pytest configuration and shared fixtures for backend tests.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from flask import Flask
from backend.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db_connection():
    """Mock database connection and cursor."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'id': 1,
        'username': 'testuser',
        'name': 'Test User',
        'type': 'User',
        'gender': 'Male',
        'location': 'United States',
        'followers': 100,
        'following': 50,
        'public_repos': 25,
        'total_sponsors': 10,
        'total_sponsoring': 5,
        'estimated_earnings': 500
    }


@pytest.fixture
def sample_stats_data():
    """Sample statistics data for testing."""
    return {
        'total_users': 1000,
        'total_sponsorships': 5000,
        'top_sponsoring': {
            'username': 'topsponsor',
            'avatar_url': 'https://example.com/avatar.png',
            'total_sponsoring': 100
        },
        'top_sponsored': {
            'username': 'topsponsored',
            'avatar_url': 'https://example.com/avatar2.png',
            'total_sponsors': 200
        }
    }

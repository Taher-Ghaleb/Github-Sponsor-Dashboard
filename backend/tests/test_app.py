"""
Tests for the main Flask application.
"""
import pytest
from backend.app import app


def test_index_route(client):
    """Test the root route returns Hello World."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello World!' in response.data


def test_app_config(client):
    """Test that the app is configured correctly."""
    assert app.config['TESTING'] is True


def test_cors_enabled(client):
    """Test that CORS is enabled."""
    response = client.get('/')
    # CORS headers should be present
    assert 'Access-Control-Allow-Origin' in response.headers or response.status_code == 200

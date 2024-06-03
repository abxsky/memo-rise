from rest_framework.test import APIClient
from rest_framework import status
import pytest
from django.contrib.auth.models import User

#Unit Testing
@pytest.mark.django_db
class TestCreateCategory:
    def test_if_user_is_anonymus_returns_401(self):
        
        client = APIClient()
        response = client.post('/store/categories/', {'title': 'a'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_if_data_is_invalid_returns_40(self):
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        response = client.post('/store/categories/', {'title': ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
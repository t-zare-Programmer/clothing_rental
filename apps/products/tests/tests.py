import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.categories.models import Category

@pytest.mark.django_db
def test_create_product_api():
    client = APIClient()

    User = get_user_model()

    user = User.objects.create_user(
        phone_number="09123456789",
        password="testpass123"
    )

    category = Category.objects.create(title="Test Category")

    client.force_authenticate(user=user)

    response = client.post("/api/products/", {
        "title": "Test Product",
        "description": "Test Desc",
        "category": category.id,
        "product_type": "rent",
        "rent_price": 1000,
        "deposit_price": 500
    }, format="json")

    print(response.data)
    assert response.status_code == 201

#==================================================================================
@pytest.mark.django_db
def test_unauthorized_user_cannot_create_product():
    client = APIClient()

    category = Category.objects.create(title="Test Category")

    response = client.post("/api/products/", {
        "title": "Test Product",
        "description": "Test Desc",
        "category": category.id,
        "product_type": "rent",
        "rent_price": 1000,
        "deposit_price": 500
    }, format="json")

    assert response.status_code == 401
import pytest
from httpx import AsyncClient, ASGITransport
from main import app  # Импортируйте ваш объект FastAPI

@pytest.mark.anyio
async def test_read_root():
    # Используем ASGITransport для тестирования без запуска реального сервера
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI Secure API"}

@pytest.mark.anyio
async def test_admin_access_without_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/admin-data")
    # Должно вернуть 401, так как токен не передан
    assert response.status_code == 401
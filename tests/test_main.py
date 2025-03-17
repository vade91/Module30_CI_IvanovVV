import pytest
import json
from sqlalchemy.future import select

from fastapi.testclient import TestClient
from ..src_app.main import app
from ..src_app.models import Recipe
from ..src_app.database import session

from httpx import ASGITransport, AsyncClient

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_all_recipes(create_table):
    """
    Тест эндпоинта /recipes:
    1. Получение статус-кода 200
    2. Структура преобразуема в список
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/recipes")

    assert response.status_code == 200
    assert isinstance(json.loads(response.text), list) == True


@pytest.mark.asyncio
async def test_root_404():
    """
    Тест корня сервиса. Должен вернуться 404
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get('/')

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_recipe(one_recipe):
    """
    Тест эндпоинта /recipes (post):
    1. Возвращается 200
    2. Добавленное имя блюда такое же как в аналогичном ключе фикстуры
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/recipes", json=one_recipe)
        assert response.status_code == 200
        assert response.json()['dish_name'] == one_recipe['dish_name']


@pytest.mark.asyncio
async def test_get_details():
    """
    Тест эндпоинта /recipes/id (post):
    1. Возвращается 200
    2. Проверяем, что счетчик просмотров увеличился на 1 после просмотра блюда
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        get_cnt = await session.execute(
            select(Recipe.views_cnt).where(Recipe.id == 1)
        )
        cnt_before = get_cnt.scalar()
        response = await ac.get("/recipes/1")
        assert response.status_code == 200
        assert response.json()["views_cnt"] == cnt_before + 1
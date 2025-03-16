import pytest

from database import engine
import models as models


@pytest.fixture
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@pytest.fixture
def one_recipe():
    data = {"dish_name": "Mashed potato",
            "cooking_time_m": 15,
            "reagents": "potato, milk, butter",
                "description": "mash potato, mix all"}
    return data
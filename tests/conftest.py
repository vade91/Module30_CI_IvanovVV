import pytest

from ..src_app.database import engine
from ..src_app.models import Base


@pytest.fixture()
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture()
def one_recipe():
    data = {
        "dish_name": "Mashed potato",
        "cooking_time_m": 15,
        "reagents": "potato, milk, butter",
        "description": "mash potato, mix all",
    }
    return data

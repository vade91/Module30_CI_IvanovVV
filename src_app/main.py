from typing import List

from sqlalchemy.future import select

from fastapi import FastAPI, Path
from fastapi.exceptions import HTTPException

from .database import engine, session
from .models import Recipe, Base
from .schemas import RecipeIn, RecipeOut


app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/recipes', response_model=RecipeOut, tags=['Recipes'])
async def add_recipe(receipt: RecipeIn) -> Recipe:
    """
    Асинхронный роут добавляет новый рецепт в базу данных
    """
    new_receipt = Recipe(**receipt.dict())
    async with session.begin():
        session.add(new_receipt)
    return new_receipt

@app.get('/recipes', response_model=List[RecipeOut], tags=['Recipes'])
async def get_all_recipes() -> List[Recipe]:
    """
    Асинхронный роут получает список имеющихся рецептов в базе
    """
    async with session.begin():
        res = await session.execute(select(Recipe
                                           ).order_by(Recipe.views_cnt.desc()
                                                      ).order_by(Recipe.cooking_time_m))

    return res.scalars().all()

@app.get('/recipes/{recipe_id}', response_model=RecipeOut, tags=['Recipes'])
async def get_recipe_details(
        recipe_id: int =Path(...,
                             title='Id of the recipe to display',
                             ge=0)
                              ):
    """
    Асинхронный роут получает конкретный рецепт по его id.
    у такого рецепта прибавляется число просмотров (views_cnt)
    """
    result = await session.execute(select(
        Recipe).where(Recipe.id == recipe_id))
    dish = result.scalar()
    if dish:
        dish.views_cnt += 1
        await session.commit()
        return RecipeOut(**dish.__dict__)
    else:
        raise HTTPException(status_code=404, detail="Recipe not found")

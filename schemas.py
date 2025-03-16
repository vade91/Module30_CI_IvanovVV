from pydantic import BaseModel

class BaseRecipe(BaseModel):
    """
    Базовый класс рецепта. Содержит поля:
    1. Название блюда
    2. Время приготовления в минутах
    3. Ингридиенты
    4. Описание готовки
    """
    dish_name: str
    cooking_time_m: int
    reagents: str
    description: str

class RecipeIn(BaseRecipe):
    ...

class RecipeOut(BaseRecipe):
    """
    При создании базовый класс дополняется полями:
    1. id - первичный ключ таблицы
    2. Кол-во просмотров, начинается с нуля
    """
    id: int
    views_cnt: int

    class Config:
        orm_mode = True

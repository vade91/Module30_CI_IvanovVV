from sqlalchemy import Column, String, Integer

from database import Base

class Recipe(Base):
    __tablename__ = 'Recipes'
    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, index=True)
    cooking_time_m = Column(Integer, index=True)
    reagents = Column(String)
    description = Column(String)
    views_cnt = Column(Integer, index=True, default=0)

from fastapi import APIRouter

from .entities.meals_of_plan_entity import MealsOfPlan
from .controllers.meals_of_plan_controller import meals_of_plan_router

from .entities.nutritional_plan_has_meal_entity import NutritionalPlanHasMeal
from .controllers.nutritional_plan_has_meal_controller import nutritional_plan_has_meal_router

from .entities.meals_options_entity import MealsOptions
from .controllers.meals_options_controller import meals_options_router


plan_meals_routers = APIRouter()
plan_meals_routers.include_router(meals_of_plan_router)
plan_meals_routers.include_router(nutritional_plan_has_meal_router)
plan_meals_routers.include_router(meals_options_router)

plan_meals_entities = [MealsOfPlan, NutritionalPlanHasMeal, MealsOptions]

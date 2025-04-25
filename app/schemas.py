from pydantic import BaseModel
from typing import Dict

class FoodLensIn(BaseModel):
    user_id: int
    nutrients: Dict[str, float]
import requests
from typing import Any, Optional, Type
from gentopia.tools.basetool import BaseTool, BaseModel, Field

class DishOriginParameters(BaseModel):
    dish_name: str = Field(..., description="Name of the dish to find its origin")

class DishOriginTool(BaseTool):
    """Tool for identifying the origin of a dish using Spoonacular API."""
    name = "dish_origin_tool"
    description = "A tool that identifies the origin of a dish based on its name using Spoonacular API."

    args_schema: Optional[Type[BaseModel]] = DishOriginParameters

    # Spoonacular API URL and key (you need to add your API key here)
    SPOONACULAR_API_URL = "https://api.spoonacular.com/recipes/complexSearch"
    SPOONACULAR_API_KEY = "7ae86da940954fe4a740602f011ba899"  # Replace with your actual API key

    def _run(self, dish_name: str) -> str:
        # Call Spoonacular API to search for the dish
        params = {
            "query": dish_name,
            "number": 1,  # Limit to 1 result
            "apiKey": self.SPOONACULAR_API_KEY
        }

        try:
            response = requests.get(self.SPOONACULAR_API_URL, params=params)
            response.raise_for_status()  # Raise error if the request fails
            data = response.json()

            if data.get("results"):
                dish_info = data["results"][0]
                cuisine = dish_info.get("cuisines", ["Unknown"])[0]  # Get the first cuisine type
                return f"The origin (or cuisine) of {dish_name} is: {cuisine}"
            else:
                return f"Sorry, I could not find the origin of {dish_name}."
        
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching the origin: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous execution not implemented.")
    
if __name__ == "__main__":
    # Example use of the tool
    origin_params = DishOriginParameters(
        dish_name="pasta"
    )

    origin_tool = DishOriginTool()
    origin_text = origin_tool._run(**origin_params.dict())
    print(f"Dish Origin: {origin_text}")

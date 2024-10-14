from typing import Any, Optional, Type, List
from gentopia.tools.basetool import BaseTool, BaseModel, Field

class RecipeParameters(BaseModel):
    ingredients: List[str] = Field(..., description="List of ingredients to use for the recipe")

class RecipeTool(BaseTool):
    """Tool for generating recipes from provided ingredients."""
    name = "recipe_tool"
    description = "A tool that generates a recipe based on the provided ingredients."

    args_schema: Optional[Type[BaseModel]] = RecipeParameters

    def _run(self, ingredients: List[str]) -> str:
        # Simple example logic: Combine ingredients into a mock recipe
        # In practice, you could connect to an API or a trained model
        recipe = f"Here is a simple recipe using: {', '.join(ingredients)}."
        recipe += "\n1. Mix all the ingredients.\n2. Cook over medium heat for 30 minutes."
        recipe += "\n3. Serve hot. Enjoy your meal!"
        return recipe

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous execution not implemented.")
    
if __name__ == "__main__":
    # Example use of the tool
    recipe_params = RecipeParameters(
        ingredients=["tomato", "onion", "garlic"]
    )

    recipe_tool = RecipeTool()
    recipe_text = recipe_tool._run(**recipe_params.dict())
    print(f"Generated Recipe: {recipe_text}")

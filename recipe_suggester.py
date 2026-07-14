"""Suggest recipes based on food image"""


class RecipeSuggester:
    def __init__(self):
        self.recipes_db = {
            "pizza": [
                "Classic Margherita Pizza - Fresh mozzarella, basil, tomato sauce",
                "Pepperoni Pizza - Crispy pepperoni with melted cheese",
                "Vegetarian Pizza - Mixed vegetables and herbs",
            ],
            "pasta": [
                "Spaghetti Carbonara - Eggs, bacon, and parmesan",
                "Fettuccine Alfredo - Creamy parmesan sauce",
                "Penne Arrabbiata - Spicy tomato and garlic",
            ],
            "salad": [
                "Caesar Salad - Romaine, croutons, parmesan",
                "Greek Salad - Tomatoes, cucumbers, feta cheese",
                "Garden Salad - Mixed greens and vegetables",
            ],
            "soup": [
                "Tomato Soup - Creamy tomato with basil",
                "Chicken Noodle Soup - Classic comfort food",
                "Vegetable Soup - Mixed seasonal vegetables",
            ],
            "curry": [
                "Butter Chicken Curry - Creamy tomato-based",
                "Vegetable Curry - Spiced vegetables",
                "Red Curry - Coconut and spices",
            ],
            "rice": [
                "Fried Rice - Vegetables, egg, and soy sauce",
                "Biryani - Fragrant rice with meat or vegetables",
                "Risotto - Creamy arborio rice dish",
            ],
            "burger": [
                "Classic Cheeseburger - Beef patty with cheese",
                "Veggie Burger - Plant-based patty",
                "Chicken Burger - Grilled chicken patty",
            ],
            "sandwich": [
                "BLT Sandwich - Bacon, lettuce, tomato",
                "Club Sandwich - Triple-decker sandwich",
                "Grilled Cheese - Classic comfort sandwich",
            ],
        }

    def suggest_recipes(self, description: str, image_type: str) -> list:
        """Suggest recipes based on image description and type"""
        if image_type != "FOOD":
            return []

        suggestions = []
        description_lower = description.lower()

        for keyword, recipes in self.recipes_db.items():
            if keyword in description_lower:
                suggestions.extend(recipes)

        if not suggestions:
            suggestions = [
                "Baked version - Try baking this dish",
                "Grilled version - Try grilling for extra flavor",
                "Homemade version - Make it fresh at home",
            ]

        return suggestions[:5]

    def format_recipes(self, recipes: list) -> str:
        """Format recipes for display"""
        if not recipes:
            return "No recipes found for this food item."

        formatted = "📖 **Suggested Recipes:**\n\n"
        for i, recipe in enumerate(recipes, 1):
            formatted += f"{i}. {recipe}\n"

        return formatted

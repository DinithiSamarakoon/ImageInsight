"""Utility functions for the application"""
from PIL import Image
from typing import Tuple


def validate_image(image: Image.Image) -> Tuple[bool, str]:
    """Validate if image is valid"""
    if image is None:
        return False, "Please upload an image first"

    if not isinstance(image, Image.Image):
        return False, "Invalid image format"

    return True, "Valid"


def format_analysis_output(
    description: str,
    image_type: str,
    extracted_text: str,
    text_confidence: float,
    recipes: list,
) -> str:
    """Format analysis output for display"""
    output = "# 🖼️ Image Analysis Results\n\n"

    output += "## 📸 Image Description\n"
    output += f"**Type:** {image_type}\n"
    output += f"**Description:** {description}\n\n"

    if extracted_text:
        output += "## 📝 Extracted Text\n"
        output += f"**Confidence:** {text_confidence * 100:.1f}%\n"
        output += f"```\n{extracted_text}\n```\n\n"
    else:
        output += "## 📝 Extracted Text\nNo text found in image.\n\n"

    if recipes:
        output += "## 🍽️ Suggested Recipes\n"
        for i, recipe in enumerate(recipes, 1):
            output += f"{i}. {recipe}\n"
    else:
        output += "## 🍽️ Suggested Recipes\nNot a food item.\n"

    return output


def create_summary(
    description: str, image_type: str, text_found: bool, recipe_count: int
) -> dict:
    """Create a summary of the analysis"""
    return {
        "total_analysis": True,
        "has_description": bool(description),
        "image_type": image_type,
        "has_text": text_found,
        "recipe_suggestions": recipe_count,
    }

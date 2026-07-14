"""Image description using BLIP model"""
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


class ImageCaptioner:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

    def generate_caption(self, image: Image.Image) -> str:
        """Generate caption for a PIL Image"""
        try:
            inputs = self.processor(images=image, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_length=50)
            caption = self.processor.decode(outputs[0], skip_special_tokens=True)
            return caption
        except Exception as e:
            return f"Error generating caption: {str(e)}"

    def analyze_image(self, image: Image.Image) -> dict:
        """Analyze image and return structured data"""
        caption = self.generate_caption(image)
        return {
            "description": caption,
            "image_type": self._classify_image_type(caption),
        }

    def _classify_image_type(self, caption: str) -> str:
        """Classify image type based on caption"""
        caption_lower = caption.lower()
        if any(
            word in caption_lower
            for word in [
                "food",
                "dish",
                "meal",
                "recipe",
                "eat",
                "soup",
                "salad",
                "pizza",
                "pasta",
                "rice",
                "meat",
                "vegetable",
            ]
        ):
            return "FOOD"
        elif any(
            word in caption_lower
            for word in ["person", "people", "face", "human", "man", "woman", "child"]
        ):
            return "PERSON"
        elif any(
            word in caption_lower
            for word in ["building", "house", "street", "landscape", "nature", "tree", "sky"]
        ):
            return "SCENE"
        else:
            return "OBJECT"

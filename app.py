"""Main application using Gradio interface"""
import gradio as gr
from PIL import Image
from image_captioner import ImageCaptioner
from text_extractor import TextExtractor
from recipe_suggester import RecipeSuggester
from utils import validate_image, format_analysis_output, create_summary


class ImageAnalyzerApp:
    def __init__(self):
        self.captioner = ImageCaptioner()
        self.text_extractor = TextExtractor()
        self.recipe_suggester = RecipeSuggester()

    def analyze_image(self, image: Image.Image) -> tuple:
        """Main analysis function"""
        is_valid, message = validate_image(image)
        if not is_valid:
            return message, "", "", "", ""

        # Generate image description
        analysis = self.captioner.analyze_image(image)
        description = analysis["description"]
        image_type = analysis["image_type"]

        # Extract text
        text_result = self.text_extractor.extract_text(image)
        extracted_text = text_result["text"]
        text_confidence = text_result["confidence"]

        # Suggest recipes if food
        recipes = self.recipe_suggester.suggest_recipes(description, image_type)
        recipes_text = self.recipe_suggester.format_recipes(recipes)

        # Format output
        full_output = format_analysis_output(
            description, image_type, extracted_text, text_confidence, recipes
        )

        # Create summary
        summary = create_summary(
            description, image_type, text_result["text_found"], len(recipes)
        )

        return (
            full_output,
            description,
            extracted_text if extracted_text else "No text found",
            recipes_text,
            str(summary),
        )


def launch_app():
    """Launch Gradio interface"""
    app = ImageAnalyzerApp()

    with gr.Blocks(
        title="AI Image Analyzer",
        theme=gr.themes.Soft(),
    ) as interface:

        gr.Markdown(
            """
        # 🤖 AI Image Analyzer
        Upload an image or capture a photo to analyze it. The app will:
        - 📸 Generate a description of the image
        - 📝 Extract any text present in the image
        - 🍽️ Suggest recipes if it's a food item
        """
        )

        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(
                    type="pil",
                    label="📷 Upload Image or Capture Photo",
                    sources=["upload", "webcam"],
                )
                analyze_btn = gr.Button("🔍 Analyze Image", size="lg")

            with gr.Column(scale=1):
                output_text = gr.Markdown(label="Analysis Results")

        gr.Markdown("---")

        gr.Markdown("## 📊 Detailed Results")

        with gr.Row():
            with gr.Column():
                description_output = gr.Textbox(
                    label="📸 Image Description", lines=3, interactive=False
                )
            with gr.Column():
                text_output = gr.Textbox(
                    label="📝 Extracted Text", lines=3, interactive=False
                )

        with gr.Row():
            recipes_output = gr.Markdown(label="🍽️ Recipes")

        with gr.Row():
            summary_output = gr.Textbox(
                label="📋 Analysis Summary", lines=2, interactive=False
            )

        analyze_btn.click(
            fn=app.analyze_image,
            inputs=image_input,
            outputs=[
                output_text,
                description_output,
                text_output,
                recipes_output,
                summary_output,
            ],
        )

    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
    )


if __name__ == "__main__":
    launch_app()

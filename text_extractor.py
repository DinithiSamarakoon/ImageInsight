"""Extract text from images using OCR"""
import easyocr
from PIL import Image


class TextExtractor:
    def __init__(self, languages=["en"]):
        self.languages = languages
        self.reader = None

    def _load_reader(self):
        """Lazy load the OCR reader on first use"""
        if self.reader is None:
            print("Loading OCR model... (this happens only once)")
            self.reader = easyocr.Reader(self.languages, gpu=False)

    def extract_text(self, image: Image.Image) -> dict:
        """Extract text from image and return structured data"""
        try:
            self._load_reader()
            results = self.reader.readtext(image)

            extracted_text = "\n".join([text[1] for text in results])
            confidence_scores = [text[2] for text in results]

            avg_confidence = (
                sum(confidence_scores) / len(confidence_scores)
                if confidence_scores
                else 0
            )

            return {
                "text": extracted_text.strip(),
                "confidence": round(avg_confidence, 2),
                "text_found": len(extracted_text.strip()) > 0,
                "char_count": len(extracted_text.strip()),
            }
        except Exception as e:
            return {
                "text": "",
                "confidence": 0,
                "text_found": False,
                "char_count": 0,
                "error": str(e),
            }

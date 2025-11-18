"""
API-based Translation
Uses Google Translate and other translation APIs
"""

from deep_translator import GoogleTranslator
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class APITranslator:
    """
    Translation using external APIs (Google Translate)
    """
    
    LANGUAGE_MAP = {
        'ta': 'tamil',
        'hi': 'hindi',
        'te': 'telugu',
        'en': 'english',
        'tamil': 'ta',
        'hindi': 'hi',
        'telugu': 'te',
        'english': 'en'
    }
    
    def __init__(self, source_lang: str = 'ta', target_lang: str = 'en'):
        """
        Initialize API translator
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        logger.info(f"API Translator initialized: {source_lang} → {target_lang}")
    
    def translate(self, text: str) -> str:
        """
        Translate text using Google Translate API
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""
        
        try:
            translator = GoogleTranslator(
                source=self.source_lang,
                target=self.target_lang
            )
            result = translator.translate(text)
            return result
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return f"Error: {str(e)}"
    
    def translate_batch(self, texts: List[str]) -> List[str]:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            
        Returns:
            List of translated texts
        """
        return [self.translate(text) for text in texts]
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Text to detect language
            
        Returns:
            Language code
        """
        try:
            from langdetect import detect
            lang = detect(text)
            return lang
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'unknown'
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return ['ta', 'hi', 'te', 'en']
    
    def translate_with_confidence(self, text: str) -> Dict[str, any]:
        """
        Translate with confidence score (simulated)
        
        Args:
            text: Text to translate
            
        Returns:
            Dictionary with translation and confidence
        """
        translation = self.translate(text)
        
        return {
            'translation': translation,
            'source_lang': self.source_lang,
            'target_lang': self.target_lang,
            'confidence': 0.95,  # Simulated confidence
            'method': 'google_translate_api'
        }


class MultiAPITranslator:
    """
    Fallback translator using multiple APIs
    """
    
    def __init__(self, source_lang: str = 'ta', target_lang: str = 'en'):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.primary = APITranslator(source_lang, target_lang)
    
    def translate(self, text: str) -> str:
        """
        Translate with fallback support
        """
        # Try primary translator
        try:
            result = self.primary.translate(text)
            if result and not result.startswith("Error"):
                return result
        except Exception as e:
            logger.warning(f"Primary translator failed: {e}")
        
        # If primary fails, return error message
        return "Translation service temporarily unavailable"
    
    def translate_with_all_methods(self, text: str) -> Dict[str, str]:
        """
        Get translations from all available methods
        """
        results = {}
        
        try:
            results['google'] = self.primary.translate(text)
        except Exception as e:
            results['google'] = f"Error: {e}"
        
        return results


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("API-based Translation Demo")
    print("=" * 60)
    
    # Tamil to English
    translator = APITranslator(source_lang='ta', target_lang='en')
    
    test_texts = [
        "உணவு",
        "நான் வீட்டுக்கு செல்கிறேன்",
        "வணக்கம்"
    ]
    
    print("\nTamil to English:")
    for text in test_texts:
        translation = translator.translate(text)
        print(f"  {text} → {translation}")
    
    # Hindi to English
    print("\nHindi to English:")
    translator_hi = APITranslator(source_lang='hi', target_lang='en')
    
    hindi_texts = ["नमस्ते", "मैं खाना खा रहा हूं"]
    for text in hindi_texts:
        translation = translator_hi.translate(text)
        print(f"  {text} → {translation}")
    
    # With confidence
    print("\nTranslation with confidence:")
    result = translator.translate_with_confidence("உணவு")
    print(f"  Translation: {result['translation']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Method: {result['method']}")

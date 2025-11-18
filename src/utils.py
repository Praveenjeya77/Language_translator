"""
Utility Functions for Translation System
"""

import yaml
import logging
import os
from typing import Dict, List, Optional
from pathlib import Path

def load_config(config_path: str = "config.yaml") -> Dict:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}


def setup_logging(config: Optional[Dict] = None):
    """
    Setup logging configuration
    
    Args:
        config: Configuration dictionary
    """
    if config and 'logging' in config:
        log_config = config['logging']
        level = getattr(logging, log_config.get('level', 'INFO'))
        format_str = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(
            level=level,
            format=format_str
        )
    else:
        logging.basicConfig(level=logging.INFO)


def get_language_name(code: str) -> str:
    """
    Get full language name from code
    
    Args:
        code: Language code (ta, hi, te, en)
        
    Returns:
        Full language name
    """
    names = {
        'ta': 'Tamil',
        'hi': 'Hindi',
        'te': 'Telugu',
        'en': 'English'
    }
    return names.get(code, code)


def get_native_name(code: str) -> str:
    """
    Get native language name
    
    Args:
        code: Language code
        
    Returns:
        Native name
    """
    names = {
        'ta': 'தமிழ்',
        'hi': 'हिन्दी',
        'te': 'తెలుగు',
        'en': 'English'
    }
    return names.get(code, code)


def validate_text(text: str, max_length: int = 5000) -> bool:
    """
    Validate input text
    
    Args:
        text: Input text
        max_length: Maximum allowed length
        
    Returns:
        True if valid, False otherwise
    """
    if not text or not text.strip():
        return False
    if len(text) > max_length:
        return False
    return True


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting
    import re
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]


def batch_text(texts: List[str], batch_size: int = 32) -> List[List[str]]:
    """
    Split texts into batches
    
    Args:
        texts: List of texts
        batch_size: Size of each batch
        
    Returns:
        List of batches
    """
    return [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]


def save_translations(translations: List[Dict], output_path: str):
    """
    Save translations to file
    
    Args:
        translations: List of translation dictionaries
        output_path: Output file path
    """
    try:
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        logging.info(f"Translations saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving translations: {e}")


def load_translations(input_path: str) -> List[Dict]:
    """
    Load translations from file
    
    Args:
        input_path: Input file path
        
    Returns:
        List of translation dictionaries
    """
    try:
        import json
        with open(input_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        return translations
    except Exception as e:
        logging.error(f"Error loading translations: {e}")
        return []


def create_directory_structure():
    """Create necessary directories for the project"""
    directories = [
        'models',
        'models/cache',
        'models/checkpoints',
        'data',
        'data/train',
        'data/val',
        'data/test',
        'logs',
        'outputs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logging.info("Directory structure created")


def get_device() -> str:
    """
    Get best available device for PyTorch
    
    Returns:
        Device string ('cuda', 'mps', or 'cpu')
    """
    try:
        import torch
        if torch.cuda.is_available():
            return 'cuda'
        elif torch.backends.mps.is_available():
            return 'mps'
        else:
            return 'cpu'
    except:
        return 'cpu'


def format_translation_output(
    source_text: str,
    translation: str,
    source_lang: str,
    target_lang: str,
    model: str = "unknown",
    confidence: float = None
) -> Dict:
    """
    Format translation output as dictionary
    
    Args:
        source_text: Original text
        translation: Translated text
        source_lang: Source language code
        target_lang: Target language code
        model: Model used
        confidence: Confidence score
        
    Returns:
        Formatted dictionary
    """
    result = {
        'source_text': source_text,
        'translation': translation,
        'source_language': {
            'code': source_lang,
            'name': get_language_name(source_lang),
            'native': get_native_name(source_lang)
        },
        'target_language': {
            'code': target_lang,
            'name': get_language_name(target_lang),
            'native': get_native_name(target_lang)
        },
        'model': model
    }
    
    if confidence is not None:
        result['confidence'] = confidence
    
    return result


def read_file(file_path: str) -> str:
    """
    Read text from file
    
    Args:
        file_path: Path to file
        
    Returns:
        File contents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return ""


def write_file(content: str, file_path: str):
    """
    Write text to file
    
    Args:
        content: Text content
        file_path: Output file path
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Content written to {file_path}")
    except Exception as e:
        logging.error(f"Error writing file: {e}")


class TranslationCache:
    """Simple in-memory cache for translations"""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key: str) -> Optional[str]:
        """Get translation from cache"""
        return self.cache.get(key)
    
    def set(self, key: str, value: str):
        """Set translation in cache"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
    
    def size(self) -> int:
        """Get cache size"""
        return len(self.cache)


# Example usage
if __name__ == "__main__":
    setup_logging()
    
    print("Testing utility functions...")
    
    # Test language functions
    print(f"\nLanguage: ta")
    print(f"  Full name: {get_language_name('ta')}")
    print(f"  Native name: {get_native_name('ta')}")
    
    # Test text validation
    print(f"\nText validation:")
    print(f"  Valid text: {validate_text('Hello world')}")
    print(f"  Empty text: {validate_text('')}")
    
    # Test sentence splitting
    text = "This is sentence one. This is sentence two! Is this three?"
    sentences = split_into_sentences(text)
    print(f"\nSentences: {sentences}")
    
    # Test device detection
    device = get_device()
    print(f"\nBest device: {device}")
    
    # Test translation formatting
    result = format_translation_output(
        source_text="உணவு",
        translation="food",
        source_lang="ta",
        target_lang="en",
        model="transformer",
        confidence=0.95
    )
    print(f"\nFormatted output:")
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

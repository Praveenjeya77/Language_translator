"""
Indian Language Translation System
Neural Machine Translation for Tamil, Hindi, and Telugu
"""

__version__ = '1.0.0'
__author__ = 'Your Name'
__email__ = 'your.email@example.com'

from .api_translator import APITranslator
from .utils import (
    load_config,
    setup_logging,
    get_language_name,
    get_native_name
)

__all__ = [
    'APITranslator',
    'load_config',
    'setup_logging',
    'get_language_name',
    'get_native_name'
]

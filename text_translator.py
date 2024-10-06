import socket
import os
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from transformers import MarianMTModel, MarianTokenizer
from googletrans import Translator


# Set seed to ensure consistent language detection results
DetectorFactory.seed = 0

def is_valid_text(text: str) -> bool:
    """Check if the input is a valid text (not empty or random symbols).
    
    Args:
        text (str): The input text to check.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    valid = bool(text and text.strip())
    print(f"Validating text: '{text}' - Valid: {valid}")
    return valid

def detect_language(text: str) -> str:
    """Detect the language of a given string.
    
    Args:
        text (str): The input text to detect the language for.
        
    Returns:
        str: The language code (e.g., 'en' for English), or an error message.
    """
    try:
        language = detect(text)
        print(f"Detected language: {language} for text: '{text}'")
        return language
    except LangDetectException:
        with open(os.path.basename(__file__).replace('.py', '.log'),'a') as file:
            file.write("Language detection failed.")
        return "Could not detect the language"

def is_connected(host="www.google.com", port=80, timeout=5) -> bool:
    """Check if the machine is connected to the internet.
    
    Args:
        host (str): The host to ping.
        port (int): The port to connect to.
        timeout (int): Timeout in seconds for the connection attempt.
        
    Returns:
        bool: True if connected, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection((host, port))
        print("Internet connection established.")
        return True
    except OSError:
        with open(os.path.basename(__file__).replace('.py', '.log'),'a') as file:
            file.write("No internet connection.")
        return False

def translate_offline(text: str, source_lang: str, target_lang: str = 'en') -> str:
    """Translate text using MarianMT offline models.
    
    Args:
        text (str): The text to translate.
        source_lang (str): The source language code.
        target_lang (str): The target language code.
        
    Returns:
        str: The translated text.
    """
    model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
    print(f"Loading offline model for translation from {source_lang} to {target_lang}.")
    
    # Load the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    # Tokenize and translate
    tokenized_text = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**tokenized_text)
    translation = tokenizer.decode(translated[0], skip_special_tokens=True)
    print(f"Offline translation result: '{translation}'")
    return translation

def translate_online(text: str, target_language: str = 'en') -> str:
    """Translate text using Google Translate.
    
    Args:
        text (str): The text to translate.
        target_language (str): The target language code.
        
    Returns:
        str: The translated text.
    """
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        print(f"Online translation result: '{translation.text}'")
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return ""

def translate_text(text: str, target_language: str = 'en', USE_GOOGLE = True) -> str:
    """Detect language, check internet connectivity, and translate accordingly.
    
    Args:
        text (str): The input text to translate.
        target_language (str): The target language code.
        
    Returns:
        str: The translated text or an error message.
    """
    if not is_valid_text(text):
        with open(os.path.basename(__file__).replace('.py', '.log'),'a') as file:
            file.write("Invalid input text.")
        return "Invalid input text."

    # Detect language
    language_code = detect_language(text)
    
    # Check if there is an internet connection
    if is_connected() and USE_GOOGLE:
        print("Internet connection detected")
        return translate_online(text, target_language)
    else:
        return translate_offline(text, language_code, target_language)

if __name__ == '__main__':
    
    # Example usage
    input_text = "好きなだけ"  # Japanese for "as much as you like"
    translated_text = translate_text(input_text, "en")  # Translates to English
    print(f"Translated text: {translated_text}")

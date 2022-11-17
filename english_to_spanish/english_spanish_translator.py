from translate import Translator

def translator(text):
    translator = Translator(from_lang="English",to_lang="Spanish")
    text = translator.translate(text)
    return text

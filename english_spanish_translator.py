from translate import Translator

#The email we read will get sent here to be translated

translator = Translator(from_lang="English", to_lang="Spanish")
translation = translator.translate(message)

# After translation, it will get sent via sms
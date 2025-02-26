import json
def translate_into(path, data, key=None):
    with open(path, "r", encoding="utf-8") as f:
        translations = json.load(f)
        language = data.get('current_language', 'Uzbek')  
        if key:
            return translations[key][language]
        return translations
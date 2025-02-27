import json
def translate_into(path, data, key=None):
    """Berilgan fayldan tarjimani yuklaydi va tanlangan tilga mos matnni qaytaradi.

    Fayl yo'lini, ma'lumotlar lug'atini va ixtiyoriy kalitni qabul qiladi. Agar kalit
    berilgan bo'lsa, faqat shu kalitga mos tarjimani qaytaradi, aks holda butun
    tarjimani qaytaradi. Tilni 'current_language' dan oladi, standart sifatida 'Uzbek'.

    Args:
        path (str): Tarjima faylining yo'li (JSON formati).
        data (dict): Foydalanuvchi ma'lumotlari, 'current_language' ni o'z ichiga oladi.
        key (str, optional): Qaytariladigan maxsus tarjima kaliti. Standart: None.

    Returns:
        str or dict: Kalit berilgan bo'lsa tarjima matni (str), aks holda butun tarjima (dict).
    """
    with open(path, "r", encoding="utf-8") as f:
        translations = json.load(f)
        language = data.get('current_language', 'Uzbek')  
        if key:
            return translations[key][language]
        return translations
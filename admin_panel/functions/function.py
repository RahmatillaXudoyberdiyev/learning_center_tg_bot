from aiogram.types import Message
from aiogram.types import FSInputFile
import os



# Bahodir Sadullayev
# Info : To'liq xisobotni exel faylga o'tkazib telegram bot orqali yuborish

async def all_reports(message : Message) :
    import pandas as pd
    csv_file = "all_users.csv"
    excel_file = "all_users.xlsx"

    # Fayl mavjudligini tekshirish
    if not os.path.exists(csv_file):
        await message.answer("CSV fayl topilmadi!")
        return

    # CSV dan Excelga o‘girish
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False, engine='openpyxl')

    # Faylni yuborish
    file = FSInputFile(excel_file)
    await message.answer_document(file)
async def today_reports(message : Message) :
    import pandas as pd
    csv_file = "users_today.csv"
    excel_file = "users_today.xlsx"

    # Fayl mavjudligini tekshirish
    if not os.path.exists(csv_file):
        await message.answer("CSV fayl topilmadi!")
        return

    # CSV dan Excelga o‘girish
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False, engine='openpyxl')

    # Faylni yuborish
    file = FSInputFile(excel_file)
    await message.answer_document(file)
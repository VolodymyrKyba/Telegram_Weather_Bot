from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
period_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Зараз")],
        [KeyboardButton(text="Протягом дня")],
        [KeyboardButton(text="Протягом тижня")]
    ],
    resize_keyboard=True  # Зменшує розмір клавіатури для зручності
)
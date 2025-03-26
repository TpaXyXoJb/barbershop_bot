from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Временные данные: список мастеров
fake_masters = ["Анна", "Иван", "Мария"]


def get_masters_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"select_master:{name}")]
        for name in fake_masters
    ])
    return keyboard


@router.callback_query(lambda c: c.data == "book_appointment")
async def choose_master(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите мастера:", reply_markup=get_masters_keyboard()
    )
    await callback.answer()

from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .start import menu_keyboard

router = Router()

# Временные данные: список мастеров и услуг
fake_masters = ["Анна", "Иван", "Мария"]
fake_categories = ["Мужские стрижки", "Женские стрижки"]


def get_masters_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"select_master:{name}")]
        for name in fake_masters
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu")
    ])
    return keyboard


def get_categories_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=cat, callback_data=f"select_category:{cat}")]
        for cat in fake_categories
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="book_appointment")
    ])
    return keyboard


@router.callback_query(F.data == "book_appointment")
async def choose_master(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите мастера:", reply_markup=get_masters_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "menu")
async def go_back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Добро пожаловать! Что вы хотите сделать?", reply_markup=menu_keyboard
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_master:"))
async def choose_category(callback: types.CallbackQuery):
    master = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"Вы выбрали мастера: {master}\nТеперь выберите категорию услуги:",
        reply_markup=get_categories_keyboard()
    )
    await callback.answer()

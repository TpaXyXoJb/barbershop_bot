from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

from .start import menu_keyboard

router = Router()

fake_masters = ["Анна", "Иван", "Мария"]
fake_categories = ["Мужские стрижки", "Женские стрижки"]
fake_services = {
    "Мужские стрижки": ["Классическая", "Под машинку", "Fade"],
    "Женские стрижки": ["Каре", "Пикси", "Каскад"]
}


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


def get_services_keyboard(category: str) -> InlineKeyboardMarkup:
    services = fake_services.get(category, [])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=service, callback_data=f"select_service:{service}")]
        for service in services
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data=f"book_appointment")
    ])
    return keyboard


def get_dates_keyboard() -> InlineKeyboardMarkup:
    today = datetime.today()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(10)]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=date, callback_data=f"select_date:{date}")]
        for date in dates
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


@router.callback_query(F.data.startswith("select_category:"))
async def choose_service(callback: types.CallbackQuery):
    category = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"Категория: {category}\nТеперь выберите услугу:",
        reply_markup=get_services_keyboard(category)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_service:"))
async def choose_date(callback: types.CallbackQuery):
    service = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"Услуга: {service}\nВыберите дату:",
        reply_markup=get_dates_keyboard()
    )
    await callback.answer()

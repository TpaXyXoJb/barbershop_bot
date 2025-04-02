from aiogram import Router, types, F
from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           ReplyKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardRemove
                           )
from datetime import datetime, timedelta

from .start import menu_keyboard
from bot.temp_state import user_state

router = Router()

fake_masters = ["Анна", "Иван", "Мария"]
fake_categories = ["Мужские стрижки", "Женские стрижки"]
fake_services = {
    "Мужские стрижки": ["Классическая", "Под машинку", "Fade"],
    "Женские стрижки": ["Каре", "Пикси", "Каскад"]
}
fake_times = ["10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]


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
        InlineKeyboardButton(text="🔙 Назад", callback_data="book_appointment")
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


def get_time_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=time, callback_data=f"select_time:{time}")]
        for time in fake_times
    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="book_appointment")
    ])
    return keyboard


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


@router.callback_query(F.data == "menu")
async def go_back_to_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "👋 Добро пожаловать! Что вы хотите сделать?",
        reply_markup=menu_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "book_appointment")
async def choose_master(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = {}
    await callback.message.edit_text(
        "Выберите мастера:",
        reply_markup=get_masters_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_master:"))
async def choose_category(callback: types.CallbackQuery):
    master = callback.data.split(":")[1]
    user_state[callback.from_user.id]["master"] = master
    await callback.message.edit_text(
        f"Вы выбрали мастера: {master}\nТеперь выберите категорию услуги:",
        reply_markup=get_categories_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_category:"))
async def choose_service(callback: types.CallbackQuery):
    category = callback.data.split(":")[1]
    user_state[callback.from_user.id]["category"] = category
    await callback.message.edit_text(
        f"Категория: {category}\nТеперь выберите услугу:",
        reply_markup=get_services_keyboard(category)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_service:"))
async def choose_date(callback: types.CallbackQuery):
    service = callback.data.split(":")[1]
    user_state[callback.from_user.id]["service"] = service
    await callback.message.edit_text(
        f"Услуга: {service}\nВыберите дату:",
        reply_markup=get_dates_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_date:"))
async def choose_time(callback: types.CallbackQuery):
    date = callback.data.split(":")[1]
    user_state[callback.from_user.id]["date"] = date
    await callback.message.edit_text(
        f"Дата: {date}\nВыберите время:",
        reply_markup=get_time_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("select_time:"))
async def ask_phone(callback: types.CallbackQuery):
    time = callback.data.split(":")[1]
    state = user_state.get(callback.from_user.id, {})
    state["time"] = time
    msg = (
        f"Мастер: {state.get('master')}\n"
        f"Услуга: {state.get('service')}\n"
        f"Дата: {state.get('date')}\n"
        f"Время: {time}\n"
        "📱 Отправьте номер телефона для завершения записи:"
    )
    await callback.message.answer(
        msg,
        reply_markup=get_phone_keyboard()
    )
    await callback.answer()


@router.message(F.contact)
async def process_contact(message: types.Message):
    phone = message.contact.phone_number
    await message.answer(
        f"✅ Номер получен: {phone}",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer("Запись завершена! 🎉 (заглушка)")

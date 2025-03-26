from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📅 Записаться", callback_data="book_appointment"),
        InlineKeyboardButton(text="📖 Мои записи", callback_data="my_bookings")
    ],
    [
        InlineKeyboardButton(text="💇 Примеры стрижек", callback_data="haircuts")
    ]
])


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Добро пожаловать! Что вы хотите сделать?", reply_markup=menu_keyboard)

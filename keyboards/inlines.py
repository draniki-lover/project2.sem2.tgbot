from aiogram import types

from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Начнем!", callback_data="start")],
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

def usage() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="Ввести самостоятельно")],
        [KeyboardButton(text="Увидеть стандартные графики")],
        [KeyboardButton(text="Отмена")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons
    )

def graph_type_choice() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Задать вручную"),
        KeyboardButton(text="Выбрать из коллекции")
    )
    builder.row(KeyboardButton(text="Отмена"))
    return builder.as_markup(resize_keyboard=True)

def standard_functions_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    # Первый ряд
    builder.row(
        KeyboardButton(text="y = x"),
        KeyboardButton(text="y = x²")
    )
    # Второй ряд
    builder.row(
        KeyboardButton(text="y = √x"),
        KeyboardButton(text="y = |x|")
    )
    # Третий ряд
    builder.row(
        KeyboardButton(text="y = sin(x)"),
        KeyboardButton(text="y = cos(x)")
    )
    # Четвертый ряд
    builder.row(
        KeyboardButton(text="y = e^x"),
        KeyboardButton(text="y = ln(x)")
    )
    # Отмена
    builder.row(KeyboardButton(text="Назад"))
    return builder.as_markup(resize_keyboard=True)

def back_keyboard():
    buttons = [
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
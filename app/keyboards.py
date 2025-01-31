from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Создать напоминание')],
                                     [KeyboardButton(text="Удалить напоминание")],
                                     [KeyboardButton(text="Посмотреть все записи")]],
                           resize_keyboard=True,
                           input_field_placeholder="Выберите в меню снизу")


def get_medications_keyboard(medications):
    get_kb = InlineKeyboardBuilder()

    for medication in medications:
        if len(medication) >= 2:
            name = medication[1]
            time = medication[2]
            button_text = f"{name} - {time}"
            callback_data = f"delete_{medication[0]}"

            get_kb.button(text=button_text, callback_data=callback_data)
            get_kb.adjust(1)




    return get_kb.as_markup()



start_plan = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приступить к планированию',callback_data='plan')]])


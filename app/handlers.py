import asyncio

import aioschedule
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from datetime import datetime

import app.keyboards as kb
from app.database.database import add_medication, get_medications, delete_medication, get_reminders
from app.keyboards import get_medications_keyboard

router = Router()

class AddMedicine(StatesGroup):
    name = State()
    time = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply("Выбери нужную функцию", reply_markup=kb.start_plan)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer("Вы вызвали меню поддержки")

@router.callback_query(F.data == 'plan')
async def start_plan(callback: CallbackQuery):
    await callback.message.answer("Вы перешли в главное меню", reply_markup=kb.main)

@router.message(lambda message: message.text == "Создать напоминание")
async def add_pill(message: Message, state: FSMContext):

    await state.set_state(AddMedicine.name)
    await message.answer("Введіть назву препарата", reply_markup=ReplyKeyboardRemove())

@router.message(AddMedicine.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddMedicine.time)
    await message.answer('Введіть час прийому')

@router.message(AddMedicine.time)
async def register_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    try:
        data = await state.get_data()
        name = data['name']
        time = data['time']
        user_id = str(message.from_user.id)
        add_medication(user_id, name, time)
        await message.answer(f'Препарат {name} принят в {time}', reply_markup=kb.main)

    except Exception as e:
        await message.reply(f"Ошибка: {e}")
    finally:
        await state.clear()


@router.message(lambda message: message.text == "Посмотреть все записи")
async def view_records(message: types.Message):
    user_id = str(message.from_user.id)
    medications = get_medications(user_id)
    if medications:
        response = "Ваши записи:\n\n"
        response += "\n".join([f"●{name} ({time})" for _, name, time in medications])
    else:
        response = "У вас нет записей"
    await message.reply(response)

@router.message(lambda message: message.text == "Удалить напоминание")
async def delete_reminder(message: CallbackQuery):
    user_id = str(message.from_user.id)
    medications = get_medications(user_id)
    if not medications:
        await message.message.answer("Нет записей")
        return

    inline_kb = get_medications_keyboard(medications)
    await message.answer("Выберите запись для удаления", reply_markup=inline_kb)

@router.callback_query(lambda call: call.data.startswith("delete_"))
async def handle_delete_medications(call: CallbackQuery):
    med_id = int(call.data.split("_")[1])
    delete_medication(med_id)
    await call.message.edit_text("Запись удалена")
    await call.answer()


from aiogram import Bot

async def send_reminders(bot: Bot):
    reminders = get_reminders()  # Получаем напоминания
    for user_id, name in reminders:
        try:
            await bot.send_message(chat_id=user_id, text=f"Напоминание: {name}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

async def schedule(bot: Bot):
    aioschedule.every().minute.do(send_reminders, bot=bot)  # Передаем бот как аргумент
    print("Planner is working")
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
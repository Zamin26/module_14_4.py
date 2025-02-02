from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import get_all_products
import asyncio

api = ""
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):                                             # наследованный от StatesGroup
    age = State()                                                        # 3 объекта класса
    growth = State()
    weight = State()

@dp.callback_query_handler(text = 'calories')                            # handler исправлен'
async def set_age(call):
    await call.message.answer('Введите свой возраст:')                   # ответ на сообщение
    await UserState.age.set()                                            # ввода возраста в атрибут

kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "Рассчитать"),            # Кнопка рассчитать
            KeyboardButton(text = "Информация"),            # Кнопка информация
        ]
    ], resize_keyboard=True)                                # Размер кнопок автоматический


button3 = KeyboardButton(text = "Купить"),                # Добавление кнопки купить в клавиатуру
kb.add(button3)

menu = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data='formulas')
menu.add(button1)
menu.add(button2)


menu_kb = InlineKeyboardMarkup()                # Inline меню из 4 кнопок
button4 = InlineKeyboardButton(text = 'Product1', callback_data="product_buying")
button5 = InlineKeyboardButton(text = 'Product2', callback_data="product_buying")
button6 = InlineKeyboardButton(text = 'Product3', callback_data="product_buying")
button7 = InlineKeyboardButton(text = 'Product4', callback_data="product_buying")
menu.add(button4)
menu.add(button5)        # добавление кнопок
menu.add(button6)
menu.add(button7)


@dp.message_handler(commands = ['start'])                       # хендлер на вызов команды
async def start(message):
    await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup = kb)
    # возвращение ответа, reply_markup показывает клавиатуру






# Домашнее задание


@dp.message_handler(text = "Купить")                            # хендлер на вызов команды купить
async def get_buying_list(message):                             # изменение функции
    products = get_all_products()                               # новая функция, ссылается на файл crud_functions
    for i in products:
        with open(f'files/{i} таблетки.jpg','rb') as img:
            await message.answer(f"Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}")
            await message.answer_photo(img, reply_markup=kb)            # ответ картинкой
        await message.answer('Выберите продукт для покупки:', reply_markup=menu_kb)










@dp.callback_query_handler(text = 'product_buying')    #call back дата, на какую кнопку будет отрабатывать handler
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!", reply_markup=menu_kb)      # ответ на приобретение товара
    await call.answer()

@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    await message.answer("Выбери опцию", reply_markup=menu)

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.callback_query_handler(text = 'formulas')    #call back дата, на какую кнопку будет отрабатывать handler
async def get_formulas(call):
    await call.message.answer("6.25 * рост(см) + 10 * вес(кг) - 5 * возраст(лет) + 5 для мужчин\n6.25 * рост(см)"
                              "+ 10 * вес(кг) - 5 * возраст(лет) - 161 для женщин", reply_markup=kb)
    await call.answer()

@dp.message_handler(state = UserState.age)                      # реагирует на переданное состояние UserState.age
async def set_growth(message, state):
    await state.update_data(age=message.text)                   # обновляет данные в состоянии age
    await message.answer(f"Введите свой рост:")                 # сообщение после ввода
    await UserState.growth.set()                                # ввод роста в атрибут UserState.growth

@dp.message_handler(state=UserState.growth)                     # реагирует на переданное состояние UserState.growth.
async def set_weight(message, state):
    await state.update_data(growth=message.text)                # обновляет данные в состоянии growth
    await message.answer(f"Введите свой вес:")                  # сообщение после ввода
    await UserState.weight.set()                                # ввод роста в атрибут UserState.weight


@dp.message_handler(state=UserState.weight)                     # реагирует на переданное состояние UserState.weight.
async def send_calories(message, state):
    await state.update_data(weight=message.text)                # обновляет данные в состоянии weight
    await message.answer(f"Введите свой вес:")                  # сообщение после ввода
    data = await state.get_data()                               # данные сохранены в переменную data
    norma_calories_man = 6.25 * float(data['growth']) + 10 * float(data['weight']) - 5 * float(data['age']) + 5     # для мужчин
    norma_calories_woman = 6.25 * float(data['growth']) + 10 * float(data['weight']) - 5 * float(data['age']) - 161 # для женщин
    await message.answer(f' Норма калорий составляет для мужчины: {norma_calories_man:.2f}, '
                         f'для женщины: {norma_calories_woman:.2f}.')                   # Результат вычисления
    await state.finish()                                                                # закрытие машины


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

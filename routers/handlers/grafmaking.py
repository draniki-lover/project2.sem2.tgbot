from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from keyboards import inlines
from states.state import Form
from services.wolf_serv import get_wolfram_plot
from middlewares.func_valid import FunctionValidatorMiddleware
from filters.graph_filt import EmptyFunctionCheckMiddleware
from filters.graph_limit import GraphRateLimiter


router = Router()
router.message.middleware(GraphRateLimiter())
router.message.middleware(FunctionValidatorMiddleware())
router.message.middleware(EmptyFunctionCheckMiddleware())

STANDARD_FUNCTIONS = {
    "y = x": "y = x",
    "y = x²": "y = x^2",
    "y = √x": "y = sqrt(x)",
    "y = |x|": "y = |x|",
    "y = sin(x)": "y = sin(x)",
    "y = cos(x)": "y = cos(x)",
    "y = e^x": "y = exp(x)",
    "y = ln(x)": "y = log(x)"
}

async def show_previous_step(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == Form.waiting_standard_choice:
        await state.set_state(Form.waiting_graph_type)
        await message.answer(
            "Выбери способ задания графика:",
            reply_markup=inlines.graph_type_choice()
        )
    elif current_state == Form.waiting_graph_type:
        await state.set_state(Form.waiting_communication_style)
        await message.answer(
            "Возвращаюсь к началу\nНажми /help - там ты вероятно сможешь найти, что тебе надо🙌",
            reply_markup=inlines.start_kb(),
        )

@router.callback_query(lambda c: c.data in ["start"])
async def process_communication_style(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Form.waiting_graph_type)
    await callback.message.answer(
        "Хорошо, теперь выбери, как хочешь задать график",
        reply_markup=inlines.graph_type_choice()
    )

@router.message(Form.waiting_graph_type)
async def process_graph_type(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await show_previous_step(message, state)
    elif message.text == "Задать вручную":
        await state.set_state(Form.waiting_function_input)
        await message.answer(
            "Введи функцию в формате:\n\n"
            "Примеры:\n"
            "• y = x^2 + 3x - 5\n"
            "• f(x) = sin(x) * cos(x)\n"
            "• sqrt(x) + 1",
            reply_markup=types.ReplyKeyboardRemove()
        )
    elif message.text == "Выбрать из коллекции":
        await state.set_state(Form.waiting_standard_choice)
        await message.answer(
            "А теперь выбери, график какой из стандартных функций хочешь увидеть",
            reply_markup=inlines.standard_functions_keyboard()
        )

async def send_wolfram_plot(message: types.Message, function: str):
    status_msg = await message.answer("Строим график...")

    wolfram_query = f"plot {function}" if not function.lower().startswith(('plot', 'graph')) else function

    try:
        image_data = await get_wolfram_plot(wolfram_query)

        if image_data:
            await message.answer_photo(
                types.BufferedInputFile(
                    file=image_data.getvalue(),
                    filename="graph.png"
                ),
                caption=f"График функции: {function}"
            )
        else:
            alt_query = f"graph of {function}"
            image_data = await get_wolfram_plot(alt_query)

            if image_data:
                await message.answer_photo(
                    types.BufferedInputFile(
                        file=image_data.getvalue(),
                        filename="graph.png"
                    ),
                    caption=f"График функции: {function}"
                )
            else:
                await message.answer(f"Не удалось построить график для: {function}\nПопробуйте другой формат")

    except Exception as e:
        await message.answer(f"Ошибка при построении графика: {str(e)}")

    finally:
        await status_msg.delete()

@router.message(Form.waiting_function_input)
async def process_function_input(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(Form.waiting_graph_type)
        await message.answer(
            "Выбери способ задания графика:",
            reply_markup=inlines.graph_type_choice()
        )
        return

    user_input = message.text.strip()
    await send_wolfram_plot(message, user_input)

    await message.answer(
        "График построен. Введи новую функцию или нажмите 'Назад':",
        reply_markup=inlines.back_keyboard()
    )

@router.message(Form.waiting_standard_choice)
async def process_standard_choice(message: types.Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, выбери вариант из предложенных кнопок")
        return

    if message.text == "Назад":
        await show_previous_step(message, state)
    elif message.text in STANDARD_FUNCTIONS:
        function = STANDARD_FUNCTIONS[message.text]
        await send_wolfram_plot(message, function)
        await show_previous_step(message, state)
    else:
        await message.answer("Пожалуйста, выбери вариант из предложенных кнопок")

# Graph Builder Bot  
Telegram-бот для построения графиков математических функций с помощью WolframAlpha API.

## Участники проекта
- Шманькова Ксения (468113)  
- Шмидт Виктория (468114)  

## О проекте
Graph Builder Bot - это Telegram бот, разработанный для удобного построения графиков математических функций. Бот интегрирован с WolframAlpha API и предоставляет два способа построения графиков:
1. Ввод пользовательской функции
2. Выбор из коллекции стандартных функций

Основные возможности:
- Построение графиков по введенным формулам
- Коллекция стандартных математических функций
- История построенных графиков
- Валидация вводимых функций
- Ограничение частоты запросов (rate limiting)

## Технологии
- Python 3
- aiogram (фреймворк для Telegram ботов)
- WolframAlpha API
- Pydantic (для работы с конфигурацией)

## Структура проекта

```text
graph-bot/
├── config/
│   └── bot_config.py         # Конфигурация бота (токены, настройки)
├── graph_storage/            # Хранилище графиков
│   ├── graph_20250608_*.png  # Примеры сохраненных графиков
│   └── graphs_data.json      # Метаданные графиков
├── keyboards/
│   └── inlines.py            # Все типы клавиатур
├── logs/
│   └── main.log              # Файл логов
├── middlewares/              # Промежуточное ПО
│   ├── func_valid.py         # Валидатор функций
│   ├── graph_filt.py         # Фильтр пустых запросов
│   └── graph_limit.py        # Лимитер запросов
├── routers/                  # Обработчики команд
│   ├── commands.py           # Базовые команды
│   └── handlers/
│       ├── about.py          # Информация о боте
│       ├── clean.py          # Очистка истории
│       ├── grafmaking.py     # Построение графиков
│       └── history.py        # Работа с историей
├── services/                 # Внешние сервисы
│   └── wolfram_service.py    # Работа с WolframAlpha API
├── states/                   # Состояния FSM
│   └── state.py              # Определение состояний
├── utils/                    # Вспомогательные модули
│   └── logger.py             # Настройка логгирования
├── main.py                   # Точка входа
├── README.md                 # Документация
└── requirements.txt          # Список всех необходимых Python-пакетов
```
## Предварительные требования
- Python 3.10+ (проверить версию: python --version)
- Telegram-бот (получить токен у [@BotFather](https://telegram.me/BotFather))
- WolframAlpha API ключ (зарегистрироваться на [developer.wolframalpha.com](developer.wolframalpha.com))
- Git (для клонирования репозитория)
## Инструкция по установке и запуску

### Предварительные требования
- [Python 3.10+](https://www.python.org/downloads/)
- [Telegram аккаунт](https://telegram.org/)
- [WolframAlpha Developer аккаунт](https://developer.wolframalpha.com/)

### Установка

1. **Клонируйте репозиторий**:
```bash
git clone https://github.com/your-username/graph-bot.git
cd graph-bot
```
2. **Установите зависимости**:
```bash
pip install -r requirements.txt
```
3. **Настройте окружение**:
- Создайте файл .env в корне проекта:
```bash
TELEGRAM_API_KEY=your_telegram_bot_token
WOLFRAM_APP_ID=your_wolfram_app_id
```
4. **Запуск бота**:
```dash
python main.py
```

### Получение API ключей
Telegram Bot Token:
- Напишите [@BotFather](https://telegram.me/BotFather) в Telegram
- Используйте команду /newbot
- Скопируйте полученный токен

WolframAlpha App ID:
- Зарегистрируйтесь на портале разработчика
- Создайте новое приложение
- Скопируйте App ID


## Использование бота

После запуска бота вы можете взаимодействовать с ним через Telegram:

```
/start - начать работу с ботом
/help - получить справку по использованию бота
/about - информация о проекте
/history - просмотр истории графиков
/delete - очистка истории
```

Пример ввода функции:
```
y = x^2 + 3x - 5
f(x) = sin(x)*cos(x)
```


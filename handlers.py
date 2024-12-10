from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import requests
from datetime import datetime
from googletrans import Translator
import keyboards as kb  # Your keyboards
from config import WEATHER_API_KEY

router = Router()
translator = Translator()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт! Напиши назву міста і я покажу тобі погоду!")

# Обробка запиту погоди
@router.message()
async def get_weather(message: Message):
    if message.photo or message.audio or message.video or message.document:
        await message.delete()  # Видалити медіафайл
        await message.answer("Формат фото, аудіо та відео файлів не підтримується.")
        return

    try:
        city = message.text.strip()  # Отримуємо назву міста
        # Формуємо запит до OpenWeatherMap
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric")
        
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].capitalize()
            translated = translator.translate(description, src="auto", dest="uk")
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            # Формуємо відповідь
            weather_info = (
                f"Погода у: {city} 🌍\n"
                f"🌡 Температура: {temp}°C\n"
                f"☁️ Опис: {translated.text}\n"
                f"💧 Вологість: {humidity}%\n"
                f"🌬 Швидкість вітру: {wind_speed} м/с"
            )
            await message.answer(weather_info)
        else:
            await message.reply("Не вдалося знайти інформацію про це місто. Спробуй ще раз!")

    except Exception as e:
        await message.reply("Сталася помилка! Правильно введіть назву міста")

# Обробка медіафайлів (фото, аудіо, відео, документи)
@router.message(F.photo | F.audio | F.video | F.document)
async def block_media(message: Message):
    await message.delete()  # Видалення медіа
    await message.answer("Надсилання медіа-файлів (фото, аудіо, відео, документи) не підтримується.")

# Handling city input
# @router.message(StateFilter(Form.city))  # Use StateFilter instead of state
# async def get_period_name(message: Message, state: FSMContext):
#     city = message.text.strip()
#     await state.update_data(city=city)
#     await message.answer(
#         f"Now, choose the period for the weather forecast:", 
#         reply_markup=kb.period_button  # Your keyboard for period selection
#     )
#     await state.set_state(Form.period)  # Set the state to 'period'

# Handling period selection
# @router.message(StateFilter(Form.period))  # Use StateFilter instead of state
# async def get_weather(message: Message, state: FSMContext):
#     user_data = await state.get_data()
#     city = user_data.get("city")
#     period = message.text.strip().lower()

#     # Validate the period input
#     if period not in ["зараз", "протягом дня", "протягом тижня"]:
#         await message.answer("Please select a valid period: 'Протягом дня' or 'Протягом тижня'")
#         return

#     # Get weather data based on the period
#     if period == "зараз":
#         weather_info = await get_weather_data_now(city)
#     elif period == "протягом дня":
#         weather_info = await get_weather_data_daily(city)
#     elif period == "протягом тижня":
#         weather_info = await get_weather_data_weekly(city)

#     await message.answer(weather_info)
#     # await state.clear()  # Finish the process

# # Get weather data for the current weather
# async def get_weather_data_now(city: str):
#     try:
#         response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric")
        
#         if response.status_code == 200:
#             data = response.json()
#             city_name = data["name"]
#             temp = data["main"]["temp"]
#             description = data["weather"][0]["description"].capitalize()
#             humidity = data["main"]["humidity"]
#             wind_speed = data["wind"]["speed"]

#             weather_info = (
#                 f"Weather in {city_name} 🌍\n"
#                 f"🌡 Temperature: {temp}°C\n"
#                 f"☁️ Description: {description}\n"
#                 f"💧 Humidity: {humidity}%\n"
#                 f"🌬 Wind Speed: {wind_speed} m/s"
#             )
#             return weather_info
#         else:
#             return "Failed to get weather information for this city. Please try again!"
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# # Get weather data for the daily forecast
# async def get_weather_data_daily(city: str):
#     try:
#         geocoding_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}")
        
#         if geocoding_response.status_code == 200:
#             geocoding_data = geocoding_response.json()
#             lat = geocoding_data["coord"]["lat"]
#             lon = geocoding_data["coord"]["lon"]
            
#             response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={WEATHER_API_KEY}&units=metric")
#             data = response.json()
#             weather_info = "Daily forecast:\n"
#             # for day in data["daily"]:
#             #     date = day["dt"]
#             #     temp = day["temp"]["day"]
#             #     description = day["weather"][0]["description"]
#             #     weather_info += f"Date: {date}\nTemperature: {temp}°C\nDescription: {description}\n\n"
            
#             return weather_info
#         else:
#             return "Failed to find coordinates for this city."
#     except Exception as e:
#         return f"An error occurred while retrieving weather data: {str(e)}"

# # Get weather data for the weekly forecast
# async def get_weather_data_weekly(city: str):
#     try:
#         # Get coordinates for the city
#         geocoding_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}")
        
#         if geocoding_response.status_code == 200:
#             geocoding_data = geocoding_response.json()
#             lat = geocoding_data["coord"]["lat"]
#             lon = geocoding_data["coord"]["lon"]
            
#             # Fetch weekly forecast using 'onecall' API
#             response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={WEATHER_API_KEY}&units=metric")
            
#             if response.status_code == 200:
#                 data = response.json()
#                 weather_info = "Weekly forecast:\n"
#                 for day in data["daily"][:7]:  # Limit to 7 days
#                     date = day["dt"]  # Unix timestamp
#                     temp_day = day["temp"]["day"]  # Day temperature
#                     temp_night = day["temp"]["night"]  # Night temperature
#                     description = day["weather"][0]["description"].capitalize()
#                     humidity = day["humidity"]
                    
#                     # Convert Unix timestamp to readable date
#                     readable_date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
                    
#                     weather_info += (
#                         f"📅 Date: {readable_date}\n"
#                         f"🌡 Day Temp: {temp_day}°C\n"
#                         f"🌙 Night Temp: {temp_night}°C\n"
#                         f"☁️ Description: {description}\n"
#                         f"💧 Humidity: {humidity}%\n\n"
#                     )
#                 return weather_info
#             else:
#                 return "Failed to get weekly weather forecast. Please try again!"
#         else:
#             return "Failed to find coordinates for this city. Please check the city name."
#     except Exception as e:
#         return f"An error occurred while retrieving weather data: {str(e)}"

# class Form(StatesGroup):
#     city = State()  # First step: getting the city
#     period = State()  # Second step: getting the period
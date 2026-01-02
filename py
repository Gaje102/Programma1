import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from aiogram import Bot, Dispatcher, F, types
from pydantic import BaseModel

app = FastAPI()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
templates = Jinja2Templates(directory="templates")

class UserData(BaseModel):
    user_id: int

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create-invoice")
async def create_invoice(data: UserData):
    link = await bot.create_invoice_link(
        title="Прокрут колеса",
        description="1 попытка в Колесе Фортуны",
        payload=f"spin_{data.user_id}",
        provider_token="", # Пусто для Звезд
        currency="XTR",
        prices=[types.LabeledPrice(label="Stars", amount=50)]
    )
    return {"link": link}

@dp.pre_checkout_query()
async def checkout(query: types.PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def got_payment(message: types.Message):
    await message.answer("Оплата прошла! Удачи в игре!")

# Для запуска на хостинге
if __name__ == "__main__":
    import uvicorn
    import asyncio
    async def main():
        await dp.start_polling(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    uvicorn.run(app, host="0.0.0.0", port=8000)

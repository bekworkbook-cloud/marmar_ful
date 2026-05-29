import os
from aiogram.types import LabeledPrice

from src.config import bots, settings



BOT_FOR_CUSTOMER = bots.bots["customer_bot"]

# Токены, полученные в BotFather для каждого провайдера
PROVIDER_TOKENS = {
    "click": settings.CLICK_TEST_TOKEN,
    "payme": settings.PAYCOM_TEST_TOKEN
}

async def send_payment_invoice(chat_id: int, provider: str, price: int, payload: str):
    """
    Отправляет инвойс на оплату в указанный чат.
    
    :param bot: Экземпляр бота
    :param chat_id: Telegram ID пользователя
    :param provider: Название провайдера ('click' или 'payme')
    :param price: Цена в сумах (UZS)
    :param payload: Уникальная строка (например, ID заказа), которая вернется после оплаты
    """
    provider_token = PROVIDER_TOKENS.get(provider.lower())
    
    if not provider_token:
        raise ValueError(f"Неизвестный провайдер: {provider}. Доступные варианты: click, payme")

    # Telegram ожидает сумму в минимальных единицах (1 UZS = 100 тийинов)
    amount_in_tiyins = price * 100
    
    # Формируем список цен (можно добавить несколько пунктов: товар, доставка, налоги)
    prices = [
        LabeledPrice(label=f"Оплата заказа через {provider.capitalize()}", amount=amount_in_tiyins)
    ]

    await BOT_FOR_CUSTOMER.send_invoice(
        chat_id=chat_id,
        title="Оплата заказа",
        description="Пожалуйста, завершите оплату для подтверждения заказа.",
        payload=payload,  # Внутренний ID для связи транзакции с заказом в БД
        provider_token=provider_token,
        currency="UZS",
        prices=prices,
        # need_name=True,         # Раскомментируйте, если нужно запросить имя
        # need_phone_number=True, # Раскомментируйте, если нужен телефон
    )
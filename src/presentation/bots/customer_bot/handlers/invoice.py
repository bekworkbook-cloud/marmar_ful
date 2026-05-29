from aiogram import Router, F, Bot
from aiogram.types import PreCheckoutQuery, Message

from src.infrastructure.database.models.base import async_session_maker
from src.infrastructure.database.dao.order_dao import OrderDAO
from src.core.domain.enums.order_status import OrderStatus
from src.core.domain.interfaces.order_repo import OrderRepository
from src.infrastructure.database.repositories.order_repo_impl import OrderRepositoryImpl

from ..keyboards.inline import InlineKb as ikb



router = Router()

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    # Безопасно парсим payload
    try:
        order_id = int(pre_checkout_query.invoice_payload.split(":")[1])
    except (IndexError, ValueError):
        return await bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id,
            ok=False,
            error_message="Ошибка: неверный формат данных заказа."
        )

    # Обязательно используем async with для управления жизненным циклом сессии
    async with async_session_maker() as session:
        order_dao = OrderDAO(session)
        order_repo = OrderRepositoryImpl(order_dao)
        order = await order_repo.get_by_id(order_id)

        # 1. Сначала проверяем, найден ли заказ
        if not order:
            return await bot.answer_pre_checkout_query(
                pre_checkout_query_id=pre_checkout_query.id,
                ok=False,
                error_message="К сожалению, заказ не найден в системе."
            )
        print(type(order.status))
        # 2. Проверяем статус (нельзя оплатить уже отмененный или уже оплаченный заказ)
        if order.status != OrderStatus.PENDING.value:
            return await bot.answer_pre_checkout_query(
                pre_checkout_query_id=pre_checkout_query.id,
                ok=False,
                error_message="Этот заказ уже оплачен или более неактуален."
            )

        # Если все хорошо, даем добро Telegram на списание средств
        await bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id,
            ok=True
        )


@router.message(F.successful_payment)
async def process_successful_payment(message: Message, bot: Bot):
    order_dao = OrderDAO(async_session_maker())
    order_repo = OrderRepositoryImpl(order_dao)
    payment_info = message.successful_payment
    order_id = int(payment_info.invoice_payload.split(":")[1])

    async with async_session_maker() as session:
        order_dao = OrderDAO(session)
        order = await order_repo.get_by_id(order_id)

        if order:
            # Вот теперь можно смело менять статус на ожидание оператора!
            order.status = OrderStatus.AWAITING_CONFIRMATION.value
            await order_repo.update(order)
            
            # Здесь же можно отправить сообщение оператору или в группу ресторана:
            # await bot.send_message(OPERATOR_CHAT_ID, f"Новый заказ №{order_id} оплачен и ждет подтверждения!")

    await message.answer(
        f"Спасибо! Оплата на сумму {payment_info.total_amount // 100} {payment_info.currency} прошла успешно.\n"
        "Оператор скоро свяжется с вами или подтвердит заказ.",
        reply_markup=ikb.get_mini_app_kb()
    )
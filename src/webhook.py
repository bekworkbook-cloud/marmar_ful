from fastapi import APIRouter, Request, HTTPException
from aiogram.types import Update
import logging

from src.config import bots

webhook_router = APIRouter()

@webhook_router.post("/webhook/{bot_id}")
async def webhook(bot_id: str, request: Request):
    logging.info(f"[{bot_id}] Received webhook request")
    
    if bot_id not in bots.bots:
        logging.error(f"[{bot_id}] Bot not found in configuration")
        raise HTTPException(status_code=404, detail="Bot not found")
    
    try:
        update_data = await request.json()
        bot = bots.bots[bot_id]
        dp = bots.dispatchers[bot_id]
        
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        logging.info(f"[{bot_id}] Update processed successfully")
    except Exception as e:
        logging.error(f"[{bot_id}] Critical error processing update: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"ok": True}
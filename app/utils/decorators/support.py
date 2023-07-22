import asyncio


import schedule as schedule

from app.aiogram.handlers import update_ticket_status


async def update_all_tickets_loop():
    while True:
        await asyncio.sleep(15 * 60)
        await update_ticket_status()

schedule.every(15).minutes.do(update_ticket_status)


async def usedesk():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

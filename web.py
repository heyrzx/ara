from aiohttp import web, ClientSession
import asyncio
import os
from bot import main as start_bot

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()

    # Get the PORT from environment (default to 8080)
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

async def keep_alive():
    await asyncio.sleep(10)  # Wait for server to start
    while True:
        try:
            async with ClientSession() as session:
                async with session.get("http://localhost:8080") as resp:
                    print(f"Keep-alive ping: {resp.status}")
        except Exception as e:
            print(f"Keep-alive error: {e}")
        await asyncio.sleep(300)  # Wait 5 minutes between pings

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_web_server())
    loop.create_task(start_bot())
    loop.create_task(keep_alive())
    loop.run_forever()

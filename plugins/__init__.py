#@iryme
from aiohttp import web
from .route import routes

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def main():
    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

if __name__ == '__main__':
    asyncio.run(main())

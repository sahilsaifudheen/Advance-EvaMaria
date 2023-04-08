from aiohttp import web

async def root_route_handler(request):
    return web.json_response("GreyMatter_Bots")

app = web.Application()
app.add_routes([
    web.get("/", root_route_handler, allow_head=True),
])

if __name__ == "__main__":
    web.run_app(app)

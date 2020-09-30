from aiohttp import web

import socketio
from application.router.Router import Router
from application.Socket.Socket import Socket

app = web.Application()
sio = socketio.AsyncServer()
sio.attach(app)


Router(app, web)
Socket(sio)

# def ttestHandler(request):
#     return web.json_response(dict(result='ok'))
#
# def powHandler(request):
#     value = request.match_info.get('value')
#     pow = request.match_info.get('pow')
#     name = request.rel_url.query['name']
#     result = float(value) * float(pow)
#     return web.json_response(dict(result=result, name=name))
#
# def staticHandler(request):
#     return web.FileResponse('./public/index.html')
#
# app.router.add_route('GET', '/test', ttestHandler)
# app.router.add_route('GET', '/pow/{value}/{pow}', powHandler)
# app.router.add_route('*', '/', staticHandler)

async def on_startup(app):
    print('Я родился!')
async def on_shutdown(app):
    print('Я помер!')
async def on_cleanup(app):
    print('Я совсем помер!')

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.on_cleanup.append(on_cleanup)

web.run_app(app)
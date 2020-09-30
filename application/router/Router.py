class Router:
    def __init__(self, app, web):
        # self.app = app
        self.web = web
        app.router.add_static('/js/', path=str('./public/js/'))
        app.router.add_static('/css/', path=str('./public/css/'))
        app.router.add_route('GET', '/test', self.ttestHandler)
        app.router.add_route('GET', '/pow/{value}/{pow}', self.powHandler)
        app.router.add_route('*', '/', self.staticHandler)

    def ttestHandler(self, request):
        return self.web.json_response(dict(result='ok'))

    def powHandler(self, request):
        value = request.match_info.get('value')
        pow = request.match_info.get('pow')
        name = request.rel_url.query['name']
        result = float(value) * float(pow)
        return self.web.json_response(dict(result=result, name=name))

    def staticHandler(self, request):
        return self.web.FileResponse('./public/index.html')


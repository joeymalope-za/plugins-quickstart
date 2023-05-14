import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
_TODOS = {}

@app.post("/todos/<string:username>")
async def add_todo(username):
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    return quart.Response(response='OK', status=200)

@app.get("/todos/<string:username>")
async def get_todos(username):
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)

@app.delete("/todos/<string:username>")
async def delete_todo(username):
    request = await quart.request.get_json(force=True)
    todo_idx = request["todo_idx"]
    # fail silently, it's a simple plugin
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)

@app.get("/todos/getCartItems/<string:username>")
async def get_cart_items(username):
    return quart.Response(response=json.dumps(_TODOS.get(username, [
        {
            "id": 4809281732672,
            "title": "South Park Towelie Ugly Holiday Sweater",
            "price": "64.95",
            "currency_code": "USD",
            "description": null,
            "url": "https://www.southparkshop.com/products/south-park-towelie-ugly-holiday-sweater"
        },
        {
            "id": 6566410944564,
            "title": "South Park Towelie Ugly Holiday Sweater",
            "price": "51.95",
            "currency_code": "GBP",
            "description": null,
            "url": "https://southparkshop.co.uk/products/south-park"
        },
        {
            "id": 6632357953600,
            "title": "South Park 2 For 1 Hugs Crewneck Sweatshirt",
            "price": "36.95",
            "currency_code": "USD",
            "description": null,
            "url": "https://www.southparkshop.com/products/south-park-2-for-1-hugs-crewneck-sweatshirt"
        },
        {
            "id": 4377994330176,
            "title": "South Park Cartman Bad Kitty Fleece Hooded Sweatshirt",
            "price": "39.95",
            "currency_code": "USD",
            "description": null,
            "url": "https://www.southparkshop.com/products/south-park-cartman-bad-kitty-fleece-hooded-sweatshirt"
        },
        {
            "id": 4813556547648,
            "title": "South Park Merry Christmas Holiday Fleece Crewneck Sweatshirt",
            "price": "36.95",
            "currency_code": "USD",
            "description": null,
            "url": "https://www.southparkshop.com/products/south-park-merry-christmas-holiday-fleece-crewneck-sweatshirt"
        },
    ])), status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()

import os

from app import create_app

from dotenv import load_dotenv
if not os.environ.get('FLASK_CONFIG'):
    load_dotenv('.env')

app = create_app(os.environ.get('FLASK_CONFIG'))

@app.route("/test")
def test():
    return "<h1>szhu9903</h1>"

@app.route('/wstest/')
def test_wsmsg():
    with open('./static/test.html') as f1:
        html_str = f1.read()
    return html_str

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer
    from geventwebsocket.handler import WebSocketHandler
    server = WSGIServer(('0.0.0.0', 8890), app, handler_class=WebSocketHandler)
    server.serve_forever()
    # app.run(host='0.0.0.0', port=8006)
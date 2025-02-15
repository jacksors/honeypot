import datetime
import random
import threading

from flask import Flask, request

def start_flask_honeypot(port: int):
    app = Flask(__name__ + str(port))

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(**kwargs):
        request_info = {
            "src_ip": request.remote_addr,
            "path": request.path,
            "query": request.args,
            "data": request.data,
            "time": datetime.datetime.now().isoformat()
        }
        print(request_info)

        return {"status": random.randint(-1024, 1024)}

    app.run("0.0.0.0", port)

if __name__ == "__main__":
    ports = [80, 3000, 5000, 8080]
    threads = []
    for port in ports:
        thread = threading.Thread(target=start_flask_honeypot, args=[port])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

import datetime
import random
from multiprocessing import Process
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

    app.run("0.0.0.0", port, debug=True)

if __name__ == "__main__":
    ports = [80, 3000, 5000, 8080]
    processes = []
    for port in ports:
        process = Process(target=start_flask_honeypot, args=[port])
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

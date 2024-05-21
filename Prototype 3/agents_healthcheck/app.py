from flask import Flask, request
from main import hello_http  # Import your cloud function

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    return hello_http(request)


if __name__ == "__main__":
    # Set up your local server with increased header size limits
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)
    app.run(host="0.0.0.0", port=8080, threaded=True)

from flask import Flask, jsonify, request
from requests import get as http_get
from translatepy import Translator

app = Flask(__name__)
CORS(app)


class Quote:
    def __init__(self) -> None:
        self.translator = Translator()
        self.url = "https://api.quotable.io/random"
        self.lang = "Ukrainian"

    def request(self) -> dict:
        return http_get(self.url).json()

    def translate(self, text) -> str:
        return self.translator.translate(text, self.lang)

    def translated(self) -> dict:
        data = self.request()
        return {
            "content": self.translate(data["content"]),
            "author": self.translate(data["author"])
        }

    def __str__(self) -> str:
        quote = self.translated()
        return "%s\n― %s" % (quote["content"], quote["author"])
      
      
@app.route("/")
def get() -> jsonify:
    try:
        data = Quote().translated()
        return jsonify({"success": len(data["content"]) != 0, "data": data})
    except Exception as e:
        return jsonify({"success": False, "exception": type(e).__name__})


if __name__ == "__main__":
    socketio.run(app)

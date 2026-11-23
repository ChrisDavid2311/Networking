from bottle import Bottle, request, static_file, run
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from html import escape

app = Bottle()

TALKBACK_ID = ""
TALKBACK_KEY = ""


@app.get("/")
def home():
    return static_file("index.html", root="/home/chrisrpi")


@app.post("/send")
def send_command():
    command = request.forms.get("command", "").strip().upper()

    if command not in ("ON", "OFF"):
        return "Only ON and OFF commands are allowed."

    url = (
        f"https://api.thingspeak.com/talkbacks/{TALKBACK_ID}/commands.json"
    )
    body = urlencode({
        "api_key": TALKBACK_KEY,
        "command_string": command
    }).encode("utf-8")

    try:
        req = Request(url, data=body, method="POST")
        with urlopen(req, timeout=15) as reply:
            result = reply.read().decode("utf-8")
        return f"Queued command: {escape(command)}<br><a href='/'>Back</a>"
    except Exception as error:
        return f"Could not queue command: {escape(str(error))}<br><a href='/'>Back</a>"


run(app, host="127.0.0.1", port=8080)

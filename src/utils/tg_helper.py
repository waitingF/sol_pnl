import json
import requests


def send_tg_msg(msg: str):
    tg_bot_token = "7542725303:AAFLrVVw6qNi-j_M7GS2hznYbTBSm2gdvUk"
    url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
    data = {
        "chat_id": -4652041330,
        "text": msg,
        "parse_mode": "HTML",
    }

    requests.post(url, json=data)


if __name__ == "__main__":
    send_tg_msg("test")




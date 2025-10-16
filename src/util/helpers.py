import requests

def get_user_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "unknown"

import requests
from datetime import *
import smtplib
import time

HYD_LAT = 17.385044
HYD_LONG = 78.486671
LOCAL_UTC_OFFSET = 5.30
sender_mail = "senders_mail@gmail.com"
sender_password = "app_password"
receiver_mail = "receivers_mail#gmai.com"


def check_visibility_of_iss():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_latitude = float(iss_response.json()["iss_position"]["latitude"])
    iss_longitude = float(iss_response.json()["iss_position"]["longitude"])

    if (iss_latitude - 5 <= HYD_LAT <= iss_latitude + 5) and (iss_longitude - 5 <= HYD_LONG <= iss_longitude + 5):
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": HYD_LAT,
        "lng": HYD_LONG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", parameters)
    response.raise_for_status()
    current_time = datetime.now(timezone.utc).hour  # To convert IST into UTC

    sunrise = response.json()["results"]["sunrise"]
    sunset = response.json()["results"]["sunset"]
    sunrise = int(sunrise.split("T")[1].split(":")[0])
    sunset = int(sunset.split("T")[1].split(":")[0])

    if current_time <= sunrise or current_time >= sunset:
        return True
    else:
        return False


while True:
    time.sleep(60)
    if check_visibility_of_iss() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=sender_mail, password=sender_password)
            connection.sendmail(from_addr=sender_mail, to_addrs=receiver_mail, msg="Look Above and Spot the ISS")
            print("MAIL SENT")

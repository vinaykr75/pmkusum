import requests
import asyncio
import time
from telegram import Bot

# Telegram Bot credentials
TELEGRAM_TOKEN = "1914965034:AAHlwihnpmHYItKNSXlFGCYHQqhGsAs67EU"
TELEGRAM_CHAT_ID = "-1002324009273"

# API URL
API_URL = "https://pmkapi.jharkhand.gov.in/api/JH/Compb_Consumer_Preregs/GetDistrictWiseQuota?sanction_id=0&District=323&PROJCD=null&%22%22"

# Initialize previous RegQuota value
previous_regquota_value = 0

# Function to fetch API data
def fetch_api_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()  # Return JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")
        return None

# Asynchronous function to notify via Telegram
async def notify_telegram(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Asynchronous function to check for updates to RegQuota
async def check_regquota_changes():
    global previous_regquota_value
    data = fetch_api_data()
    if data is None:
        return

    # Extract the 'Data' array
    result_array = data.get("Data")
    if not isinstance(result_array, list):
        print("The 'Data' field is not an array.")
        return

    # Check the first item's 'RegQuota' value
    reg_quota_value = result_array[0].get("Remaining_RegQuota", 0)

    # Compare with the previous value
    if reg_quota_value != previous_regquota_value and reg_quota_value > 0:
        previous_regquota_value = reg_quota_value
        await notify_telegram(f"'RegQuota' data has changed! New value: {reg_quota_value}")
        print("'RegQuota' data has changed, notification sent.")
    else:
        print("No changes detected in 'RegQuota' data.")

# Main asynchronous loop
async def main():
    print("Bot is running...")
    while True:
        await check_regquota_changes()
        await asyncio.sleep(60)  # Check every 60 seconds

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())

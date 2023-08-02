import requests
import time
import json

class Yumikolab:
    def __init__(self, api_id, api_hash, token, session=None, phone_number=None):
        """
        Initialize the Yumikolab.

        Parameters:
            - api_id (int): The API ID obtained from the Telegram website.
            - api_hash (str): The API hash obtained from the Telegram website.
            - token (str): The bot token obtained from BotFather on Telegram.
            - session (str, optional): The session file path. If not provided, a default value will be used.
            - phone_number (str, optional): The phone number associated with the bot. (Not used in this implementation)
        """
        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token
        self.session = session
        self.phone_number = phone_number

        if self.session is None:
            self.session = f"{self.token}.session"

        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def yumikostart(self):
        """
        Start the bot and continuously poll for updates.

        This method will keep polling the Telegram API for updates and call the _handle_update method
        for each received update.
        """
        self._start_polling()

    def _start_polling(self):
        """
        Internal method to continuously poll for updates and handle them.
        """
        offset = 0

        while True:
            try:
                updates = self._get_updates(offset)
                for update in updates:
                    self._handle_update(update)
                    offset = update["update_id"] + 1
            except Exception as e:
                print("Error occurred:", e)
                time.sleep(5)

    def _get_updates(self, offset):
        """
        Internal method to fetch updates from Telegram API.

        Parameters:
            - offset (int): The offset value to fetch new updates.

        Returns:
            - list: A list of updates received from the Telegram API.
        """
        response = requests.get(self.base_url + "getUpdates", params={"offset": offset})
        data = response.json()
        if data["ok"]:
            return data["result"]
        else:
            raise ValueError("Failed to fetch updates.")

    def _handle_update(self, update):
        """
        Internal method to handle incoming updates.

        Parameters:
            - update (dict): The update received from Telegram API.
        """
        if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message["text"]
            self.send_message(chat_id, f"You said: {text}")

    def send_message(self, chat_id, text):
        """
        Send a message to a chat.

        Parameters:
            - chat_id (int): The ID of the chat to send the message to.
            - text (str): The text of the message to be sent.
        """
        data = {
            "chat_id": chat_id,
            "text": text,
        }
        response = requests.post(self.base_url + "sendMessage", data=data)
        if not response.json()["ok"]:
            raise ValueError("Failed to send message.")

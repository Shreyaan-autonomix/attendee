from bots.google_meet_bot_adapter.google_meet_ui_methods import (
    GoogleMeetUIMethods,
)
from bots.web_bot_adapter import WebBotAdapter


class GoogleMeetBotAdapter(WebBotAdapter, GoogleMeetUIMethods):
    def get_chromedriver_payload_file_name(self):
        return "google_meet_bot_adapter/google_meet_chromedriver_payload.js"

    def get_websocket_port(self):
        return 8765

    def get_first_buffer_timestamp_ms(self):
        return self.media_sending_enable_timestamp_ms

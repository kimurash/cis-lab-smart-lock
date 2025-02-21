import os

from dotenv import load_dotenv
from slack_sdk import WebhookClient

from reader import FeliCaReader


if __name__ == '__main__':
    try:
        reader = FeliCaReader()
        reader.read()
    except Exception as e:
        load_dotenv()
        SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

        client = WebhookClient(SLACK_WEBHOOK_URL)
        response = client.send(
            text="スマートロックが停止しました",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"```{e}```"
                    }
                }
            ]
        )

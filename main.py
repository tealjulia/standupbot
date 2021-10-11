import os
import time
import logging
import random
import schedule
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def shuffle_users(slack_client):

  try:
    user_list = slack_client.users_list(
      channel='#general'
    )

  except SlackApiError as err:
    logging.error('Request to Slack API Failed: {}.'.format(err.response.status_code))
    logging.error(err.response)

  random.shuffle(user_list["members"])
  chat_message = ""

  for user in user_list["members"]:
      chat_message += f'{user["real_name"]} \n'

  return chat_message


def send_message(slack_client):

  chat_message = shuffle_users(slack_client)

  try:
    slack_client.chat_postMessage(
      channel='#test',
      text=chat_message
    )
  except SlackApiError as err:
    logging.error('Request to Slack API Failed: {}.'.format(err.response.status_code))
    logging.error(err.response)

if __name__ == "__main__":

  SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
  slack_client = WebClient(SLACK_BOT_TOKEN)

  schedule.every().monday.at("09:28").do(lambda: send_message(slack_client))
  schedule.every().tuesday.at("08:58").do(lambda: send_message(slack_client))
  schedule.every().wednesday.at("08:58").do(lambda: send_message(slack_client))
  schedule.every().thursday.at("08:58").do(lambda: send_message(slack_client))
  schedule.every().friday.at("08:58").do(lambda: send_message(slack_client))


  while True:
    schedule.run_pending()
    time.sleep(1)
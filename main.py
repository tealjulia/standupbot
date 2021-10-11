import os
import time
import logging
import random
import schedule
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.shuffle_user('cron', day_of_week='mon-fri', hour=9)


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

sched.start()
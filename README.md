# Schedule Telegram Bot

It's a telegram bot designed to generate work schedules. The bot is designed to work in chats (groups) where there are several people. It can also be used by one person. 

## Preparing participants

To add members to the schedule, in the file Cleaning.json (in the Schedules folder), in the column "members" you need to write the names of all the participants of the schedule in double quotation marks. Below, in the column "id_members" in the same way, you should write the id of participants' Telegram accounts. 

## Customizing the code

In the variable "TOKEN" you should enter the token of your bot. The bot token can be obtained from the official Telegram bot "https://t.me/BotFather" when creating a new bot. After that, in the variable "admin" it is necessary to enter the ID of admin account, because some commands will be possible to run only by admin. ID must be entered as a numeric value (int), not as a string.

## List of bot commands

### /generate - generate a new cleaning schedule
### /show - show current cleaning schedule
### /done - mark your cleaning date as done.

## P.S.
So far, there is only one schedule template, from which a new work schedule appears, which contains the cleaning dates (on Sundays) of all participants entered in the Cleaning.json file. There are plans to expand the capabilities of the bot in the future

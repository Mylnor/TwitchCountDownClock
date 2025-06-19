# Twitch Countdown clock
Allows you to add time to a visual clock you can add to your stream

There are three settings files for you; settings.json, time.json and _twitch.json
Settings.json contain some visualisation options to change the colors of your clock and restricts the users it listens to
Time.json has the time left on the clock, this gets edited by the app every second
Twitch.json contains the appid and secret to let the app listen to chat commands

# Installation
1. Rename _twitch.json to twitch.json
2. get your appid and secret from https://dev.twitch.tv/console
	a. call it something like kaicountdownclock or something
	b. OAuth url should point to https://localhost:17563/
	c. Category is chatbot
	d. make the Clienttype confidential
	e. copy and paste the appid and appsecret into the twitch.json file
3. edit the settings.json to your liking and matching your stream theme/design, dont forget to set your user(s).
4. open time.json and set the amount of time (it will edit it every second so dont touch after while running)
5. run the file to start the bot and it will start a browser tab to connect to twitch
6. all the commands available to you are via chat (they are limited to those you allow in the settings)
	a. !clockadd60,30,15 and 5
	b. !clockbonustime (will set it based on the current Boolean)

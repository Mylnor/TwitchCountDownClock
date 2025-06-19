# TwitchCountDownClock
Allows you to add time to a visual clock you are add to your stream

There are three settings files for you; settings.json, time.json and twitch.json
Ive separated them because then you can show your settings.json on stream and leave the sensitive appid and appsecret in the other file for no one to see :)

1. get your appid and secret from https://dev.twitch.tv/console
	a. call it something like kaicountdownclock or something
	b. OAuth url should point to https://localhost:17563/
	c. Category is chatbot
	d. make the Clienttype confidential
	e. copy and paste the appid and appsecret into the twitch.json file
2. edit the settings.json to your liking and matching your stream theme/design
3. open time.json and set the amount of time (it will edit it every second so dont touch after while running)
4. run the file to start the bot and it will start a browser tab to connect to twitch
5. all the commands available to you are via chat (they are limited to those you allow in the settings)
	a. !clockadd60,30,15 and 5
	b. !clockbonustime (will set it based on the current Boolean)

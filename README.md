# DAPNET Discord Bot

Python based Discord bot to send pages to the Decentralized Amateur Paging Network (DAPNET). 

---

# Description

The Decentralized Amateur Paging Network or DAPNET, is a paging network maintained by Amateur Radio Operators for Amateur Radio Operators. Remember the old Skytel pagers, the old Motorola text pagers and others? This network brings that ability back for the use of Amateur Radio Opertors (Hams). This network was first developed in Germany and is slowly gaining use in the United States and can use your Pi-Star hotspot to send pages to a local pager.

This bot lives on your Discord Server and allows Ham Operators to send a page to other users of the DAPNET Network. If this is in a Family server, make sure that only the licensed ham that is setup for the bot is able to use it (See the setup instructions below). Note that you need to have a DAPNET Username and Password in order to use this software. This will not send unless the Discord User has registered their DAPNET Credentials with the bot.

This software is solely for the use of Amatuer Radio Operators only.

---

## API's Used

This bot sends data to the following locations:

| Service | Description | Website |
|---------|---------|---------|
|hampager.de|Used to send the page to DAPNET users. Only sends the data needed to send a page.|[https://hampager.de](https://hampager.de)|

---
# Installation and Setup

### Installation Steps
1) Obtain Discord Keys
2) Install needed packages, clone Repo and install library dependencies
3) Configure the script

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi. (Mine is running on a Raspberry Pi 4 2 GB model with many other bots and scripts running with no issues.)

If you want to run this on a Windows or Mac machine, you will need to install Python3 and be familiar installing from a requirements.txt.

### Obtaining Discord Keys

The first step in this process will be obtaining the Discord keys that you need. 

##### Add Bot to your Discord Server and obtain Server ID

* Go to: [https://discord.com/developers/applications](https://discord.com/developers/applications)
* Click ```New Application```
* Give it a name (I called it DAPNET)
* On the next screen, you can upload an avatar for the bot.
* Click the ```bot``` selection under settings
* Click ```Add Bot```
* Give it a Name (I used the same name )
* Then Copy the Bot Token (you will need this for the config.py part of the script)
* Turn off ```Public Bot```
* Make sure to turn on the ```Message Intents``` Setting under ```Privileged Gateway Intents```.
* Save Settings
* Click ```OAuth2``` and then ```URL Generator```
* For Scope Choose ```bot``` and ```appplications.commands```
* For Permissions, choose the following:
    - Under General Permissions:
        - Read Messages/View Channels
    - Under Text Permissions:
        - Send messages
        - Send Messages in threads
        - Embed Links
        - Attach Files
        - Read message History
        - Use Slash Commands
* Copy the generated URL
* Paste it into a browser window Address bar
* Choose the Server you want to authorize it to and then click authorize.
* It should pop into the server.
* Next you will need to get your server id.
  * To get this, you will need to, on Discord, go into ```User Settings```->```Advanced``` and turn on ```Developer Mode``` (if it is not already on.)
  * Then just right click on your server's icon and click ```Copy ID```. Then go back into your ```config.py``` and paste that ID in the ```discord_server_id``` field.

Once you have these keys you need and the bot authorized into your server, you will eventually copy them into the appropriate places in the config.py file, but now we need to get the files and get things installed.

---

### Installing the Script

The next step is installing the needed packages, cloning the repo to get the script and then installing the needed libraries for the script to work properly.

This is probably the easiest step to accomplish.

Please run the following commands:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

git clone https://github.com/n8acl/dapnet_discord_bot.git

cd dapnet_discord_bot

pip3 install -r requirements.txt
```

Now you have everything installed and are ready to configure the script.

## Configure the Script
Once you have your Discord Keys, have cloned the repo and installed everything, you can now start configuring the bot. Open the config.py file in your editor of choice and copy in the keys you obtained from Discord into the appropriate spots.

## Running the Script

Once you have the config file edited, start the bot by typing the following:

```bash
screen -R dapnet_discord_bot
```

Then in the new window:
```bash
cd dapnet_discord_bot

python3 dapnet_bot.py
```

Once that is done, hit CTRL-A-D to disconnect from the screen session. If something ever happens, you can reconnect to the session by typing:

```bash
screen -R dapnet_discord_bot
```

And see why it errored or quit and restart. This is useful if you need to contact me for support.

---

# Bot Commands

All Commands can be issued from any text channel.

In order to use the bot, you will need to register your DAPNET Username and Password with the bot. This will tie your Discord User ID to those credentials and when that user ID sends a messge to DAPNET, this will user the registered credentails. If you do not register your DAPNET User ID and Password with the bot, it will not send any messages.

Know that when you "Register" with the bot, those credentials are stored in a database local to the bot, you are not registering your credentials with me, the developer. I cannot get access to those.

In order to register your credentials with the bot, use the /register command as listed below.

| Command | Description |
|---------|-------------|
|/send < callsign >< msg >|This sends a message to a DAPNET User. This command accepts 2 parameters<br><br>- callsign - This is the callsign of the person you are tring to reach<br>- msg - This is the text of the message you want to send. The text can only be 80 characters long.|
|/register < username >< password > | This commands registers a user to the bot. This is needed for a Discord User to be able to send a message. If the Discord User is not registered to the bot, that user will not be able to send a DAPNET Message. This commands does NOT create a DAPNET Account. The User will need to do that. This command requires 2 parameters: <br><br>- username - This is the DAPNET Username of the Discord User trying to register to the bot. This is usually the callsign of the user. NOTE: THIS IS NOT YOUR DISCORD USERNAME.<br>- password - This is the DAPNET Password of the Discord User trying to register to the bot. NOTE: THIS IS NOT YOUR DISCORD PASSWORD.|
|/help|Brings up help text with the above command list.|

---
## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Discord: Ravendos#7364
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net
- DAPNET: n8acl

Or open an issue on Github. I will respond to it, and of course you, when I can. 

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log
* 05/30/2022 - Version 05302022 - Initial Release
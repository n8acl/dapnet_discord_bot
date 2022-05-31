#################################################################################

# DAPNET Discord Bot
# Developed by: Jeff Lehman, N8ACL
# Current Version: 05302022
# https://github.com/n8acl/dapnet_discord_bot

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Twitter: @n8acl
# Discord: Ravendos#7364
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl
# DAPNET: n8acl (since this is a DAPNET Bot)

###################   DO NOT CHANGE BELOW   #########################

#############################
##### Import Libraries
import config as cfg
import os
import json
import requests
from requests.auth import HTTPBasicAuth
import http.client, urllib
import discord
import sqlite3

#############################
##### Define Variables
linefeed = "\r\n"
dapnet_url = 'http://www.hampager.de:8080/calls'
db_file = os.path.dirname(os.path.abspath(__file__)) + "/dapnet.db"

#############################
# Create Discord Bot
TOKEN = cfg.discord_bot_token
bot = discord.Bot(debug_guilds=[cfg.discord_server_id])

#############################
##### Define Functions

def create_connection(db_file):
    # Creates connection to APRSNotify.db SQLlite3 Database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def exec_sql(conn,sql):
    # Executes SQL for Updates, inserts and deletes
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def select_sql(conn,sql):
    # Executes SQL for Selects
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def new(conn):

   create_config_table = """ create table if not exists config (
      discord_userid varchar(50),
      dapnet_username varchar(50),
      dapnet_password varchar(50)
); """

   exec_sql(conn, create_config_table)

   conn.close()

def register_user(db_file, userid, username, password):
    conn = create_connection(db_file)

    results = select_sql(conn, "select count(dapnet_username) from config where discord_userid = '" + userid + "';")

    for row in results:
        usercnt = int(row[0])

    if usercnt == 0:
        sql = "insert into config (discord_userid, dapnet_username, dapnet_password) "
        sql = sql = sql + "values ('" + userid + "','" + username + "','" + password + "');"

        exec_sql(conn,sql)
    else:
        sql = "update config set dapnet_username = '" + username + "', password = '" + password + "' where discord_userid = '" + userid + "';"

        exec_sql(conn,sql)

    conn.close()

def send_dapnet(send_to, text, username, password):
    
    data = json.dumps({"text": text, "callSignNames": [send_to], "transmitterGroupNames": [cfg.dapnet_txgroup], "emergency": False})
    response = requests.post(dapnet_url, data=data, auth=HTTPBasicAuth(username,password)) 

#############################
# Define Bot Functions

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#dapnet = bot.create_group("dapnet","Sending Dapnet Messages")

@bot.command(description="Send DAPNET Message")
async def send(ctx, callsign: discord.Option(str,"Callsign to send message to.", required=True)=None,  msg: discord.Option(str,"Messge to send to user.", required=True)=None):

    conn = create_connection(db_file)

    userid = str(ctx.author.id)


    results = select_sql(conn, "select count(dapnet_username) from config where discord_userid = '" + userid + "';")

    for row in results:
        usercnt = int(row[0])

    if usercnt == 0:
        title = "User Not Registered"
        description = 'You are not registered to use the DAPNET Bot. Please register to the bot first using /register.'

    else:
        user = select_sql(conn, "select dapnet_username, dapnet_password from config where discord_userid = '" + userid + "';")

        for row in user:
            username = row[0].upper()
            password = row[1]
        
        text = username + ': ' + str(msg)

        if len(text) <= 80:

            send_dapnet(callsign,text, username, password)

            title = "Sending DAPNET Message to " + callsign.upper()
            description = 'Message Text: ' + linefeed + text

        else:
            title = "DAPNET Error Message"
            description = 'Message Length too long. Message length can only be 80 Characters. You are ' + str(len(text)-80) + ' characters over.'

    embed = discord.Embed(title = title,
        description=description,
    )

    conn.close()

    await ctx.respond(embed = embed,ephemeral=True)

@bot.command(description="Register to use bot")
async def register(ctx, username: discord.Option(str,"DAPNET Username to Register.", required=True)=None, password: discord.Option(str,"DAPNET Password to Register.", required=True)=None):

    userid = str(ctx.author.id)

    register_user(db_file,userid, str(username), str(password))

    title = 'Registered New User to Bot'
    description = 'Following DAPNET User has been Registered to the Bot: ' + linefeed
    description = description + 'Username: ' + str(username) + linefeed
    description = description + 'Password: ' + str(password)

    embed = discord.Embed(title = title,
        description=description,
    )

    await ctx.respond(embed = embed,ephemeral=True)

#dapnet.command()
@bot.command(description="DAPNET Bot Help")
async def help(ctx):
    description = """
    This bot is very simple. 

    Commands:
    
    /send - This sends a message to a DAPNET User. This command accepts 2 parameters
        - callsign - This is the callsign of the person you are tring to reach
        - msg - This is the text of the message you want to send. The text can only be 80 characters long.
    
    /register - This commands registers a user to the bot. This is needed for a Discord User to be able to send a message. If the Discord User is not registered to the bot, that user will not be able to send a DAPNET Message. This commands does NOT create a DAPNET Account. The User will need to do that. This command requires 2 parameters:
        - username - This is the DAPNET Username of the Discord User trying to register to the bot. This is usually the callsign of the user. NOTE: THIS IS NOT YOUR DISCORD USERNAME.
        - password - This is the DAPNET Password of the Discord User trying to register to the bot. NOTE: THIS IS NOT YOUR DISCORD PASSWORD.

    /help - This help text

    More information about me can be found at https://github.com/n8acl/dapnet-discord-bot
    """

    embed = discord.Embed(title = "DAPNET Bot Help",
            description=description,
        )

    await ctx.respond(embed = embed,ephemeral=True)
        
#############################
##### Main Program

if not os.path.exists(db_file):
   conn = create_connection(db_file)
   new(conn)

# Start Bot
bot.run(TOKEN)
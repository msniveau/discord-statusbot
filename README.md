# discord-statusbot
small python bot to monitor / query a gameserver via discord

[![Discord Bots](https://discordbots.org/api/widget/496764374338240514.svg)](https://discordbots.org/bot/496764374338240514)

[invite the hosted bot](https://discordapp.com/oauth2/authorize?client_id=496764374338240514&scope=bot&permissions=0)

# documentation
## setup via docker
for setting up your own instance you may want to follow these [instructions](https://hub.docker.com/r/msniveau/discord-statusbot) for setting up the bot via docker


## commands
| **prefix**  | **syntax**                          | **example**                                     | **description**                                                                                                              |
|-------------|-------------------------------------|-------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| !nick       | !nick {somenick}                    | !nick querybot                                  | sets the nickname of the bot                                                                                                 |
| !servers    | !servers                            | !servers                                        | print all available servers (tags)                                                                                           |
| !status     | !status {tag}                       | !status mysrv                                   | prints the current server status (@formatting: status)                                                                       |
|             | !status {tag} all                   | !status mysrv all                               | print all information about this gameserver                                                                                  |
| !print      | !print {tag}                        | !print mysrv                                    | prints the current config of "mysrv"                                                                                         |
| !monitoring | !monitoring {tag} {true/false}      | !monitoring mysrv true                          | enables / disables the monitoring of this server stauts, changes will be reported to the channel this command was executed in |
| !format     | !format {type} {status} {format}    | !format status online servername: {server_name} | further details below                                                                                                        |
| !addserver  | !addserver {tag} [game] {ip} {port} | !addserver myark arkse 123.123.213.123 27016    | add a gameserver                                                                                                             |
| !delserver  | !delserver {tag}                    | !delserver myark                                | deletes a gameserver                                                                                                         |
                                                                                                   |

## formatting
#### general information
the message formatting differs between monitoring/status and online/offline
for setting the message format for monitoring + offline (server status changes from online to offline while monitoring is enabled) you can use a command like that:

`!format monitoring offline general Oh my god, the gameserver {tag} is offline!`

this would set the general monitoring formatting to the message defined. but you can also define specific formats for some games (because it may provides more information or something like that). for that you just need to replace "general" by the game you want. for example:

`!format monitoring offline arkse Oh my god, the ark-gameserver {tag} is offline!`

#### variables
there are a few variables possible. most of them are related to the query result. for getting available variables just use the command *"!status <tag> all"* command. this should result in something like that:
```ini
server_name = my fancy gameserver
map = de_dust2
```

you can just use the key as formatting variable. for example:

`!format status online csgo The csgo named {server_name} is up and running on {map}!`

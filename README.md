
# Minecraft Server Updater `Java Edition`

This is a python package to automate the updating of your Minecraft server.<br>
It's very annoying to have to download the jar, ftp it over, stop the server, back up your world, etc.
This script automates all of that. Just copy `run.py` to the root folder of your server.
Then run `python run.py` 

## How it works:
- It will check if you have the latest version of Minecraft using Mojang's manifest URL. If your server is out of date, it will download the latest version from the official Mojang S3 bucket.
- It will then backup your world into a new folder, in case something goes wrong.
- It then updates the server jar and starts the server back up in a screen session so it's in the background.

## Please Note:
- This script only works on Windows
- This fork has not yet been fully tested, and may be buggy.
- As of now, as a side effect of a measure to ensure tileability, this script forcefully stops the server before each run, which may corrupt world files.

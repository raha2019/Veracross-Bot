# Veracross-Bot
To data strip assignments from the Austin Prep Veracross Portal
----------------------------------------------------------------
Setup:
- Run requirements.txt to install requirements
- Go to the discord developer portal and create a new bot application (if you don't know how to do that, this is a great guide): https://realpython.com/how-to-make-a-discord-bot-python/ and insert your bot token in bot.py
- Make sure the chrome driver version you are using is the same as the one installed on the machine running the program (in this repo is version 89) and keep it in this folder.


Limitations:
- Program only works for the first 100 lines of data entered due to pandas issues. However, this number can be changed in homework.py by setting the for loop
to whatever value you need.
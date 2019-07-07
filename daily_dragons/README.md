# Welcome to `Who Wants To Be A Billionaire`

In `Who Wants To Be A Billionaire` you take the role of a new 
billionaire trying to find their way around their new found wealth. 

You will have a series of opportunities to choose investments, each
decision you make will have consequences on the world around you.

For better or worse, your mission is to make as much money as you
can, but remember: wealth is useless if you no longer have a planet
afterwards.

# Setup

Executables are located in daily_dragons/production. We have provided 
.exe in production/windows and a .deb in production/linux. <br>
<br>

If neither of this work for you, or you'd prefer to run from source, 
follow the below instructions:

### With pipenv:
```
$ cd daily_dragons
$ pipenv run python main.py
```

### Without pipenv:

```
$ python3 -m pip install -r requirements.txt
$ python3 main.py
```
Please note that on your specific system the python command may be 
different.

# How to play

Upon start up you will be prompted for your name, and then presented
with various investment opportunities. Each of which will cost different
amounts, and have different effects to impact your planet's climate. The
more you invest into a certain organization, the further their policies 
will go. <br>
<br>
You can view the impact a certain investment will have on your world by
submitting the company's number. You can then choose your investment by
submitting: `invest <number>`. <br>
Once you have chosen which you want to invest in and confirm your 
selection, the round will end. Each round takes place over five years. 
You will be presented with news of the current state of the world, and 
you will then choose your investment for the next round. <br>
<br>
After ten rounds your final score will be calculated as a function of 
your net worth and how much money you managed to make. Feel free to 
access the in-game help menu at any time by submitting `help`, and good 
luck!<br>
<br>
# TL;DR
#### Commands List
`help` ==> Prints a list of in-game commands<br>
`stats` ==> Check player's stats <br>
`earth` ==> Check the planet's stats <br>
`<number>` ==> Check an investment option's effects<br>
`invest <number>` ==> Invest in `<number>` option
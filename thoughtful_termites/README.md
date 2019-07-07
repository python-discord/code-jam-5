# Savanna
> A project by Thoughtful Termites (`@mathsman`, `@meta`, `@hanyuone`)
for Code Jam 5

Welcome to Savanna, our application that helps you, the user,
to become more eco-friendly by setting environmentally green goals.

### Installation and Setup

1. Install `pipenv` and run `pipenv install` on the project.

2. Run `__main__.py` to start the control panel.

3. Configure the bot using the 'Configure Bot' button. This will require
you to set up your own Discord bot
[here](https://discordapp.com/developers/applications/). Enter in the
bot's token and client ID as prompted.

4. Configure goals and reminders using the 'Open Goals' button. More info
on this in the Usage section below.

5. Run bot using the 'Start Bot' button.


### Goals

1. Launch the goals list via the control panel and create a goal, 
with a custom description.
If you can't think of any ideas, you can press a button for the app to
suggest a goal for you.

2. You can set reminders for any environmental goal that you have by
right-clicking it and selecting "Edit Reminders". To add a reminder on a
daily basis, the 'Add Daily Reminder' button is provided for convenience.

3. You may customise your goals and reminders by selecting one or more, 
right clicking and choosing "Edit". You can also delete them by selecting 
"Delete".

4. Once you believe you have completed your goal, select "Complete Goal" 
after right-clicking it. This will accrue points used to 
unlock mini games.

5. After you have finished a certain number of goals, you can go to
the "Unlocks" window to unlock various minigames or features, accessible
on the Discord bot. This is accessible from the 'Unlock Minigames' button
at the Control Panel.

### Minigames & Features

We have a large variety of minigames and features on our Discord bot,
including:

- `>trivia`: A general trivia game that tests the user's knowledge.
- `>farmer`: A farming simulator, which you play once a day.

Some minigames are available once you finish a certain number of goals:

- `>climate_commentary` (1 goal): Offers a variety of different comments
in regards to the wide subject of climate change.
  - `>climate_commentary x`: Select a specific piece of commentary with
  an ID of `x`.
- `>rankings` (2 goals): Rank five separate countries by their
contribution to climate change.
- `>hangman` (4 goals): Guess the letters in a mystery word, but be
careful not to guess incorrectly!
  - React with the regional indicator
emoji to guess a letter.
- `>treefinder` (8 goals): Find the trees in a mystery field, but don't
accidentally remove the trees!
  - Use `guess x y` to excavate a tile on the field.
  - Use `flag x y` to flag a certain tile.

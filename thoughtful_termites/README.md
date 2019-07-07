# Savanna
> A project by Thoughtful Termites (`@mathsman`, `@meta`, `@hanyuone`)
for Code Jam 5

Welcome to Savanna, our application that allows you, the user,
to become more eco-friendly by setting environmentally green goals.

Here's how Savanna works:

1. Launch the app and create a goal, with a custom description.
If you can't think of any ideas, you can press a button for the app to
suggest a goal for you.
2. You can set reminders for any environmental goal that you have by
right-clicking it and selecting "Edit Reminders". Both weekly and daily
reminders, which are sent through our Discord bot, are available.
3. At any point in time, you may customise your goals by selecting "Edit
Goal", or delete the goal by selecting "Delete".
4. Once you have completed your goal, select "Complete" after
right-clicking.
5. After you have finished a certain number of goals, you can go to
the "Unlock" window to unlock various minigames or features, accessible
on the Discord bot.

### Minigames & Features

We have a large variety of minigames and features on our Discord bot,
including:

- `>trivia`: A general trivia game that tests the user's knowledge.
- `>farmertown`: Are you the best farmer in the town?

    Play a game of FarmerTown with the bot.
    This game is complex - read carefully!

    - You can sow a crop every 12 hours
    - You can get the results of that crop 12 hours later
    - Each crop has differing levels of drought risk, and germination rates.
        Generally, the higher the risk, the higher the profit.
    - The aim of the game is to get the most money.
    - If a drought occurs, the germination rate is 0, and the profit is 0. Costs are the same.
    - Costs are calculated by the raw cost of the crop * the tonnes put in
    - Profit is calculated by the sale price * tonnes put in * germination rate.

    How to get started:
    - Create an account with `>farmertown create`
    - See a list of crops to plant with `>farmertown croplist`
    - Sow a crop with `>farmertown sow CROP_NAME_HERE`
    - Wait 12 hours
    - Find the results of the crop and add this to your bank balance with `>farmertown results`
    - Repeat!
    - Check your balance with `>farmertown balance`

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

### Installation

1. Install `pipenv` and run `pipenv install` on the project.
2. Set up the Discord bot (in `bot/`) and copy your bot token and client
ID into their respective fields.
3. Run `__main__.py` to start both the PyQT app and the Discord bot.
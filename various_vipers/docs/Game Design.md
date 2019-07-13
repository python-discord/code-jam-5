# Design Document

### 1. UI Pages
- Navigation between them
    - back button in every page.
```
PAGE LAYOUT:
    Play
        Main game screen
            Task panel
            Pause panel
    Options - to options screen
    Credits - to credits screen
    Quit - close application
```
- Buttons
    - play
    - options
    - credits
    - quit
 - Main Screen:
     - show navigation buttons
     - should be able to start the game
     - should be able to quit the game
     - hiscore should be visible here
 - Options
     - volume: BG music
     - volume: sound effect
     - show fps
     - boost fps
 
---

### 2. Assets
- Art for game entities
    - art for different tasks (on earth and inside the task)
    - images for earth biomes
    - image for sun (will need to scale size/shape)
- Art for UI elements
    - images for the buttons
    - images for the buttons (hover)
    - background image for the main menu and other screens
- Music
    - BG music for the game
- Sound Effects
    - menu button click
    - task click
    - task completion
    - task failure
    - game ended

---

### 3. Game Design

#### 3.1. Camera

Game camera is in a fixed position and never moves. Player controls images of earth which move left and right. Earth can be moved by using `A + D` and `< + >` keyboard buttons. Earth images cycle through.

#### 3.2. Environment

Gamescreen consists of:
1. Earth images/biomes with tiles
2. Sun image (gets bigger and brighter with time / based on heat)
3. Clouds moving across the screen
4. Screen markers to help navigate to tasks
5. Tasks on earth
6. Tasks as new panel window

#### 3.3. Game UI

- Pause menu (via ESC button)
    - Buttons: resume, exit
- Task panel where player plays the minigame

#### 3.4. Gameplay

Gameplay consists of tasks that the player needs to do to save the EARTH. On completing the task successfully, sun gets less aggresive (yay). If player is too slow on completing the tasks it causes global warming (boo).

Heat is accumulated faster and tasks spawn more frequently with time - this is to prevent it from being a never-ending game.

##### 3.4.1. Tasks

Tasks will spawn randomly on earth surface that player has to complete in order to save the earth. Task theme will depend on where it spawns on earth (City, Forest, etc.).

Tasks should be timed before closing if not completed in time.

- Cursor maze
    - Players tries to move the mouse through the maze, avoiding walls.
- Rock Paper Scissors
    - Player gets a 1/3 chance to win. Task takes almost no time to complete.
- Tic Tac Toe
    - Player plays tic tac toe against the computer.

#### 3.5. Game balance

The game was balanced by adding values to spreadsheet - see `/docs` directory.


- how many different "tasks" should there be? Can they be generated to be infinite, unique, replayable every time?
    - 3 tasks / minigames. Assets will be predetermined (based on biome). Gameplay/maze for cursor maze will be generated and unique every time.
- on average how long should the game last?
    - min (player idles and does not play): ~60 seconds
    - max (player does everything as fast as possible): 1 hour to infinite
    - avg: 2 - 5 minutes
- how fast the "heat" goes up?
    - 0.5% each second + 0.09% for each task on earth
- how fast the "tasks" spawn?
    - every 5s, going down by 0.1s up to minimum of 0.5s
- how long it should take to do the "task"?
    - 3-15s
- how long it should take to scroll through earth?
    - ~5s
- how many in-game days in real-time seconds?
    - 30 days
- how many maximum number of tasks should it be allowed to be on earth?
    - 10 tasks

---

### 4. Professional game drafts

![draft_1](https://i.imgur.com/9KpvGtH.gif)

![draft_2](https://i.imgur.com/iqNilJ6.gif)

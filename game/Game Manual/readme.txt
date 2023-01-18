The Becoming of a Mathematician

Hartanto Kwee Jeffrey
Email: g1515212@blmcss.edu.hk

General Information:

    Please download Python and Pygame version 2.0.0 ver 6 (version 1.9.2 has not been tested, but you may try)
    Please also install simpleaudio, pyaudio and wave.
    Please use the arrow keys to navigate through menus


Pending (More than enough):

Questions:
- Probable geometry questions
- Question display module?
    - Remove from battle?
    - Practice Mode also has to use it, exactly the same code
- Create questions and change the mQuestion module to allow
  more questions
- Differentiation: small changes in value to find the slope at that point
- Integration: trapezoid rule?
- How to randomly generate an equation to differentiate and integrate?

Game Mechanics:
- Add several save files

Game Display:
- Add experience bar
- Add explanation of skills in shop
- Change resolution anywhere

Game Content:

Algorithm:
- Migation to Arcade?
- Change algorithm:
    - Don't create a menu obejct every time the function is invoked
    - Perhaps create a class to store state
    - Create global instances of the class in Adventure Mode
- PERFORMANCE:



Changelog:
/** 1/5/2020 - **/
- Bugfixes:
- NoneType returned when there is no save file. Causes the program to crash due to AttributeError.

/** 1/5/2020 - **/
- The game will be released for students to try out.
- Name list:


/** 25/4/2020 - 30/4/2020 **/
- The game is completed. Testing is now required.
- Finished questions, boss and game design. Formulas have been implemented.
- Ultimate debugging
- Design revamp for improved user friendliness
- Images only load when they are needed -> Performance time is damaged


/** 24/4/2020 **/
"The computer's up an running again!!! after I accidentally cut its power..."
- Finished the new mQuestion system
    - Added nested object attribute call e.g. {1,value,{2,value}}
    - Added function call e.g. {1,valueByNo,10}
- Cannot decide on a database to store the questions

/** 22/4/2020 - 23/4/2020**/
"Some troublshooting, and some more troubleshooting..."
- Completed Multiplayer Mode
    - Through multiprocessing, a player may open a server within a program
      Consider whether making mMultiplayerServer another file is necessary
- Partially completed the new mQuestion
    - Creates object, and coefficient in the statements will refer to the objects
    - Consider implementing checking modes

/** 19/4/2020 - 21/4/2020**/
"The unproductivity is killing me..."
- Started implementing Multiplayer Mode
- Offline Multiplayer is fully available
- Online Multiplayer remains heavily undebugged
- Fading animation added (pyAnimation)
- Revamped AVillage

/** 13/4/2020 **/
"It's the end of the Easter Holiday..."
- Implemented AShop fully
- Implemented AMenu, including all of it's components
- Implemented FrameMenu in pyMenu for creating quick menus
- Implemented ALoad
- Completed Adventure Mode

/** 12/4/2020 **/
- Implemented AVillage, ABossBattle, AGrinding
- Built general layout for AShop: ShopMenu class
- Performance problem solved:
    - Loading images take up too much memory
    - Load images when necessary (Beware of the GlobalVar)
    - Reduce image resolution if required (some are 1900 x 1900)
    - JPEGs does not support transparency

/** 11/4/2020 **/
"Such an unproductive day :("
- Implemented AdventureBattle
    - Serves as the commonplace between Grinding and Boss Battles
    - Includes procedures from choosing escaping to
      choosing potions to dealing damage
    - Returns 4 types of flags
        - "escape": The player escapes, jump directly out to the village
        - "win": The player defeats the boss
        - "lose": The player is defeated and died
        - "draw": The battle is still not finished -> invoke Main() once more
    - Problems: high memory usage and lagging
- Implemented damage displaying mechanisms in Battle
- Improved display in the Battle class
    - Fits at most 7 lines of text in question (Maybe)
    - Floating arrow to prompt player to press Enter
- Menu now has the scrolling function
(- PERFORMANCE ISSUES
    - The program takes about 70000 K of memory, compared
      with 30000 K in normal execution
    - Constaly blitting images might be the problem
    - Memory test results:
        - Selection Menu : 16000 K
        - Text : 17000 K
	- Text Input: 67320 K / 15904 K
        - Main Menu: 72000 K
        - Battle: 71000 K (in fact, lagging)
        - AdventureBattle: peaks at 79000K)

/** 10/4/2020 **/
- Started implementing battle
    - Health bars
    - Display the player and the opponent
    - Class: Battle
        - Other forms of battles (Multiplayer, Adventure Mode) can 
          inhert the Battle class and add their own battle sequences
        - Implemented question answering sequence
- Added GlobalVar (global variables across modules/files)
    - CentralClock
    - Fonts and their filenames (String)
    - Colors (a class accessible by color.___)
- Added pyTimer


/** 9/4/2020 **/
- Implemented AnswerCheck
- Added exception functionality in QuestionGenerator:
    Displays the comment of a question when an error occurs
- Implemented pyInput: TextInput class added
- Implemented PracticeMode
- Implemented Player and load/save modules
    Initialization() --> Player
    LoadSave(filename) --> Player
    SaveFile(filename, player) --> bool


/** Project start to 8/4/2020 **/
- Implemented Main Menu
- Implemented selection menu module
- Implemented text wrapping module
- Implemented QuestionGenerator
    Submodules:
    - QuestionGenerator
    - QuestionReader

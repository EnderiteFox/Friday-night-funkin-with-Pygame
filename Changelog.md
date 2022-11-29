# V1.1
Added long notes  

# V1.2
Added main menu, fixed bugs, changed some files organisation  

# V1.2.1
Fixed critical stack overflow issue  

# V1.3
Added Main menu  
Added options (Note speed, side and no death mechanic)  
Added health mechanic  
Added accuracy (the same as Kade engine accurate mode)  
Added New songs  

# V1.4
Added backgrounds  
Added new note skin (Stepmania), you can change it in the settings  

# V1.5
Added characters  
You can now hide the notes of a character by adding "modifications": ["hideNotes1"] in the songData.json file (it hides the opponent's notes, for the player use "hideNotes2")  
Added new songs  

# V1.5.1
Added main menu music  
Added Death menu  
Added keybinds option  
Options now save when you quit the game  
Added a README.txt file with instructions how to play  

# V1.5.2
Added downscroll  
Added song progress bar  
Added new musics  
Fixed a bug with the no dying option not saving correctly  

# V1.6
Changed the menu, now you can see more easily which option is selected  
Reworked the long notes system, they are now integrated to gameplay!  
How they work:  
- If you miss a note and it has a long note attached to it, you will have only 1 miss, the long note can't deal damage  
- If you hit a note and it has a long note attached to it, the long note will be able to deal damage  
- If you release a long note too early and you hit less than 75% of it, you will get a miss  
- If you release a long note too early and you hit more than 75% of it, you won't get a miss (so if you miss a little bit of the long note in the end of it you won't get a miss)  
- When a long note can't deal damage, it will appear transparent  
Tell me what you think about this mechanic and if I need to change something!  
The game is now available as a .exe file! (Took me 3 days to figure out how to do this XD)  

# v1.7
- Characters animations rework (with multiple frames for each animation, so animated animations I guess)  
- Fixed characters not appearing on certain conditions (I think Python >=3.9 and EduPython)  
- Improved display for screen with a resolution inferior to 1080p  
- Improved compatibility with other operating systems (using op.path.sep)  
- Fixed some maths, now animated backgrounds will display correctly, with their speed changed according to the bpm (faster bpm = faster animation)  
- Fixed a bug with the song progress bar not displaying correctly when playing in downscroll mode  
- Added idle animation  
- Characters now use a png and xml file, so now it's easier to add characters  
- Now animations are more fluid, as they use all images from the png  
- Added the offset editor, a seperate program (accessible from the options menu), is used to change the offsets of characters, to display them at the correct position  
- Added a color indicator in the info bar depending on the current accuracy (0-70%: red, 70-85%: orange, 85-100%: green)  
- Added a color indicator in the info bar depending on the current health (0-50%: red, 50-75%: orange, 75-100%: green)(only when the health is displayed in the info bar)  
- Added the option to disable info bar color indicators to save performance  
- Added the option to display health in the info bar instead of a health bar  
- Fixed a bug with the vertical offset being inverted  
- Changed the menu music (changed to the main menu music from the FNF indie cross mod) 
- Changed how the options work in the code, to make it cleaner and easier to add new options  
- Code optimisations  
- Added 6 new songs:  
 - Last reel (FNF indie cross)(the notes are not synced to the music after half of the song for some reason)  
 - Nightmare run (FNF indie cross)(Some notes are not appearing as they are death notes)  
 - Burning in hell (FNF indie cross)(same here)  
 - Power outage (Funkin' at Freddy's)  
 - Chartering (FF celebration mod)  
 - Sussy Wussy (FF celebration mod)  
 - Hellclown is not working, this is because the character texture is saved differently, I have to find how to create textures with XML files to fix it in 1.8.1  
 
# v1.8
- Cleaned some code
- Now crashing in-game won't crash the game. It will instead send you back to the main menu
- Added transitionValue object. It is used by modcharts to make a linear transition between a start value and an end value
- Added simple modcharts. They can:
  - Control the transparency of arrows
  - Control the alpha of characters
  - Change characters in-game
  - Change the arrow skin in-game
- The simple modcharts wiki is [here](https://github.com/EndersteveGamer/Friday-night-funkin-with-Pygame/wiki/How-to-use-simple-modcharts)
- Added all mid-song alpha changes using modcharts
- Added all mid-song character changes using modcharts (in Sorrow and Satisfracture)
- Fixed the "You can't run" song

# v1.8.1
- Added 3 new songs:
  - Unhinged (Vs Impostor Black Betrayal)
  - Uncertain demise (FNF Trepidation)
  - No head red (FNF Trepidation)
- Arrows are now saved the same way as characters, with png and xml files, so it's now easier to add new arrow styles. Check [here](https://github.com/EndersteveGamer/Friday-night-funkin-with-Pygame/wiki/How-to-add-note-skins) to add note styles
- Removed "run" and "hellclown" from the music list as they crash the game (they will be readded later once the game has the necessary features to add them back). You can still add them manually from the musicList.json file
- Fast-editing an offset in the offset editor by pressing shift now edits the offset faster

# v1.9

v1.9 (Special arrows update):
- You can now use the + and - key to change the volume of the game (WIP)
- Special notes were added!
  - These notes can have a different note skin than the others
  - You can edit the amount of health that these notes add or remove when hitting or missing the note
  - These notes can be marked as mustHit (so they won't count as a miss if you don't hit them)
  - They can also execute modcharts when you hit or miss them (WIP)

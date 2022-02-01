# Friday-night-funkin-with-Pygame
This is just Friday Night Funkin, but coded in Python using the Pygame library

Download to play: 

You can add the files from any FNF mod, just follow the instructions:
- Create a folder in assets\musics
- add the Inst.ogg and Voices.ogg music files in the folder
- add the chart json file from the song in the foldes, and rename it to chart.json
- Make sure the chart.json file organisation is {"song":{"notes":[]}} (often you just have to add the entire file in {"song": the whole file}
- Edit the json file in assets\MusicList.json to add the name of your song (This should be the same name as the folder that contains your music)
- Edit the line 107 to the name of your song (play("song name here")) (not having the name of a music in the function will play a random song)
- Play

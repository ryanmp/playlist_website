#playlist_website

##Dead-Simple audio playlist generator for a website

This is a static generator that turns a folder of songs into a website which relies on jQuery for UI. Each song gets a waveform representation, inspired by the SoundCloud music player. 

Visit:

[ryanmp.github.io/playlist_website](http://ryanmp.github.io/playlist_website/index.html)

to see it in action.

##Development Notes

runme.py looks for tracks in songs_input folder and uses them as input when rendering the jinja template.

poll.py runs runme.py when any changes are detected.

###Todo List

* Transcode to multiple file formats using sox (better compatibility across devices)

###Known Bugs

When trying to seek, sometimes the player jumps back to the start of the song. To be investigated and fixed soon...


## Features
- allow outputting different audio formats via pydub (mp3, wav, etc)
- write script to package as a binary for release
- figure out how to better package voices and allow for easier selection from CLI
- GUI?


## Bugs
- lines with multiple asterisks (`*** START OF THE PROJECT GUTENBERG EBOOK ALICE'S ADVENTURES IN WONDERLAND ***`) generate weird audio
    - clean these kinds of lines
- lines with spaces are not filtered as containing only punctuation (`generating audio for line   --------------- -----------------------------------`)
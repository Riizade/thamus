## Features
- allow outputting different audio formats via pydub (mp3, wav, etc)
- allow configuring to use other models (Bark, etc) and figure out which perform best
- write script to package as a binary for release
    - https://pypi.org/project/cx-Freeze/
    - PyInstaller
    - nuitka
    - BeeWare Briefcase  
- figure out how to better package voices and allow for easier selection from CLI
- GUI?


## Bugs
- lines with multiple asterisks (`*** START OF THE PROJECT GUTENBERG EBOOK ALICE'S ADVENTURES IN WONDERLAND ***`) generate weird audio
    - clean these kinds of lines
- lines with spaces are not filtered as containing only punctuation (`generating audio for line   --------------- -----------------------------------`)

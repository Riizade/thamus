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
- cannot use deepspeed yet because the dependency can't be installed via pip
- need to break up larger lines, otherwise it fails to generate audio or just gets weird
    - good length for English text is about 150 characters, one sentence, or 30 words.
- multiple spaces mess up audio generation (collapse multi-space, tab, etc to single space)

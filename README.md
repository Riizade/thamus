# thamus
Converts ebooks to mp3 audiobook files

# License

- [Tortoise](https://github.com/neonbjb/tortoise-tts/tree/main) has its full source included in this repository (`./tortoise/`) and redistributed under the original [Apache License 2.0](./tortoise/LICENSE) with minor modifications
    - Tortoise was cloned at commit hash `4003544b6ff4b68c09856e04d3eff9da26d023c2` on 2023-08-28
    - Below is a list of all changes made to the tortoise source
        - The tortoise source had its imports modified to reflect its new directory structure
- The provided sample books are in the public domain and were acquired from [Project Gutenberg](https://www.gutenberg.org/)
- The rest of the repository is covered under the provided MIT License

# Development

Development only tested on Windows.

There may be dependency issues on Linux or other platforms.

In particular, the audio backend for pytorch might need to be `Sox` instead of `SoundFile` (`pipenv install sox`)

## Prerequisites

### pipenv

- run `pipenv install` from the main directory of this repo

### Conda (deprecated)

- install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- create conda project
    - `conda create --name thamus python=3.9 numba inflect`
- activate conda project
    - `conda activate thamus`
- install [PyTorch](https://pytorch.org/get-started/locally/)
    - open an Anaconda prompt and execute the relevant command
        - for CUDA 11.8 `conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia`
        - for CUDA 11.7 `conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia`
        - for CPU (no CUDA/GPU) `conda install pytorch torchvision torchaudio cpuonly -c pytorch`
- install other dependencies
    - `conda install transformers=4.29.2`
    - if on Windows: `conda install -c conda-forge pysoundfile`

## Example Run

`pipenv run python -m src.main --book example_books/wonderland.epub --voice tortoise/tortoise/voices/train_grace`

# origin of the name thamus

This project is named for Plato's play [Phaedrus](http://classics.mit.edu/Plato/phaedrus.html) in which King [Thamus](https://en.wikipedia.org/wiki/Thamus_(mythical_King_of_Egypt)) believes that the gift of writing will "will create forgetfulness in the learners' souls".

In other words, King Thamus might approve of this project because its purpose is to replace the written word with speech, thus preventing the supposed deleterious effects of written language on the human mind.

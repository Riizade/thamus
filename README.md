# thamus
Converts ebooks to mp3 audiobook files

## Development Prerequisites

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

## origin of the name thamus

This project is named for Plato's play [Phaedrus](http://classics.mit.edu/Plato/phaedrus.html) in which King [Thamus](https://en.wikipedia.org/wiki/Thamus_(mythical_King_of_Egypt)) believes that the gift of writing will "will create forgetfulness in the learners' souls".

In other words, King Thamus might approve of this project because its purpose is to replace the written word with speech, thus preventing the supposed deleterious effects of written language on the human mind.

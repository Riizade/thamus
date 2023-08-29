#!/usr/bin/env python3

import pypandoc
import click
from pathlib import Path
import tortoise.tortoise.utils as tortoise_utils
import tortoise.tortoise.api as tortoise_api
from torch import FloatTensor
import torchaudio
import tempfile
import pydub
from tqdm import tqdm
import re
import string

@click.command(name="convert")
@click.option("--book", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False), help="The filepath of the ebook you'd like to convert to audio")
@click.option("--voice", required=True, type=click.Path(exists=True, file_okay=False, dir_okay=True), help="The path of the directory containing the voice clips to use as a reference; check the voices/ directory for options")
@click.option("--quality", type=click.Choice(['ultra_fast', 'fast', 'standard', 'high_quality']), default="standard", help="The quality preset to use when generating audio. Higher quality takes more time.")
@click.option("--kv-cache/--no-kv-cache", type=bool, default=True, help="Enables caching during audio generation, should speed up generation time.")
@click.option("--use-deepspeed/--no-deepspeed", type=bool, default=True, help="Enables deepspeed during audio generation, should speed up generation time.")
@click.option("--full/--half", type=bool, default=True, help="Whether to use full precision (32-bit) or half precision (16-bit). Full precision should be higher quality, but generate more slowly.")
def main(book: click.Path, voice: click.Path, quality: str, kv_cache: bool, use_deepspeed: bool, full: bool):
    path = Path(book)
    reference_directory = Path(voice)
    text = convert_to_plaintext(path)
    audio_path = path.with_suffix(".wav")
    reference_clips = collect_reference_clips(reference_directory)
    write_audio(text=text, write_path=audio_path, quality=quality, reference_clips=reference_clips, kv_cache=kv_cache, deepspeed=use_deepspeed, half=not full)

def collect_reference_clips(clip_path: Path) -> list[FloatTensor]:
    clip_paths = list(clip_path.iterdir())
    reference_clips = [tortoise_utils.audio.load_audio(audiopath=str(p), sampling_rate=22050) for p in clip_paths]
    return reference_clips

def write_audio(text: str, write_path: Path, quality: str, reference_clips: list[FloatTensor], kv_cache: bool = True, deepspeed: bool = True, half: bool = True):
    # split text into lines so that each clip is shorter
    # the model works best with clips 5-10 seconds in length 
    lines = text.splitlines()
    # create a temporary directory to save intermediate short audio clips
    temporary_directory = tempfile.TemporaryDirectory(prefix="thamus_tmp_audio_clips_")
    print(f"temporary directory created at: {temporary_directory.name}")
    
    tts = tortoise_api.TextToSpeech(kv_cache=kv_cache, use_deepspeed=deepspeed, half=half)

    # generate audio for each line
    print(f"generating audio for each of {len(lines)} lines...", flush=True)
    for line_idx, line in enumerate(tqdm(lines)):
        # skip lines with only punctuation
        if all(c in string.punctuation for c in line):
            print(f"skipping empty line {line}", flush=True)
            continue
        # generate the audio data using Tortoise
        print(f"generating audio for line {line}", flush=True)
        generated_data = tts.tts_with_preset(text=line, preset=quality, voice_samples=reference_clips)


        # save the generated clip to file in the temporary directory
        # below code was modeled after tortoise/do_tts.py
        if isinstance(generated_data, list):
            for sub_idx, g in enumerate(generated_data):
                torchaudio.save(Path(temporary_directory.name) / f'output_{line_idx}_{sub_idx}.wav', g.squeeze(0).cpu(), 24000)
        else:
            torchaudio.save(Path(temporary_directory.name) / f'output_{line_idx}.wav', generated_data.squeeze(0).cpu(), 24000)
    
    # generate a list of output files in alphabetical order
    file_list = list(Path(temporary_directory.name).iterdir())
    file_list.sort(key=lambda x: x.stem)

    # concatenate all the saved audio clips into one massive clip
    print("combining audio clips", flush=True)
    combined_clip = pydub.AudioSegment.from_wav(file_list[0])
    for f in tqdm(file_list[1:]):
        combined_clip = combined_clip + pydub.AudioSegment.from_wav(f)
    
    # save the combined clip to disk
    combined_clip.export(write_path, format="wav")

    # remove the temporary directory
    temporary_directory.cleanup()

def clean_text_chunk(text_chunk: str) -> str:
    # remove _italics_
    text_chunk = re.sub(r"_", " ", text_chunk)
    # remove --- hyphens for footnotes
    text_chunk = re.sub(r"(\-{3,})", "Footnote:", text_chunk)
    return text_chunk

def convert_to_plaintext(path: Path) -> str:
    try:
        return pypandoc.convert_file(path, "plain", extra_args=["--wrap=none"])
    except RuntimeError as e:
        print(f"pypandoc could not read the given file due to error: {e}", flush=True)
        exit(1)

if __name__ == "__main__":
    main()

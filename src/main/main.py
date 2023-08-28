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

@click.command(name="convert")
@click.option("--book", required=True, type=click.Path(exists=True, file_okay=True, dir_okay=False), help="The filepath of the ebook you'd like to convert to audio")
@click.option("--voice", required=True, type=click.Path(exists=True, file_okay=False, dir_okay=True), help="The path of the directory containing the voice clips to use as a reference; check the voices/ directory for options")
@click.option("--quality", type=click.Choice(['ultra_fast', 'fast', 'standard', 'high_quality']), default="standard")
def main(book: click.Path, voice: click.Path, quality: str):
    path = Path(book)
    reference_directory = Path(voice)
    text = convert_to_plaintext(path)
    audio_path = path.with_suffix(".wav")
    reference_clips = collect_reference_clips(reference_directory)
    write_audio(text, audio_path, quality, reference_clips)

def collect_reference_clips(clip_path: Path) -> list[FloatTensor]:
    clip_paths = list(clip_path.iterdir())
    reference_clips = [tortoise_utils.audio.load_audio(audiopath=p, sampling_rate=22050) for p in clip_paths]
    return reference_clips

def write_audio(text: str, write_path: Path, quality: str, reference_clips: list[FloatTensor]):
    # split text into lines so that each clip is shorter
    # the model works best with clips 5-10 seconds in length 
    lines = text.splitlines()
    # create a temporary directory to save intermediate short audio clips
    temporary_directory = tempfile.TemporaryDirectory(prefix="tmp_audio")
    
    tts = tortoise_api.TextToSpeech(kv_cache=True)

    # for each line
    for line_idx, line in enumerate(lines):
        # generate the audio data using Tortoise
        generated_data, _debug_state = tts.tts_with_preset(text=line, preset=quality)

        # save the generated clip to file in the temporary directory
        # below code was modeled after tortoise/do_tts.py
        if isinstance(generated_data, list):
            for sub_idx, g in enumerate(generated_data):
                torchaudio.save(temporary_directory / f'output_{line_idx}_{sub_idx}.wav', g.squeeze(0).cpu(), 24000)
        else:
            torchaudio.save(temporary_directory / f'output_{line_idx}.wav', generated_data.squeeze(0).cpu(), 24000)
    
    # generate a list of output files in alphabetical order
    file_list = list(Path(temporary_directory.name).iterdir())
    file_list.sort(key=lambda x: x.stem)

    # concatenate all the saved audio clips into one massive clip
    combined_clip = pydub.AudioSegment.from_wav(file_list[0])
    for f in file_list[1:]:
        combined_clip = combined_clip + pydub.AudioSegment.from_wav(f)
    
    # save the combined clip to disk
    combined_clip.export(write_path, format="wav")

    # remove the temporary directory
    temporary_directory.cleanup()


def convert_to_plaintext(path: Path) -> str:
    try:
        return pypandoc.convert_file(path, "plain", extra_args=["--wrap=none"])
    except RuntimeError as e:
        print(f"pypandoc could not read the given file due to error: {e}", flush=True)

if __name__ == "__main__":
    main()
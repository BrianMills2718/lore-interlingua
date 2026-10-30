"""Narrate the review MP4: speak each passage of narration.json with Edge TTS (en-US-AndrewNeural) and mix it over the
score, starting 0.6 s into its caption's slot, with the score at 35 %. Needs edge-tts and ffmpeg.

    python narrate.py   # writes The_Living_Interval_narrated_480p.mp4 next to the review MP4
"""
import asyncio
import json
import pathlib
import subprocess
import tempfile

import edge_tts

HERE = pathlib.Path(__file__).parent
SRC, OUT = HERE / "The_Living_Interval_review_480p.mp4", HERE / "The_Living_Interval_narrated_480p.mp4"
VOICE, LEAD, SCORE = "en-US-AndrewNeural", 0.6, 0.35


async def speak(text: str, path: pathlib.Path) -> None:
    # a negative rate ("-3%") came back as NoAudioReceived (2026-10-29); the default rate works
    for wait in (5, 10, 20, None):
        try:
            return await edge_tts.Communicate(text, VOICE).save(str(path))
        except edge_tts.exceptions.NoAudioReceived:
            if wait is None:
                raise
            await asyncio.sleep(wait)


def seconds(path: pathlib.Path) -> float:
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                          "csv=p=0", str(path)]))


def main() -> None:
    lines = json.loads((HERE / "narration.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        clips = [pathlib.Path(tmp) / f"n{i:02d}.mp3" for i in range(len(lines))]
        for (start, end, text), clip in zip(lines, clips):
            asyncio.run(speak(text, clip))
            if seconds(clip) > end - start - LEAD:
                raise SystemExit(f"passage at {start}s runs {seconds(clip):.1f}s, past its {end - start}s slot")
        graph = [f"[{i + 1}:a]adelay={int((s + LEAD) * 1000)}|{int((s + LEAD) * 1000)},volume=1.6[v{i}]"
                 for i, (s, _, _) in enumerate(lines)]
        graph += ["".join(f"[v{i}]" for i in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0[vo]",
                  f"[0:a]volume={SCORE}[m]", "[m][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]"]
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(SRC)] + [a for c in clips for a in ("-i", str(c))]
        cmd += ["-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "160k", "-shortest", str(OUT)]
        subprocess.run(cmd, check=True)
    print(f"wrote {OUT.name}: {seconds(OUT):.1f}s, {len(lines)} passages")


if __name__ == "__main__":
    main()

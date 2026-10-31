import numpy as np, traceback, transformers
from transformers import Qwen3OmniMoeProcessor
print("transformers", transformers.__version__)
p = Qwen3OmniMoeProcessor.from_pretrained("Qwen/Qwen3-Omni-30B-A3B-Instruct")
video = np.random.RandomState(0).randint(0, 255, (16, 3, 480, 256), dtype=np.uint8)
for flag in (True, False):
    try:
        out = p(text="<|vision_bos|><|video_pad|><|vision_eos|>", videos=[video], use_audio_in_video=flag, return_tensors="pt", do_resize=False)
        print(f"use_audio_in_video={flag}: OK keys={sorted(out.keys())}")
    except BaseException as e:
        print(f"use_audio_in_video={flag}: {type(e).__name__}: {e}")
        tb = traceback.extract_tb(e.__traceback__)[-1]
        print("  at", tb.filename.split("site-packages/")[-1], tb.lineno, tb.line)

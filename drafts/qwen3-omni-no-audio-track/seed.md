# seed.md — Ryan's raw input (human-written only)

ASSEMBLED, NOT WRITTEN, BY RYAN. Every line below is quoted or closely paraphrased from text Ryan posted publicly,
with its source. Nothing here is invented. Gaps are marked `GAP` and need Ryan's own words before the [HUMAN]
sections can say more than the public record does.

Sources:
- ISSUE = https://github.com/vllm-project/vllm/issues/48383 (comments by RyanJHamby, 2026-07-12)
- PR = https://github.com/vllm-project/vllm/pull/48420 (body, and RyanJHamby's two comments, 2026-07-18)
- COMMITS = c38b98f (first fix), f25d0ca "Raise clear ValueError instead of silent fallback per review", 2d8f7ee (CI fix)

## The question
- A user reported that Qwen3-Omni video inference raises an error when the input video has no audio track. [ISSUE, body by the reporter]
- GAP: why you picked this issue up.

## What I actually did (setup, key choices, why)
- Reproduced directly against the HF `Qwen3OmniMoeProcessor` with a synthetic no-audio video of the reported shape (16, 3, 480, 256); calling the same processor with `use_audio_in_video=False` succeeded. [PR body]
- First fix: when no audio was extracted but `use_audio_in_video=True` was requested, fall back to `use_audio_in_video=False` for that call, "there's nothing to interleave". [PR body, c38b98f]
- Added a regression test following the existing `test_audio_in_video.py` pattern, for both Qwen2.5-Omni-3B and Qwen3-Omni-30B-A3B-Instruct. [PR body]
- After review, replaced the silent fallback with a clear `ValueError` ("Raise clear ValueError instead of silent fallback per review"). [f25d0ca]
- GAP: what the review said and why it persuaded you (or not). The inline review text was not readable from my tools.
- AI role (Ryan, 2026-10-31): about half and half. Ryan's own, by his statement: the reproduction, the first fix (the silent fallback), and the CI investigation. Root cause: the AI traced it, Ryan confirmed it. Second fix (2d8f7ee): the AI wrote it, Ryan reviewed and tested it. GAP: who wrote the guard commits f25d0ca and 7166e20; the draft says only 'a guard' and 'the new guard'.

## What I expected
- GAP: not written anywhere public. The PR body implies the fallback was expected to be enough.

## What happened / what surprised me
- Several `multi-modal-processor` CI jobs failed with real errors, not flakes. [PR comment 2026-07-18]
- Cause 1: Qwen3-Omni's `_call_hf_processor` pops `mm_data["audios"]` and builds `mm_data["audio"]`, then calls the Qwen2.5-Omni parent, which also pops `"audios"`. The parent therefore always saw none, so the new guard raised even with real audio. [PR comment]
- Cause 2: on a full multimodal-processor-cache hit, `_call_hf_processor` is called with empty `mm_data`, and both guards read that as "no audio track". [PR comment]
- A third, pre-existing problem: an `assert "audio" in mm_counts` in `_apply_hf_processor_mm_only` fires whenever the audio limit is 0, whether or not the video lacks audio. [PR comment]
- GAP: what surprised you, in your words.

## Dead ends along the way
- The silent fallback (see above) was the first approach and was replaced. [COMMITS]
- GAP: anything else you tried or ruled out.

## My decision or recommendation (and for whom)
- Guard on `mm_data.get("videos")` and on `"audio" not in mm_data`, so the error fires only for genuine unconsumed video data. [PR comment, 2d8f7ee]
- GAP: your recommendation for anyone writing a guard in an inherited `_call_hf_processor`.

## What I'd do differently
- GAP.

## Open question this raises
- GAP. Candidate drawn from the record, to accept or reject: the parent and child classes each pop `"audios"`, and the tests did not cover the cache-hit path until CI did.

## Clearances
- Employer-related content: none (Ryan, 2026-10-31)
- People named (with permission): none. Ryan chose 'a maintainer' (2026-10-31); the reporter is not named either.

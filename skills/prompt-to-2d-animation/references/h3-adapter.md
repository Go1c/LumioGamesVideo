# MiniMax H3 Video Adapter

Use this reference only after MiniMax H3 has been selected and is legally available for the user's
location and intended distribution.

## Relevant capabilities

- H3 Base output is 4–15 seconds at 24 FPS with native audio; this workflow ignores generated
  audio and resamples the useful visual window.
- Base FL2VA supports text, first frame, last frame, or first-and-last frames.
- Base Ref2VA supports multimodal references. Current documented limits are up to 9 images,
  3 videos, and 3 audio files, with at most 12 files total.
- Local H3 Base targets 768p. Hosted Context-IR/Regenerate components may differ and are not a
  portable plugin requirement.

## Mapping

| Plugin job | H3 mode |
|---|---|
| Prompt-only concept | T2VA, or generate anchor then I2VA |
| Character anchor | I2VA |
| Loop with matching start/end anchor | FL2VA |
| Character plus motion/video reference | Ref2VA |

Prefer anchor-driven modes. For a 1–2 second useful action, generate a legal 4-second H3 clip with
stable holds around the action, then set the job's trim window before frame extraction.

## Prompt output

Write an integrated shot description with explicit timestamps, fixed composition, character
invariants, action, clean background, and negative constraints. Preserve user-visible dialogue or
text exactly, but this plugin normally forbids visible text and discards audio.

## License gate

The current H3 Community License excludes the United States, European Union, United Kingdom, and
Republic of Korea from its Applicable Territory and also restricts use/display/distribution of H3
outputs outside the Applicable Territory. Commercial terms and disclosure duties may also apply.
Do not infer authorization from technical availability. If the license does not cover the task,
select another provider or deliver plan-only output.

Official sources:

- https://github.com/MiniMax-AI/MiniMax-H3
- https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE

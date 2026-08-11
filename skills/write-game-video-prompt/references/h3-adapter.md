# MiniMax H3 Adapter

Use this adapter only after MiniMax H3 has been selected and is permitted for the execution
location and intended distribution.

## Capability mapping

- H3 Base produces 4–15 second, 24 FPS audio-video clips; the local open release targets 768p.
- FL2VA supports text-only, first-frame, last-frame, and first-plus-last-frame conditioning.
- Ref2VA accepts multimodal references: currently documented limits are up to 9 images, 3 videos,
  3 audio files, and 12 files total.
- Hosted Context-IR or Regenerate/2K capabilities are not part of the portable local Base contract.

| Generic mode | H3 route |
|---|---|
| text-to-video | FL2VA text path |
| image-to-video / first-frame-to-video | FL2VA first-frame path |
| first-last-frame-to-video | FL2VA first-plus-last path |
| reference-to-video / video-to-video | Ref2VA |

For an action shorter than four seconds, generate a legal four-second clip with stable handles and
trim the useful window. Do not stretch a fast action merely to fill the provider minimum.

## License gate

The H3 Community License described by the source report excludes the United States, European Union,
United Kingdom, and Republic of Korea from its Applicable Territory and places restrictions on
H3 Works and outputs. Commercial, attribution, and disclosure terms may also apply.

Re-check the current official license before every shipping workflow. Technical access is not
authorization. Select another provider or return a plan-only package when authorization is absent.

Official sources:

- https://github.com/MiniMax-AI/MiniMax-H3
- https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/LICENSE

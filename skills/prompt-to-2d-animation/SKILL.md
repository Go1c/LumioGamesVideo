---
name: prompt-to-2d-animation
description: Generate short 2D game-character animations from a text prompt and optional reference image, then convert selected videos into transparent PNG sequences, sprite atlases, flipbooks, or Spine 4.1–4.3 sequence packages. Use for character idle loops, emotes, attacks, spell actions, video-to-frames conversion, chroma-key cleanup, sprite packaging, or requests mentioning 2D animation, sequence frames, spritesheets, flipbooks, or Spine output. Do not use for true skeletal auto-rigging, Live2D motion generation, or frame-accurate gameplay hitboxes.
---

# Prompt to 2D Animation

Create a game-ready frame animation, not merely a demo video. Treat Spine output as a
flipbook container unless the user supplies a real rig and explicitly requests another workflow.

Use `$write-game-video-prompt` for the shared provider/mode, reference-role, rights, provenance,
and generation prompt contract. Then create the specialized `animation-job.json` below for frame
processing and package delivery.

## Choose the path

- Prompt only: generate and lock one character anchor image, then animate it.
- Prompt plus reference image: use the reference as the identity and style anchor.
- Existing video: skip generation and start at media inspection.
- Frames already cleaned: skip to package building.
- True Spine bones, meshes, weights, IK, or Live2D parameters: explain that this skill does not
  infer a rig; offer a flipbook package or a separate rigging project.

If required image/video tools are unavailable, produce a plan-only package containing the final
prompts, `animation-job.json`, processing commands, and unresolved capability checks. Never claim
that media was generated when it was not.

## 1. Normalize the job

Read [references/safety-and-rights.md](references/safety-and-rights.md) when a reference image,
remote provider, commercial release, recognizable person, or licensed model is involved.

Create `animation-job.json` from [assets/animation-job.schema.json](assets/animation-job.schema.json).
Infer safe defaults when the request permits:

- `character-idle-loop`: 2–4 seconds, 12 delivery FPS, loop.
- `character-emote`: 1–2 seconds of useful action, 12 delivery FPS, one-shot.
- `character-action`: 1–2 seconds of useful action, 12 delivery FPS, one-shot.
- 512×512 transparent canvas, bottom-center pivot, at most 48 delivered frames.

Provider minimum duration can exceed useful action duration. Record `trim_start_seconds` and
`trim_duration_seconds` instead of stretching a quick action unnaturally.

Validate the job before generating media:

```bash
python scripts/validate_job.py animation-job.json
```

## 2. Lock the character anchor

For prompt-only jobs, create one clean anchor image before video generation. For referenced jobs,
use the supplied image unless it is unsuitable for animation. Follow
[references/prompting.md](references/prompting.md).

Lock face, hairstyle, costume, palette, silhouette, view direction, character scale, and weapon.
Prefer a single unobstructed character on a flat background color absent from the character.
Do not proceed with a visibly inconsistent anchor.

## 3. Generate and select the video

Inspect available video capabilities, select the closest supported mode, and keep the core job
provider-neutral. Read [references/h3-adapter.md](references/h3-adapter.md) only when MiniMax H3 is
the selected provider.

The render prompt must enforce one character, one action, locked camera, constant scale, full
silhouette, clean separation, no cuts, no text, no new props, and preservation of identity/style.
Generate no more variants than `render_policy.max_video_variants`.

Reject candidates with identity drift, extra/missing limbs, warped weapons, crop changes, camera
motion, incomplete action, or unusable background separation. Regenerate from the anchor instead
of extracting frames from a fundamentally broken candidate.

## 4. Build a clean frame sequence

Read [references/frame-pipeline.md](references/frame-pipeline.md), then use the bundled scripts.
Render-enabled processing requires Python 3.9+, FFmpeg/FFprobe, and Pillow.

```bash
python scripts/inspect_video.py selected.mp4

python scripts/extract_frames.py selected.mp4 frames/raw \
  --clip-id swordsman-slash --fps 12 --size 512x512 \
  --start 1.0 --duration 1.5 --chroma-key 0x00FF00

python scripts/stabilize_sequence.py frames/raw frames/cleaned \
  --clip-id swordsman-slash --mode alpha-bottom-center
```

Use chroma key only when the chosen key color does not occur in the character. Otherwise use a
host-provided segmentation/matting capability and save straight-alpha PNGs. If no reliable matte
path exists, stop before transparent-asset packaging and report the blocker.

Do not use bbox stabilization for jumps, dashes, deliberate root motion, or large weapon arcs when
the moving silhouette would corrupt the anchor. Use `--mode none` and define a manual pivot.

## 5. Package the flipbook and Spine sequence

Read [references/spine-flipbook-profile.md](references/spine-flipbook-profile.md) before generating
Spine output.

```bash
python scripts/build_spine_flipbook.py frames/cleaned package \
  --clip-id swordsman-slash --fps 12 --once \
  --spine-version 4.1 --pivot bottom-center

python scripts/validate_package.py package
```

The builder outputs the engine-neutral sequence manifest, atlas metadata, Spine JSON, Spine atlas,
and atlas page images. Mark the result as `animation_kind: flipbook`, never `skeletal`.

## 6. Review and deliver

Read [references/qa-rubric.md](references/qa-rubric.md). Require data QA for every package and
visual QA whenever media exists. A loop must play three consecutive cycles without a visible seam.
Do not infer gameplay hit timing from generated pixels; events remain explicit user-authored data.

Deliver:

- the selected source video and approved anchor;
- cleaned transparent PNG frames;
- `sequence-manifest.json`, atlas pages, and `atlas.json`;
- optional Spine JSON and `.atlas` for a confirmed 4.1+ target;
- `provenance.json` and `qa-report.json`;
- a clear statement of whether visual QA passed, remains pending, or failed.

Never overwrite source inputs. Write each retry or revision to a new output directory.

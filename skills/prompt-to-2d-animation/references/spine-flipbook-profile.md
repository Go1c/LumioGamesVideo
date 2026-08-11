# Spine Flipbook Profile

This profile packages a full-frame PNG sequence as one Spine sequence attachment. It is a playback
container, not an inferred skeletal rig.

## Compatibility

- Target Spine and Spine Runtime major/minor versions must match.
- Sequence attachments are supported by Spine Runtimes 4.1 and later; plugin v0.1 emits and
  validates the 4.1, 4.2, and 4.3 profiles only.
- Do not bundle Spine Editor or Spine Runtime. Loading and redistribution remain subject to the
  user's Spine license.

## Skeleton shape

The generated skeleton has:

- one `root` bone;
- one `sprite` slot;
- one region attachment whose `path` is `<clip-id>_`;
- one sequence descriptor with `count`, `start: 0`, `digits: 4`, and `setup: 0`;
- one sequence timeline with a start key and a terminal hold key.

The sequence timeline uses:

- `mode: loop` for loops;
- `mode: once` for one-shots;
- `index: 0`;
- `delay: 1 / delivery_fps`.

Add a second `hold` key at `frame_count / delivery_fps` so Spine computes a non-zero animation
duration. Its index is `0` for a loop and the last frame index for a one-shot.

The atlas must contain exact region names such as `swordsman-slash_0000`,
`swordsman-slash_0001`, and so on. Atlas pages may contain multiple regions and multiple pages.

## Pivot mapping

PNG coordinates start at the top-left; Spine uses a Y-up coordinate system. For a pixel pivot
`(pivot_x, pivot_y)`:

```text
attachment_x = frame_width / 2 - pivot_x
attachment_y = pivot_y - frame_height / 2
```

The default bottom-center pivot is `(width / 2, height)`, which places the image center half a frame
height above the root.

## Required output

- `<clip-id>.json` — Spine skeleton and sequence animation;
- `<clip-id>.atlas` — Spine atlas metadata;
- `<clip-id>-<page>.png` — atlas page images;
- `sequence-manifest.json` — engine-neutral truth;
- `atlas.json` — machine-readable page and region placement.

Always set `animation_kind` to `flipbook`. Never describe this output as bone animation, mesh
deformation, IK, Live2D motion, or editable body-part animation.

## QA

Load the package with the exact target runtime/editor version when available. Verify frame order,
delay, one-shot/loop behavior, pivot, alpha blending, atlas region lookup, and page-size limits.
Without a matching runtime, mark visual/runtime QA as pending even if structural validation passes.

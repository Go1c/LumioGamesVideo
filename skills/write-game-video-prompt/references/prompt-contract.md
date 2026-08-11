# Game Video Prompt Contract

## Output order

Write every prompt package in this order:

1. **Goal** — one sentence describing the intended player/viewer effect.
2. **Reference roles** — asset ID, what to retain, and what not to copy.
3. **Immutable facts** — identity, costume, product form, environment, UI layout, verified gameplay
   facts, dialogue, and brand colors.
4. **Timeline** — explicit time ranges with one dominant event per range.
5. **Camera and composition** — shot size, lens/FOV intent, camera path, subject scale, safe areas.
6. **Visual behavior** — motion, lighting, particles, transition, and end state.
7. **Audio** — dialogue, sound effects, ambience, music, or an explicit silent-master requirement.
8. **Negative constraints** — cuts, drift, extra subjects/limbs, altered text, new props, zoom,
   camera shake, false UI, or invented gameplay.
9. **Delivery** — duration, aspect ratio, resolution, FPS, loop behavior, and output variants.

## Mode-specific rules

| Mode | Use when | Required prompt detail |
|---|---|---|
| text-to-video | Identity and continuity do not matter | Describe the full subject and scene |
| image-to-video | One approved frame anchors identity/layout | State what must remain unchanged |
| first-frame-to-video | The clip must leave a known state | Describe motion away from the first state |
| first-last-frame-to-video | The clip must arrive at a known state | Describe a plausible path between endpoints |
| reference-to-video | Multiple images/video/audio have distinct roles | Map each asset to identity, motion, camera, or sound |
| video-to-video | Source timing/motion is primary | State permitted and forbidden transformations |

Do not use one reference vaguely for every purpose. A motion reference does not grant permission to
copy a person's identity; a character image does not define camera movement; gameplay footage does
not authorize invented mechanics.

## Candidate log

For every candidate record job ID, prompt revision, provider/model, mode, seed, source hashes,
render time, cost when known, rejection reason, and selected status. Do not delete rejected
metadata when comparing provider or prompt performance.

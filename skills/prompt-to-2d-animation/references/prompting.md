# Anchor and Video Prompting

## Mode selection

| Available input | Preferred mode | Notes |
|---|---|---|
| Text only | Generate an anchor image, then image-to-video | Use direct text-to-video only for disposable concepts |
| One character image | First-frame image-to-video | Preserve identity and camera framing |
| Same start/end image | First-and-last-frame video | Useful loop constraint; still requires seam QA |
| Character plus motion reference | Multi-reference/video-reference mode | Explicitly bind identity and motion sources |
| Existing video | No generation | Inspect, trim, matte, and package |

## Character anchor

The anchor should show one unobstructed 2D game character, the requested view, complete moving
silhouette, stable proportions, clean line art, limited palette, and a flat background color that
does not occur in the character. Exclude text, UI, scenery, particles, motion blur, cast shadows,
cropping, and extra props.

Record these invariants:

- face and hair silhouette;
- costume panels and colors;
- body proportions and view direction;
- held item shape, hand, and side;
- canvas occupancy and ground/pivot position;
- key color or matte strategy.

## Video prompt structure

Write the final prompt in this order:

1. **Format** — 2D game animation, fixed camera, single continuous shot.
2. **Identity invariants** — exact character features and costume to preserve.
3. **Starting pose** — feet/root, hands, weapon, gaze, silhouette.
4. **Timed action** — anticipation, main action, overshoot, settle.
5. **End state** — return to anchor for loops or hold a clear final pose for one-shots.
6. **Background/matte** — flat contrasting color, no shadows or background motion.
7. **Negative constraints** — no cuts, zoom, camera shake, text, new props, extra limbs,
   costume changes, scale changes, crop, or style drift.

## Timing examples

### One-shot inside a provider's four-second minimum

```text
0.0–0.8s: hold the approved starting pose, only subtle breathing.
0.8–1.1s: anticipation, weight shifts back, sword draws behind the shoulder.
1.1–1.6s: one fast forward slash with a clear readable arc.
1.6–2.2s: overshoot and controlled recovery into a stable final pose.
2.2–4.0s: hold the final pose; no secondary action or camera movement.
```

Extract only the useful action window after generation.

### Idle loop

```text
0–4s: one slow breathing cycle. Torso rises and falls once, eyes blink once near the midpoint,
hair tips and cloth settle back to their exact starting positions by 4.0s. Camera and feet remain
locked. The first and last pose match.
```

## Failure handling

- Identity drift: strengthen invariant descriptions and reuse the anchor; do not add more action.
- Extra limbs or warped weapon: simplify the pose/action and reduce motion amplitude.
- Background contamination: switch to a non-conflicting key color or a segmentation tool.
- Crop/scale drift: increase negative space in the anchor and repeat locked-camera constraints.
- Loop pop: reduce secondary motion and use the same start/end anchor when supported.

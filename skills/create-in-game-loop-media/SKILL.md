---
name: create-in-game-loop-media
description: Design, generate, repair, measure, encode, and package looping video textures for in-game televisions, billboards, terminals, surveillance feeds, holograms, fictional advertisements, news screens, tutorials, and ambient world media. Use for seamless or intentionally hidden-loop video assets, first/last-frame generation, loop seam QA, playback budgets, or world-building media; do not use for interactive UI or assume first/last-frame conditioning guarantees a seamless loop.
---

# Create In-Game Loop Media

Create world-building video that survives repeated playback and the target device's viewing
conditions. Treat a matching first/last anchor as a generation constraint, not proof of a seamless
loop.

## 1. Define the playback contract

Read [references/loop-production.md](references/loop-production.md). Record:

- in-world device, physical viewing distance, aspect ratio, resolution, color/emissive treatment;
- loop duration, audio trigger behavior, codec/container, target platform, and memory/bandwidth cap;
- fictional brand facts, required text/logo, and whether deterministic overlays are available;
- acceptable seam-hiding device such as a blink, glitch, occlusion, wipe, darkness, or static.

Keep important typography as an overlay or precomposed deterministic plate.

## 2. Design the loop

Choose one strategy:

- genuinely periodic motion with the same approved first/last anchor;
- a deliberate diegetic transition that hides the seam;
- postproduction trim and crossfade;
- a ping-pong loop only when reversing motion and audio remains plausible.

Use `$write-game-video-prompt` with workflow `in-game-loop`. Prefer first-last-frame generation
for a constrained endpoint and generate a small motion-intensity sweep.

## 3. Repair and measure

Review at least three consecutive cycles. Use the bundled analyzer on a candidate or master:

```bash
python scripts/analyze_loop.py candidate.mp4 --json
```

The numeric seam result is a comparison signal, not a perceptual pass. Reject visible identity,
logo, lighting, camera, or audio discontinuities even when the metric is low.

## 4. Package

Deliver:

- loop brief, brand/reference manifest, job, prompts, and candidate log;
- mezzanine master plus target-platform encodes;
- exact duration, dimensions, FPS, codec, average bitrate, file size, and estimated aggregate
  storage for the requested asset count;
- seam analysis, three-cycle preview, audio trigger recommendation, `provenance.json`, and
  `qa-report.json`.

Do not claim engine compatibility without testing the named engine/platform import and playback
path.

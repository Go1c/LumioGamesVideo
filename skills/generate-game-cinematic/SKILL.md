---
name: generate-game-cinematic
description: Plan, generate, select, assemble, and review short game cinematics, mission briefings, boss reveals, dialogue scenes, story transitions, and cutscene prototypes from story beats plus optional character, environment, gameplay, camera, or audio references. Use for flattened cinematic video deliverables; do not use when the user needs an editable engine timeline, camera track, skeletal animation, or gameplay implementation.
---

# Generate Game Cinematic

Create short, editable-by-shot cinematic packages rather than forcing a long sequence into one
generation. Treat generated video as a flattened cinematic, not a Unity Timeline, Unreal Sequencer,
camera path, animation graph, or proof of gameplay.

## 1. Lock the cinematic contract

Read [references/shot-contract.md](references/shot-contract.md). Define:

- narrative purpose and the player knowledge before and after the scene;
- target duration, aspect ratio, delivery platform, and transition into/out of gameplay;
- continuity bible for every recurring character, prop, environment, palette, and voice;
- dialogue, subtitles, soundscape, music, and silent-master requirements;
- facts that must remain deterministic in engine or postproduction.

Do not start rendering until contradictory references have been resolved.

## 2. Build the shot plan

Split the scene into 4–15 second shots when using H3-class short-video models. Give each shot one
dominant action and explicit start/end states. Reuse the continuity bible and approved anchors
across shots. Prefer a real gameplay frame as the final anchor when a shot must transition into
play.

Use `$write-game-video-prompt` to create one validated `game-video-job.json` and prompt package
per shot. Use reference-to-video for identity, motion, camera, or audio transfer; otherwise prefer
anchor-driven image-to-video over unconstrained text-to-video.

## 3. Generate and select

Apply the remote, paid-generation, rights, and license gate before rendering. Generate within the
approved variant budget. Score candidates independently for identity, action, composition, camera,
continuity, dialogue/audio timing, transition suitability, and artifacts.

Reject rather than repair a shot with a wrong character, missing story beat, broken limb, invented
prop, false text, or incompatible start/end state.

## 4. Assemble and verify

Assemble only approved shots. Keep deterministic titles, quest text, legal text, and UI in a
separate overlay or engine layer. Normalize codec, dimensions, frame rate, color, loudness, and
handles. Review the full sequence, not only individual clips.

Deliver:

- `cinematic-brief.md` and `continuity-bible.json`;
- `shot-plan.json`, one job/prompt package per shot, and candidate decision log;
- selected source clips, edit decision list or project handoff, final master, and optional silent
  master;
- `provenance.json` and `qa-report.json`;
- a clear statement that the result is flattened video.

When rendering is unavailable, deliver the complete plan-only package and mark all visual/audio QA
as pending.

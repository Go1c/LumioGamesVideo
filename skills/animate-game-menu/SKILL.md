---
name: animate-game-menu
description: Turn a static title screen, character-select screen, player card, menu mockup, UI screenshot, or Figma export into a generated animated background or attract-mode video while preserving deterministic interactive UI in the game engine. Use for menu motion, character entrances, ambient backgrounds, card reveals, lobby intros, and non-interactive UI cinematics; do not use to implement functional buttons or application state.
---

# Animate Game Menu

Generate the moving visual layer while keeping clickable, readable, and stateful UI deterministic.
The output is a background plate or attract-mode video, not a functioning menu.

## 1. Split deterministic and generative layers

Read [references/ui-motion-contract.md](references/ui-motion-contract.md). Keep these in engine or
postproduction unless the user explicitly accepts rasterized text risk:

- title, logo, player names, price, legal text, buttons, icons, counters, focus state, and cursor;
- localization-sensitive strings;
- anything whose position or value changes with game state.

Allow the video layer to contain character motion, environmental animation, particles, lighting,
decorative card movement, and non-semantic texture.

## 2. Approve a confirmation frame

Build one static frame at the target aspect ratio and safe area. Lock character identity, layout,
visual hierarchy, background separation, and reserved overlay regions. Correct text and logo errors
before animation; do not ask the video model to repair them.

Use `$write-game-video-prompt` to create an image-to-video or first-last-frame job. For a looping
menu background, also apply `$create-in-game-loop-media`.

## 3. Generate and select

Prefer a locked camera and low-to-moderate motion. Reject changed player identity, swapped cards,
moving safe areas, fake button states, unreadable overlays, camera moves that expose empty canvas,
or animation that competes with interaction.

## 4. Deliver the layer contract

Deliver:

- source UI specification and approved confirmation frame;
- layer map with generated background, deterministic overlays, masks, and safe areas;
- generation job, prompts, selected clean plate, and loop variant when requested;
- codec/color recommendations for the named target engine or platform;
- OCR/layout comparison, `provenance.json`, and `qa-report.json`.

When the source UI is unavailable, create a clearly labeled concept frame; do not present it as the
project's implemented menu.

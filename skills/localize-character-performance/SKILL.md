---
name: localize-character-performance
description: Create controlled game-character performance variants across actions, dialogue, voices, and languages using approved character images, motion video, source performance, scripts, or audio references. Use for NPC dialogue, emotes, quest-completion lines, multilingual character clips, motion transfer, lip-sync experiments, or identity-preserving performance video. Do not use without explicit likeness and voice rights or for automatically replacing an actor's authorized performance.
---

# Localize Character Performance

Keep character identity, camera, blocking, and emotional intent fixed while varying only the
approved action, dialogue, language, or voice dimension.

## 1. Pass the rights gate

Read [references/performance-contract.md](references/performance-contract.md). Record the source,
rights holder, allowed languages, allowed lines, commercial scope, retention policy, and explicit
consent for every recognizable likeness, motion performance, and voice reference.

Having a recording does not imply permission to synthesize new lines. Stop at plan-only when the
authorization is unknown or narrower than the requested output.

## 2. Create the performance lock

Define:

- approved character anchor and immutable face, costume, palette, silhouette, and proportions;
- source blocking, camera, gesture beats, gaze, emotion, and start/end pose;
- source script plus human-approved translations;
- target duration and shared semantic/timing beats across languages;
- whether the output may use a synthetic voice, approved voice reference, or must remain silent.

Use `$write-game-video-prompt` to select reference-to-video or another supported mode and create
one job per language or controlled variant. Change only the variable under test.

## 3. Generate a controlled matrix

Use the same anchor, motion reference, composition, duration, generation settings, and seed groups
where the provider permits. Never mix arbitrary best takes if the user is evaluating cross-language
consistency. Keep source and generated audio separable when possible.

## 4. Review every version

Check character identity, blocking, key-event timing, extra/missing limbs, facial artifacts,
dialogue accuracy, pronunciation, lip-event timing, voice authorization, loudness, and camera
consistency. Use ASR only as a screening signal; a fluent reviewer must approve shipping dialogue.

Deliver:

- `rights-manifest.json` and `performance-bible.json`;
- source/target script and timing matrix;
- one generation job and prompt package per variant;
- selected clips and comparable scorecard;
- transcript/translation review, `provenance.json`, and `qa-report.json`.

Label synthetic or transformed performance as required by provider, contract, law, platform, or
storefront policy.

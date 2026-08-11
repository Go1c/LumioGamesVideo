# Cinematic Shot Contract

## Global brief

Record narrative purpose, player knowledge before/after, target duration, platform, aspect ratio,
rating constraints, dialogue, sound, music, gameplay transition, and whether the scene is final,
prototype, or pitch material.

## Continuity bible

For each recurring element record an asset ID plus immutable facts:

- character: face, body, costume, palette, silhouette, handedness, carried items, voice;
- environment: geography, time, weather, light direction, landmarks, damage state;
- prop: dimensions, color, location, ownership, state;
- camera: screen direction, lens/FOV intent, movement, horizon, subject scale;
- audio: room tone, recurring motif, pronunciation, loudness target.

## Per-shot fields

| Field | Requirement |
|---|---|
| shot_id | Stable lower-case ID |
| duration | Normally 4–15 seconds for H3 |
| start_state | Visible state before motion |
| dominant_action | One primary event |
| end_state | Required handoff to next shot/gameplay |
| references | Asset IDs with explicit roles |
| camera | Framing, movement, and forbidden movement |
| audio | Dialogue/SFX/ambience/music or silent |
| handles | Safe trim time before and after the useful beat |
| rejection rules | Objective reasons to discard a candidate |

## Review

Score identity, story-beat completion, composition, camera compliance, continuity, audio timing, and
artifacts from 1–5. Identity, story beat, and continuity must each score at least 4. Reject any
immutable-fact violation regardless of average score.

---
name: write-game-video-prompt
description: Turn a game-video brief and optional image, video, audio, UI, gameplay, or brand references into a provider-neutral generation job and model-ready prompt for text-to-video, image-to-video, first/last-frame, reference-to-video, or video-to-video workflows. Use for H3 prompts, FL2VA or Ref2VA mode selection, general game-video planning, or whenever another Lumio Games Video skill needs a shared prompt, rights, generation, provenance, and QA contract.
---

# Write Game Video Prompt

Compile an idea into a reproducible generation job. Keep the job provider-neutral until a provider
has been selected and its capabilities, cost, upload behavior, and license have been checked.

## Select the generation mode

- Use text-to-video only for concepts that do not need a persistent identity.
- Generate and approve an anchor, then use image-to-video, when identity or art direction matters.
- Use first-frame-to-video for a controlled entrance from an existing game or UI frame.
- Use first-last-frame-to-video for a required transition or loop candidate. This constrains the
  endpoints but does not prove a seamless loop.
- Use reference-to-video when images, motion video, gameplay, voice, or music must be retained.
- Use video-to-video when the source motion and timing should remain primary.

Read [references/prompt-contract.md](references/prompt-contract.md) before writing the final prompt.
Read [references/h3-adapter.md](references/h3-adapter.md) only when MiniMax H3 is selected.

## Create the source-of-truth job

Copy [assets/game-video-job.example.json](assets/game-video-job.example.json) or the matching file
under `assets/examples/`, adapt it, and keep one job per deliverable variant. Use these workflow
values:

- `cinematic`
- `character-performance`
- `menu-motion`
- `in-game-loop`
- `gameplay-previs`
- `marketing`
- `2d-animation`

Validate before generation:

```bash
python scripts/validate_job.py game-video-job.json
```

Do not invent absent assets. Record missing inputs as unresolved checks and keep
`generation.execution` set to `plan-only`.

## Apply the external-generation gate

Before a paid render or remote upload, state:

- provider and model;
- generation mode, duration, resolution, aspect ratio, audio behavior, and variant count;
- every file that will leave the machine;
- known territory, commercial-use, attribution, disclosure, likeness, voice, music, and IP risks.

Obtain confirmation before setting `provider_terms_approved`, `remote_upload_approved`, or
`paid_generation_approved` to `true`. Store credentials only in the host secret store.

## Write the prompt package

Produce:

1. a concise creative intent;
2. immutable subject and brand facts;
3. timed visual beats with one dominant event per beat;
4. camera, framing, scale, lighting, and transition constraints;
5. dialogue, soundscape, music, and silence instructions when applicable;
6. negative constraints for cuts, drift, typography, extra subjects, unwanted props, or false UI;
7. reference-role mapping that says what to retain from each asset;
8. provider-neutral prompt plus an optional provider-specific adaptation.

Never ask a video model to preserve important text when a deterministic engine, editor, or overlay
can render it exactly.

## Generate, select, and report

Generate no more than `generation.variants`. Reject candidates that violate any immutable fact or
mandatory QA check. Track provider, model, seed, prompt revision, source hashes, chosen candidate,
editing steps, and final hashes in `provenance.json`.

If compatible media tools are unavailable, deliver a plan-only package containing:

- `game-video-job.json`;
- provider-neutral and provider-specific prompts;
- reference manifest;
- expected commands or tool calls;
- unresolved capability, rights, cost, and QA checks.

Never claim that a video or asset was rendered when only the prompt package exists.

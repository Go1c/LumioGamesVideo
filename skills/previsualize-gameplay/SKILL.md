---
name: previsualize-gameplay
description: Use generated video to compare controlled visual hypotheses for gameplay cameras, combat readability, VFX intensity, lighting, boss reveals, encounter scale, environments, and greybox scenes before implementation. Use for gameplay previs, blockout visualization, art-direction tests, camera studies, VFX concept tests, or decision-making experiments. Always label outputs as concepts; never treat generated pixels as proof that mechanics, performance, physics, AI, networking, or controls are implementable.
---

# Previsualize Gameplay

Use video as a decision instrument, not as a fabricated gameplay demo. Every experiment must answer
a concrete production question and preserve a traceable gap between the concept and implementation.

## 1. Frame the decision

Read [references/experiment-contract.md](references/experiment-contract.md). Write one question and
2–4 mutually exclusive hypotheses, such as near/medium/wide camera or low/medium/high VFX density.
Define the audience, decision owner, deadline, success metrics, and implementation constraints.

Use standardized engine screenshots, FOV, player position, environment, character anchors, and
camera references. Mark unknown mechanics and performance limits rather than allowing the model to
invent them silently.

## 2. Build controlled variants

Use `$write-game-video-prompt` to create one job per hypothesis. Hold all non-tested variables
fixed, including duration, reference pack, composition, seed groups, and generation budget. Produce
at least three candidates per hypothesis when the approved budget permits.

Add a persistent `CONCEPT — NOT GAMEPLAY` label to any clip that may leave the internal review
context.

## 3. Evaluate and decide

Have design, art, and engineering score readability, emotional target, implementation difficulty,
technical risk, and divergence from current game state. Do not select solely on visual polish.
Document which hypothesis won, what was rejected, and what must be proven in the engine.

Deliver:

- `experiment-brief.md`, reference manifest, hypothesis matrix, and controlled job/prompt set;
- candidates with concept labels and blind review scorecard;
- decision record and next engine prototype task;
- later, an optional divergence report comparing the generated concept with the real implementation.

When no render capability exists, deliver the controlled experiment package with visual results
marked pending.

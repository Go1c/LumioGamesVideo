---
name: create-game-marketing-video
description: Plan, generate, edit, and review truthful game trailers, store-page videos, launch teasers, UA ads, social cuts, character teasers, DLC or skin showcases, and platform-specific 16:9, 1:1, or 9:16 variants from approved gameplay, key art, logos, copy, music, and brand references. Use for marketing video production and creative testing; do not invent gameplay features, mislabel generated scenes as gameplay, or rasterize critical legal and CTA text without deterministic review.
---

# Create Game Marketing Video

Create platform-ready marketing variants while preserving a visible boundary between real
gameplay, generated cinematic material, and deterministic copy.

## 1. Establish the truth boundary

Read [references/marketing-integrity.md](references/marketing-integrity.md). Build a claims sheet
that lists every depicted mechanic, character, item, environment, offer, price, release statement,
and call to action. Mark each fact as verified, illustrative, prohibited, or pending.

Classify every planned shot as:

- captured gameplay;
- generated cinematic or illustrative footage;
- UI/product render;
- deterministic text/logo/legal overlay.

Never use a generated interaction to imply an unavailable mechanic.

## 2. Design masters and variants

Define audience, platform, duration, safe areas, sound-on/off behavior, hook, proof, hero moment,
CTA, disclosure, and localization needs. Design a truth-preserving master beat sheet before making
16:9, 1:1, or 9:16 versions.

Use `$write-game-video-prompt` for generated shots and reference-to-video adaptations. Keep logos,
prices, ratings, legal copy, dates, store badges, and CTAs deterministic.

## 3. Generate, edit, and review

Apply asset, music, likeness, provider, platform, and paid-generation rights gates. Reject identity
drift, fictitious features, fake UI, incorrect product form/color, unreadable text, or a crop that
changes the claim. Preserve original gameplay timing when gameplay is the proof.

Run human review for brand, gameplay truth, platform policy, legal copy, audio rights, localization,
and AI disclosure before release.

Deliver:

- audience brief, claims sheet, asset/rights manifest, beat sheet, and shot labels;
- jobs, prompts, candidate log, selected shots, captions, and deterministic overlay package;
- mezzanine master and requested platform encodes;
- `provenance.json`, `qa-report.json`, disclosure decision, and creative-test identifiers.

When analytics are available, compare approved creative per GPU-hour and human-hour—not raw render
count alone.

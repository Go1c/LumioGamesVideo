# Vendor Source Notes

## Snapshot

The reference snapshot was copied on 2026-08-11 from:

`/Users/cui/Downloads/zealman-AutoDL镜像工作流`

The source uses several overlapping labels: the guide calls the image `v8.88`, the API HTML title
uses `v8.8`, and the workflow folders use `V9`. Preserve those labels rather than inventing a
normalized upstream version. The bundled documents also disagree on some ComfyUI versions and
active-workflow counts; verify the live instance before execution.

## Canonical material retained

| Material | Count |
|---|---:|
| `V9镜像内工作流/**/*.json` | 259 |
| `V9面板API-json/*.json` | 29 |
| `工作流说明/*.md` | 22 |
| Root guides/API/address files | 6 |
| Total files | 316 |

The copied set is about 22 MB. No model weights, generated user media, credentials, or executable
update archives are part of the skill.

## Material intentionally excluded

The download contained byte-identical `(1)` copies of both workflow trees, the category guides, and
all root files. Only the canonical non-`(1)` copy was retained. The following non-workflow binaries
were also excluded:

- duplicate panel update ZIP and DOCX packages under `zealman面板更新包*`;
- duplicate `comfyui_00044_*.mp4` demonstrations;
- duplicate `QQ群*.png` images.

The source scan found documentation and workflow fields that mention tokens or authorization, but no
long key-like credential values. Continue to treat every future refresh as untrusted input and scan
it before copying.

## Ownership and publication boundary

The vendor guide contains an explicit notice prohibiting secondary development and publication of
the image. This repository does not assert ownership or redistribution/derivative rights over the
imported JSON or documentation. Keep the corpus clearly marked as vendor reference, preserve it
unchanged, and obtain a rights decision before committing it to a public distribution.

Lumio-native workflows must be independently specified, authored, tested, and documented. A staged
copy is an experiment or execution artifact, not evidence of original authorship.

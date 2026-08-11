# QA Rubric

## Candidate video

Reject before extraction on any critical failure:

- changed identity, costume, view, palette, or character scale;
- extra/missing limb, unusable hand, broken weapon, or severe face deformation;
- camera pan/zoom/cut, character crop, or incomplete action;
- background cannot be separated without destroying the character.

## Cleaned sequence

Score 1–5:

| Dimension | Pass threshold |
|---|---:|
| Identity and style consistency | 4 |
| Limb and silhouette correctness | 4 |
| Action readability/completion | 4 |
| Frame-to-frame stability | 4 |
| Alpha/matte quality | 4 |
| Pivot stability | 4 |
| Loop seam, when applicable | 4 |

All applicable scores must average at least 4, with no critical failure. At 512×512, planted-foot
pivot drift should not exceed 2 pixels; scale proportionally for other canvases.

## Package

Require:

- sequential frame indices and identical dimensions;
- manifest FPS, duration, frame count, pivot, loop flag, and files agree;
- atlas regions cover every frame exactly once and stay within page bounds;
- Spine skeleton version is 4.1, 4.2, or 4.3 and matches the target runtime major/minor;
- sequence delay equals `1 / fps` within floating-point tolerance;
- one-shot uses `once`, loop uses `loop`;
- package is labeled `flipbook`, not `skeletal`;
- disk size, atlas pages, page dimensions, and approximate RGBA memory are reported.

## Status vocabulary

- `passed`: structural and visual/runtime checks completed successfully.
- `data-passed-visual-pending`: files validate but no matching viewer/runtime was available.
- `failed`: at least one required check failed.
- `blocked`: required tool, right, provider authorization, matte, or source input is unavailable.

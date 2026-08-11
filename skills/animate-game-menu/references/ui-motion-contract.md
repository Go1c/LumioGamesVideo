# UI Motion Layer Contract

## Layer split

| Layer | Default owner | Examples |
|---|---|---|
| Generated motion plate | Video model | character idle, particles, fog, lighting, decorative cards |
| Deterministic visual overlay | Engine/editor | logo, title, button labels, player names, icons, prices |
| Interactive state | Engine | focus, hover, selection, input, accessibility, dynamic counters |
| Audio | Engine/editor | UI cues, music stem, narration, accessibility feedback |

## Confirmation-frame gate

Approve target dimensions, safe areas, subject positions, hierarchy, overlay masks, palette, and
first/last state before video generation. Export an overlay guide with pixel coordinates or
normalized bounds.

## QA

- Compare generated frames against the confirmation frame for subject identity and reserved zones.
- Run OCR on any unavoidable rasterized text and verify manually.
- Test text expansion and right-to-left/localized layouts in the engine overlay.
- Review menu readability with the video playing, not only paused.
- For loops, review three cycles and apply the in-game loop workflow.

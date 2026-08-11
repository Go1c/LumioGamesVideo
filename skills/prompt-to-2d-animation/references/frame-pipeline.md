# Frame Processing Pipeline

## Runtime requirements

- Python 3.9 or newer
- FFmpeg and FFprobe on `PATH`
- Pillow 10 or newer

The scripts refuse to write into a non-empty output directory. Use a new revision directory rather
than overwriting prior results.

## Inspect before extracting

Run `scripts/inspect_video.py`. Record duration, dimensions, source FPS, pixel format, frame count,
and whether the source reports an alpha-capable pixel format.

The useful action window can be shorter than the provider clip. Set `--start` and `--duration` on
extraction. The product of delivery FPS and trimmed duration must not exceed 48 frames in v0.1.

## Extract and matte

`scripts/extract_frames.py` performs constant-FPS sampling, aspect-preserving scale, fixed-canvas
padding, and optional chroma key removal. It does not provide semantic segmentation.

Recommended defaults:

| Field | Default |
|---|---:|
| Delivery FPS | 12 |
| Canvas | 512×512 |
| Maximum frames | 48 |
| Pixel format | Straight RGBA PNG |
| Naming | `<clip-id>_0000.png` onward |

Choose a key color absent from the character. Green is not safe for green costumes, green effects,
or translucent yellow edges. Inspect hair, weapon holes, motion blur, and semi-transparent effects
after keying. When chroma key is unsuitable, use a host segmentation/matting tool and preserve the
same naming and canvas contract.

## Stabilize carefully

`scripts/stabilize_sequence.py` supports:

- `none`: copy to a normalized frame set without shifting;
- `alpha-bottom-center`: align the alpha bounding box bottom center;
- `alpha-center`: align the alpha bounding box center.

Bbox alignment is appropriate for planted idle/emote clips on a clean alpha matte. It is not
appropriate for jumps, dashes, root motion, or actions where a weapon changes the alpha bounds.
Those clips require `none` or a manually chosen pivot.

The script fails rather than cropping non-transparent pixels after a shift.

## Atlas and memory budget

Every frame is a full RGBA texture region. Approximate uncompressed GPU memory before compression:

```text
width × height × 4 bytes × frame count
```

Examples:

- 512×512 × 24 frames ≈ 24 MiB
- 512×512 × 48 frames ≈ 48 MiB
- 1024×1024 × 24 frames ≈ 96 MiB

This is why v0.1 defaults to 512×512 at 12 FPS. Reduce resolution or frames for mobile targets.
The atlas builder uses one or more pages up to the configured maximum page size.

## Frame acceptance checks

- identical canvas size and RGBA mode;
- consecutive zero-padded indices with no missing frame;
- no empty alpha frame;
- no black/white/key-color fringe around the silhouette;
- no unexplained scale, crop, or pivot jump;
- one-shot contains the complete action window;
- loop first/last transition remains invisible for three cycles.

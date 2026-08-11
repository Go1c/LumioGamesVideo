# In-Game Loop Production

## Strategy selection

1. Prefer genuinely periodic motion for fans, hologram pulses, idle mascots, or ambient effects.
2. Use the same approved endpoint anchor for first/last-frame generation when supported.
3. Hide difficult seams behind an in-world blink, glitch, wipe, occluder, static burst, or darkness.
4. Use trim/crossfade only when it does not create double images, motion reversal, or audio phase
   artifacts.
5. Use ping-pong only for reversible motion and silent or separately looped audio.

## Seam review

Review three cycles at normal speed and frame-step the boundary. Check subject pose, camera,
lighting, particles, typography/logo, compression, and audio click. Numeric first/last-frame
difference is useful for ranking candidates but cannot certify a seamless loop.

## Delivery record

Record duration, FPS, pixel dimensions, aspect ratio, codec/profile, pixel format, alpha, audio
codec/channels/rate, average bitrate, file size, color metadata, and tested engine/platform.

Estimate aggregate storage:

```text
total megabytes ≈ average megabits/second × seconds × asset count ÷ 8
```

For distant screens, reduce resolution and consider silent playback. Trigger localized audio only
near the device when appropriate.

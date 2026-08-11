#!/usr/bin/env node
/* Optional integration check. Requires @esotericsoftware/spine-core matching the package version. */

const fs = require("fs");
const path = require("path");
const spine = require("@esotericsoftware/spine-core");

if (process.argv.length !== 3) {
  console.error("usage: node tests/validate_spine_runtime.cjs <package-dir>");
  process.exit(2);
}

const packageDir = path.resolve(process.argv[2]);
const manifest = JSON.parse(
  fs.readFileSync(path.join(packageDir, "sequence-manifest.json"), "utf8"),
);
const clipId = manifest.clip_id;
const atlas = new spine.TextureAtlas(
  fs.readFileSync(path.join(packageDir, `${clipId}.atlas`), "utf8"),
);
const parser = new spine.SkeletonJson(new spine.AtlasAttachmentLoader(atlas));
const data = parser.readSkeletonData(
  JSON.parse(fs.readFileSync(path.join(packageDir, `${clipId}.json`), "utf8")),
);
const animation = data.findAnimation(clipId);

if (!animation) throw new Error(`animation not found: ${clipId}`);
if (Math.abs(animation.duration - manifest.duration_seconds) > 1e-9) {
  throw new Error(
    `duration mismatch: runtime=${animation.duration}, manifest=${manifest.duration_seconds}`,
  );
}

console.log(
  JSON.stringify({
    clip_id: clipId,
    bones: data.bones.length,
    slots: data.slots.length,
    skins: data.skins.length,
    animations: data.animations.length,
    duration_seconds: animation.duration,
  }),
);

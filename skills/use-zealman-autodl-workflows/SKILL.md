---
name: use-zealman-autodl-workflows
description: Select, inspect, stage, adapt, and run the imported Zealman AutoDL ComfyUI v8.88/V9 UI and panel-API workflow library for image, video, storyboard, lip-sync, voice, motion-transfer, character-replacement, upscaling, batch, and concurrent-generation tasks. Use when the user mentions Zealman, AutoDL, the imported mirror workflows, a workflow prefix such as A/G/H/J/P/U, or asks to render a Lumio game-video job through that environment. Keep the bundled vendor corpus immutable, do not treat UI and API JSON as interchangeable, and do not upload assets, spend credits, create or release instances, or publish vendor materials without the required authorization.
---

# Use Zealman AutoDL Workflows

Use the imported Zealman bundle as a traceable execution adapter and learning reference. Keep the
project's provider-neutral game-video skills as the creative source of truth; use this skill to map
their jobs onto a concrete ComfyUI workflow.

## Locate the reference corpus

Treat `assets/vendor/zealman-autodl-v8.88/` as immutable vendor material. Read
[references/source-notes.md](references/source-notes.md) before redistributing or deriving a new
Lumio workflow from it.

Use these canonical locations:

- `V9镜像内工作流/`: 259 ComfyUI UI-graph JSON files for interactive import and editing;
- `V9面板API-json/`: 29 prompt/API JSON files containing `_api_config` parameter mappings;
- `工作流说明/`: one detailed guide per workflow category;
- `Codex镜像功能指引.md`: environment paths, service rules, workflow routing, and API sequence;
- `zealman-api接口说明.html`: bundled panel endpoint reference.

Do not load the whole corpus into context. Search first, then read only the matching category guide
and selected JSON.

## 1. Define the job and pass the rights gate

Apply the matching Lumio skill first when the request is a cinematic, character performance, menu,
loop, gameplay previs, marketing video, or 2D animation. Use `$write-game-video-prompt` to establish
inputs, reference roles, generation mode, budget, remote-upload approval, and QA requirements.

Record the requested output, required inputs, duration, aspect ratio, audio behavior, target GPU,
and whether the user wants selection only, a staged workflow, interactive ComfyUI use, a single API
run, or concurrent generation. Require explicit likeness and voice permission for cloning or
replacement. Only remove watermarks or subtitles from material the user is authorized to alter.

## 2. Find and inspect candidates

Read [references/capability-map.md](references/capability-map.md), then search by intent, model, or
workflow prefix:

```bash
skill_root=skills/use-zealman-autodl-workflows
python3 "$skill_root/scripts/find_workflows.py" --query "首尾帧 LTX" --kind ui
python3 "$skill_root/scripts/find_workflows.py" --query "motion transfer" --kind api --json
```

Inspect each serious candidate before choosing it:

```bash
python3 "$skill_root/scripts/inspect_workflow.py" \
  "$skill_root/assets/vendor/zealman-autodl-v8.88/V9面板API-json/P07-动作迁移-Wan2.2AnimateV4.json"
```

Report the selected workflow, JSON kind, required image/video/audio/text inputs, exposed API
parameters, model filenames, custom-node types, likely GPU constraints, and why it is a better fit
than the nearest alternative. Start with a basic or documented workflow for the first test; use a
director, long-video, multi-reference, or high-resolution workflow only when its added complexity is
required.

## 3. Stage before changing anything

Never edit a file under `assets/vendor/`. Create a working copy and provenance sidecar:

```bash
python3 "$skill_root/scripts/stage_workflow.py" \
  "V9镜像内工作流/G视频-Wan图生/G01-图生视频-Wan2.2万相基础版.json" \
  game-video-output/job-001/workflows \
  --name lumio-job-001-wan-i2v.json
```

Keep each revision in a new file or output directory. Preserve the sidecar's source path and SHA-256
when adapting node values, API mappings, or model references.

## 4. Choose the correct execution path

Use a UI-graph JSON to open and debug inside ComfyUI. On a Zealman instance, place only an authorized
staged copy under `/root/ComfyUI/user/default/workflows/<分类>/` and leave the preinstalled original
intact.

Use an API JSON only when `_api_config` and enabled parameters have been inspected. Place an
authorized staged API copy under `/root/zealman-app/workflows/`. A UI graph is not a valid API payload;
first run it in ComfyUI and convert it through the panel's “API 生成” flow.

Before touching a live instance, read the complete bundled `Codex镜像功能指引.md`. Operate only on
the documented user-visible `/root/zealman-app`, `/root/ComfyUI`, and `/root/并发` paths. Respect its
read-only files, symlinks, and CUDA/PyTorch constraints.

Resolve the panel base URL and credentials from the active session, user input, or a secret store.
Never save an AutoDL token, bearer token, credential, or signed URL in this repository, a workflow,
the shell history, provenance, or logs. A read-only health/status check is safe; instance creation,
uploads, configuration writes, generation, batch execution, stop/release actions, and paid compute
must remain within the user's explicit request.

Before remote upload or generation, state the target instance, workflow and revision, files that
will leave the machine, model/GPU assumptions, resolution, duration, task count, likely cost scope,
and rights/retention risks. Obtain confirmation when those facts were not already explicitly
approved.

For panel API runs, follow the documented sequence: upload file inputs, connect WebSocket, submit
`/api/workflow/generate`, observe progress/history, then retrieve output. Use concurrent endpoints
only for an explicitly approved batch and cap the first smoke test to one small task.

## 5. Verify and hand off

Verify service health, workflow JSON kind, enabled parameters, model files, custom nodes, input
paths, GPU headroom, output history, and the downloaded artifact. Run the relevant Lumio visual,
audio, continuity, loop, truthfulness, or 2D-package QA after generation.

Deliver:

- selected source path and SHA-256 plus the staged workflow and sidecar;
- input-to-parameter mapping and unresolved model/custom-node dependencies;
- exact execution mode, target, task count, and approval state;
- prompt/job revision, output paths, provider/instance facts, and cost when available;
- actual QA results and a truthful `plan-only`, `staged`, `rendered`, or `failed` status.

## 6. Distill Lumio-native workflows cleanly

Keep vendor references and Lumio-authored work separate. Record the production need, observed
behavior, independent node/design decisions, tests, and license review for every new Lumio workflow.
Do not rename a vendor JSON and claim it as original work. Do not publish the imported bundle or a
derivative until the repository owner has confirmed redistribution and derivative-use rights.

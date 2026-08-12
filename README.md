# Lumio Games Video

一个符合 [Agent Plugins 1.0.0](https://agent-plugins.org/) 的通用游戏视频生产插件。它把
提示词和可选的图片、视频、音频、UI、Gameplay、Logo 等参考素材，编译成可复现的生成
任务、候选筛选、后处理、QA 和游戏交付流程。

插件覆盖原调研中的六条路线，并增加提示词生成 2D 角色动作、序列帧与 Spine
Flipbook 的专项能力。核心保持 provider-neutral；MiniMax H3 是可选适配器，不是强制
依赖。

## 九个 Skill

| Skill | 功能 | 主要产物 |
|---|---|---|
| `write-game-video-prompt` | 公共提示词、模式选择、参考映射、权利与生成任务编排 | `game-video-job.json`、prompt package |
| `use-zealman-autodl-workflows` | 检索、检查、暂存并执行项目内的 Zealman AutoDL/ComfyUI 参考工作流 | workflow copy、source sidecar、参数映射、执行记录 |
| `generate-game-cinematic` | 剧情过场、任务简报、Boss Reveal、转场 | continuity bible、shot plan、cinematic master |
| `localize-character-performance` | 角色动作迁移、对白表演和多语言版本 | rights manifest、timing matrix、localized clips |
| `animate-game-menu` | 主菜单、选人、Player Card 和开场 UI 动态背景 | confirmation frame、motion plate、UI layer contract |
| `create-in-game-loop-media` | 电视、广告牌、终端、监控、新闻等循环视频纹理 | loop master、平台编码、seam report |
| `previsualize-gameplay` | 镜头、VFX、光照、Boss 和灰盒玩法视觉预演 | hypothesis matrix、concept clips、decision record |
| `create-game-marketing-video` | Trailer、商店页、UA、社媒、DLC/皮肤展示 | claims sheet、platform cuts、release QA |
| `prompt-to-2d-animation` | 提示词/参考图生成 2D 动作并转为游戏帧资产 | PNG sequence、atlas、Spine 4.1–4.3 Flipbook |

## 公共生产链路

```text
游戏视频需求
   ↓
参考素材与权利清单
   ↓
game-video-job.json
   ↓
T2V / I2V / 首尾帧 / Ref2V / V2V 模式选择
   ↓
多候选生成与拒绝日志
   ↓
工作流专项后处理和 QA
   ↓
游戏、商店、社媒或帧动画资产
```

没有兼容的图像/视频工具时，所有 Skill 都必须降级为 plan-only package，提供最终 job、
提示词、参考映射、预期工具调用和未完成的能力/权利/QA 检查，不能假装已经生成媒体。

## 典型用法

可以对 Agent 说：

- “把这个 Boss 出场故事点和角色设定图做成 12 秒游戏过场。”
- “保持这个 NPC 的表演和镜头，生成中英日三个对白版本。”
- “把这张角色选择界面做成动态背景，按钮和玩家名字仍由引擎绘制。”
- “为赛博朋克城市生成一批可循环的广告牌和电视视频。”
- “用三组镜头距离对比这个灰盒 Boss 战，但明确标成概念而非 Gameplay。”
- “从真实 Gameplay 生成 16:9 Trailer 和 9:16 社媒版，不得虚构功能。”
- “只给提示词，生成一个 Q 版剑士挥砍动作并输出 Spine Flipbook。”
- “用项目内的 Zealman AutoDL 工作流，为这个首尾帧任务选流、检查依赖并暂存一份可修改副本。”

## 通用任务契约

`write-game-video-prompt` 提供跨工作流的任务 Schema 和无额外依赖的校验器：

```bash
python3 skills/write-game-video-prompt/scripts/validate_job.py \
  skills/write-game-video-prompt/assets/game-video-job.example.json
```

任务会记录 workflow、参考素材角色、权利状态、生成模式、provider/model、执行位置、
付费与远程上传确认、交付格式和强制 QA。

每个候选的 seed、输入 hash、产物与取舍决定记录在 `decision-log.json`
（Schema 见 `skills/write-game-video-prompt/assets/decision-log.schema.json`）：

```bash
python3 skills/write-game-video-prompt/scripts/log_candidate.py \
  init --job game-video-job.json --log candidates/decision-log.json
```

## Zealman 执行链路

对已批准的 job，可在 Zealman AutoDL 面板上完成选流到出片的闭环：

```bash
skill=skills/use-zealman-autodl-workflows

# 1. 选流并暂存可修改副本（自动生成 provenance sidecar）
python3 "$skill/scripts/stage_workflow.py" "V9面板API-json/G02-首尾帧-Wan2.2首尾帧视频.json" \
  out/workflows --name lumio-flf.json

# 2. 把 job 的提示词、参考图、时长、seed 映射到工作流参数
python3 "$skill/scripts/apply_job.py" out/workflows/lumio-flf.json --list
python3 "$skill/scripts/apply_job.py" out/workflows/lumio-flf.json \
  --job game-video-job.json \
  --map "119:text=prompt:prompts/final.txt" \
  --map "145:image=asset:loop-first" \
  --map "182:seed=seed:random"

# 3. 上传、提交、轮询、下载，并写入 decision log 与 sidecar 状态
python3 "$skill/scripts/run_workflow.py" out/workflows/lumio-flf.run-request.json \
  --output-dir out/candidates --base-url "$ZEALMAN_BASE_URL" --register
```

runner 会拒绝 plan-only job 与未批准上传的远程执行；面板地址只在会话内使用，
不会写入任何文件。

## 循环媒体

对已有候选或 master 检查媒体信息和首尾显示帧差异：

```bash
python3 skills/create-in-game-loop-media/scripts/analyze_loop.py candidate.mp4 --json
```

数值只用于比较候选，不能代替连续播放三轮的视觉和音频检查。

## 2D 与 Spine

没有参考图时，`prompt-to-2d-animation` 会先要求生成并锁定角色锚点，再生成短动作
视频，最后抽取透明 PNG 帧、稳帧、生成 atlas 和 Spine sequence package。

Spine 输出属于 **Flipbook**：一个 root bone/slot 播放逐帧贴图。它不是自动拆件、
mesh、权重、IK 或可单独编辑肢体的骨骼动画。Live2D `.motion3.json` 需要既有参数
模型，同样不能由视频帧直接得到。

只处理已有视频时：

```bash
skill=skills/prompt-to-2d-animation

python3 "$skill/scripts/inspect_video.py" selected.mp4

python3 "$skill/scripts/extract_frames.py" selected.mp4 frames/raw \
  --clip-id swordsman-slash --fps 12 --size 512x512 \
  --start 1.0 --duration 1.5 --chroma-key 0x00FF00

python3 "$skill/scripts/stabilize_sequence.py" frames/raw frames/cleaned \
  --clip-id swordsman-slash --mode alpha-bottom-center

python3 "$skill/scripts/build_spine_flipbook.py" frames/cleaned package \
  --clip-id swordsman-slash --fps 12 --once \
  --spine-version 4.1 --pivot bottom-center

python3 "$skill/scripts/validate_package.py" package
```

## 包结构

```text
plugin.json
.codex-plugin/plugin.json
skills/
├── write-game-video-prompt/
├── use-zealman-autodl-workflows/
├── generate-game-cinematic/
├── localize-character-performance/
├── animate-game-menu/
├── create-in-game-loop-media/
├── previsualize-gameplay/
├── create-game-marketing-video/
└── prompt-to-2d-animation/
tests/
SPEC.md
```

任何支持 Agent Plugins/Agent Skills 的客户端都可以读取根 `plugin.json` 与
`skills/`；不支持 Codex manifest 的客户端可以忽略 `.codex-plugin/`。

## 运行要求

Plan-only 只需要能读取 Agent Skill 的客户端。媒体分析和 2D 帧处理需要：

- Python 3.9+
- FFmpeg 与 FFprobe
- Pillow 10+

```bash
python3 -m pip install -r requirements.txt
```

图像、视频、音频生成和语义抠图由宿主 Agent 的可用工具提供。插件不保存 API token，
也不内置模型权重、视频 provider、Spine Editor 或 Spine Runtime。Zealman 参考集只保留
工作流 JSON 与说明文件，不包含更新包、演示视频或用户生成素材。

## 开发验证

```bash
python3 -m unittest discover -s tests -v

for skill in skills/*; do
  python3 /path/to/skill-creator/scripts/quick_validate.py "$skill"
done

python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

产品边界、工作流契约和验收标准见 [SPEC.md](SPEC.md)。仓库尚未选择开源许可证；确定
许可证前请勿把本包作为已授权的公开发行物重新分发。导入的 Zealman vendor 参考资料另有
禁止二次开发后发布的声明，在权利确认前同样不得公开分发或宣称为 Lumio 原创。

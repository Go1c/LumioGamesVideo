# Lumio Games Video Plugin v0.1 执行规范

状态：Draft

规范日期：2026-08-11

目标版本：`0.1.0`

## 1. 产品定义

本仓库 MUST 交付一个符合 Agent Plugins 1.0.0 的通用插件，把游戏相关的文字需求和
可选图片、视频、音频、UI、Gameplay、Logo 等参考素材，编译为可执行的视频生产任务。

插件定位来自调研报告的核心结论：

> 视频模型近期最适合成为 game engine 周围的 multimodal video compiler，而不是替代
> game engine、Gameplay 逻辑或实时渲染器。

v0.1 MUST 覆盖调研中的六类工作流：

1. 剧情过场与任务简报；
2. 角色表演、动作迁移与多语言本地化；
3. 动态菜单、角色选择与开场 UI；
4. 游戏世界内视频资产与循环媒体；
5. 概念验证、镜头预演与玩法视觉原型；
6. 营销、商店页、UA 与社媒短视频。

此外，v0.1 MUST 包含用户重点提出的第七类工作流：

7. 提示词/参考图生成 2D 角色动作，再转为透明序列帧、sprite atlas 和 Spine
   Flipbook。

MiniMax H3 MAY 是首个参考适配器，但插件核心 MUST provider-neutral。宿主没有媒体
生成能力时 MUST 输出 plan-only package，不得宣称已经生成视频。

`use-zealman-autodl-workflows` MAY 把项目内导入的 Zealman AutoDL/ComfyUI 工作流作为
具体执行适配器，但它 MUST 保持 vendor 参考只读，不得把该适配器变成公共 job 契约的
强制依赖。

## 2. 核心边界

插件生成的是离线或准离线视频和帧资产。它 MUST NOT：

- 宣称生成视频等于可玩的 Gameplay；
- 宣称 flattened cinematic 等于 Unity Timeline、Unreal Sequencer 或相机轨迹；
- 把动态菜单视频当作真正的可交互 UI；
- 把视频帧当作自动生成的 Spine 骨骼、mesh、权重或 Live2D 参数；
- 用生成的攻击画面推断命中帧、碰撞、AI、物理、网络或性能；
- 自动获得角色、演员、声音、音乐、Logo、品牌或 Gameplay 素材的使用权；
- 在缺少 provider、模型、上传、付费或地域许可确认时执行对应外部生成。

## 3. 插件与 Skill 架构

```text
lumio-games-video
├── write-game-video-prompt              # 公共编排层
├── use-zealman-autodl-workflows         # 可选 Zealman/AutoDL 执行适配器
├── generate-game-cinematic              # 调研方向 1
├── localize-character-performance       # 调研方向 2
├── animate-game-menu                    # 调研方向 3
├── create-in-game-loop-media             # 调研方向 4
├── previsualize-gameplay                 # 调研方向 5
├── create-game-marketing-video           # 调研方向 6
└── prompt-to-2d-animation                # 新增重点方向 7
```

### 3.1 Skill 契约总表

| Skill | 触发输入 | 强制产物 | 硬边界 |
|---|---|---|---|
| `write-game-video-prompt` | 任意游戏视频想法和参考素材 | 通用 job、参考角色映射、最终提示词、生成/权利/QA 计划 | 不直接假装完成媒体生成 |
| `use-zealman-autodl-workflows` | Zealman/AutoDL、镜像工作流、前缀或已完成的游戏视频 job | 选流理由、依赖与参数映射、staged copy、source sidecar、执行状态 | vendor 只读；UI/API JSON 不混用；无授权不上传、付费或发布 |
| `generate-game-cinematic` | story beat、角色/场景、镜头或 Gameplay 过渡 | continuity bible、shot plan、逐镜头 job、master | flattened video 不是引擎 timeline |
| `localize-character-performance` | 角色、动作、脚本、语言或声音参考 | rights manifest、performance lock、timing matrix、版本评分 | 无肖像/声音授权不得渲染 |
| `animate-game-menu` | UI 截图/Figma、角色卡、Logo、菜单布局 | confirmation frame、motion plate、overlay/safe-area contract | 视频不是交互 UI |
| `create-in-game-loop-media` | 广告牌、电视、终端等世界内媒体需求 | loop master、三轮预览、seam report、平台编码 | 首尾帧约束不等于无缝 |
| `previsualize-gameplay` | 灰盒、镜头/VFX/光照假设 | 实验 brief、控制变量 job、decision matrix | 必须标记 Concept，不得冒充 Gameplay |
| `create-game-marketing-video` | Gameplay、KV、Logo、文案、音乐、平台 | claims sheet、shot labels、平台 cuts、release QA | 不得虚构产品功能 |
| `prompt-to-2d-animation` | 动作提示词和可选参考图/视频 | 透明 PNG、manifest、atlas、可选 Spine package | Spine 仅为 Flipbook，不是自动 rig |

每个 Skill 的 frontmatter description MUST 同时说明功能、触发场景和不适用边界。
Skill 正文 MUST 使用命令式流程，并按需链接一层深度的 references、scripts 和 assets。

### 3.2 调研 Skill 映射

| 调研/官方 Skill | 本插件落点 | 处理方式 |
|---|---|---|
| `h3-prompt-writing` | `write-game-video-prompt` | 保留结构化提示词逻辑，改为 provider-neutral，H3 作为 adapter |
| `3d-animation-short-generator` | `generate-game-cinematic`、`previsualize-gameplay` | 重写 story/anchor/shot/assembly SOP |
| `co-op-game-intro-generator` | `animate-game-menu` | 重写为“视频背景 + 引擎 UI”分层工作流 |
| `brand-promo-video-generator` | `create-game-marketing-video`、`create-in-game-loop-media` | 复用 brand facts、provenance、beat、shot 和 review |
| `minimalist-product-ad-generator` | marketing/loop references | 作为产品/皮肤/世界内广告方法，不设重叠顶层触发 |
| `music-video-subtitle-generator` | marketing 工作流 | 作为节奏、字幕和角色曲模板，不设重叠顶层触发 |
| paper/collage/handdrawn Skills | 后续 style presets | v0.1 不作为核心基础设施；可在 cinematic/marketing 内选用 |
| Zealman AutoDL v8.88/V9 本地快照 | `use-zealman-autodl-workflows` | 作为只读 vendor 选流与执行适配器；不宣称所有权或发布权 |

这种映射遵循调研提出的三层策略：直接集成公共提示词逻辑、重写高价值游戏生产 SOP、
把低优先级视觉风格保留为模板，而不是把九个官方 Skill 原样复制并继续依赖 Hub Canvas。

## 4. 公共任务契约

`write-game-video-prompt/assets/game-video-job.schema.json` 是所有视频工作流的公共
source of truth。每个 job MUST 记录：

- `workflow`：七类业务工作流之一；
- `goal`：可验证的创意或生产目标；
- `inputs.assets[]`：素材 ID、类型、来源、在提示词中的角色、权利状态和远程上传许可；
- `generation`：provider/model、T2V/I2V/首尾帧/Ref2V/V2V 模式、时长、比例、分辨率、
  音频、候选数、plan-only/local/remote、provider 条款和付费确认；
- `delivery`：交付类型、loop、FPS 和容器；
- `rights`：公开发布与 AI 披露决定；
- `qa_checks`：该工作流不可省略的检查。

生成前 MUST 执行：

```bash
python skills/write-game-video-prompt/scripts/validate_job.py game-video-job.json
```

专项工作流 MAY 增加自己的 schema。例如 2D 动画继续使用
`animation-job.schema.json` 约束帧数、canvas、alpha、pivot 和 Spine 版本。

## 5. 公共生产门

### Gate 0 — 意图与交付

明确用户要解决的生产问题、观众、平台、时长、比例、音频、版本数量和最终可导入产物。
不得只记录“做得更酷”之类无法验收的目标。

### Gate 1 — 素材与权利

对每项图片、视频、声音、演员、音乐、Gameplay、Logo 和文案记录来源与允许用途。
可识别人物和声音必须有具体、明确的生成式处理许可。权利未知时只允许 plan-only。

### Gate 2 — 模式与 provider

按控制需求选择：

| 需求 | 默认模式 |
|---|---|
| 无身份连续性要求的概念 | T2V |
| 角色、产品、场景或 UI 需要锁定 | 先做 anchor，再 I2V |
| 必须从已知画面开始 | First-frame |
| 必须到达已知画面或尝试循环 | First+last-frame |
| 图片、动作视频、Gameplay、声音需要分别保留 | Ref2V |
| 源视频的运动/时序必须占主导 | V2V |

在远程上传或付费生成前，Agent MUST 展示 provider/model、所有上传文件、时长、分辨率、
候选数、预计成本以及许可/披露风险，并取得确认。

### Gate 3 — Prompt package

最终提示词 MUST 包含创意目标、参考素材角色、不可变事实、时间段、镜头与构图、动作、
声音、负面约束和交付规格。每个时间段 SHOULD 只有一个主事件。

重要 Logo、价格、日期、法律文字、按钮、玩家 ID、字幕和 CTA SHOULD 由引擎或编辑器
确定性绘制，而不是依赖视频模型重画。

### Gate 4 — 候选与拒绝

不得超过 job 的候选预算。每条候选 MUST 记录 seed、prompt revision、provider/model、
源文件 hash、生成时间/成本和拒绝原因。违反不可变事实的候选必须拒绝，不能用平均分
掩盖角色错误、虚构玩法或错误文字。

### Gate 5 — 后处理与 QA

统一尺寸、FPS、编码、色彩、响度、字幕、安全区和文件名。所有最终产物 MUST 带
`provenance.json` 与 `qa-report.json`，明确自动检查、人工检查、待检查和失败项。

## 6. 七类专项工作流

### 6.1 剧情过场与任务简报

1. 建立 narrative purpose 与 gameplay transition。
2. 建立角色、场景、道具、镜头和声音 continuity bible。
3. 将长场景拆为单个 4–15 秒 shot；每 shot 定义 start/action/end。
4. 为每 shot 创建独立 job、prompt 和候选日志。
5. 仅拼接通过身份、剧情、镜头、连续性与音频 QA 的 shot。
6. 输出 master、silent master、EDL/工程交接和 flattened-video 声明。

### 6.2 角色表演与多语言本地化

1. 先建立 likeness、performance、voice、script 和 translation 权利清单。
2. 锁定角色身份、blocking、镜头、情绪和动作节点。
3. 由人工批准翻译，并使各语言目标语义/时长尽量可比。
4. 每个语言/变量使用相同 reference、构图、provider 设置和 seed group。
5. 分语言检查身份、动作时刻、转写、发音、口型事件、声音和镜头。
6. 输出每语言独立得分，不得只报告总体平均。

### 6.3 动态菜单与开场 UI

1. 把画面分成 generated motion plate、deterministic overlay 和 interactive engine state。
2. 先批准一张目标尺寸 confirmation frame 与 safe-area mask。
3. 只生成角色、环境、粒子、灯光和装饰性运动。
4. Logo、按钮、玩家名、价格、计数器和交互焦点保留在引擎。
5. 做 OCR、布局、安全区、可读性和循环检查。
6. 输出 motion plate、overlay contract 和引擎集成说明。

### 6.4 游戏内循环媒体

1. 定义世界内设备、观看距离、分辨率、时长、音频触发和包体预算。
2. 选择周期运动、相同首尾 anchor、diegetic seam、crossfade 或 ping-pong 策略。
3. 生成不同运动强度的有限候选。
4. 使用 `analyze_loop.py` 比较首尾帧，但必须再连续播放三轮人工检查。
5. 输出 mezzanine、目标平台编码、seam report 和总体存储估算。
6. 未在目标引擎/平台测试时不得写“已兼容”。

### 6.5 Gameplay Previz

1. 把问题写成 2–4 个互斥假设，每次只改变一个主要变量。
2. 固定 engine screenshot/FOV、参考素材、时长、prompt 结构、候选数和评分表。
3. 每个假设生成可比候选，并显著标记 `CONCEPT — NOT GAMEPLAY`。
4. 由设计、美术和工程分别评价可读性、情绪、实现难度和技术风险。
5. 输出获胜假设、被拒方案和最小 engine prototype 任务。
6. 后续 MAY 记录生成概念与真实实现的 divergence。

### 6.6 营销、商店页、UA 与社媒

1. 建立 claims sheet，把每个功能/商品/价格/日期标为 verified、illustrative、pending 或
   prohibited。
2. 每个 shot 标记为 Gameplay、生成 cinematic、UI/product render 或确定性 overlay。
3. 先设计 truth-preserving master，再派生 16:9、1:1 和 9:16。
4. Logo、CTA、法律文字、评级、价格、商店 badge 与字幕确定性绘制。
5. 发布前由 Gameplay truth、品牌、法务/平台、IP/声音、本地化和 AI 披露负责人审核。
6. 评估 approved creative/GPU-hour 与 approved creative/human-hour，而不是原始生成数。

### 6.7 提示词到 2D 动画与 Spine

1. 没有参考图时先生成并批准角色 anchor；有参考图时锁定角色设计。
2. 生成固定镜头、单角色、单动作、干净背景的短视频。
3. 选择可用候选并抽取固定 FPS、固定 canvas 的 PNG。
4. chroma key 或可靠 segmentation 后生成 straight-alpha，按 pivot 稳帧。
5. 输出 PNG sequence、manifest、atlas pages 和可选 Spine 4.1/4.2/4.3 sequence。
6. Spine 文件必须标记 `animation_kind: flipbook`，不能标记 skeletal。

默认动作 recipe：

| Recipe | 默认时长/FPS | 行为 |
|---|---|---|
| `character-idle-loop` | 2–4 秒、12 FPS | 呼吸、眨眼、轻微重心循环 |
| `character-emote` | 1–2 秒、12 FPS | 高兴、受击、点头、挥手 |
| `character-action` | 1–2 秒、12 FPS | 攻击、施法、冲刺、跳跃 |

最多交付 48 帧；默认 512×512 transparent canvas 与 bottom-center pivot。真正的 Spine
rig/Live2D 必须作为独立的角色拆件、遮挡补全、mesh/weight、参数和人工修正项目。

## 7. H3 参考适配

当 MiniMax H3 被选中时：

- H3 Base 生成 4–15 秒、24 FPS 的音视频；本地开源基线按 768p 处理；
- FL2VA 对应 T2V、首帧、末帧与首尾帧；
- Ref2VA 对应多图片、视频和音频参考；
- 小于 4 秒的有效动作 SHOULD 生成带 handles 的合法 4 秒 clip，再 trim；
- Hosted Context-IR/Regenerate/2K 不得冒充为本地 Base 能力；
- 每次发布前必须重新检查 H3 当前地域、商业、署名和 AI 披露条款。

本规范不把 H3 写死为唯一 provider。其他模型只要满足 job 的输入、控制和交付条件即可
替换。

## 8. 输出目录建议

```text
game-video-output/<job-id>/
├── game-video-job.json
├── inputs/
│   └── reference-manifest.json
├── prompts/
├── candidates/
│   └── decision-log.json
├── selected/
├── delivery/
├── provenance.json
└── qa-report.json
```

2D 工作流 MAY 在 `delivery/` 下增加 `frames/`、`atlas.json`、Spine JSON、
`.atlas` 与 page images。

每次 retry/revision MUST 写到新的输出目录，不得覆盖用户输入或前一版产物。

## 9. 验收与指标

所有工作流共同检查：

- job/schema 有效；
- 素材来源、权利、远程上传和付费状态可追踪；
- 生成数不超过批准预算；
- 不可变事实无违规；
- provenance 和 QA 完整；
- plan-only、rendered、visual-pending、failed 等状态真实。

业务指标 SHOULD 使用：

- accepted clip / GPU-hour；
- accepted seconds / GPU-hour；
- approved asset / human-hour；
- 平均候选数和重生成次数；
- 工作流专项指标：continuity、ASR/发音、OCR、loop seam、truthful claims、alpha/runtime。

## 10. Definition of Done

v0.1.0 发布前必须：

1. 根 `plugin.json` 通过 Agent Plugins 1.0.0 官方 Schema。
2. `.codex-plugin/plugin.json` 通过 Codex 插件校验。
3. 九个 Skill 分别通过 Agent Skill 校验且没有 TODO。
4. 通用 job example 同时通过 JSON Schema 和 bundled validator。
5. 通用 validator 覆盖错误 mode/input、远程上传、付费、rights、delivery 和 workflow QA。
6. loop analyzer 通过合成视频测试，并明确其数值不是视觉认证。
7. 2D 帧管线通过抽帧、alpha、稳帧、atlas 与 package 校验。
8. Spine 4.1、4.2、4.3 package 能被对应 runtime 解析。
9. 至少对 cinematic、menu、loop、previs、marketing、character performance 和 2D 各做
   一次 plan-only 前向测试。
10. 包内没有 token、用户素材、模型权重、Spine Runtime 或第三方专有二进制。
11. Zealman vendor 参考集保持只读、有来源说明、无重复下载副本和非工作流二进制。
12. 仓库所有者确定公开发布许可证与 vendor 资料发布边界，并添加一致的 `LICENSE` 与
    manifest 字段。

## 11. 规范来源

- 本项目调研：`/Users/cui/Downloads/视频生成研究.md`
- Zealman AutoDL 工作流快照：`/Users/cui/Downloads/zealman-AutoDL镜像工作流`
- [Agent Plugins 1.0.0](https://agent-plugins.org/specification.md)
- [Agent Skills Specification](https://agentskills.io/specification.md)
- [MiniMax H3 官方仓库](https://github.com/MiniMax-AI/MiniMax-H3)
- [Spine JSON export format](https://esotericsoftware.com/spine-json-format.md)

若本文与 Agent Plugins、Agent Skills、provider、平台或 Spine 正式规范冲突，以对应
上游规范及项目实际授权为准。

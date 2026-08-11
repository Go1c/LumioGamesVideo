# U视频-MINIMAX-H3

本文档收录 `comfyui-workflow/U视频-MINIMAX-H3/` 目录下按 Windows 文件名自然排序的全部 13 个工作流。说明根据工作流名称、实际节点、上传输入及内部示例提示词整理。


## M14-minimax_h3_动漫视频超分

**工作流类型：** 动漫视频超分与 RTX 增强工作流

**主要用途：** 读取动漫或二次元风格视频，先用 Real-ESRGAN AnimeVideo 模型逐帧超分，再可选走 NVIDIA RTX 视频增强。与 M 目录 `M15-minimax_h3_动漫视频超分` 为同能力副本，便于在 MiniMax H3 生成链路旁直接做成片提清。

**能做到的效果：**
- 加载视频并提取连续帧与音频信息。
- 使用 `realesr-animevideov3.pth` 对画面做动漫向超分。
- 可选启用 Deno RTX / RTX 视频增强进一步提清。
- 将处理后的帧与原音频重新合成为视频。

**主要输入：** 一段待放大的动漫或插画风格视频，以及超分模型、RTX 增强开关和视频输出参数。

**核心模型与技术：** Real-ESRGAN AnimeVideo v3、ImageUpscaleWithModel、DenoRTXVFXEasyUpscale、Video Helper Suite。

## U01-minimax_h3_light2v多图参考生视频加速版

**工作流类型：** MiniMax H3 多图参考生视频加速工作流

**主要用途：** 使用 MiniMax H3 Reference-to-Video 与 LightX2V 4 步加速 LoRA，根据最多约 9 张参考图生成带音频的短视频。可按兆像素与画幅表选择输出尺寸，适合角色、服装、场景多参考一致性镜头。

**能做到的效果：**
- 上传多张参考图，按节点说明复制加载图可扩展到更多参考位。
- 用分镜式提示词描述动作、运镜与音效。
- 通过 LightX2V Turbo 4 步 LoRA 降低采样步数、加快出片。
- 按秒数自动推算对齐到模型约束的帧数。
- 解码视频与音频并可选 RTX 视频超分后保存。

**主要输入：** 多张参考图片、分镜/主体描述提示词、视频秒数、分辨率预设（兆像素与画幅）、采样与随机种子。

**核心模型与技术：** MiniMax H3 ref2va、Qwen3-VL MiniMax H3 文本视觉编码器、MiniMax H3 Video/Audio VAE、LightX2V Turbo 4 步 LoRA、MiniMaxH3ReferenceToVideo、SageAttention、RTXVideoSuperResolution。

## U02-minimax_h3_light2v首尾帧图生视频加速版

**工作流类型：** MiniMax H3 首尾帧图生视频加速工作流

**主要用途：** 以首帧与尾帧图片锁定起止画面，再用 LightX2V 加速的 MiniMax H3 Image-to-Video 生成中间过渡，适合角色姿态转换、镜头推进收束和竖屏展示动画。

**能做到的效果：**
- 分别指定视频起始帧与结束帧的主体与构图。
- 用分镜提示词控制运镜、光线和氛围过渡。
- 使用 LightX2V Turbo 4 步 LoRA 加速采样。
- 联合解码画面与音频并输出视频。
- 通过显存清理节点降低连续跑图压力。

**主要输入：** 一张首帧图片、一张尾帧图片、动作与氛围提示词、时长/分辨率与采样参数。

**核心模型与技术：** MiniMax H3 fl2va、Qwen3-VL MiniMax H3、MiniMax H3 Video/Audio VAE、LightX2V Turbo 4 步 LoRA、MiniMaxH3ImageToVideo、SageAttention。

## U03-minimax_h3_light2v-文生视频加速版

**工作流类型：** MiniMax H3 文生视频加速工作流

**主要用途：** 无需参考图，直接用电影级文本提示生成 MiniMax H3 音视频短片，并叠加 LightX2V 4 步加速，适合预告片风、动作场景和纯文本试镜。

**能做到的效果：**
- 仅凭提示词生成含动作、运镜与氛围的短视频。
- 支持写实电影感、城市夜景、动作预告等叙事描写。
- 使用 LightX2V Turbo 降低步数、加快出片。
- 同步生成并解码音频轨。
- 按预设分辨率与秒数控制成片规格。

**主要输入：** 文生视频提示词、视频秒数、分辨率预设、采样与随机种子。

**核心模型与技术：** MiniMax H3 fl2va、Qwen3-VL MiniMax H3、MiniMax H3 Video/Audio VAE、LightX2V Turbo 4 步 LoRA、SageAttention。

## U04-minimax_h3_light2v-5图参考生视频加速版

**工作流类型：** MiniMax H3 五图参考生视频加速工作流

**主要用途：** 固定五路参考图输入的 Reference-to-Video 加速版，示例为古风仙侠多镜头叙事（人物、服饰、场景交叉引用），适合短剧预演和角色一致性镜头。

**能做到的效果：**
- 使用五张参考图约束人物、服装与场景外观。
- 按分秒分镜写运镜、对白氛围与环境音效。
- 通过 LightX2V Turbo 4 步 LoRA 加速生成。
- 保持参考主体在多镜头间的一致性。
- 输出带音频的成片视频。

**主要输入：** 五张参考图片、分镜提示词、视频秒数、分辨率与采样参数。

**核心模型与技术：** MiniMax H3 ref2va、Qwen3-VL MiniMax H3、MiniMax H3 Video/Audio VAE、LightX2V Turbo 4 步 LoRA、MiniMaxH3ReferenceToVideo、SageAttention。

## U05-minimax_h3-多参考图light2v加速生成-LTX超分

**工作流类型：** MiniMax H3 多参考生成 + LTX 2.3 超分综合工作流

**主要用途：** 先用 MiniMax H3 LightX2V 多参考快速出片，再接入 LTX 2.3 空间超分与 Crisp Enhance，在保持剧情与角色参考的同时提升清晰度，适合竖屏古风短片等成片提质。

**能做到的效果：**
- 多参考图驱动 MiniMax H3 生成带分镜描述的短视频。
- 使用 LightX2V 加速降低首轮生成耗时。
- 将结果送入 LTX 2.3 做潜空间/空间超分与画质增强。
- 联合处理视频与音频潜空间后重新封装。
- 适合“先快出、再提清”的两段式生产。

**主要输入：** 多张参考图片、分镜提示词、MiniMax 生成参数，以及 LTX 超分相关尺寸与采样参数。

**核心模型与技术：** MiniMax H3 ref2va + LightX2V、Qwen3-VL MiniMax H3、LTX 2.3 22B Distilled FP8、LTX 2.3 Spatial Upscaler x2、LTX2.3 Crisp Enhance、Licon VBVR I2V LoRA、Gemma 3 12B。

## U06-minimax_h3_light2v多图参考生视频叠加加速插帧优化版

**工作流类型：** MiniMax H3 多图参考 + 加速 + 插帧优化工作流

**主要用途：** 在多图参考生视频基础上叠加 LightX2V 加速与插帧后处理，示例用 `subject_definitions` 绑定多角色外观，适合需要更流畅帧率的古风/剧情短镜头。

**能做到的效果：**
- 多参考图约束多角色与场景一致性。
- LightX2V Turbo 4 步加速采样。
- 生成后可走插帧提升时间流畅度。
- 支持音频条件与显存清理。
- 部分加速/缓存节点在个别机器上可能不兼容，报错时可按标注关闭。

**主要输入：** 多张参考图片、主体定义与分镜提示词、秒数/分辨率、插帧与采样参数。

**核心模型与技术：** MiniMax H3 ref2va、Qwen3-VL MiniMax H3、LightX2V Turbo 4 步 LoRA、MiniMaxH3ReferenceToVideo、EasyCache、插帧后处理、SageAttention。

## U06-minimax_h3_light2v多图参考生视频叠加加速插帧优化版V2

**工作流类型：** MiniMax H3 Turbo 多图参考 + 插帧优化工作流

**主要用途：** U06 的 V2 迭代，将加速链路改为 MiniMax H3 Turbo（`minimax_h3_turbo_v4_step600_ema`）与专用 Turbo 采样器，并保留插帧与 First Block Cache，适合在兼容环境下进一步压低生成步数。

**能做到的效果：**
- 多参考图驱动角色一致的短视频生成。
- 使用 MiniMax H3 Turbo LoRA/采样器加速。
- 可选 First Block Cache 降低重复计算。
- 生成后插帧提升帧率。
- 可用 TAEH3 等预览/解码辅助节点加快调试。

**主要输入：** 多张参考图片、主体定义与分镜提示词、Turbo 采样参数、插帧与输出设置。

**核心模型与技术：** MiniMax H3 ref2va、`minimax_h3_turbo_v4_step600_ema.safetensors`、MiniMaxH3TurboLoRA、MiniMaxH3TurboSampler、ApplyMiniMaxH3FirstBlockCache、TAEH3、插帧后处理。

## U06-minimax_h3_light2v多图参考生视频叠加加速插帧优化版V3

**工作流类型：** MiniMax H3 LightX2V 多图参考 + 插帧优化工作流

**主要用途：** U06 的 V3 迭代，回到 LightX2V 4 步加速主路径，并保留 First Block Cache、TAEH3 与插帧模块，作为 V2 Turbo 路线之外的稳定加速备选。

**能做到的效果：**
- 多参考图生成并绑定多角色外观。
- LightX2V Turbo 4 步加速采样。
- First Block Cache 可选加速重复推理。
- 插帧优化输出流畅度。
- 与 V2 共用同类输入组织，便于对比两条加速路线。

**主要输入：** 多张参考图片、主体定义与分镜提示词、秒数/分辨率、缓存与插帧开关。

**核心模型与技术：** MiniMax H3 ref2va、LightX2V Turbo 4 步 LoRA、ApplyMiniMaxH3FirstBlockCache、TAEH3、MiniMaxH3ReferenceToVideo、插帧后处理、SageAttention。

## U07-MiniMax-H3全能参考工作流Work-Fisher

**工作流类型：** MiniMax H3 文生/单图/多图参考综合工作流

**主要用途：** Work-Fisher 整合的全能参考入口，可在文生、单图参考与多图参考间切换，内置 5/10/15 秒提示词三流程模板，并提供低显存保留建议，适合电影级对白短片与角色锁定叙事。

**能做到的效果：**
- 在文生、单图参考、多图参考模式间切换。
- 使用内置 5/10/15 秒导演式提示词模板快速写片。
- 用 `@图片` / 参考位锁定主角、服装与场景一致性。
- 支持原生立体声与多镜头时间轴描述。
- 通过保留显存参数适配约 8G 起的不同显卡配置。

**主要输入：** 提示词（或选用内置模板）、可选单张/多张参考图、秒数与分辨率、保留显存与采样参数。

**核心模型与技术：** MiniMax H3 fl2va / ref2va、Qwen3-VL MiniMax H3、LightX2V Turbo、MiniMaxH3MultiRateSamplerEXPT8、MiniMaxH3AVDecodeT8、ReservedVRAMSetter、SageAttention。

## U08-Aiden-minimax文-图-首尾帧生视频-自动切换-8G-48G

**工作流类型：** MiniMax H3 文生/图生/首尾帧自动切换工作流

**主要用途：** 按是否上传图片自动在文生、单图图生与首尾帧模式间切换，覆盖约 8G–48G 显存档位；可选 Qwen3.5 反推写词、RIFE 插帧与 RTX 超分，适合从一条提示或一张图快速出竖屏短视频。

**能做到的效果：**
- 无图走文生，单图走图生，双图走首尾帧，条件分支自动切换。
- 使用 Qwen3.5 GGUF 视觉语言模型辅助反推/扩写提示词。
- 按分辨率选择器适配不同显存档位。
- 可选 RIFE 插帧与 RTX 视频超分做后处理。
- 支持高动态分组与显存清理。

**主要输入：** 文生提示词，和/或一张首帧图、可选尾帧图；秒数、分辨率档位、插帧/超分开关。

**核心模型与技术：** MiniMax H3 fl2va、Qwen3-VL MiniMax H3、Qwen3.5 9B GGUF + mmproj、MiniMaxH3ImageToVideo、ImpactConditionalBranch、RIFE 4.9、RTXVideoSuperResolution、UniBlockSwap。

**视频教程：** [哔哩哔哩](https://www.bilibili.com/video/BV1oYu36QEyZ)

## U09-Minimax-H3二采重绘-秒变清晰-超高一致性-效率起飞wuwukasi

**工作流类型：** MiniMax H3 多参考二采重绘与放大工作流

**主要用途：** 先以较低分辨率完成一采参考生成，再以更高分辨率做二采重绘放大，强调角色一致性与清晰度；支持最多约 9 张参考图与多路参考音频，适合需要“先快出再提清”的全能参考成片。

**能做到的效果：**
- 一采快速生成剧情与角色运动草稿。
- 二采按更高宽高重绘放大，提升细节与清晰度。
- 多参考图 + 多参考音频锁定外观与声音条件。
- 可单独调节一采/二采步数与短边分辨率。
- 使用 Turbo 权重与低显存注意力优化效率。

**主要输入：** 多张参考图片、可选参考音频、主体/分镜提示词、一采与二采分辨率及步数。

**核心模型与技术：** MiniMax H3 ref2va、`minimax_h3_turbo_v4_step600.safetensors`、Qwen3-VL MiniMax H3、MiniMaxH3ReferenceToVideo、MiniMaxChunkFeedForward、MiniMaxLowVRAMAttention、EasyCache。

## U10-DaSiWa-MiniMaxH3-MythicAlchemy-v12导演台

**工作流类型：** MiniMax H3 导演台综合工作流

**主要用途：** Darksidewalker MythicAlchemy v12 导演台，在同一 Controls 面板中切换 T2V / I2V / FLF2V / R2V 与音频条件，并集成超分、插帧等后处理，适合需要完整文档化参数面板的专业向短片制作。

**能做到的效果：**
- 在文生、单图、首尾帧、多参考图模式间统一切换。
- 用导演节点编排分镜、参考图时间对齐与提示词。
- 设置分辨率预设、画幅与后处理（AnimeSharp 超分、RIFE 插帧、RTX 增强等）。
- 支持音频条件与多示例提示模板。
- 适合作为 MiniMax H3 全功能控制台长期复用。

**主要输入：** 按所选模式提供提示词，和/或首帧、尾帧、多参考图、音频；Settings 面板中的分辨率、画幅与后处理开关。

**核心模型与技术：** MiniMaxH3Director / MiniMaxH3DirectorGuide、MiniMax H3 fl2va / ref2va、Qwen3-VL MiniMax H3（含 int4/nvfp4 档）、2x-AnimeSharpV4、RIFE v4.26、TAEH3、DaSiWa RTX Upscaler、SageAttention。

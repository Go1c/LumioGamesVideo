# H黑鹤001Ltx终章

本文档收录 `comfyui-workflow/H黑鹤001Ltx终章/` 目录下按 Windows 文件名自然排序的全部 5 个工作流。说明根据实际节点、上传输入及内部示例提示词整理。


## ▶▶LTX23-动作迁移流

**工作流类型：** 动作迁移工作流

**主要用途：** 将驱动视频中的身体动作迁移到一张目标人物图片上。示例使用舞蹈视频，并以“The character is dancing”描述目标动作，适合图片跳舞、角色表演和人物动作复刻。

**能做到的效果：**
- 从驱动视频逐帧提取身体和手部姿态。
- 让单张人物图片按照视频动作生成新视频。
- 保留参考人物的外观，同时继承舞蹈节奏和肢体变化。
- 自动匹配参考图尺寸与驱动视频输出尺寸。
- 可选择保留原音频或提取伴奏作为生成音轨。
- 通过 IC-LoRA 引导加强动作序列控制。

**主要输入：** 一张目标人物图片、一段动作驱动视频、动作提示词、裁剪时间、帧率和输出尺寸。

**核心模型与技术：** LTX 2.3 22B Distilled Q6_K GGUF、LTX 2.3 IC-LoRA Union Control、DWPose、LTXAddVideoICLoRAGuide、MelBand RoFormer、SageAttention。

**视频教程：** [哔哩哔哩](https://www.bilibili.com/video/BV1E4Vp6cEu5)

## ▶▶LTX23-全能视频编辑流

**工作流类型：** 视频编辑工作流

**主要用途：** 面向已有视频素材的 LTX 2.3 自然语言编辑流程。上传视频后可用英文指令添加、移除或替换元素，也能转换整段风格；示例指令为移除画面左侧的兔子角色，适合视频内容修改和创意重制。

**能做到的效果：**
- 在指定位置添加带明确外观的新物体。
- 移除指定人物、动物或其他目标。
- 将原有角色、服装或道具替换为新内容。
- 将整段视频转换为吉卜力动画等统一风格。
- 保留原视频音频，或分离伴奏后参与音视频编辑。
- 在一次采样与二次采样空间放大模式间切换。

**主要输入：** 一段待编辑视频、英文编辑指令、裁剪起止时间、输出尺寸、帧率，以及一次或二次采样模式。

**核心模型与技术：** LTX 2.3 22B Distilled Q6_K GGUF、Edit Anything Global LoRA、Gemma 3 12B GGUF、LTX 多图引导、Spatial Upscaler、MelBand RoFormer、SageAttention。

**视频教程：** [哔哩哔哩](https://www.bilibili.com/video/BV1E4Vp6cEu5)

## ▶▶LTX23-视频去字幕水印流

**工作流类型：** 视频修复与增强工作流

**主要用途：** 使用 LTX 2.3 和对应 IC-LoRA 修复已有视频，可按需求切换提示词与 LoRA，去除字幕、文字遮挡或短视频平台水印，也能进行高清化和去模糊处理。内置示例提示词要求移除字幕、标题及相关文字遮挡并自然还原底层画面，适合视频清理、画质修复和素材再利用。

**能做到的效果：**
- 移除视频中的字幕、标题、说明文字和其他文字遮挡。
- 去除短视频平台水印，并自然重建被遮挡的画面细节。
- 将视频高清化，提升清晰度、纹理细节和整体观感。
- 清除模糊、噪点与压缩伪影，并重建高频细节。
- 在修复时保持人物、场景、动作、镜头运动和时序风格一致。
- 保留原视频音频并与修复后的画面重新合成为 MP4。

**主要输入：** 一段待处理视频、与任务对应的 IC-LoRA 和英文修复提示词，以及裁剪起止时间、输出尺寸、帧率和随机种子。

**核心模型与技术：** LTX 2.3 22B Distilled Q6_K GGUF、字幕移除/水印移除/视频高清化/视频修复 IC-LoRA、Gemma 3 12B GGUF、LTXAddVideoICLoRAGuide、LTX 音视频 VAE、SageAttention、分块 VAE 解码。

**视频教程：** [哔哩哔哩](https://www.bilibili.com/video/BV1E4Vp6cEu5)

## ▶▶LTX23-图音编辑流(导演节点)

**工作流类型：** 导演时间轴图像与音频编辑工作流

**主要用途：** 通过 LTX Director 时间轴组织图片、提示词、音频和运动片段，再联合生成连续音视频。适合把分镜图与声音素材编排成短片，也可对指定时间段进行重生成。

**能做到的效果：**
- 在导演时间轴中分段放置参考图、局部提示词和音频。
- 同时启用主画面、音频与运动轨道，统一控制片段时长。
- 使用图片引导约束人物、商品或场景外观。
- 通过 Talking Head LoRA 制作带对白或演唱的人物镜头。
- 支持指定起止秒数和局部重拍范围。
- 分块解码音视频并输出带声音的 MP4。

**主要输入：** 时间轴参考图片、分段或全局提示词、音频片段、可选运动引导、起止时间、帧率及自定义宽高。

**核心模型与技术：** LTX 2.3 22B Distilled Q6_K GGUF、Gemma 3 12B GGUF、LTX Director/LTXDirectorGuide、Talking Head LoRA、Licon/Transition 可选 LoRA、SageAttention、分块 VAE 解码。

**视频教程：** [哔哩哔哩](https://www.bilibili.com/video/BV1E4Vp6cEu5)

## ▶▶LTX23-指定替换视频编辑

**工作流类型：** 遮罩式视频指定区域替换工作流

**主要用途：** 先用 SAM 3.1 按文字定位并跟踪视频中的目标区域，再借助 LTX 2.3 遮罩重绘完成换人、换物、换脸或局部内容替换。源示例以“fox head”选择目标、以“An orange cat is walking on the street”描述替换后的画面。

**能做到的效果：**
- 根据遮罩提示词在首帧检测需要替换的对象。
- 将首帧检测结果跟踪到整段视频，生成连续时序遮罩。
- 对遮罩扩展、柔化和块化，降低边缘突兀感。
- 把参考图片与原视频帧组合为区域引导。
- 保留原视频未遮罩区域及原音频。
- 可在一次采样和潜空间二倍放大二次采样之间切换。

**主要输入：** 一段待编辑视频、一张替换参考图、SAM 遮罩提示词、英文编辑结果提示词、裁剪时间、输出尺寸、帧率及采样模式。

**核心模型与技术：** LTX 2.3 22B Distilled Q6_K GGUF、LTX 2.3 Inpaint Masked R2V LoRA、SAM 3.1 Multiplex、SAM3 Detect/VideoTrack、LTXVAddGuideMulti、ReservedRegionFrameComposer、Spatial Upscaler、MelBand RoFormer、SageAttention。

**视频教程：** [哔哩哔哩](https://www.bilibili.com/video/BV1E4Vp6cEu5)


# C图像-Zimage

本文档收录 `comfyui-workflow/C图像-Zimage/` 目录下全部 19 个工作流，按 Windows 文件名自然排序。说明依据各 JSON 的实际节点、上传输入及内部示例提示词整理。

## C01-文生图-Zimage基础版

**工作流类型：** 文生图

**主要用途：** 基于 Z-Image Turbo 的入门级文生图流程，内置多条中文风格提示词，可快速尝试校园、暗黑悬疑、赛博朋克和水墨国风等不同题材。

**能做到的效果：**
- 使用中文自然语言直接生成图片。
- 内置五条不同题材和画风的示例提示词。
- 支持一次批量生成多张图片。
- 使用 AWPortrait-Z LoRA 增强人物表现。
- 通过 Turbo 采样快速完成出图。

**主要输入：** 中文提示词、画面尺寸、批量数量和随机种子，无需上传图片。

**核心模型与技术：** Z-Image Turbo、Qwen3 4B 文本编码器、AWPortrait-Z LoRA、Turbo 快速采样。

## C02-文生图-ZimageControlNet

**工作流类型：** 文生图

**主要用途：** 在 Z-Image Turbo 文生图基础上加入可开关的 ControlNet 分支，以参考图的姿势、深度或边缘结构约束文字生成结果。

**能做到的效果：**
- 使用中文提示词生成 Z-Image 图片。
- 从参考图提取人体姿势并控制角色动作。
- 使用深度图保持前后空间和主体轮廓。
- 通过 Canny 边缘或 HED 软边缘控制构图细节。
- 一键开启或关闭 ControlNet，对比纯文生图结果。
- 将参考图、控制图和最终成图组合预览。

**主要输入：** 中文提示词、可选控制参考图、预处理器编号、画面尺寸和随机种子。

**核心模型与技术：** Z-Image Turbo、Qwen3 4B、Z-Image Turbo Fun ControlNet Union 2.1、DWPose/Depth/Canny/HED 预处理、ModelPatch。

## C03-文生图-ZimageDetailDaemon

**工作流类型：** 文生图

**主要用途：** 基于 Z-Image Turbo 与 Detail Daemon 的细节增强文生图流程，通过自定义采样器、噪声调度和细节曲线强化局部纹理。

**能做到的效果：**
- 根据英文长提示词从零生成动漫或插画图片。
- 强化毛发、耳朵、尾巴、服装纹理等细小结构。
- 通过 Detail Daemon 调整不同采样阶段的细节强度。
- 使用自定义 Sigma 曲线控制细节介入区间。
- 对比标准采样与 Detail Daemon 增强结果。

**主要输入：** 正向提示词、画面尺寸、随机种子及 Detail Daemon 强度和区间参数，无需上传图片。

**核心模型与技术：** Z-Image Turbo、Qwen3 4B、AuraFlow 采样、Detail Daemon Sampler、Detail Daemon Graph Sigmas、自定义高级采样。

## C04-文生图-Zimage红潮ZIB超真实感定妆照

**工作流类型：** 文生图

**主要用途：** 使用 RedZDX Z-Image Base 蒸馏模型生成写实全身定妆照，并在出图后进行 SeedVR2 高清放大。示例提示词为纯色背景下、完整头脚入镜的古风汉服女性。

**能做到的效果：**
- 从长篇自然语言生成写实全身人物。
- 通过 WujiEditor 设置尺寸及摄影、动漫等风格预设。
- 以 8 步蒸馏采样快速形成画面。
- 保留纯色背景、服饰刺绣和人物整体造型等提示词细节。
- 使用 SeedVR2 将短边放大到设定尺寸并进行颜色校对。

**主要输入：** 正向提示词、宽高、风格预设、随机种子和放大尺寸，无需上传图片。

**核心模型与技术：** RedZDX-ZIB Distilled、Qwen3 4B、flux_ultra_vae、WujiLoader/WujiEditor、Clownshar KSampler、SeedVR2。

## C05-洗图-Zimage洗图大合集

**工作流类型：** 综合

**主要用途：** 集成文生图、参考图自动反推洗图和局部遮罩修复。示例包括镜中自拍、古风动漫转换及指定人体局部重绘。

**能做到的效果：**
- 直接用中文提示词进行 Z-Image 文生图。
- 上传图片后由 Qwen3-VL 反推主体、构图和光影提示词。
- 按最长边缩放原图并以可调降噪幅度重新绘制。
- 将原图与洗图结果并排组合预览。
- 对上传图片的手绘遮罩区域进行局部修复。
- 在流程间自动清理显存与内存。

**主要输入：** 文生图提示词，或上传一张待洗图图片；局部修复时还需在上传图上绘制遮罩，并可调尺寸、降噪和随机种子。

**核心模型与技术：** Full-Red-Z-image、Qwen3-VL 8B GGUF、Z-Image 双阶段采样、图像反推、VAE 重绘、SDXL 局部修复、遮罩扩展、显存清理。

## C06-洗图-Zimage终极版自动洗图CN高清放大

**工作流类型：** 图生图

**主要用途：** 上传原图后自动反推中文提示词，以 Canny ControlNet 保持轮廓完成双段重绘，再用 SeedVR2 做高清放大。示例反推内容为黄昏城市水岸中的人物。

**能做到的效果：**
- 使用 Qwen3-VL 自动分析原图并生成中文描述。
- 通过 Canny 边缘约束主体轮廓与构图。
- 以两段高级采样逐步完成洗图。
- 调整输入最长边、ControlNet 强度和重绘种子。
- 通过 SeedVR2 放大到高分辨率并进行 LAB 色彩校正。
- 输出原图与最终结果的对比卷轴。

**主要输入：** 一张待洗图图片、反推指令、最长边、ControlNet 强度、采样步数、随机种子和放大分辨率。

**核心模型与技术：** Z-Image Turbo、Qwen3-VL 4B、Qwen3 4B、Fun ControlNet Union 2.1、Canny、双段 KSamplerAdvanced、SeedVR2。

## C07-文生图-Zimage-Nunchaku加速

**工作流类型：** 文生图

**主要用途：** 使用 Nunchaku FP4 量化加载器加速 Z-Image Turbo 文生图。示例提示词为银杏校园小径中的日漫少女。

**能做到的效果：**
- 以中文提示词生成日漫、校园等题材图像。
- 使用 SVDQ FP4 量化模型降低模型加载与推理负担。
- 支持 5090 与其他显卡对应的量化模型选择。
- 使用 9 步采样快速出图。
- 自定义竖图尺寸与随机种子。

**主要输入：** 正向提示词、宽高、随机种子及 Nunchaku 模型版本，无需上传图片。

**核心模型与技术：** Nunchaku Z-Image DiT、svdq-fp4 Z-Image Turbo、Qwen3 4B、AuraFlow、res_multistep 采样。

## C08-图像黑兽DarkBeast-ZiT-V8-UltraSimple-Workflow-ComfyUI

**工作流类型：** 文生图

**主要用途：** DarkBeast Z-Image Turbo 的两阶段简化文生图流程，先生成基础图，再将图像放大编码后以较低降噪二次精修。

**能做到的效果：**
- 根据英文摄影提示词直接生成竖版人物图。
- 第一阶段以 8 步完整降噪形成主体和构图。
- 将首轮结果双倍缩放后重新编码。
- 第二阶段以 0.5 降噪补充纹理和细节。
- 分别保存首轮和精修结果便于对比。

**主要输入：** 正向提示词、画面尺寸、随机种子、两阶段采样参数和可选 LoRA，无需上传图片。

**核心模型与技术：** DarkBeast ZIT 模型、Qwen3 4B、DarkKlein BFS LoRA、AuraFlow、VAE 二次编码、两阶段 KSampler。

## C09-图像黑兽DarkBeast-ZIT&Klein-V8-Hybrid-Workflow-ComfyUI

**工作流类型：** 综合

**主要用途：** 将 DarkBeast Z-Image 文生图与 Flux2 Klein 参考编辑组合为混合流程，可先生成图像，再用参考图和编辑指令进行两轮 Klein 处理，亦可启用 SeedVR2 放大。

**能做到的效果：**
- 用 Z-Image 双采样生成基础人物或场景。
- 将首轮图像放大后低降噪精修。
- 上传参考图并注入 ReferenceLatent 条件。
- 按英文编辑指令替换人物脸部和发型等指定内容。
- 通过 Flux2 Klein 连续进行两轮参考编辑。
- 可选使用 SeedVR2 输出高清版本。

**主要输入：** 文生图提示词、Z-Image 尺寸与种子；编辑分支需上传一张参考图并填写编辑提示词。

**核心模型与技术：** DarkBeast ZIT、Flux2 Klein 9B、Qwen3 4B/8B、ReferenceLatent、Flux2Scheduler、自定义高级采样、SeedVR2。

## C10-图像Moody Zimage Simple Workflow - V4

**工作流类型：** 文生图

**主要用途：** Moody RealMix ZIT 的两阶段写真文生图流程，附带 Ultimate SD Upscale、皮肤对比放大、Face Detailer 和 SeedVR2 等可选后处理。

**能做到的效果：**
- 以中文摄影描述生成写真人像。
- 首轮采样确定构图，潜空间放大后第二轮补充细节。
- 使用 Ultimate SD Upscale 分块放大并自动计算瓦片尺寸。
- 可对人脸进行检测、SAM 分割和局部细化。
- 可通过额外放大模型强化皮肤对比。
- 可选以 SeedVR2 输出 4K 级结果。

**主要输入：** 正向提示词、基础尺寸、LoRA、首轮与次轮种子、各放大倍率及可选人脸细化提示词，无需上传图片。

**核心模型与技术：** MoodyRealMix ZIT V4 DPO、Qwen3 4B、双段 KSamplerAdvanced、Ultimate SD Upscale、YOLO/SAM FaceDetailer、4x-UltraSharp、SeedVR2。

## C11-Zimage双采-三采-双放大

**工作流类型：** 文生图

**主要用途：** 先用 Z-Image Base 与 Turbo 分段双采，再用 Flux2 Klein 做第三次高清重绘，并可接 SeedVR2 放大。示例为月下樱花古风人物。

**能做到的效果：**
- 用 Z-Image Base 前段采样建立构图。
- 用 Z-Image Turbo 接续采样完成双采结果。
- 将双采图放大编码后交给 Klein 参考重绘。
- 以“高清”等提示词补充纹理并保持原图条件。
- 使用 SeedVR2 对三采结果继续超分。
- 将双采、三采和放大结果组合展示。

**主要输入：** 正负提示词、分辨率、种子、Base/Turbo 分段步数、Klein 重绘参数和 SeedVR2 分辨率，无需上传图片。

**核心模型与技术：** Z-Image Base、Z-Image Turbo、Flux2 Klein 9B、瑶光/真实幻想及蒸馏 LoRA、ReferenceLatent、三阶段采样、SeedVR2。

## C12-瑶光-动漫-MJ风格工作流

**工作流类型：** 文生图

**主要用途：** 围绕 Z-Image Base/Turbo 的多组文生图方案，集中提供瑶光、动漫、Midjourney、厚涂与数字摄影等 LoRA 风格切换和多阶段高清生成。

**能做到的效果：**
- 从中文长提示词生成写实、古风或动漫图片。
- 在 Base 与 Turbo 模型之间选择不同采样方案。
- 通过瑶光和蒸馏 LoRA 加速 Base 模型出图。
- 切换 Midjourney、厚涂、吉卜力、真实光影等风格 LoRA。
- 使用双采或三采流程逐步补充构图和纹理。
- 通过 SeedVR2 等放大分支输出高清结果并进行对比。

**主要输入：** 正负提示词、分辨率、随机种子、模型分支、LoRA 及其权重、采样和放大参数，无需上传图片。

**核心模型与技术：** Z-Image Base/Turbo、Z-Image Anime AIO、Qwen3 4B、瑶光/蒸馏/Midjourney/厚涂类 LoRA、多阶段采样、SeedVR2。

## C13-kinghere-Z-image-动漫-小说-造影

**工作流类型：** 综合

**主要用途：** 使用 Kinghere Z-Image AIO 生成动漫、小说角色和戏剧化造影图，同时提供上传图片反推提示词与姿势、深度、Canny 控制素材预览。

**能做到的效果：**
- 根据动漫写实长提示词生成小说角色立绘。
- 以两段不同采样器连续完善画面。
- 上传图片后由 Qwen3-VL 生成中文详细描述。
- 将反推文本直接送入生成提示词。
- 从控制参考图提取 DWPose、Depth 或 Canny 图。
- 比较不同采样阶段的输出效果。

**主要输入：** 正向提示词、画面尺寸和种子；反推或控制时上传一张图片，并选择预处理器。

**核心模型与技术：** kinghere Z-image 动漫小说造影 V3 AIO、Qwen3-VL 4B、双 KSamplerAdvanced、DWPose/Depth/Canny、Fun ControlNet Union 2.1。

## C14-黑鹤001-ZITB+F2K+NSW+高清修复(整合流)

**工作流类型：** 综合

**主要用途：** 集成 Z-Image Turbo/Base、Flux2 Klein 编辑、图片反推、局部处理与高清修复的多分支工作流，适合从文字生成或从上传图继续编辑和修复。

**能做到的效果：**
- 使用 Z-Image 分支从提示词生成基础图片。
- 上传参考图后自动分析画面并生成编辑提示词。
- 通过 Flux2 Klein 进行单图或多图参考编辑。
- 对人物、构图或画面内容进行可控重绘。
- 使用分块、超分和高清修复节点补充纹理。
- 在不同模型及修复结果之间切换、比较和保存。

**主要输入：** 文本提示词、画面尺寸、种子与模型分支；图像编辑和修复分支需上传参考图或待修复图，并设置重绘及放大参数。

**核心模型与技术：** Z-Image Turbo/Base、Flux2 Klein、视觉语言模型反推、ReferenceLatent/图像条件、分块处理、多阶段采样与高清修复。

**视频教程：** [哔哩哔哩](https://www.bilibili.com/video/BV1AaQhBWELC)

## C15-Z-ImageBase&Turbo双重采样洗图工作流

**工作流类型：** 综合

**主要用途：** 同时提供纯文生图和上传图片洗图，以 Z-Image Base 与 Turbo 在不同采样阶段接力，并加入 Canny ControlNet、Qwen3.6 反推和 SeedVR2 放大。

**能做到的效果：**
- 直接按提示词进行 Base 与 Turbo 双重采样文生图。
- 上传图片并由 Qwen3.6 视觉模型生成详细提示词。
- 根据原图尺寸自动裁切和建立重绘尺寸。
- 在原图与 Canny 边缘图之间切换控制输入。
- 以 Base/Turbo 分段采样保持结构并补充细节。
- 在文生图、洗图结果中选择一路进行 SeedVR2 4K 放大。

**主要输入：** 文生图提示词或一张待洗图图片、反推补充说明、宽高、种子、总步数与切分步数、ControlNet 和放大参数。

**核心模型与技术：** Z-Image Base、ZIT Remix Reality Turbo、Qwen3-4B Engineer GGUF、Qwen3.6-35B 视觉 GGUF、Fun ControlNet Union、Canny、双阶段采样、SeedVR2。

## C16-短剧文生图专用-支持场景-角色

**工作流类型：** 文生图

**主要用途：** 面向短剧人物和场景素材的 Z-Image Base 文生图流程，示例为真实电影光影下的明制汉服人物与古宅场景，并提供可关闭的 SeedVR2 放大。

**能做到的效果：**
- 用中文长提示词生成短剧人物与环境画面。
- 通过瑶光与如梦似幻 LoRA 调节真实感和氛围。
- 使用 8 步蒸馏 LoRA 加速 Base 模型。
- 自定义横竖尺寸和随机种子。
- 生成后预缩放并使用 SeedVR2 高清放大。
- 对比原始生成与放大结果。

**主要输入：** 角色/场景提示词、宽高、随机种子、三个 LoRA 权重和可选放大参数，无需上传图片。

**核心模型与技术：** Z-Image Base BF16、Qwen3 4B、瑶光、如梦似幻、Fun Distill 8-Steps LoRA、res_2s_ode、SeedVR2。

## C17-Z-image瑜伽服小姐姐

**工作流类型：** 文生图

**主要用途：** 以 Leggings 为核心主题，由本地 Qwen3.6 批量扩写瑜伽服人物提示词，再交给 Z-Image Turbo 生成人像。内置多种面料、姿势、场景和摄影角度案例。

**能做到的效果：**
- 输入数量后批量生成多组瑜伽服中文提示词。
- 将 LLM 输出拆成列表并逐条送入文生图。
- 生成东亚女性、瑜伽服和商业摄影主题图片。
- 使用专用瑜伽裤、身材、真实光影和情绪 LoRA。
- 自定义 1024×1536 等尺寸、种子和采样参数。

**主要输入：** 提示词生成数量、角色主题或生成规则、画面尺寸和随机种子，无需上传图片。

**核心模型与技术：** Z-Image Turbo FP16、Qwen3.6-35B-A3B GGUF、Qwen3 4B、Leggings/BetterCurvyFigure/flow-dpo/teenymooddy LoRA、TextToList。

## C18-豹豹喵呜制作-白玉AIO三采超高清写真生成

**工作流类型：** 综合

**主要用途：** 以 Z-Image Base 一采、Z-Image Turbo 二采、Flux2 Klein 三采完成超高清写真，也可上传图片用 Qwen3.6 反推提示词后进入生成与修复链路。

**能做到的效果：**
- 用自然语言生成暖金古风等写真人像。
- Z-Image Base 负责首轮构图与主体生成。
- Z-Image Turbo 续采补充纹理。
- Flux2 Klein 结合 LCS 色彩锚定和锐度干预进行第三轮修复。
- 对大图进行自动瓦片拆分、逐块处理和重组。
- 执行去灰、频率分离、柔光混合和颜色匹配。

**主要输入：** 正向提示词、尺寸、放大倍率和随机种子；自动反推时上传一张参考图。

**核心模型与技术：** White Marble Z-Image Base AIO、Z-Image Turbo、Flux2 Klein 9B、Qwen3.6-35B 视觉 GGUF、LCS Color Anchor/Sharpness、瓦片三采、频率分离。

## C19-人物设定三视图zimage双采

**工作流类型：** 文生图

**主要用途：** 将简短角色设定扩写为统一的角色设定图提示词，再用 Z-Image Base 与 Turbo 双采生成一张包含头像、正面、侧面和背面的横向设定板。

**能做到的效果：**
- 将简短中文角色描述扩写为完整英文设定提示词。
- 生成左侧头像加右侧正、侧、背全身像的统一布局。
- 强调同一角色的脸、发型、体型和服装一致性。
- 使用纯白影棚背景和均匀平光呈现材质。
- 先用 Base 建立画面，再以 Turbo 接续补充细节。
- 可选使用 SeedVR2 输出高清版本。

**主要输入：** 角色设定文本、布局补充词、画面尺寸、随机种子和可选放大参数，无需上传图片。

**核心模型与技术：** White Marble Z-Image Base AIO、Z-Image Turbo、Qwen3.5 9B GGUF 提示词扩写、双阶段采样、SeedVR2。


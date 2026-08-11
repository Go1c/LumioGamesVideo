# D图像-Flux

本文档收录 `comfyui-workflow/D图像-Flux/` 目录下全部 15 个工作流，并按 Windows 文件名自然排序。说明依据各源 JSON 中的真实节点、输入项、模型配置与示例提示词整理。

## D01-flux1_dev基础工作流

**工作流类型：** 文生图

**主要用途：** Flux.1 Dev 基础文生图流程，使用英文长提示词从空白潜空间生成图片。源内示例为自然光、暖色调、浅景深和胶片颗粒质感的女性艺术家写实肖像。

**能做到的效果：**
- 根据英文场景、人物和摄影描述生成图片。
- 默认输出 1024×1024，可修改宽高和批量数。
- 支持随机种子及固定种子复现。
- 通过双文本编码器处理较长的细节描述。
- 采用零化负面条件的标准 Flux.1 Dev 采样链路。

**主要输入：** 英文正向提示词、输出宽高、批量数、随机种子、采样步数；无需上传图片。

**核心模型与技术：** `flux1-dev.safetensors`、`clip_l.safetensors`、`t5xxl_fp16.safetensors`、`ae.safetensors`、DualCLIPLoader、EmptySD3LatentImage、Euler + Simple 调度。

## D04-修复-Flux修手

**工作流类型：** 图像编辑

**主要用途：** 使用 Flux.1 Fill 对上传图片的遮罩区域进行局部重绘，主要面向手部结构修复。源内正向示例为 `perfect hands.`，也可填写其他英文局部编辑要求。

**能做到的效果：**
- 仅重绘手工涂抹的遮罩区域。
- 修复手指、手掌、关节及握持关系。
- 保留遮罩外的主体、服装和背景内容。
- 按最长边等比缩放图片与遮罩，默认 1536。
- 默认一次生成两个候选修复结果。

**主要输入：** 一张待修复图片、在遮罩编辑器中涂抹的区域、可选英文提示词、最长边分辨率、生成批次数、随机种子。

**核心模型与技术：** `flux.1-fill-dev-OneReward-transformer_fp8.safetensors`、T5-XXL FP8、CLIP-L、`ae.safetensors`、InpaintModelConditioning、Differential Diffusion、Flux Guidance、RepeatLatentBatch。

## D10-合集-FluxKlein文生图多图编辑大合集

**工作流类型：** 综合

**主要用途：** 集成 Flux 2 Klein 9B 的文生图和一至三图参考编辑流程，可组合人物、服装、物体、配饰与场景素材完成语义编辑和多图合成。

**能做到的效果：**
- 根据中文长提示词直接生成人物或场景。
- 单图修改人物外观、颜色、服饰与画面内容。
- 双图完成人物合影、换装或主体与场景融合。
- 三图组合人物、服装、配饰等多个视觉来源。
- 通过多级 ReferenceLatent 保留参考图特征。
- 支持自定义输出尺寸、种子和结果对照。

**主要输入：** 文生图模式输入文字提示词与输出尺寸；编辑模式上传一至三张参考图并填写编辑指令，同时设置随机种子。

**核心模型与技术：** Flux 2 Klein 9B FP8、Qwen3 8B 文本编码器、Flux2 VAE、ReferenceLatent、Flux2 Scheduler、SamplerCustomAdvanced。

## D11-合集-Flux2Klein超强多功能

**工作流类型：** 综合

**主要用途：** 将文生图、双图/三图参考编辑、局部重绘、扩图，以及 Canny、Depth、OpenPose 预处理集中在一套 Flux 2 Klein 9B 流程中。源内编辑示例为“保持产品的大小和位置不变，将产品放在欧式装修的客厅中”。

**能做到的效果：**
- 在空白潜空间与参考图编辑之间切换。
- 串联两至三张参考图完成产品置景和多素材合成。
- 利用上传图片的遮罩进行局部重绘。
- 向左右等方向扩展画布并羽化衔接区域。
- 从输入图生成 Canny、深度图或人体姿态参考。
- 可选使用 SeedVR2 对结果进行高清重建并比较前后效果。

**主要输入：** 一至三张参考图、局部重绘图片及遮罩、中文编辑提示词、输出宽高、随机种子；控制模块还可输入扩图边距、Canny 阈值和姿态图。

**核心模型与技术：** `flux-2-klein-9b-fp8.safetensors`、`qwen_3_8b_fp8mixed.safetensors`、Flux2 VAE、ReferenceLatent、InpaintModelConditioning、Canny/DepthAnything/OpenPose、ImagePadForOutpaint、SeedVR2。

**视频教程：** https://www.bilibili.com/video/BV1arkgBWE2p/

## D12-图生图-Flux2Klein单图

**工作流类型：** 图生图

**主要用途：** 对单张参考图进行 Flux 2 Klein 9B 重绘，并提供两条可对照的 LoRA 采样分支。源内可共享输入示例包括“将三维渲染的游戏画面，变为真实的照片”和将照片转成黑白钢笔素描数字绘画。

**能做到的效果：**
- 将游戏渲染画面转换为照片质感。
- 将彩色照片转为黑白钢笔线稿或数字绘画。
- 两个并行分支可使用不同步数与 LoRA 强度比较结果。
- 保留输入图的主体姿态、表情和基本构图。
- 自动按输入图尺寸建立输出潜空间。
- 将原图与两版结果组合成对照卷轴。

**主要输入：** 一张参考图、图像转换提示词、随机种子；可调整 LoRA、采样步数和输入缩放像素数。

**核心模型与技术：** Flux 2 Klein 9B FP8、Qwen3 8B、Flux2 VAE、`Klein-yizhixing-lora.safetensors`、ReferenceLatent、Flux2 Scheduler、双分支高级采样。

**视频教程：** https://www.bilibili.com/video/BV1LYPyzVE4Y/

## D13-图生图-Flux2Klein多图

**工作流类型：** 图像编辑

**主要用途：** 使用两张输入图进行多图参考编辑，并提供普通 Klein 与写实 LoRA 两条结果分支。源内示例指令为“将图1的女性模特服装换成图2”和“将蓝色区域替换为图2的瓶子”。

**能做到的效果：**
- 将图 2 的服装迁移到图 1 人物。
- 将图 2 的产品替换到图 1 指定区域。
- 串联两张图的 ReferenceLatent 保留主体与参考素材特征。
- 比较基础 Klein 与 DXrealistic LoRA 的编辑结果。
- 自动跟随输入尺寸建立采样尺寸。
- 拼接输入图与不同分支结果，便于直观对照。

**主要输入：** 图 1 主体图、图 2 服装或物体参考图、中文编辑指令、随机种子；可调整缩放像素数和 LoRA 强度。

**核心模型与技术：** Flux 2 Klein 9B FP8、Qwen3 8B、Flux2 VAE、`DXrealistic.safetensors`、ReferenceLatent、ImageStitch、Flux2 Scheduler。

**视频教程：** https://www.bilibili.com/video/BV1LYPyzVE4Y/

## D14-分镜-Flux克莱因9B多角度多场景

**工作流类型：** 图生图

**主要用途：** 从一张参考图自动分析主体与画面调性，生成连续多角度、多场景分镜提示词，再由 Flux 2 Klein 9B 输出分镜画面。源内提示词工程采用“焦点接力”规则，示例以夕阳下抱吉他的女孩演示连续镜头。

**能做到的效果：**
- 自动分析参考图属于静谧、悬疑或激烈画面。
- 提取视觉锚点并规划镜头焦点转移。
- 生成推进、特写、互动、后果和拉远等连续镜头。
- 通过单次换行拆分提示词并逐条送入图像生成。
- 保留原图主体特征，同时改变机位、动作和场景。
- 输出适合故事板使用的多镜头图像。

**主要输入：** 一张参考图、分镜系统提示词、需要生成的镜头组数、输出尺寸、随机种子；图像生成示例指令为“图1模特和图二模特合影站在图上的场景中”。

**核心模型与技术：** Flux 2 Klein 9B FP8、Qwen3 8B、Flux2 VAE、Qwen3.5 9B GGUF 视觉语言模型、llama.cpp、多行提示词拆分、ReferenceLatent、Flux2 Scheduler。

## D16-图生图-FluxKontext-Nunchaku加速

**工作流类型：** 图生图

**主要用途：** 使用 Nunchaku 量化加载 Flux.1 Kontext，对单张图片执行快速风格转换。源内示例提示为 `Transform into the zealman_ctdm style`，并配置动漫转真人方向的 Kontext LoRA。

**能做到的效果：**
- 根据英文指令转换输入图的整体视觉风格。
- 使用参考图潜空间保留主体和构图。
- 输入图默认裁切缩放到 1024×1536。
- 支持替换 Kontext LoRA 完成不同风格转换。
- 通过 FP4 DiT 与 INT4 T5 降低模型运行负担。

**主要输入：** 一张待转换图片、英文风格编辑提示词、目标宽高、LoRA 与强度、随机种子。

**核心模型与技术：** `svdq-fp4_r32-flux.1-kontext-dev.safetensors`、NunchakuFluxDiTLoader、AWQ INT4 T5-XXL、CLIP-L、`kontext-qtorealanime.safetensors`、FluxKontextImageScale、ReferenceLatent。

## D17-Klein-9B全自动换脸-任意姿势编辑

**工作流类型：** 综合

**主要用途：** 在同一套 Flux 2 Klein 9B 流程中提供自动换脸与任意姿势编辑。换脸示例要求用图 2 的面部和发型替换图 1，同时保留身体、服饰和背景；姿势示例要求保持人物与环境一致，仅按图 2 或 OpenPose 编辑器调整动作。

**能做到的效果：**
- 自动裁切面部参考并替换面部与发型。
- 可关闭头发遮罩，仅替换面部。
- 从姿势参考图或 OpenPose 编辑器生成目标姿态。
- 保留主体服装、配饰、环境、光影和色调。
- 分别输出换脸结果、姿势编辑结果及参考对照。
- 可选用 SeedVR2 对任一结果进行高清重建。

**主要输入：** 换脸模式上传主体图和面部参考图；姿势模式上传主体图和姿势参考图，或编辑 OpenPose 骨架；另可输入换脸/姿态中文指令、种子和高清重建参数。

**核心模型与技术：** Flux 2 Klein 9B FP8、Qwen3 8B、Flux2 VAE、PersonMaskUltra V2、AutoCropFaces、OpenPose Editor、ReferenceLatent、换脸与姿态 LoRA、SeedVR2。

**视频教程：** https://www.bilibili.com/video/BV1ZoSSBcEfX

## D18-Flux2Klein9b-5参考图版

**工作流类型：** 图像编辑

**主要用途：** 将最多五张可独立启停的参考图注入 Flux 2 Klein 9B，按文字描述组合多人物、多服装与场景。源内示例描述五位不同发型和服装的动漫女性在阳光草原合影。

**能做到的效果：**
- 同时引用最多五张图片中的角色与服装特征。
- 每张参考图可单独启用或关闭。
- 按图号描述人物，降低多角色属性混淆。
- 组合多人站位、互动、场景和整体画风。
- 支持 1920×1080 等自定义横向输出尺寸。
- 使用开关控制各 ReferenceLatent 是否加入条件链。

**主要输入：** 最多五张参考图及各自启用开关、完整画面提示词、输出宽高、随机种子。

**核心模型与技术：** `Flux2-Klein-9B-True-v2-fp8mixed.safetensors`、Qwen3 8B、Flux2 VAE、LoadImageWithSwitch、Switch Conditioning、串联 ReferenceLatent、Flux2 Scheduler。

## D18-klein9b真人剧制造机-多图编辑

**工作流类型：** 综合

**主要用途：** 多参考图真人剧与剧情画面制造流程，围绕人物绑定、场景恢复、镜头构图和剧情动作生成结构化提示词，再用 Flux 2 Klein 9B 完成多人合成与编辑。

**能做到的效果：**
- 组合多个人物、服装、道具和场景参考。
- 自动识别并分别描述各参考图角色。
- 按用户剧情指定人物位置、动作和互动。
- 支持近景、俯拍、背拍等镜头要求。
- 保持角色与参考图编号之间的对应关系。
- 支持结果对照与 SeedVR2 高清重建。

**主要输入：** 多张人物或场景参考图、剧情与编辑要求、画面构图要求、正向优化要求、输出尺寸、种子及高清重建参数。

**核心模型与技术：** Flux 2 Klein 9B、Qwen3 8B、Flux2 VAE、本地多模态 GGUF 提示词分析、llama.cpp、参考图拼接、串联 ReferenceLatent、SeedVR2。

## D18-klein9b真人剧制造机-多图编辑-极速版

**工作流类型：** 综合

**主要用途：** 面向多人真人剧照和剧情场景合成的多图编辑流程，自动把多张参考图拼接给本地视觉语言模型分析，再生成结构化中文提示词驱动 Flux 2 Klein 9B。源内示例为三名不同服装女性在上海外滩合影并向观众打招呼。

**能做到的效果：**
- 输入多张人物或场景参考图并组合到同一画面。
- 自动分析人物发型、服装、动作、道具和位置。
- 根据故事情节重写构图、站位与背景描述。
- 支持自由指令以及参考图描述、故事情节等结构化输入。
- 生成参考图与结果的拼接对照。
- 可选通过 SeedVR2 输出高清版本。

**主要输入：** 一至六张人物或场景参考图、中文故事/编辑要求、输出宽高、随机种子、SeedVR2 放大参数。

**核心模型与技术：** Flux 2 Klein 9B、Qwen3 8B、Flux2 VAE、Qwen3.6 35B A3B GGUF 视觉语言模型、llama.cpp、ImageConcatMulti、多级 ReferenceLatent、SeedVR2。

## D19-Flux2Klein9B超强一致换装

**工作流类型：** 图像编辑

**主要用途：** 使用人物图与服装参考图完成一致性换装。源内示例提示为“换装，保持服装、颜色一致”，并通过服装分割先提取参考图中的衣物区域，再注入 Klein 条件链。

**能做到的效果：**
- 将服装参考图的衣物迁移到目标人物。
- 保留服装颜色、款式和主要材质特征。
- 通过服装语义分割减少背景和人物身份干扰。
- 保留目标人物的脸、体型、姿势与场景。
- 自动按目标图尺寸建立输出潜空间。
- 提供原图与结果滑动对比。

**主要输入：** 一张目标人物图、一张服装参考图、中文换装提示词、输入缩放像素数、输出种子。

**核心模型与技术：** Flux 2 Klein 9B FP8、Qwen3 8B、Flux2 VAE、SegformerB2ClothesUltra、ReferenceLatent、Flux2 Scheduler、SamplerCustomAdvanced。

## D20-RAW画质重建Adonis_Workflow

**工作流类型：** 图生图

**主要用途：** 将手机画质、低分辨率、高 ISO、网点或轻微失焦图片重建为更清晰的彩色 RAW 观感。源内完整提示要求去除半色调网点、周期栅格与重复噪声，恢复皮肤、毛发、服装、背景和边缘细节，同时锁定人物身份与几何结构。

**能做到的效果：**
- 去除网点、栅格、斜线纹理和重复噪声。
- 重建低分辨率与高 ISO 区域的细节纹理。
- 对失焦和运动模糊区域进行边缘与细节恢复。
- 保留人物面部几何、身体比例、眼鼻口和表情。
- 恢复皮肤毛孔、发丝、服装与环境表面质感。
- 可添加轻量胶片颗粒并比较重建前后效果。

**主要输入：** 一张待重建图片、英文 RAW 重建提示词、输出百万像素、随机种子、总步数、基础/精修 LoRA 强度、胶片颗粒参数。

**核心模型与技术：** Flux 2 Klein 9B FP8、Qwen3 8B、Flux2 VAE、`flux2klein_adonis_base.safetensors`、`flux2klein_adonis_refine.safetensors`、RES4LYF 双阶段采样、ReferenceLatent、FastFilmGrain。

## D21-全自动换脸Klein9b-bfs

**工作流类型：** 图像编辑

**主要用途：** 使用 Flux 2 Klein 9B BFS 模型自动完成换脸。源内示例要求将图 1 人物面部替换为图 2 的面部与妆容，不改变服装，并保持色调与环境融合。

**能做到的效果：**
- 自动检测并裁切面部参考区域。
- 将参考脸与妆容迁移到目标人物。
- 保留目标图服装、身体、姿势和背景。
- 通过多级 ReferenceLatent 同时约束主体图与面部图。
- 按目标图尺寸采样，并支持 1 至 1.5 百万像素输入处理。
- 提供原图与换脸结果对比并保存输出。

**主要输入：** 图 1 目标人物图、图 2 面部参考图、中文换脸指令、处理像素数、随机种子。

**核心模型与技术：** `F2K-9b-darkBeastMar0326Latest_dbkleinv2BFS.safetensors`、Qwen3 8B、Flux2 VAE、AutoCropFaces、FluxKontextImageScale、ReferenceLatent、Flux2 Scheduler、SamplerCustomAdvanced。


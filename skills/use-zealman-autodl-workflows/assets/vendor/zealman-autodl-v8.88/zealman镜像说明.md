# 🎨 Zealman ComfyUI (v8.88)

欢迎使用 Zealman ComfyUI
本镜像旨在为用户提供“零门槛”的 AI 创作体验。
<span style="font-weight:bold; background:linear-gradient(to right, red, red); -webkit-background-clip:text; color:transparent;">- 禁止基于本镜像二次开发后发布！！！</span>
<span style="font-weight:bold; background:linear-gradient(to right, orange, orange); -webkit-background-clip:text; color:transparent;">- 工作流全无加密全免费+ 不再为加密工作流付费困扰</span>
<span style="font-weight:bold; background:linear-gradient(to right, orange, orange); -webkit-background-clip:text; color:transparent;">- API创建，方便集成到您自己的自主项目调用更便捷</span>
<span style="font-weight:bold; background:linear-gradient(to right, orange, orange); -webkit-background-clip:text; color:transparent;">- 镜像内置并发生成功能，智能负载均衡多工作流</span>

## 🐧1群1046279436（满） 🐧2群1102535136

![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-813015505-ZoMYV6nMJ2QDjyAR5TSF.png)

**进入控制面板打开comfyui（默认自动启动）**![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-155685863-S7PtjdHgl8LkLkWvbv26.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-390732651-lEYb6MSJAVnuWgEkIgek.png)

<iframe src="https://player.bilibili.com/player.html?bvid=BV1RwXvBpEJg&page=1" style="width:100%; height:500px;"
        scrolling="no" frameborder="no" allowfullscreen="true"> </iframe>
**Zealman bilibili地址**

https://space.bilibili.com/295578108

**字字Autodl-zealman插件文字版说明和下载**
https://my.feishu.cn/wiki/SJDhwbLrviXiQ2kbd0gcfVcAnah?from=from_copylink

**字字Autodl-zealman插件视频说明**
https://www.bilibili.com/video/BV1ekoqBBEPt

## v8.88版本：

comfyui  **v0.27.1**（支持自动升降切换版本，内置依赖自动安装，并发接口同步支持）
工作流矩阵按当前镜像目录重排同步（活跃 **235** 套，含 OLD 共 **267** 套）：

1.新增30+ int8_convrot加速模型，几乎涵盖了常见个各种图像视频基础类模型
2.插件集体更新到最新版
3.增强前后端，并发生成，现在支持批量添加多个图像或视频生成任务自动跑。支持主机内批量添加参考图片、视频、音频文件等做为生成素材，URL方式批量传参数。支持开多个镜像机器，并发智能分配任务。生成结果全部自动拉取到主机，支持一键打包自定义时间段内所有结果文件下载到本地。如果工作流中增加oss节点也支持跑完自动上传到您的oss地址。
4.新增多个LTX2.3,KREA2工作流。
5.新增 P24/P25 Scail-2 高阶 Plus v4（人物替换、动作迁移分拆）及 P27 Scail2 循环动作迁移长视频。
6.最容易的低成本AI创业赚钱项目 = 开一zealman镜像，自己写个网页前端调镜像的API+充值功能。一个镜像可队列任务，用户多开多个镜像可智能分配任务,怎么省钱都帮你做了。

**管理面板**

- 支持 ComfyUI 一键启动、停止、状态查看
- 启动后可显示公网访问地址并快速复制

**开发者 API 与并发集群**

- 内置 `ZEALMAN-API` 示例工作流
- 支持将当前镜像内可跑通的工作流转换为 API 接口
- 支持并发运行工作流，调用镜像集群量产视频、图像、漫剧

**模型与文件管理**

- 支持大文件分块上传 `.safetensors`、`.bin`
- 支持AutoDL官方模型库软链接挂载模型，常用模型日更全覆盖
- 支持模型目录管理与迁移，无缝换镜像版本

**资产与系统管理**

- 资产管理界面查看生成结果更方便
- 支持批量打包下载生成结果与批量清理输出文件
- 支持集群并发资产管理查看

**预制工作流矩阵（与 `/root/ComfyUI/user/default/workflows` 同步，当前活跃 **235** 套；含 OLD 历史兼容共 **267** 套）**

| 分类目录 | 数量 | 说明 |
|----------|------|------|
| A图像-Qwen生成 | 10 | Qwen 文生图、洗图、ControlNet、Nunchaku |
| B图像-Qwen编辑 | 17 | Qwen 编辑、多角度、换脸、ControlNet、多视图循环 |
| C图像-Zimage | 19 | Zimage 基础、洗图、黑兽、Moody、双采/瑶光/kinghere、三视图等 |
| D图像-Flux | 15 | FluxKlein、Flux2Klein、Klein9B 换脸/剧制造机、RAW 重建 |
| E图像-SDXL-IL | 3 | Illustrious、SDXL、二次元漫画 |
| F图像-FireRed图像编辑 | 2 | FireRed 图像编辑、人物换背景 |
| G视频-Wan图生 | 26 | Wan2.2、首尾帧、长视频、Ditto、大丝袜、精品漫剧流 |
| H视频-LTX | 31 | LTX2.3、音画同步、首尾帧、数字人/歌手、导演台、短剧/多参考 |
| H黑鹤001Ltx终章 | 5 | 黑鹤001 LTX2.3 全能编辑、动作迁移、去字幕水印等 |
| J视频-对口型数字人 | 15 | InfiniteTalk、LTX2.3 数字人、电商带货、Bernini 换产品 |
| K视频-人物替换 | 12 | 换装、影视二创、Bernini、SCAIL2 角色替换 |
| L视角-高斯泼渐 | 2 | 高斯泼溅 3D 改角度 |
| M高清放大去水印 | 14 | 放大、修复、视频修复、去水印、RTX 放大、超分 |
| N声音 | 8 | FishAudio S2pro；mmaudio；ACE-Step；QwenTTS；stable-audio |
| P视频-动作迁移 | 23 | Wan Animate、Scail2、SteadyDancer、分段队列长视频等 |
| Q分镜图gptimage-banana2类 | 1 | 全能图像 Pro 剧情分镜 |
| R图像-Ideogram | 5 | Ideogram4 文生图、宫格故事板 |
| S图像-Boogu | 2 | boogu 图像生成、编辑 |
| T-图像-Krea | 6 | Krea2 文生图、双采/三采、角色三视图、美学流 |
| Y通用制作 | 8 | 通用图像生成与编辑入口 |
| Z工具设置 | 10 | API 示例、批量加载、清缓存等 |
| 根目录补充 | 2 | JoyAI-Echo 多镜头音视频；通用反推 |
| OLD（历史兼容） | 33 | LTX2.0、旧 Flux/Animate、BindWeave、MoCha 等 |

---

## 当前完整工作流目录清单

### /root/ComfyUI/user/default/workflows/A图像-Qwen生成

- A01-文生图-Qwen2512高清放大.json
- A02-文生图-Qwen无限素材多分镜多角度.json
- A03-洗图-Qwen洗图大合集.json
- A04-洗图-Qwen2512艺术感高清放大.json
- A05-洗图-Qwen2512真实感高清放大.json
- A06-图生图-QwenControlNet.json
- A08-洗图-Qwen二次元转真人高清放大.json
- A09-图生图-QwenControlNet-Nunchaku加速.json
- A10-文生图-Qwen-Nunchaku加速.json
- A11-QuantFunc-Nunchaku-Qwen-Image-2512.json

### /root/ComfyUI/user/default/workflows/B图像-Qwen编辑

- B01-编辑-Qwen编辑合集.json
- B02-编辑-Qwen2511单双三图编辑.json
- B03-编辑-Qwen2511单双三图编辑V2.json
- B04-编辑-Qwen2511多角度多场景分镜.json
- B05-编辑-Qwen2509人物多角度展示.json
- B06-编辑-Qwen2509极限姿态参考.json
- B07-编辑-Qwen极速换脸.json
- B08-编辑-Qwen2511多角度V1.json
- B09-编辑-Qwen2511多角度V2.json
- B10-编辑-Qwen2511多角度分镜.json
- B11-编辑-Qwen人物一致性ControlNet.json
- B12-编辑-Qwen2509编辑Nunchaku加速.json
- B13-千问角色一键多角度_multiple_character_angles-v1.0.json
- B14-QWEN-AIO-人物自由姿势编辑.json
- B15-Qwen自动生成多视图for循环.json
- B16-多图参考生成分镜4宫格-9宫格-25宫格-By跳爷.json
- B17-一键图片转360全景图.json

### /root/ComfyUI/user/default/workflows/C图像-Zimage

- C01-文生图-Zimage基础版.json
- C02-文生图-ZimageControlNet.json
- C03-文生图-ZimageDetailDaemon.json
- C04-文生图-Zimage红潮ZIB超真实感定妆照.json
- C05-洗图-Zimage洗图大合集.json
- C06-洗图-Zimage终极版自动洗图CN高清放大.json
- C07-文生图-Zimage-Nunchaku加速.json
- C08-图像黑兽DarkBeast-ZiT-V8-UltraSimple-Workflow-ComfyUI.json
- C09-图像黑兽DarkBeast-ZIT&Klein-V8-Hybrid-Workflow-ComfyUI.json
- C10-图像Moody Zimage Simple Workflow - V4.json
- C11-Zimage双采-三采-双放大.json
- C12-瑶光-动漫-MJ风格工作流.json
- C13-kinghere-Z-image-动漫-小说-造影.json
- C14-黑鹤001-ZITB+F2K+NSW+高清修复(整合流).json
- C15-Z-ImageBase&Turbo双重采样洗图工作流.json
- C16-短剧文生图专用-支持场景-角色.json
- C17-Z-image瑜伽服小姐姐.json
- C18-豹豹喵呜制作-白玉AIO三采超高清写真生成.json
- C19-人物设定三视图zimage双采.json

### /root/ComfyUI/user/default/workflows/D图像-Flux

- D01-flux1_dev基础工作流.json
- D04-修复-Flux修手.json
- D10-合集-FluxKlein文生图多图编辑大合集.json
- D11-合集-Flux2Klein超强多功能.json
- D12-图生图-Flux2Klein单图.json
- D13-图生图-Flux2Klein多图.json
- D14-分镜-Flux克莱因9B多角度多场景.json
- D16-图生图-FluxKontext-Nunchaku加速.json
- D17-Klein-9B全自动换脸-任意姿势编辑.json
- D18-Flux2Klein9b-5参考图版.json
- D18-klein9b真人剧制造机-多图编辑-极速版.json
- D18-klein9b真人剧制造机-多图编辑.json
- D19-Flux2Klein9B超强一致换装.json
- D20-RAW画质重建Adonis_Workflow.json
- D21-全自动换脸Klein9b-bfs.json

### /root/ComfyUI/user/default/workflows/E图像-SDXL-IL

- E01-文生图-Illustrious.json
- E02-文生图-SDXL-SmoothWorkflow.json
- E03-文生图-二次元漫画模型.json

### /root/ComfyUI/user/default/workflows/F图像-FireRed图像编辑

- F01-FireRed-Image-Edit-1.json
- F02-图像-FireRed人物换背景.json

### /root/ComfyUI/user/default/workflows/G视频-Wan图生

- G01-图生视频-Wan2.2万相基础版.json
- G01-图生视频-Wan2.2优化版.json
- G02-首尾帧-Wan2.2首尾帧视频.json
- G03-图生视频-Wan2.2SmoothMix.json
- G04-图生视频-Wan2.2SmoothMix图生.json
- G05-图生视频-Wan2.2+LightX2V最强动态.json
- G06-首尾帧-Wan2.2+LightX2V超动感.json
- G07-图生视频-Wan2.2+LightX2V-WorkFisher.json
- G09-长视频-Wan2.2StoryMem多分镜无限.json
- G10-图生视频-Wan2.2SmoothMixV2.json
- G11-长视频-SVIPro长视频.json
- G12-长视频-Wan2.2Remix+SVI2Pro全自动反推.json
- G13-长视频-Wan2.2Remix多角度首尾帧循环.json
- G14-图生视频-Wan2.2SmoothV2+SVI2Pro全自动.json
- G15-视频-Wan2.2首中尾帧FMLF.json
- G16-合集-图生视频大合集.json
- G17-长视频-SVIShot三图无限续播.json
- G18-图生视频-FFGO官方流.json
- G20-首尾帧-大丝袜首尾帧.json
- G21-图生视频-大丝袜8.1单双三图.json
- G22-图生视频-大丝袜I2V自动提示词动态加强.json
- G23-图生视频-大丝袜基础版.json
- G24-ditto真人转动漫(视频).json
- G25-DasiwaV10高动态逻辑优化-Qwen3.5提示词优化.json
- G26-黑鹤001-Magic-Wan-T2IV-V3+生图+视频流.json
- G27-人物替换-背景替换-Wan2.2 Animate-姿态对齐-Sam3.1-SDPose最强工作流-肥猴V5.json

### /root/ComfyUI/user/default/workflows/H视频-LTX

- H14-LTX2.3-导演台2.0.json
- H15-文图生视频-LTX2.3二合一GGUF版.json
- H16-文图生视频-LTX2.3二合一标准版.json
- H17-文图生视频-LTX2.3全面优化版.json
- H18-图生视频-LTX2.3.json
- H19-文生视频-LTX2.3.json
- H20-多人语音克隆+LTX2.3 音画同步.json
- H21-LTX2.3双图-首尾帧优化版.json
- H22-LTX-I2V-First-Last-Frame-2-Stage-Workflow-v6.json
- H23-LTX-I2V-First-Last-Frame-3-Stage-Workflow-v6.json
- H24-LTX2.3 AI2V Audio 图片音频驱动数字人（强化版）  (0331).json
- H25-LTX2.3 I2V First Last Frame 首尾帧V1.json
- H26-LTX2.3 TI2V 图文生视频（强化版） (0331).json
- H27-LTX2.3首尾帧.json
- H28-LTX2.3-高动态图生视频.json
- H29-LTX2.3图片数字人歌手.json
- H30-四宫格-LTX-2.3图生视频-全面优化版.json
- H31-LTX2.3导演台工作流-单采.json
- H32-LTX2.3导演台工作流-双采.json
- H33-四宫格分拆.json
- H34-LTX2.3导演台工作流zealman群主版.json
- H35-LTX2.3导演台低显存.json
- H36-LTX2.3-10Eos_I2V.json
- H37-LTX2.3全栈式短剧生成V18.7.json
- H37-LTX2.3全栈式短剧生成V19.3(易用版).json
- H37-Z-Image短剧拍档支持场景和角色V5.json
- H38-4宫格LTX2.3导演台.json
- H39-LTX2.3-LTX-Director-导演分镜工作流-更强的控制性-电商带货.json
- H40-LTX2.3动漫数字人特制版.json
- H41-AI代码侠土豆-LTX2.3-MSR多参考图生成.json
- H42-LTX-2.3-4宫格V3短剧-镜头硬切版.json

### /root/ComfyUI/user/default/workflows/H黑鹤001Ltx终章

- ▶▶LTX23-全能视频编辑流.json
- ▶▶LTX23-动作迁移流.json
- ▶▶LTX23-图音编辑流(导演节点).json
- ▶▶LTX23-指定替换视频编辑.json
- ▶▶LTX23-视频去字幕水印流.json

### /root/ComfyUI/user/default/workflows/J视频-对口型数字人

- J01-对口型-LTX2.3数字人GGUF版.json
- J02-对口型-LTX2.3数字人标准版.json
- J03-对口型-InfiniteTalk官方流长视频无衰减.json
- J04-对口型-InfiniteTalk单人图像驱动.json
- J05-对口型-InfiniteTalk单人视频驱动.json
- J06-对口型-InfiniteTalk双人图像驱动.json
- J07-对口型-高动态音画视频口型一条龙.json
- J08-LTX2.3数字人说话唱歌对口型-优化升级kj版.json
- J09-LTX2.3双人对话-图生视频音画同步-KJ优化版.json
- J10-AI代码侠土豆-LTX2.3数字人.json
- J11-LTX2.3高清超自然电商数字人.json
- J11-提示词参数预处理.json
- J12电商数字人物替换-姿态迁移-背景替换v3版.json
- J13-小珠光90秒全自动版-单人InfiniteTalk.json
- J14-Bernini-电商换产品视频编辑.json

### /root/ComfyUI/user/default/workflows/K视频-人物替换

- K01-换装-Wan换头换服装换背景娱乐流.json
- K02-换装-Wan2.2不挑图换装流.json
- K03-影视二创-Wan影视二创.json
- K04-影视二创-WorkFisher单人版.json
- K05-影视二创-WorkFisher多人版.json
- K06-Wan-Animate最强视频人物替换-动作迁移.json
- K07-人物替换-背景替换-Wan2.2 Animate-姿态对齐-Sam3.1-SDPose最强工作流-肥猴V5.json
- K08-Wan2.2-Bernini人物替换-动作迁移-多图参考-视频编辑工作流v1版.json
- K09-Bernini-视频换人-角色替换.json
- K10-豹豹喵呜-SCAIL-V2动作迁移-角色替换二合一工作流.json
- K11-SCAIL2动作迁移-角色替换-支持长视频-像素幻想Lab.json
- K13-AI代码侠土豆-SCAIL2-全自动循环流.json

### /root/ComfyUI/user/default/workflows/L视角-高斯泼渐

- L01-视角改变-高斯泼溅3D改角度V1.json
- L02-视角改变-高斯泼溅3D改角度V2.json

### /root/ComfyUI/user/default/workflows/M高清放大去水印

- M01-放大-SUPIR高清放大.json
- M02-放大-SeedVR2+TTP高清放大.json
- M03-放大-SeedVR2高清放大.json
- M04-修复-SeedVR2.5+FlashVSR图像修复放大.json
- M05-视频修复-SeedVR2.5+FlashVSR视频修复放大.json
- M06-去水印-AI视频去小面积水印ProPainter.json
- M07-NVIDA-RTX高清放大.json
- M08-视频水印移除流-B站小珠光.json
- M09-LTX一键去字幕水印去模糊.json
- M10-视频高清放大+补帧-SeedVR2.json
- M11-极致真实V2-亿级像素超分放大By像素幻想Lab.json
- M12-LTX2.3视频处理全功能合集-By-像素幻想Lab.json
- M13-Klein图像批量自动去水印.json
- M13-豹豹喵呜-超分放大V2.json

### /root/ComfyUI/user/default/workflows/N声音生成-音乐生成-声音克隆

- N1-多人声音克隆FishAudio S2pro.json
- N2-单人声音克隆FishAudio S2pro.json
- N3-双人声音克隆FishAudio S2pro.json
- N4-mmaudio_NSFW.json
- N5-黑鹤001-ACE-Step-音乐&歌曲生成流.json
- N6-Qwen3TTS音频克隆.json
- N6-Qwen3TTS音频创造.json
- N7-stable-audio-3-medium.json

### /root/ComfyUI/user/default/workflows/P视频-动作迁移

- P01-动作迁移-Wan多人姿态迁移最强版高配24G.json
- P02-动作迁移-Wan2.2Animate角色迁移.json
- P03-动作迁移-Wan2.2Animate循环长视频V2.json
- P04-动作迁移-SCAIL+SDPose+Uni3C最强全场景.json
- P05-动作迁移-Scail单双人自由切换.json
- P06-动作迁移-SteadyDancer骨骼迁移不限时长.json
- P07-动作迁移-Wan2.2AnimateV4.json
- P08-Wan2.2-Animate-动作迁移-视频延长.json
- P11超级王炸-分段队列-自动拼接长视频-人物丝滑换装-肥猴.json
- P12-动作迁移-小马.json
- P14-Ltx2.3动作模仿-图片跳舞-动作迁移.json
- P15-动作迁移-Wan2.2-Animate-动作迁移V7.1.json
- P16-Wan2.2 Animate动作迁移天花板真人动作对齐Q版人物-全身动作对齐半身图像.json
- P17-动作迁移-Wan2.2-Animate-动作迁移V8.json
- P18-Wan2.2-Animate-动作迁移天花板级工作流-支持Q版人物-小动物等V5.json
- P19-动作迁移-Wan2.2-Animate-动作迁移V9.json
- P20-动作迁移-Wan2.2-Animate-动作迁移V9-多参考图.json
- P22-爱屋Scail2-TTP多参-内循环-面部强化.json
- P23-豹豹喵呜-SCAIL-V2动作迁移&角色替换二合一工作流-V2.json
- P24-肥猴Scail-2人物替换-高阶Plus工作流v4.json
- P25-肥猴Scail-2动作迁移-高阶Plus工作流v4.json
- P26-肥猴分段队列-Scail-2动作迁移+人物替换-高阶Plus工作流v1.json
- P27-Scail2循环动作迁移-长视频.json

### /root/ComfyUI/user/default/workflows/Q分镜图gptimage-banana2类

- Q1-全能图像Pro剧情分镜设计.json

### /root/ComfyUI/user/default/workflows/R图像-Ideogram

- R01-Ideogram4半自动文生图-Work-Fisher-V2.json
- R02-Ideogram4工作流带翻译节点+kjnodes区域提示词节点.json
- R03-image_ideogram4_t2i.json
- R04-ideogram4出九宫格故事板.json
- R05-ideogram4出四宫格-六宫格.json

### /root/ComfyUI/user/default/workflows/S图像-Boogu

- S01-boogu文生图.json
- S02-boogu图像编辑.json

### /root/ComfyUI/user/default/workflows/T-图像-Krea

- T1-Krea2文生图超强写实质感.json
- T2-豹豹喵呜-白玉AIO-Krea2双采4K直出.json
- T3-Krea2三采流-全自动文生图全模式.json
- T4-Krea2-int8-角色设定三视图.json
- T5-krea2-leggings-瑜伽裤小姐姐-美学文生图.json
- T6-krea2-klein-包臀裙小姐姐.json

### /root/ComfyUI/user/default/workflows/Y通用制作

- Y01-图像修改千问2511.json
- Y02-图像修改克莱因.json
- Y03-图像修改FireRed.json
- Y04-图像生成Zimage.json
- Y05-图像生成Qwen2512.json
- Y06-图像改为下一个场景图.json
- Y07-Klein-文生图.json
- Y08-四宫格-LTX-2.3图生视频优化版.json

### /root/ComfyUI/user/default/workflows/Z工具设置

- Z01-工具-ZealmanAPI示例.json
- Z02-工具-通用替换模组.json
- Z03-工具-批量描述生成器.json
- Z04-设置-ComfyUI批量加载.json
- Z05-设置-ComfyUI视频帧数设置.json
- Z06-设置-API重复调用清缓存.json
- Z07-设置-最后一帧输出图像.json
- Z08-设置-视频补帧.json
- Z09-视频补帧-防丢帧-防偏色.json
- Z11-XY图表测试工作流.json

### /root/ComfyUI/user/default/workflows/OLD

- A07-文生图-Qwen-Image-Layered分层模型.json
- D01-文生图-Flux图生图文生图.json
- D02-文生图-FluxXY-LoRA测试.json
- D05-风格转换-FluxKontext半Q转写实立绘.json
- D06-图生图-FluxKontext换POSE.json
- D07-风格转换-FluxKontextQ版转写实动漫.json
- D08-文生图-Flux2DEV.json
- D09-图生图-Flux2DEV多图编辑.json
- D15-文生图-Flux-Nunchaku加速.json
- H01-图生视频-LTX2-I2V-IC控制Pose.json
- H02-图文生视频-LTX2基础版自定义音频.json
- H03-图文生视频-LTX2-IC控制全合一PoseCanny深度.json
- H04-图文生视频-LTX2简单版K采样.json
- H05-图文生视频-LTX2简单版单遍.json
- H06-文生视频-LTX2.0低显存版.json
- H07-图生视频-LTX2.0-48G专用.json
- H08-文生视频-LTX2.0多模态全自动16秒低配.json
- H09-图生视频-LTX2.0多模态全自动.json
- H10-首尾帧-LTX2.0多模态全自动首尾帧.json
- H11-文生视频-LTX2.0-48G专用.json
- H12-文生视频-LTX2.0小黄瓜版.json
- H13-图生视频-LTX2.0深度控制-48G.json
- H14-图生视频-LTX2.0线稿控制-48G.json
- O1-BindWeave单角色.json
- O2-BindWeave场景+双角色.json
- P08-动作迁移-Wan2.2Animate角色迁移V5.json
- P09-动作迁移-Wan2.2-Animate-动作迁移V6.json
- P10-动作迁移-Wan2.2-Animate-动作迁移V6.1.json
- P13-动作迁移-Wan2.2-Animate-动作迁移V7.json
- Wan2.2MoCha手动+面部参考.json
- Wan2.2MoCha手动.json
- Wan2.2MoCha自动.json
- Wan2.2Mocha自动+面部参考可用.json

### /root/ComfyUI/user/default/workflows（根目录）

- JoyAI-Echo 多镜头连贯视频与音频生成.json
- 通用反推.json

---

**画布系统**
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-741826522-IG9EOuwZcmyNVK0ZDLH5.png)

**快捷面板**
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-855406854-oqZcCACRAiqWTNTPdhop.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-634200177-T0OYE75g8YVrEoaN9ho7.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-388550552-KMFsC6Okc1lkSLZiw2sQ.png)

![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-79161906-bKLtK0CkNiguz3o5JWkK.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-802343118-HzGsB9o2ZZkyznHV1LvT.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-640053878-X22i7x6nYEt8AbERc3US.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-446122174-6XXPxCpwLljWkzh6Ckd6.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-507149246-U1MLqQAOtYqBb8HKLx0N.png)
**我的资产**
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-533611244-ChcvXDxAXg60hjm7vNxz.png)

![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-289103918-hiwgcogycgNnHG7jIT8j.png)

**工作流生成API**
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-386384697-iOtx4NxwL3RNUGwoU6sl.png)
![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-509228806-zRhUSRPVnErdl7eG98ss.png)

**多主机并发生成**

![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-898251542-W5ZNIAdjMyTC9LNSFPsr.png)

**左下角可切换暗色主题**

![image.png](https://codewithgpu-image-1310972338.cos.ap-beijing.myqcloud.com/98101-283385188-3175mwO7LSp3za1no0OK.png)

zealman autodl镜像提供**一体化 AIGC 开发与出图环境**，常年霸榜autodl应用镜像：

内置 **ComfyUI** 与可视化管理，支持一键启停、状态与**公网访问地址**展示；

配套 **ZEALMAN-API** 示例，并可将镜像内已验证工作流**封装为 API** 便于对接业务。

支持 **大模型分块上传**，**软链接挂载与目录迁移**，降低重复下载与磁盘占用；

在产出侧支持生成结果**实时预览**、**批量打包下载与清理**、**磁盘与缓存治理**及 **ComfyUI API** 配置，并支持从其他机器**同步目录/文件**到本机。

内容生产上预置**多分类200+预制工作流矩阵**，覆盖 **Qwen 文生图/洗图/编辑/ControlNet**、**Zimage**、**Flux / FluxKlein / Klein9B**、**Krea2**、**SDXL / Illustrious**、**FireRed 图像编辑**、**Ideogram4**、**Boogu**，以及 **Wan2.2、LTX2.3** 等**图生视频与长视频**能力，并延伸至**精品漫剧、流量短剧、动作迁移、舞蹈模仿、对口型、数字人、电商带货、换装、影视二创、Bernini、Scail-2、超清放大、去水印、FishAudio / QwenTTS 声音克隆**与通用制作/工具流，适合作为**可检索、可推广的「开箱即用 ComfyUI + API + 资产与模型管理」镜像方案**。

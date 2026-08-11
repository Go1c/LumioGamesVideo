# Codex 镜像功能指引（Zealman ComfyUI v8.88）

> 面向 **Codex / Cursor Agent** 连接本镜像后的快速导航：先定位能力 → 再选工作流 / 快捷页 / API → 再按约定修改与验证。  
> 用户说明与完整工作流清单见 [`zealman镜像说明.md`](./zealman镜像说明.md)。  
> **仅使用镜像内用户可见路径**（`/root/zealman-app`、`/root/ComfyUI` 等），勿依赖或写入用户不可见的开发目录。

---

## 0. 30 秒决策树

| 用户意图 | 优先入口 | 工作流目录 / 页面 |
|----------|----------|-------------------|
| 文生图 / 写真 / 三视图 | ComfyUI 工作流 或 快捷生成 | `A`/`C`/`T`/`D`；快捷页 `c18`/`t4`/`d14` |
| 改图 / 换脸 / 多角度 / 分镜图 | ComfyUI 工作流 | `B`/`D`/`F`/`Q`；快捷页 `b13`/`p18` |
| 图生视频 / 首尾帧 / 长视频 | 快捷生成 或 ComfyUI | `G`/`H`；快捷页 `image-to-video*` / `h41` |
| 短剧 / 导演台 / 影视二创 | ComfyUI 工作流 | `H`（导演台/短剧）、`K`（二创） |
| 动作迁移 / 人物替换 | 快捷生成 或 ComfyUI | `P`/`K`；快捷页 Animate V1/V4 |
| 对口型 / 数字人 / 电商口播 | 快捷生成 或 ComfyUI | `J`；快捷页 `j08`/`j11`/`j13` |
| 声音克隆 / TTS / 配乐 | 快捷生成 或 ComfyUI | `N`；快捷页 `j-single-voice-clone`/`n6` |
| 放大 / 去水印 / 修复 | 快捷生成 或 ComfyUI | `M`；快捷页 `m02` |
| 封装 HTTP API / 批量调用 | 面板「API 生成」 | `/root/zealman-app/workflows/` |
| 多机并发生成 | 面板「并发生成」 | `concurrent-generate` |
| 改工作流实现功能 | ComfyUI 工作流目录 | 见 §11 |

**默认服务**：面板 `6008`，ComfyUI `6006`（非 8188）。外网：`u…:8443`→面板，`a…:8443`→ComfyUI。

---

## 1. 环境与路径（用户可见）

| 用途 | 路径 |
|------|------|
| 管理面板 / 服务 | `/root/zealman-app/` |
| ComfyUI | `/root/ComfyUI/` |
| 预制工作流（UI JSON） | `/root/ComfyUI/user/default/workflows/` |
| 工作流备份镜像 | `/root/zealman-app/comfyui-workflows/` |
| API 工作流（`_api_config`） | `/root/zealman-app/workflows/` |
| 快捷生成 API-JSON 模板 | `/root/zealman-app/public/`（构建产物也在 `dist/`） |
| 插件目录 | `/root/ComfyUI/custom_nodes/` |
| 输出 | `/root/ComfyUI/output/` |
| 并发输入资产 | `/root/并发/` |
| 模型软链接配置 | `/root/zealman-app/modellink/user_models.json` |
| 面板配置 | `/root/zealman-app/config.json` |

```bash
# 健康检查
curl -s http://localhost:6008/api/health
curl -s http://localhost:6008/api/comfy/status
curl -s http://localhost:6008/api/comfy/external-url
```

服务启停（生产）：

```bash
cd /root/zealman-app && bash start-services.sh
```

---

## 2. 能力地图：图像生成

在 ComfyUI 左侧工作流浏览器打开对应分类；或面板「快捷生成」用已封装页。

| 系列 | 目录 | 推荐工作流 | 何时选用 |
|------|------|------------|----------|
| Qwen | `A图像-Qwen生成/` | `A01` 文生图高清放大；`A03` 洗图合集；`A10` Nunchaku 加速 | 通用中文提示、洗图、加速出图 |
| Zimage | `C图像-Zimage/` | `C01` 基础；`C11` 双采三采；`C16` 短剧文生图；`C18` 白玉 AIO；`C19` 人物三视图 | 写真、短剧角色/场景图、三视图 |
| Flux / Klein | `D图像-Flux/` | `D10`/`D11` 合集；`D14` 克莱因 9B 分镜；`D18` 剧制造机；`D20` RAW 重建 | 分镜、多图编辑、画质重建 |
| Krea2 | `T-图像-Krea/` | `T1` 写实质感；`T2` 双采 4K；`T3` 三采全模式；`T4` 角色三视图 | 强写实、角色设定表 |
| SDXL / 二次元 | `E图像-SDXL-IL/` | `E01` Illustrious；`E02` SDXL；`E03` 漫画 | 二次元 / SDXL 生态 |
| Ideogram | `R图像-Ideogram/` | `R01` 文生图；`R04` 九宫格故事板；`R05` 四/六宫格 | 文字排版感强、故事板 |
| Boogu | `S图像-Boogu/` | `S01` 文生图 | 轻量文生图 |
| 通用入口 | `Y通用制作/` | `Y04` Zimage；`Y05` Qwen；`Y07` Klein | 给业务/API 做统一入口时优先 |

**快捷生成（图像相关）**

| pageId | 名称 | 底层工作流 |
|--------|------|------------|
| `d14-flux-klein-storyboard` | Flux 克莱因 9B 分镜 | `D14-…` |
| `d20-raw-restore` | RAW 画质重建 | `D20-…` |
| `p18-klein9b-drama-multi-edit` | Klein9B 真人剧多图编辑 | `D18-klein9b真人剧制造机-多图编辑` |
| `c18-baiyu-aio-portrait` | 白玉 AIO 三采写真 | `C18-…` |
| `t4-krea2-character-sheet` | Krea2 角色三视图 | `T4-…` |

---

## 3. 能力地图：图像编辑

| 系列 | 目录 | 推荐工作流 | 何时选用 |
|------|------|------------|----------|
| Qwen 编辑 | `B图像-Qwen编辑/` | `B01` 合集；`B07` 极速换脸；`B13` 角色多角度；`B15` 多视图循环；`B16` 多宫格分镜 | 指令编辑、角色一致性、宫格分镜 |
| Klein / Flux 编辑 | `D图像-Flux/` | `D17` 换脸姿势；`D18` 多图剧制造机；`D19` 一致换装 | 真人剧、换装、多参考编辑 |
| FireRed | `F图像-FireRed图像编辑/` | `F01` 编辑；`F02` 换背景 | 人物换背景 |
| 分镜 Pro | `Q分镜图gptimage-banana2类/` | `Q1` 全能图像 Pro 剧情分镜 | 剧情分镜设计 |
| Boogu | `S图像-Boogu/` | `S02` 图像编辑 | 轻量编辑 |

**快捷生成**：`b13-qwen-multi-character-angles`（QwenEdit 角色多角度）。

---

## 4. 能力地图：视频（Wan / LTX）

### 4.1 Wan 图生 / 长视频 — `G视频-Wan图生/`

| 推荐 | 说明 |
|------|------|
| `G01` 万相基础 / 优化版 | 标准图生视频 |
| `G02` 首尾帧 | 两张图驱动过渡 |
| `G03` / `G10` SmoothMix V1/V2 | 面板快捷生成主力 |
| `G07` LightX2V | 高动态加速 |
| `G09` StoryMem | 多分镜无限长视频 |
| `G11`/`G12`/`G14` SVI / Remix | 长视频 / 全自动反推 |
| `G20`–`G25` 大丝袜 / Ditto 等 | 特定风格与动态 |

**快捷生成（视频 A–E）**：`image-to-video`、`wan22-smoothmix-v2`、`image-to-video-wan22tssp`、`image-to-video-wan22swz`、`wan22-lightx2v-i2v`。

### 4.2 LTX2.3 — `H视频-LTX/` + `H黑鹤001Ltx终章/`

| 推荐 | 说明 |
|------|------|
| `H15`/`H16` 文图二合一 | GGUF / 标准版入门 |
| `H17` 全面优化；`H18`/`H19` 图生/文生 | 日常 LTX |
| `H20` 音画同步；`H28` 高动态 I2V | 带音频 / 强动态 |
| `H14`/`H31`/`H32`/`H34`/`H35` 导演台 | 单采/双采/低显存/群主版 |
| `H37` 全栈短剧 V18.7 / V19.3；`H42` 4 宫格硬切 | 短剧流水线 |
| `H38`/`H39` 宫格导演台 / Director 电商分镜 | 宫格与带货控制 |
| `H40` 动漫数字人；`H41` MSR 多参考 | 动漫口播 / 多参大片 |
| 黑鹤终章 `▶▶LTX23-*` | 全能编辑、动作迁移、去字幕水印 |

**快捷生成**：`h41-ltx23-msr`（LTX2.3 多参直出）。  
**根目录补充**：`JoyAI-Echo 多镜头连贯视频与音频生成.json`。

---

## 5. 能力地图：影视 / 短剧 / 导演台

| 目标 | 去哪 | 代表流 |
|------|------|--------|
| 短剧全流程（LTX） | `H视频-LTX/` | `H37` V19.3 易用版；`H42` 硬切短剧 |
| 短剧角色/场景图 | `C图像-Zimage/` + `H` | `C16`；`H37-Z-Image短剧拍档…` |
| 导演台分镜 | `H视频-LTX/` | `H14` 导演台 2.0；`H31`/`H32`；`H38`/`H39` |
| 影视二创 | `K视频-人物替换/` | `K03` Wan 二创；`K04`/`K05` WorkFisher |
| 多参考成片 | `H视频-LTX/` | `H41` MSR |

**改短剧流时**：优先复制一份新 JSON 再改，避免覆盖用户已调好的 `H37`/`H42`；模型软链新增只写 `models/**/Ltx`（大写），并同步 `/root/zealman-app/modellink/user_models.json`。

---

## 6. 能力地图：动作迁移 / 人物替换 / 数字人

### 6.1 动作迁移 — `P视频-动作迁移/`

| 推荐 | 说明 |
|------|------|
| `P02` / `P07` Wan Animate V1/V4 | 快捷生成已接；通用动作迁移 |
| `P04`/`P05` SCAIL；`P06` SteadyDancer | 全场景 / 不限时长骨骼 |
| `P22` 爱屋 Scail2；`P23` 豹豹喵呜 SCAIL-V2 | Scail2 二合一 |
| `P24`/`P25` 肥猴 Scail-2 高阶 Plus v4 | 人物替换 / 动作迁移分拆 |
| `P26` 肥猴分段队列；`P27` Scail2 循环长视频 | 长视频分段 / 循环拼接 |
| `P11` 超级王炸分段队列 | 换装+长视频拼接 |
| `P14` LTX 动作模仿 | 图片跳舞类 |

**快捷生成**：`image-to-video-wan22rwqy`（Animate V1）、`wan22-animate-dzqy-v2`（Animate V4）。

### 6.2 人物替换 — `K视频-人物替换/`

| 推荐 | 说明 |
|------|------|
| `K01`/`K02` 换装 | 娱乐换头换装 |
| `K06`/`K07` Wan Animate 替换 | 姿态对齐最强流 |
| `K08`/`K09` Bernini | 多图参考 / 视频换人 |
| `K10`/`K11`/`K13` SCAIL2 | 角色替换、长视频、全自动循环 |

### 6.3 对口型数字人 — `J视频-对口型数字人/`

| 推荐 | 说明 |
|------|------|
| `J03`–`J06` InfiniteTalk | 单人/双人、图/视频驱动 |
| `J08`/`J09` LTX 对口型 KJ 优化 | 说话唱歌、双人对话 |
| `J11` 电商数字人；`J12` 电商人物替换 | 带货口播 |
| `J13` 小珠光 90 秒全自动 | InfiniteTalk 长口播 |
| `J14` Bernini 电商换产品 | 产品替换视频编辑 |

**快捷生成**：`j08-ltx-lip-sync`、`j11-ltx23-commercial-avatar`、`j13-infinitetalk`。

---

## 7. 能力地图：音频

目录：`N声音生成-音乐生成-声音克隆/`

| 工作流 | 用途 |
|--------|------|
| `N1`/`N2`/`N3` FishAudio S2pro | 多/单/双人声音克隆 |
| `N6-Qwen3TTS音频克隆` / `音频创造` | TTS 音色工坊 |
| `N5` ACE-Step | 音乐 & 歌曲 |
| `N4` mmaudio；`N7` stable-audio | 音效 / 音频生成 |

**快捷生成**：`j-single-voice-clone`（FishAudio）、`n6-qwen3tts-voice-clone`（Qwen3TTS）。

---

## 8. 能力地图：放大 / 去水印 / 工具

| 目录 | 推荐 | 用途 |
|------|------|------|
| `M高清放大去水印/` | `M01` SUPIR；`M02` SeedVR2+TTP；`M05`/`M10` 视频修复放大；`M06`/`M08`/`M09` 去水印字幕；`M11` 亿级超分；`M13` Klein 批量去水印 | 后处理 |
| `H黑鹤001Ltx终章/` | `▶▶LTX23-视频去字幕水印流` | LTX 向去字幕 |
| `Z工具设置/` | `Z01` ZealmanAPI 示例；`Z06` API 清缓存；`Z08`/`Z09` 补帧 | API 联调与工具 |
| 根目录 | `通用反推.json` | 提示词反推 |
| `OLD/` | 旧 LTX2.0 / Flux / BindWeave / MoCha | 仅历史兼容，新功能勿依赖 |

**快捷生成**：`m02-seedvr2-upscale`。

---

## 9. 快捷生成（面板）

### 9.1 配置约定（重要）

| 文件 | 规则 |
|------|------|
| `/root/zealman-app/quick-generate-home.yaml` | **外部维护 / 只读**，禁止直接改 |
| `/root/zealman-app/quick-generate-home8.yaml` | **需要改首页卡片时改这个**；主 yaml 失效时兜底 |

卡片字段：`id` / `pageId` / `name` / `desc` / `img` / `badge`。  
前端展示条件：`yaml.pageId` ∩ `config.json.pages[pageId]=true`。

启用已有页：

```bash
jq '.pages["h41-ltx23-msr"] = true' /root/zealman-app/config.json > /tmp/cfg.json && mv /tmp/cfg.json /root/zealman-app/config.json
curl -X POST http://localhost:6008/api/hot-restart
```

### 9.2 当前正式快捷页一览

| badge | pageId | 名称 |
|-------|--------|------|
| A | `image-to-video` | SmoothMix-V1 图生视频 |
| B | `wan22-smoothmix-v2` | SmoothMix-V2 |
| C | `image-to-video-wan22tssp` | Wan2.2 双噪图生视频 |
| D | `image-to-video-wan22swz` | 首尾帧转视频 |
| E | `wan22-lightx2v-i2v` | LightX2V 图生视频 |
| F | `image-to-video-wan22rwqy` | Animate 动作迁移 V1 |
| G | `wan22-animate-dzqy-v2` | Animate 动作迁移 V4 |
| H | `d14-flux-klein-storyboard` | Flux 克莱因 9B 分镜 |
| I | `b13-qwen-multi-character-angles` | QwenEdit 角色多角度 |
| J | `j-single-voice-clone` | FishAudio 单人克隆 |
| K | `d20-raw-restore` | RAW 画质重建 |
| L | `j08-ltx-lip-sync` | LTX 数字人对口型 |
| M | `j11-ltx23-commercial-avatar` | LTX 电商数字人 |
| N | `n6-qwen3tts-voice-clone` | Qwen3TTS 音色工坊 |
| O | `m02-seedvr2-upscale` | SeedVR2+TTP 放大 |
| P | `p18-klein9b-drama-multi-edit` | Klein9B 多图编辑 |
| Q | `c18-baiyu-aio-portrait` | 白玉 AIO 写真 |
| R | `t4-krea2-character-sheet` | Krea2 角色三视图 |
| S | `j13-infinitetalk` | InfiniteTalk 单人数字人 |
| T | `h41-ltx23-msr` | LTX2.3 多参直出 |

### 9.3 基于现有快捷页做功能（推荐）

用户侧 / Codex 优先：

1. 在 ComfyUI 打开对应底层工作流，复制改名后调试
2. 需要 HTTP 调用 → 面板「API 生成」映射参数，保存到 `/root/zealman-app/workflows/`
3. 需要面板开关 → 只改 `config.json` 的 `pages` + 必要时改 `quick-generate-home8.yaml` 文案
4. 用 `POST /api/hot-restart` 或 `bash start-services.sh` 让配置生效

快捷页运行链路：`/root/zealman-app/public/*.json` → `POST /api/comfy/proxy/prompt` → `ws://…/comfyui-ws?clientId=`。

> 新增整页 React 快捷 UI 属于面板源码能力，镜像用户环境通常不可见；请改工作流 + API / 现有快捷页，而不是假设能改前端源码。

---

## 10. API 与并发生成

### 10.1 文档入口

| 入口 | 说明 |
|------|------|
| 面板「接口说明」 | pageId `api-docs`，可复制 curl / fetch |
| 面板「API 生成」 | pageId `workflow-to-api`，工作流转 HTTP |

### 10.2 两层「API」含义

1. **ComfyUI 节点示例**：`Z01-工具-ZealmanAPI示例.json`（插件节点演示）
2. **面板 WorkflowToAPI**：任意可跑通流封装为 HTTP；配置在 JSON `_api_config`；文件在 `/root/zealman-app/workflows/`

### 10.3 标准调用时序

```
1. POST /api/comfy/upload/image          # 文件参数
2. 建立 WS: /comfyui-ws?clientId=<uuid>  # 先连再提交
3. POST /api/workflow/generate           # 或 POST /api/comfy/proxy/prompt
4. 听 progress/executed，或 GET /api/comfy/proxy/history?prompt_id=
5. GET /output/{subfolder}/{filename}    # type=output 优先
```

参数键格式：`nodeId:field`（如 `"6:text"`、`"13:image"`）。

常用端点：

```bash
GET  /api/health
GET  /api/comfy/status
POST /api/comfy/start | /api/comfy/stop
POST /api/comfy/proxy/prompt
GET  /api/workflow/list
GET  /api/workflow/config/:id
POST /api/workflow/save
POST /api/workflow/generate
POST /api/workflows/initialize-comfyui   # workflows/ → ComfyUI 目录
GET  /api/images
POST /api/images/zip
```

### 10.4 并发生成

- 面板：`concurrent-generate`
- 典型：`POST /api/concurrent/generate`、`POST /api/concurrent/run-batch-async`、`GET /api/concurrent/run-batch-status`、`GET /api/concurrent/assets`
- 输入资产目录：`/root/并发/`

---

## 11. 修改工作流：场景与禁区

### 11.1 按场景改哪里（仅用户可见路径）

| 场景 | 改哪里 | 说明 |
|------|--------|------|
| ComfyUI 内调试 / 改功能 | `/root/ComfyUI/user/default/workflows/<分类>/` | **优先复制新文件名**，保留原流 |
| 封装 HTTP API | 面板「API 生成」→ `/root/zealman-app/workflows/` | 须 API 格式 JSON |
| 快捷生成开关 / 文案 | `config.json`、`quick-generate-home8.yaml` | 勿改 `quick-generate-home.yaml` |
| 快捷页模板 JSON | `/root/zealman-app/public/*.json` | 与快捷页加载的 API 工作流对应 |
| 模型软链登记 | `/root/zealman-app/modellink/user_models.json` | 配合 `update-symlinks-*.sh`；新 LTX 只进 `Ltx` 目录 |

### 11.2 禁止 / 只读

- 禁止改：`/root/zealman-app/quick-generate-home.yaml`（改 `quick-generate-home8.yaml`）
- 禁止改符号链接本体：`start-comfyui.sh`、`update-symlinks.sh`（若需调整，改对应 `start-comfyui-*.sh` / `update-symlinks-*.sh`）
- 禁止改 PyTorch / CUDA 版本
- 禁止在 ComfyUI 根目录执行 `git checkout FETCH_HEAD`
- 不要写入或依赖用户不可见的开发目录内容

### 11.3 验证与重启

```bash
curl -s http://localhost:6008/api/health
curl -s http://localhost:6008/api/comfy/status
curl -X POST http://localhost:6008/api/hot-restart
# 或
cd /root/zealman-app && bash start-services.sh
```

---

## 12. Codex 任务模板（可直接套用）

### 模板 A：基于现有流改功能

```
1. 在 §2–§8 定位分类与代表 JSON
2. 复制为新文件名（保留原流），在 ComfyUI 打开调试
3. 改节点/模型名时核对 modellink 与 models/ 实际文件
4. 需要 HTTP → 面板「API 生成」；需要开关 → config.json / home8.yaml
5. 验证：curl health/status + 跑通一条最小输入
```

### 模板 B：工作流转 API 供外部调用

```
ComfyUI 跑通 → 面板「API 生成」映射 nodeId:field
→ 保存到 /root/zealman-app/workflows/
→ 按 §10.3 用 upload + WS + /api/workflow/generate 联调
→ 批量则改用 concurrent 端点
```

### 模板 C：短剧 / 影视流水线

```
角色/场景图：C16 / T4 / C19 / D14
分镜：B16 / Q1 / H39
成片：H37 / H41 / H42 或 G09 长视频
配音：N2 / N6
对口型：J08 / J11 / J13
后处理：M02 / M09
```

### 模板 D：启用已有快捷页

```
确认 pageId 在 §9.2
→ config.json.pages[pageId]=true
→ 必要时更新 quick-generate-home8.yaml 文案
→ hot-restart / start-services.sh
→ 面板「快捷生成」点进页跑通
```

---

## 13. 面板主导航（非快捷子页）

| pageId | 名称 |
|--------|------|
| `system-management` | 启动 / 管理 ComfyUI（默认页） |
| `quick-generate` | 快捷生成入口 |
| `output-management` | 我的资产 |
| `system-settings` | 上传模型等 |
| `resource-migration` | 资源迁移 |
| `workflow-to-api` | API 生成 |
| `concurrent-generate` | 并发生成 |
| `api-docs` | 接口说明 |
| `wuli-canvas` | 画布系统 |
| `version-management` | ComfyUI 版本升降 |
| `about` | 关于 |

---

## 14. 版本与规模快照

- 镜像：**v8.88** | ComfyUI 默认：**0.27.0**（可升降）
- 预制工作流：活跃约 **235** 套（含 OLD 约 **267** 套）
- 完整文件名清单：见 [`zealman镜像说明.md`](./zealman镜像说明.md)「当前完整工作流目录清单」

---

**给 Codex 的原则**：先复用镜像内已有工作流与快捷页，再最小改动；只操作 `/root/zealman-app`、`/root/ComfyUI` 等用户可见路径；「只读符号链接 / 外部 yaml」不要硬改本体。

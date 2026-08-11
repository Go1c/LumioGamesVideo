# Zealman Workflow Capability Map

Use this map only to narrow the search. Treat the selected JSON, its category guide, and the live
instance as authoritative.

| Need | Prefix or directory | Useful starting points |
|---|---|---|
| Qwen text-to-image and general generation | `A图像-Qwen生成` | `A01`, `A03`, `A10` |
| Qwen edit, multi-angle, face, storyboard grid | `B图像-Qwen编辑` | `B01`, `B13`, `B16` |
| Z-Image portrait, short-drama, character sheet | `C图像-Zimage` | `C01`, `C16`, `C18`, `C19` |
| Flux/Klein storyboard and multi-image edit | `D图像-Flux` | `D14`, `D18`, `D20` |
| SDXL or anime image generation | `E图像-SDXL-IL` | `E01`, `E02`, `E03` |
| Lightweight image editing or background change | `F图像-FireRed图像编辑` | `F01`, `F02` |
| Wan image-to-video and first/last frame | `G视频-Wan图生` | `G01`, `G02`, `G03`, `G10` |
| Wan long video or strong motion | `G视频-Wan图生` | `G07`, `G09`, `G11`, `G14` |
| LTX text/image-to-video | `H视频-LTX` | `H16`, `H17`, `H18`, `H19` |
| LTX audio-sync, director, multi-reference | `H视频-LTX` | `H20`, `H31`, `H34`, `H41` |
| LTX video editing | `H黑鹤001Ltx终章` | inspect all five purpose-named flows |
| Lip-sync or digital presenter | `J视频-对口型数字人` | `J03`, `J08`, `J11`, `J13` |
| Character or background replacement | `K视频-人物替换` | `K04`, `K07`, `K11` |
| Viewpoint change / Gaussian splatting | `L视角-高斯泼渐` | inspect both flows |
| Upscale, repair, interpolation | `M高清放大去水印` | `M02`, `M05`, `M10`, `M13` |
| Authorized watermark/subtitle removal | `M高清放大去水印` | `M06`, `M08`, `M09` |
| Voice clone, TTS, music, sound | `N声音生成-音乐生成-声音克隆` | `N02`, `N05`, `N06`, `N07` |
| Motion transfer and dance | `P视频-动作迁移` | `P02`, `P07`, `P14`, `P25`, `P27` |
| Storyboard image design | `Q分镜图gptimage-banana2类` | `Q1` |
| Ideogram image or storyboard grids | `R图像-Ideogram` | `R01`, `R04`, `R05` |
| Boogu generation/editing | `S图像-Boogu` | `S01`, `S02` |
| Krea photorealism and character sheet | `T-图像-Krea` | `T01`, `T02`, `T04` |
| MiniMax H3 text/image/reference video | `U视频-MINIMAX-H3` | `U01`, `U03`, `U07`, `U12` |
| General image-production entry points | `Y通用制作` | search by required model and operation |
| Inspection, API, frame, cache tools | `Z工具设置` | `Z01`, `Z05`, `Z06`, `Z09` |

Selection rules:

1. Prefer a matching `V9面板API-json` file when the user needs an existing HTTP surface.
2. Prefer the UI graph when the workflow must be debugged, visually adapted, or converted to a new
   API mapping.
3. Prefer a basic flow for the first smoke test; escalate to director, multi-reference, long-video,
   batch, or ultra-resolution variants only for a stated requirement.
4. Compare at least one nearby alternative and inspect model/custom-node dependencies before staging.
5. Treat voice cloning, face/character replacement, and watermark removal as rights-gated tasks.

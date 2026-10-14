# 框架与基座调研：像素空间扩散 → 约五秒短视频

核查日期：2026-10-15（Asia/Shanghai）。面向 2026-10-16 首次组会；以下是选型建议和公开资料核查，尚无本地安装、推理、训练或复现结果。仓库 `main/master` 和模型卡会更新，真正开展实验前应记录 commit、权重校验值和环境。结构化对照见 [baseline-comparison.csv](baseline-comparison.csv)。

## 1. 当前可作的决定

建议保留本工作区的最小研究目录，用 **JiT-B/16 作为像素方法学习与小规模改造的候选起点**，用 **Wan2.1-T2V-1.3B 作为约五秒潜空间视频参照**。这不是最终训练选型：GPU、任务条件和数据尚未确认。PixelGen 适合作为感知损失方案；PixelREPA、PixelDiT2 适合作为外部表征方案。它们的图像成绩不能证明迁移视频有效。

Kandinsky 6 Lite 已有真实公开的 3B 权重和五秒推理接口，但它带音频、多个编码器与 VAE；“Lite”是相对其 29B Pro 版本的命名，不能解释为比 Wan 1.3B 更轻。当前问题不需要音频，暂列第二视频参照。[官方模型卡](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-5s-Diffusers)

## 2. 研究工作流模板与模型代码是两种东西

| 方案 | 官方提供什么 | 对本项目的适用性与代价 | 当前建议 |
|---|---|---|---|
| Cookiecutter Data Science v2 | 数据、代码、模型、报告、notebook 等标准目录；可选环境、测试与文档工具。v2 使用 `ccds`，要求 Python 3.10+ | 适合整理数据和研究产物；不实现 diffusion、视频训练或实验科学设计 | 借鉴 raw/processed、代码/产物分离即可；暂不安装生成器。见[官方文档](https://cookiecutter-data-science.drivendata.org/) |
| Lightning-Hydra Template | Lightning 训练组织、Hydra 配置组合、日志、实验配置、测试和多设备入口 | 适合已有可用数据的模型原型；官方明确提示是社区模板，集成可能出错，复杂数据流水线需另做，Hydra multirun 恢复有限 | 等选择的上游本来采用 Lightning、且需要配置扫描时再引入；不要先移植 JiT 训练循环。见[官方仓库](https://github.com/ashleve/lightning-hydra-template) |
| 最小自定义工作区（现有目录） | 文献、假设、实验记录、代码、结果、组会和论文相互关联 | 入门负担最低；需要自己保持实验记录完整性 | 当前首选；保留上游入口和环境，通过薄脚本调用。此行是本项目建议，不是第三方产品 |

目录的作用是找到证据，不是增加层数。当前文献进入 `literature/`，假设进入 `research/`，实验配置与记录进入 `experiments/`，未经改动的上游代码进入 `external/`，自己的修改进入 `code/`，样例与指标进入 `outputs/`。每个 run 保存同一套字段：实验 ID、假设、代码 commit/patch、权重 hash、数据 split/version、完整配置与命令、seed、GPU/显存、时间、失败情况和评估协议。暂不创建假的依赖锁文件，也不把上游多个互相冲突的依赖装进同一个环境。

## 3. 图像像素方法：发布状态与迁移门槛

这里“像素空间”指扩散状态/生成目标在原始图像像素中；内部使用 patch embeddings、Transformer 特征或外部冻结编码器，并不自动把生成状态变成 VAE latent。但“无 VAE”也不等于“没有预训练模型依赖”。

| 方法 | 本次核查的公开实现/权重/训练 | 机制与规模证据 | 对视频起点的判断 |
|---|---|---|---|
| JiT | 作者 PyTorch/GPU 重实现；`main_jit.py`、`engine_jit.py`、`model_jit.py`；README 有训练、评估和 Dropbox 权重链接 | 直接预测 clean image（x-pred）；不要求 tokenizer、感知损失或表征对齐。论文 v1 Table 5：B/16 256² 131M，B/32 512² 133M；README 示例训练经过 8×H200 测试 | 结构最简，优先读 B；131M 是论文报告值，不是本地重新计数。视频 temporal blocks、位置编码和数据管线仍需研究。[仓库](https://github.com/LTH14/JiT)、[论文 v1 Table 5](https://arxiv.org/html/2511.13720v1#S5) |
| PixelDiT | NVlabs 仓库含 C2I/T2I 训练推理、配置及自动下载权重入口；C2I 256²/512² XL checkpoint 已列出 | patch-level DiT + pixel-level PiT，承担语义与细节；C2I 默认示例 8 GPU；不同于 JiT 的更复杂双层路径 | 可研究局部细节/计算分配，但先改成视频的工程量更大。[仓库](https://github.com/NVlabs/PixelDiT)、[C2I 指南](https://github.com/NVlabs/PixelDiT/blob/master/c2i/README.md) |
| PixelDiT2 | 同一 NVlabs 仓库已发布实现与 H/16 256²/512² 权重；不是仅有论文 | 单 patch DiT + 冻结 DINOv3 grounding；训练还用 DINOv2 REPA。C2I 指南列 H/16 256² total 1007.8M；训练示例 4 nodes×8 GPU（512²为8×8） | 外部语义 grounding 值得读，但 released H 权重不是小规模首选；B配置表不等于已发布 B checkpoint。[C2I 指南 Models/Training/Model details](https://github.com/NVlabs/PixelDiT/blob/master/c2i/README.md) |
| PixelREPA | KAIST 官方代码；`main_pixelREPA.py`；B/L/H 推理、训练例子及 Google Drive checkpoint 链接 | 用 Masked Transformer Adapter 对齐 JiT 中间特征与外部语义编码器；README 报告 8×H200 训练 | 作为 JiT + 表征对齐消融；需考虑视频表征是否要时序 encoder。[官方仓库](https://github.com/kaist-cvml/PixelREPA) |
| PixelGen | 作者仓库有 C2I/T2I 的 `fit`/`predict`、配置、HF 权重；XL/16 676M（C2I），XXL/16 1.1B（T2I） | LPIPS 局部感知 + DINO 语义感知损失；没有视频实现证据 | 适合作为损失机制研究；released XL 比 JiT-B 大。训练门槛不能由“较少 epochs”推断。[官方仓库 Checkpoints/Usages](https://github.com/Zehong-Ma/PixelGen) |

许可核查：JiT 与 PixelREPA 仓库标 MIT；**PixelDiT/PixelDiT2 根许可 NSCLv1 限研究/评估用途**，不是 Apache/MIT；子目录第三方代码与运行时 encoder 另有许可，尤其 DINOv3。PixelGen 当前可见根目录没有 LICENSE，不能把公开代码视为已有明确再分发许可；开展派生发布前向作者确认。此处仅记录许可文本状态。[NVlabs LICENSE](https://github.com/NVlabs/PixelDiT/blob/master/LICENSE)、[NOTICE](https://github.com/NVlabs/PixelDiT/blob/master/NOTICE)

所有“权重可用”均指官方链接/文件清单可见，本次没有下载并验证加载。JiT 原论文 JAX/TPU 与作者 PyTorch/GPU 重实现也应分开记录，不能默认数值完全一致。

## 4. 可用视频参照：潜空间，不是纯像素视频基线

| 候选 | 官方证据 | 约五秒配置与任务 | 资源证据及局限 |
|---|---|---|---|
| Wan2.1-T2V-1.3B | 官方代码和 HF 权重；Apache-2.0；Wan-VAE 压缩后建模。`wan/configs/wan_t2v_1_3B.py` 为 30层、1536 dim、12 heads | 原生 1.3B 为 T2V；不是自动具有14B I2V/首尾帧能力。`generate.py`默认81帧，`shared_config.py`为16fps，约5s；推荐832×480、50步 | README 报告8.19GB推理显存、4090约4min/5s480p；官方4090命令用模型 offload 与 T5 CPU。训练/微调显存未核实；1.3B不包含全部pipeline资源。[README](https://github.com/Wan-Video/Wan2.1)、[权重卡](https://huggingface.co/Wan-AI/Wan2.1-T2V-1.3B) |
| Kandinsky-6.0-Lite-5s-Diffusers | 官方3B checkpoint；模型卡 MIT；组件表明确 `AutoencoderKLHunyuanVideo`、Qwen2.5-VL、CLIP、音频VAE与vocoder | T2AV/TI2AV；示例480×864、121帧、24fps、50步；`sample_audio=False`可只生成视频。参考图像约束首帧 | 模型卡未给最低推理或训练显存；HF文件树27.8GB是磁盘文件量，不是VRAM。官方原生实现有4090 Lite SD 437s（warmup后、block offload、特定attention，排除加载和编码），不能直接套到Diffusers路径。[模型卡](https://huggingface.co/kandinskylab/Kandinsky-6.0-Lite-5s-Diffusers)、[原生README Performance](https://github.com/kandinskylab/kandinsky-6) |
| LTXV-2B-0.9.8-distilled（补充） | 官方LTX-Video仓库与HF列出2B蒸馏权重/配置；潜空间pipeline；不是把当前LTX-2当作2B | 版本0.9.8是2025年的较小候选；官方建议空间32倍数、时间8n+1。121帧/24fps是可测试的约5s配置提案，未运行 | 精确VRAM与该2B版本微调预算未核实；代码Apache-2.0，权重用版本专用 Open Weights License，不能混写。多尺度配置另外加载upscaler，可能增加成本。[模型卡](https://huggingface.co/Lightricks/LTX-Video)、[2B配置](https://github.com/Lightricks/LTX-Video/blob/main/configs/ltxv-2b-0.9.8-distilled.yaml)、[权重许可](https://huggingface.co/Lightricks/LTX-Video/blob/main/LTX-Video-Open-Weights-License-0.X.txt) |

证据定位：[Wan `generate.py`](https://github.com/Wan-Video/Wan2.1/blob/main/generate.py) 搜索 `frame_num` / `81`；[shared_config.py](https://github.com/Wan-Video/Wan2.1/blob/main/wan/configs/shared_config.py) 搜索 `sample_fps`；[1.3B配置](https://github.com/Wan-Video/Wan2.1/blob/main/wan/configs/wan_t2v_1_3B.py) 搜索 `vae_stride`、`window_size`。Wan VAE stride=(4,8,8)，patch=(1,2,2)：这直接显示其输入并非RGB pixel diffusion。

Wan 的 self-attention 默认全局 window_size=(-1,-1)，forward 调用的 `flash_attention` 默认 `causal=False`，可作为“联合去噪能利用未来 noisy tokens”的代码依据；这不等于首尾帧条件生成或显式前后向两分支。VAE 的 causal 设计与 denoiser 的 attention 也不能混为一谈。[模型代码 WanSelfAttention.forward](https://github.com/Wan-Video/Wan2.1/blob/main/wan/modules/model.py)、[attention.py 函数签名](https://github.com/Wan-Video/Wan2.1/blob/main/wan/modules/attention.py)。Kandinsky 和 LTX 的时序双向性本次未逐层核实，不据名称作结论。

本轮列出的五个像素方法都是图像模型；三个视频参照均为潜空间。**本轮没有确认一个同时满足“纯像素、公开轻量权重、约五秒、可训练”的现成视频基座。**这只表述本轮核查范围，不是证明全领域不存在。

## 5. 未知GPU预算下的分阶段建议（待组会决定）

1. **先定问题与协议**：明确双向是非因果时序attention、首尾帧插值，还是forward/backward一致性；定T2V/I2V/无条件视频、数据可用性和目标FPS。普通非因果diffusion已经可看整个noisy clip，不能单凭“双向”宣称新颖。
2. **像素图像最小复现**：若组会同意 JiT-B，先单batch inference/短训练sanity check、small subset overfit，再复现与研究问题相关的图像对照。小subset结果仅验证管线，不代表ImageNet质量。需要外部感知损失时再引入PixelGen机制，并保持backbone/训练预算一致。
3. **视频可行性测量**：先以低分辨率、8–16帧的RGB联合去噪原型测资源和时序错误；这一设置是提案，不能用其结果代表五秒自然视频。一次forward/backward实际测量GPU峰值、step time、数据吞吐，再决定是否扩到5s；不要直接按“权重字节数”估训练显存。
4. **独立跑潜空间参照**：获准运行后用Wan1.3B固定prompt、seed、50步、480p建立视频评估/失败样例管线；仅当训练预算与问题匹配再讨论LoRA或改结构。Kandinsky6只在需要其I2V/音视频能力或有足够资源时加入。
5. **一个受控改动**：同任务、同split、同帧数/FPS/分辨率、同参数或计算预算下比较pixel方案与相关对照，分开报告生成质量、时序一致性、成本。预先固定评估器与样本数量，保留失败样例。外部预训练视频模型是参考上限/工程参照，不天然构成公平的纯像素方法对照。

若只有小显存卡，当前可先做代码阅读、已有图像checkpoint少量推理和数据协议准备；若能取得单24–48GB GPU，再实际测短低分辨率训练；若多卡资源获批，再讨论长片段/高分辨率。以上是工作安排推断，不是任何模型的已验证最低显存或可达到质量。

不要把各论文的FID直接排成赢家表：PixelDiT与PixelDiT2的评估backend/reference stats不同；不同模型还存在CFG、采样步数、训练轮次、模型尺寸和外部encoder等差异。图像FID不验证视频质量，短视频应加入明确的视频评估协议与同prompt人工盲评；评估方法最终由任务与数据决定。

## 6. 组会上必须确认的问题

- 双向的精确定义与预期失效现象是什么？导师已有方法/草图/必须比较的论文吗？
- 要证明pixel-space建模本身的价值，还是解决首尾帧/时间一致性？是否允许外部感知encoder，是否允许latent模型作教师或条件？
- 可用GPU型号、数量、单卡显存、总GPU小时、存储和运行环境是多少？能否先做很小的可行性实验？
- 数据能否合法获取，选何种视频域、caption与frame-rate？训练/验证/测试如何按原始视频隔离？
- 约五秒是硬性最终指标还是先研究低分辨率短片段？首轮成功标准是资源可行、短训练收敛，还是样例质量？
- 下周只批准哪个候选基座和哪一个sanity check？会议后记录真实决定，避免把此建议当成已批准计划。

## 7. 核查边界

本次以作者仓库、论文HTML和官方HF卡为来源，核查README、代码片段、配置与文件树；没有安装、clone、下载权重/数据、训练、跑推理或验证链接后的权重完整性。未核实的最低显存、精确训练成本、Windows兼容性、PixelGen许可及额外encoder许可在CSV中保留为空或写明状态。来源的可见状态是2026-10-15的快照；正式复现应固定源码commit，并对新checkpoint重新核查。

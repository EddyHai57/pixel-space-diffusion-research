# Pixel-space Diffusion Models 研究工作区

目标：从文献理解、基线复现、可证伪假设与受控实验，推进到论文写作。当前关注像素空间扩散与约五秒短视频；研究问题和实验基座尚未确定。

## 从这里开始

1. [首次组会材料](meetings/2026-10-16/brief.md)：当前认识、需要讨论的问题和建议下周任务。
2. [PixelGen 阅读笔记](literature/notes/2602.02493-pixelgen.md)：先理解整体流程，再读公式与证据。
3. [框架与基座调研](research/framework-survey.md)：区分研究管理框架、图像方法和视频基线。
4. [论文索引](literature/index.csv)与[备份说明](literature/archive-readme.md)：查找版本、原文与官方实现。
5. [研究问题](research/problem.md)与[执行计划](research/work-plan.md)：把导师讨论转成可验证任务。

创建日期：2026-10-15（Asia/Shanghai）。这一版为研究起点，不代表已完成复现、模型选型或视频方法验证。

公开仓库保存研究记录和来源索引。原文 PDF、私人聊天截图、临时渲染、数据集和权重留在本地；克隆仓库后，可按 `literature/archive-manifest.json` 的固定版本 `pdf_url` 下载到对应 `local_pdf` 路径。未恢复 PDF 时，归档核验会明确报告缺失。

## 如何持续更新

| 新内容 | 放在哪里 | 必须保留什么 |
|---|---|---|
| 新论文 | `literature/pdfs/`、`literature/index.csv`、`literature/bibliography.bib` | arXiv ID、版本、来源、下载日期与校验值 |
| 阅读笔记 | `literature/notes/` | 问题、方法、证据位置、限制与个人疑问 |
| 研究假设 | `research/ideas.md` | 可证伪预测、对照组、否定条件 |
| 组会 | `meetings/YYYY-MM-DD/` | 会前认识与会后实际决定分开记录 |
| 实验 | `experiments/records/`、`experiments/registry.csv` | 配置、代码版本、数据版本、命令、种子、日志与指标 |
| 自己的代码 | `code/` | 实验编号、运行环境与修改理由 |
| 上游代码 | `external/` | 官方链接、commit、许可和本地修改 |
| 数据与权重 | `data/README.md` | 实际存储位置、获取方式、使用限制与版本 |
| 生成结果 | `outputs/` | 实验编号，成功与失败样例均保留 |
| 论文 | `paper/` | 每个主要论断关联原文或实验记录 |

小型文本记录在本目录维护。大数据和权重可留在服务器，本地仅保留可追踪清单。环境未选定前不生成假的依赖锁文件；基线确定后保存实际可复现环境。

## 核验方法

只读核验脚本 `scripts/verify-workspace.py` 检查 PDF 校验值、页数、CSV/manifest 一致性和 Markdown 本地文件链接。需 Python 与 `pypdf`；恢复本地原文后，在仓库根目录运行：

```powershell
python scripts/verify-workspace.py
```

核查结果见 [verification.md](research/verification.md)。没有训练结果；会议记录模板也不代表导师已作决定。

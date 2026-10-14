# 论文原文归档

截至 **2026-10-15（Asia/Shanghai）**，本目录已实际保存下列五篇论文的 arXiv 固定版本 PDF。版本、标题、作者、首次提交日期及修订日期均核对过 arXiv 官方摘要页；下载使用带版本号的官方 PDF 链接。

| 简称 | 固定版本 | 版本日期（UTC） | 页数 | 本地文件 |
|---|---|---|---:|---|
| JiT | 2511.13720v2 | 2026-01-07 | 18 | [JiT_2511.13720v2.pdf](https://arxiv.org/pdf/2511.13720v2) |
| PixelDiT | 2511.20645v2 | 2026-04-16 | 25 | [PixelDiT_2511.20645v2.pdf](https://arxiv.org/pdf/2511.20645v2) |
| PixelDiT2 | 2609.24919v2 | 2026-09-30 | 18 | [PixelDiT2_2609.24919v2.pdf](https://arxiv.org/pdf/2609.24919v2) |
| PixelREPA | 2603.14366v1 | 2026-03-15 | 24 | [PixelREPA_2603.14366v1.pdf](https://arxiv.org/pdf/2603.14366v1) |
| PixelGen | 2602.02493v2 | 2026-05-07 | 25 | [PixelGen_2602.02493v2.pdf](https://arxiv.org/pdf/2602.02493v2) |

`PixelREPA` 是方法简称，正式标题为 *Representation Alignment for Just Image Transformers is not Easier than You Think*；`JiT` 的正式标题为 *Back to Basics: Let Denoising Generative Models Denoise*。BibTeX 保留正式标题及官方作者顺序。

## 可追溯记录

公开仓库不包含 PDF 文件；上表链接指向对应 arXiv 固定版本原文，文件名是本地保存名称。克隆后按 manifest 的 `pdf_url` 下载到 `local_pdf`，再对照校验值。私人研究聊天截图也只保存在本地。

- [index.csv](index.csv)：UTF-8 BOM，可用 Excel 打开；一行对应一篇固定版本，包括来源、版本日期、本地路径、下载时间、校验状态、字节数、SHA256、页数、官方代码链接、阅读状态和笔记路径。`indexed` 仅表示建立索引，不表示完成精读；未确定的笔记路径留空。
- [archive-manifest.json](archive-manifest.json)：机器可读清单；`version_timestamp_utc` 是 arXiv 版本时间，`retrieved_at` 是本次实际下载的北京时间，二者含义不同。
- [bibliography.bib](bibliography.bib)：正式作者、标题、arXiv ID、固定版本链接与归档说明。`year` 使用首次提交年份，版本日期另外记录；没有把预印本自动改写为会议发表条目。

全部 PDF 已验证 `%PDF-` 文件头、非零且合理的文件大小、SHA256，并通过 `pypdf` 解析页树和提取第一页文字。该校验说明文件可解析，不代表逐页排版审查、方法复现或论文结果独立验证。SHA256 是本地文件完整性指纹，arXiv 未提供本次下载的对照哈希，不能当作独立的服务器签名验证。

原文保持下载所得字节，不做压缩、重排或内容修改。仅备份论文 PDF，没有下载模型权重、训练数据或源码压缩包。这是本机工作区副本，不是异地灾备。

## 复核与重取

在工作区根目录运行：

```powershell
# 只读计算当前文件哈希，与 archive-manifest.json 的归档值比较
Get-FileHash -Algorithm SHA256 .\literature\pdfs\*.pdf
```

清单记录本次固定版本，不会静默切到将来的最新版。若需重取文件，使用清单内 `pdf_url`，下载到临时文件，核对 PDF 文件头、解析结果和归档哈希后再恢复缺失副本；不要覆盖原始哈希记录。若需更新版本，应先重新检查官方摘要页，保留旧版并新增文件与记录。

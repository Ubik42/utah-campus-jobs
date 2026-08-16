# 犹他大学校内兼职信息查询

> University of Utah 校内 **Part Time** 兼职岗位信息整理 —— 完整中文翻译、可筛选 Excel、官网原文对照，方便一次性浏览和筛选。

## 这是什么

官网招聘页面适合逐条打开，但没法把所有岗位放一起检索，详情页里大量小标题的视觉层级也很接近。这个仓库把 University of Utah Campus 招聘页面在 **2026-08-16** 的兼职岗位快照抓取下来，整理成：

- **122 个 Part Time 兼职岗位**，每个岗位按「摘要 / 职责 / 最低资格 / 优先条件 / 申请说明 / 排班」统一拆分；
- 完整中文翻译，英文原文并列保留，方便对照；
- 一份可筛选的 Excel（岗位检索表），可按部门、日期、工时、薪资、Work-Study、本科生限定、驾照、食品证、酒类证、经验等条件筛选。

公开版不按任何人的身份或申请日期删岗。本科生、研究生、有或没有 Federal Work-Study 的同学，都能按自己的条件筛。

## 快速开始

1. 下载 [`jobs.xlsx`](jobs.xlsx)，打开「岗位检索」表；
2. 用表头筛选：按自己的申请日期（开放日期不晚于今天、截止日期不早于今天）、身份（是否本科生限定）、工时、时薪、证照等条件过滤；
3. 点「中文职位」那一列（单元格就是官网链接）打开原岗位页核对；
4. 要读完整正文，看「完整中文」和「英文原文」两张表，或直接读 [`jobs.zh.md`](jobs.zh.md)。

## 文件说明

| 文件 | 内容 |
| --- | --- |
| `jobs.xlsx` | 推荐入口：岗位检索、完整中文、英文原文、使用说明四张表 |
| `jobs.zh.md` | 按部门组织的 122 个岗位完整中文，附折叠英文原文 |
| `data/jobs.zh.json` | 清洗后的完整双语结构化数据 |
| `data/raw/jobsyn-campus-2026-08-16.json` | 招聘列表接口原始快照 |
| `data/translations.zh.jsonl` | 按 GUID 保存的中文翻译 |
| `data/extra-requirements.json` | 人工标注的硬性额外要求（证书、语言、学历等） |
| `docs/filtering-and-sorting.md` | 字段提取、筛选与排序口径 |
| `docs/data-dictionary.md` | Excel 与 JSON 字段解释 |
| `docs/shared-notices.md` | 岗位通用的校级补充信息（Additional Information） |

## 申请注意事项

> 这份信息是整理后的历史快照，不是学校的官方资格确认。**申请前务必回官网核对。**

1. **快照 ≠ 实时**：岗位可能提前关闭或内容已更新，点职位名打开官网页确认。
2. **「页面明确关闭」的岗位先跳过**：有 5 个岗位正文已写明 "This posting is closed and is no longer accepting applications"，即使它的截止日期还在未来（Excel「页面明确关闭」列标 ✅）。
3. **中文是 AI 翻译**：只用于快速浏览和检索，涉及资格、证照、日期、申请材料时，以英文原文为准。
4. **资格标签只是初筛，不是学校确认**：
   - **Work-Study（勤工助学）**：联邦勤工助学（Federal Work-Study）需要通过 FAFSA 申请，一般只有美国公民或符合条件的非公民（绿卡等）能获得，持 F-1 签证的国际学生通常没有资格。✅ 必需 = 没有资格就别投；🟡 可选/非必需；❌ 未明确要求。
   - **本科生限定**：✅ = 明确只面向本科生，研究生申请前先确认自己是否符合。
   - **驾照**：✅ 明确要求 = 需要已有驾照，没驾照的岗位先排除；🟡 入职后可取得。
   - **食品处理员许可证**：比较容易获得，通常线上几小时课程 + 少量费用即可，很多岗位也允许入职后再考（🟡）。
   - **经验要求**：✅ 明确要求经验年限；「教育可折抵经验」的岗位要结合专业和折抵公式自己判断。
   - **额外要求**：正文里的硬性要求（如韩语接近母语级、特定证书、特定软件、学历、体力、年龄等），只标硬门槛，不列「有责任心」这类软性描述。
5. **日期分两种**：开放日期、截止日期。正文已写关闭的岗位即使截止日期未到也要跳过（见第 2 条）。
6. **工时与薪资**：工时是解析值（如 `0-19`、`up to 10`）；薪资标 `DOE` 或年薪的不做小时换算。
7. **背景调查**：部分岗位可能要求背景调查 / 药物筛查，见 [`docs/shared-notices.md`](docs/shared-notices.md)。

## 数据来源

- 来源：[University of Utah Campus Jobs](https://employment.utah.edu/location-name/campus/organization/university-of-utah/jobs/)
- 抓取时间：2026-08-16 05:02（UTC+8）
- 原始列表岗位：319 · 兼职（Part Time）岗位：122
- 完整中文字段：职位名、摘要、职责、最低资格、优先条件、申请说明、排班

## 重新生成

只使用仓库快照、不访问网络：

```powershell
python scripts/build_dataset.py   # 生成 data/jobs.zh.json + jobs.zh.md
python scripts/build_xlsx.py      # 生成 jobs.xlsx
python -m unittest discover -s scripts -p "test_*.py"
```

重新抓取官网列表 / 补译新增字段：

```powershell
python scripts/fetch_jobs.py --output data/raw/jobsyn-campus-YYYY-MM-DD.json
python scripts/translate_with_deepseek.py
```

翻译脚本只读环境变量 `DEEPSEEK_API_KEY`，不打印、不保存密钥；接口不可用时不会切换到其他翻译服务。

## 许可

脚本代码采用 [MIT License](LICENSE)。招聘原文和原始数据版权归原发布方所有，不在该许可的授权范围内。

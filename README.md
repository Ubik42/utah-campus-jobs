# 犹他大学校内兼职信息查询

> University of Utah 校内 **Part Time** 兼职岗位信息整理 —— 完整中文翻译、可筛选 Excel、官网原文对照，方便一次性浏览和筛选。

![岗位](https://img.shields.io/badge/岗位-122个-1E7B1E) ![快照](https://img.shields.io/badge/快照-2026--08--16-1F4E79) ![License](https://img.shields.io/badge/License-MIT-808080)

## 目录

- [这是什么](#这是什么)
- [快速开始](#快速开始)
- [文件说明](#文件说明)
- [申请注意事项](#申请注意事项)
- [关于联邦勤工助学（Federal Work-Study）](#关于联邦勤工助学federal-work-study)
- [筛选口径（供重新分析参考）](#筛选口径供重新分析参考)
- [数据来源](#数据来源)
- [重新生成](#重新生成)
- [许可](#许可)

## 这是什么

官网招聘页面适合逐条打开，但没法把所有岗位放一起检索，详情页里大量小标题的视觉层级也很接近。这个仓库把 University of Utah Campus 招聘页面在 **2026-08-16** 的兼职岗位快照抓取下来，整理成：

- **122 个 Part Time 兼职岗位**，每个岗位按「摘要 / 职责 / 最低资格 / 优先条件 / 申请说明 / 排班」统一拆分；
- 完整中文翻译，英文原文并列保留，方便对照；
- 一份可筛选的 Excel（岗位检索表），可按部门、日期、工时、薪资、Work-Study、本科生限定、驾照、食品证、经验等条件筛选。

公开版不按任何人的身份或申请日期删岗。本科生、研究生、有或没有 Federal Work-Study 的同学，都能按自己的条件筛。

## 快速开始

1. 下载 [`jobs.xlsx`](jobs.xlsx)，打开「岗位检索」表；
2. 用表头筛选：按自己的申请日期（开放日期不晚于今天、截止日期不早于今天）、身份（是否本科生限定）、工时、时薪、证照等条件过滤；
3. 点「中文职位」那一列（单元格就是官网链接）打开原岗位页核对；
4. 要读完整正文，看「完整中文」和「英文原文」两张表，或直接读 [`jobs.zh.md`](jobs.zh.md)。

## 文件说明

| 文件 | 内容 |
| --- | --- |
| `jobs.xlsx` | 推荐入口：岗位检索、完整中文、英文原文、MEAE国际学生省流版、使用说明五张表 |
| `jobs.zh.md` | 按部门组织的 122 个岗位完整中文，附折叠英文原文 |
| `data/jobs.zh.json` | 清洗后的完整双语结构化数据 |
| `data/raw/jobsyn-campus-2026-08-16.json` | 招聘列表接口原始快照 |
| `data/translations.zh.jsonl` | 按 GUID 保存的中文翻译 |
| `data/extra-requirements.json` | 人工标注的硬性额外要求（证书、语言、学历等） |
| `data/core-skills.json` | 人工标注的核心能力（摄影、剪辑、设计、编程等） |
| `docs/filtering-and-sorting.md` | 字段提取、筛选与排序口径 |
| `docs/data-dictionary.md` | Excel 与 JSON 字段解释 |
| `docs/shared-notices.md` | 岗位通用的校级补充信息（Additional Information） |

## 申请注意事项

> 这份信息是整理后的历史快照，不是学校的官方资格确认。**申请前务必回官网核对。**

1. **快照 ≠ 实时**：岗位可能提前关闭或内容已更新，点职位名打开官网页确认。
2. **「页面明确关闭」的岗位先跳过**：有 5 个岗位正文已写明 "This posting is closed and is no longer accepting applications"，即使它的截止日期还在未来（Excel「页面明确关闭」列标 ✅）。
3. **中文是 AI 翻译**：只用于快速浏览和检索，涉及资格、证照、日期、申请材料时，以英文原文为准。
4. **资格标签只是初筛，不是学校确认**：
   - **Work-Study（勤工助学）**：联邦勤工助学（Federal Work-Study）是联邦资助项目，F-1 国际学生没有资格；✅ 必需 = 没有资格就别投，🟡 可选/非必需，❌ 未明确要求。详见下文「关于联邦勤工助学（Federal Work-Study）」。
   - **本科生限定**：✅ = 明确只面向本科生，研究生申请前先确认自己是否符合。
   - **驾照**：✅ 明确要求 = 需要已有驾照，没驾照的岗位先排除；🟡 入职后可取得。
   - **食品处理员许可证**：比较容易获得，通常线上几小时课程 + 少量费用即可，很多岗位也允许入职后再考（🟡）。
   - **经验要求**：✅ 明确要求经验年限；「教育可折抵经验」的岗位要结合专业和折抵公式自己判断。
   - **额外要求**：正文里的硬性要求（如韩语接近母语级、特定证书、特定软件、学历、体力、年龄等），只标硬门槛，不列「有责任心」这类软性描述。
5. **日期分两种**：开放日期、截止日期。正文已写关闭的岗位即使截止日期未到也要跳过（见第 2 条）。
6. **工时与薪资**：工时是解析值（如 `0-19`、`up to 10`）；薪资标 `DOE` 或年薪的不做小时换算。
7. **背景调查**：部分岗位可能要求背景调查 / 药物筛查，见 [`docs/shared-notices.md`](docs/shared-notices.md)。

## 关于联邦勤工助学（Federal Work-Study）

**如果你是 F-1 国际学生，这个 Federal Work-Study（FWS，联邦勤工助学）资格拿不到。** 根据[犹他大学 ISSS 官方说明](https://isss.utah.edu/f-1-visa-program/employment/on-campus-employment/index.php)，国际学生不符合 Work-Study 资格，因为它属于联邦资助项目。

招聘页面如果明确写：

- `Federal Work-Study Award required`
- `Must have Work-Study eligibility`
- `Work-Study position only`

这种职位可以直接排除——它和普通校内兼职不是一回事。

如果你是美国公民或符合条件的非公民，获得资格的流程是：

1. 提交对应学年的 FAFSA，并让犹他大学收到申请；
2. 等学校完成经济需求评估；
3. 在 CIS 的 Financial Aid 中查看资助方案；
4. 若方案里已有 Federal Work-Study，在 CIS 中接受该项目；
5. 若 FAFSA 已完成但方案里没有 FWS，可提交学校的 [2026–2027 Federal Work-Study 申请表](https://financialaid.utah.edu/forms/onbase/2026-2027-federal-work-study-form.php) 请求重新考虑；
6. 拿到 FWS Award 后才能申请 FWS 专属职位；
7. 入职前还需由雇主向资助办公室申请 EAF；EAF 才是最终的工作资格确认。

学校要求申请人具备：经济需求、就读符合条件的学位项目、保持 SAP 学业进度、至少注册一门学分课程、拥有有效 SSN，并且是美国公民或符合条件的非公民。资金有限，提交申请也不保证获批。

**如果你是 F-1，应该筛选普通的校内学生职位。** F-1 学生通常可以做符合规定的校内工作，开学期间每周最多 20 小时。

参考链接：
- [F-1 校内就业（犹他大学 ISSS）](https://isss.utah.edu/f-1-visa-program/employment/on-campus-employment/index.php)
- [Federal Work-Study 基础说明](https://financialaid.utah.edu/types-of-aid/work-study/students/basics.php)
- [2026–2027 Federal Work-Study 申请表](https://financialaid.utah.edu/forms/onbase/2026-2027-federal-work-study-form.php)

## 筛选口径（供重新分析参考）

`jobs.xlsx` 的「岗位检索」表用一组状态标签描述每个岗位的资格门槛，这些标签由脚本从英文原文自动提取，口径如下（详见 [docs/filtering-and-sorting.md](docs/filtering-and-sorting.md)）：

- **Work-Study**：必需 / 可选·非必需 / 未明确要求 —— 联邦勤工助学（FWS），F-1 国际学生没有资格。
- **本科生限定**：是 / 否 —— 是否明确只面向本科生。
- **驾照 / 食品证**：明确要求 / 入职后可取得 / 未发现明确要求。
- **经验要求**：明确要求经验年限 / 未发现明确年限。
- **页面明确关闭**：正文是否已写「不再接受申请」。
- **额外要求**：正文里的硬性门槛（语言、证书、学历、软件、体力、年龄等），人工标注于 `data/extra-requirements.json`。
- **核心能力**：岗位希望应聘者具备的能力/技能（摄影、剪辑、设计、编程、教学等），非硬门槛，人工标注于 `data/core-skills.json`。
- **需公民身份**（JSON 字段 `requires_citizenship`）：正文是否要求美国公民 / 国民 / 合法永久居民 —— 对 F-1 国际学生是硬性排除项。

「MEAE国际学生省流版」是给 MEAE 硕士 + F-1 国际学生的精简页，自动排除四类岗位：

1. Work-Study 必需；
2. 本科生限定；
3. 页面明确关闭；
4. 需公民身份。

日后拉取新的岗位快照后，先重跑 `scripts/build_dataset.py` 和 `scripts/build_xlsx.py` 按同一口径重建，再用 AI 复核「额外要求」和「需公民身份」这类需要读原文才能判断的标签。

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

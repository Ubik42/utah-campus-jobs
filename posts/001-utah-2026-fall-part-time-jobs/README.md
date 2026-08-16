# 犹他大学 2026 Fall 校内兼职

这是 University of Utah Campus 招聘页面在 2026-08-16 的兼职岗位快照，共 122 个 `Part Time` 岗位。

官网适合逐条打开，但不方便把所有岗位放在一起检索；职位详情页里大量小标题的视觉层级也很接近。这个版本把每条职位重新拆成“摘要、职责、最低资格、优先条件、申请说明、排班、补充信息”，并提供完整中文翻译和英文原文。

公开版没有按任何人的具体条件删岗。本科生、研究生、有或没有 Federal Work-Study 的同学都可以在 Excel 中自己筛选。

## 文件

- [jobs.xlsx](jobs.xlsx)：推荐入口。岗位检索、完整中文、英文原文和使用说明四张表。
- [jobs.zh.md](jobs.zh.md)：按部门组织的 122 个岗位完整中文内容，附折叠英文原文。
- [data/jobs.zh.json](data/jobs.zh.json)：清洗后的完整双语结构化数据。
- [data/raw/jobsyn-campus-2026-08-16.json](data/raw/jobsyn-campus-2026-08-16.json)：招聘列表接口原始快照。
- [data/translations.zh.jsonl](data/translations.zh.jsonl)：按 GUID 保存的中文翻译。
- [docs/filtering-and-sorting.md](docs/filtering-and-sorting.md)：字段提取、筛选和排序口径。
- [docs/data-dictionary.md](docs/data-dictionary.md)：Excel 与 JSON 字段解释。
- [xiaohongshu.md](xiaohongshu.md)：对应的小红书分享文案。

## 数据范围

- 来源：[University of Utah Campus Jobs](https://employment.utah.edu/location-name/campus/organization/university-of-utah/jobs/)
- 抓取时间：2026-08-16 05:02（UTC+8）
- 原始列表岗位：319
- 兼职岗位：122
- 完整中文字段：职位名、摘要、职责、最低资格、优先条件、申请说明、排班、补充信息

## 重新生成

只使用仓库快照，不访问网络：

```powershell
python scripts/build_dataset.py
python scripts/build_xlsx.py
python -m unittest discover -s scripts -p "test_*.py"
```

重新抓取官网列表：

```powershell
python scripts/fetch_jobs.py --output data/raw/jobsyn-campus-YYYY-MM-DD.json
```

补译新增岗位的完整字段：

```powershell
python scripts/translate_with_deepseek.py
```

翻译脚本只读取环境变量 `DEEPSEEK_API_KEY`，不会打印或保存密钥；接口不可用时不会切换到其他翻译服务。成功结果按原文哈希缓存，可中断续跑。

## 说明

- 快照不等于官网实时状态，职位可能提前关闭。
- 自动标签用于缩小范围，不是学校的资格确认。
- 中文翻译可能有误，正式申请以英文职位页面为准。

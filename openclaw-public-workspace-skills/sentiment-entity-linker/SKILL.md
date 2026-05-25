---
name: sentiment-entity-linker
description: |
  从新闻文本中提取公司名称、股票代码、所属行业，并结合官方信息、披露数据、股权结构、业务关联等构建多维证据链，进行深入、有逻辑、有依据的实体关联与关系识别。

  **Perfect for:**
  - 重大资产重组事件
  - 新产品/技术发布
  - 关键人物变动（如高管离职/入职）
  - 供应链中断或合作
  - 跨公司合作或竞争

  **Not ideal for:**
  - 宏观经济政策解读
  - 行业普涨普跌行情
  - 纯市场情绪驱动的波动
  - 缺乏明确事件驱动的日常舆情
---

# SentimentEntityLinker (证券舆情实体关联)


## 0) Public实例运行约定（CRITICAL）

- 本技能运行在 OpenClaw public 实例，工作区根目录固定为：`/home/ubuntu/.openclaw-public/workspace`。
- 若用户消息包含 `[[OPENCLAW_RUN_ID: <run_id>]]`，所有输出文件必须写入：
  - `/home/ubuntu/.openclaw-public/workspace/<run_id>/`
- 若未提供 run_id，可写入当前工作目录，但优先创建独立子目录避免覆盖。
- 需要检索新闻/网页时：
  - 优先使用 `web_search` 找来源
  - 用 `web_fetch` 抽取正文
  - 不使用不存在的 `search` 工具名


## ⚠️ CRITICAL: 证据优先级 (READ FIRST)

**ALWAYS follow this evidence hierarchy:**

1. **FIRST: 硬性证据 (Hard Evidence)** - 官方公告、财务报告、招股书、中标文件、合作协议、股权结构图等。
2. **SECOND: 可靠第三方证据 (Reliable 3rd-Party)** - 主流财经媒体深度报道、权威行业报告、政府公开数据。
3. **THIRD: 逻辑推测 (Logical Inference)** - 基于行业知识和业务逻辑的合理推断。
4. **NEVER use as primary evidence:** 社交媒体传闻、论坛帖子、无法验证来源的自媒体文章。

**Why this matters:** 确保实体关联的严肃性和可信度，避免基于不实信息得出错误结论。

---

## 1. 概述 (Overview)

`SentimentEntityLinker` 旨在超越简单的关键词匹配，对证券行业舆情文本中的实体进行**深度、多维、证据链驱动**的关联。它通过整合文本信息与结构化金融数据，构建实体间的逻辑关系，确保关联的准确性和可追溯性。

### ALWAYS ask yourself first:
1. **“本次舆情的核心驱动事件是什么？”**
2. **“关联的目的是为了寻找投资机会还是规避风险？”**
3. **“需要关联到多深的层次？（直接关联/二级关联/全产业链）”**

## 2. 核心能力 (Capabilities)

- **多源实体识别与消歧**
- **知识图谱构建与证据链关联**
- **关联强度量化与类型识别**
- **产业链与生态位分析**
- **供应链穿透与订单级关联**

## 3. 使用指南 (Usage)

### 输入要求
- `text`: 待分析的证券舆情文本。
- `context_entities`: (可选) 预设的关注实体列表。
- `external_data_sources`: (可选) 外部金融数据源接口凭证。
- `historical_documents_path`: (可选) 历史公告、财报等文档存储路径。

### 关联逻辑
1.  **文本预处理**
2.  **多源证据收集**
3.  **知识图谱推理**
4.  **结果输出**

## 4. Red Flags & Warning Signs

🚩 **关联证据薄弱**: 仅有媒体猜测，无任何官方或第三方佐证。
🚩 **关联逻辑牵强**: 跨行业、无业务交集的“概念”炒作。
🚩 **信息源单一**: 所有关联证据均来自同一篇自媒体文章。

**When in doubt, mark as "逻辑推测关联（待验证）".**

## 5. 输出规范 (Output Requirements)

| 字段 | 说明 | 是否必填 |
| :--- | :--- | :--- |
| `entity_pair` | 关联的两个实体名称 | 是 |
| `relation_type` | 关联类型 | 是 |
| `linkage_strength` | 关联强度 | 是 |
| `evidence_type` | 证据类型 | 是 |
| `evidence_detail` | 具体证据描述 | 是 |
| `supply_chain_position` | 该实体在产业链中的具体位置 | 是 |
| `financial_relevance` | 该关联对核心公司财务的潜在影响方向 | 是 |
| `source` | 证据来源 | 是 |
| `verification_status` | 已验证/待验证 | 是 |

## 6. Output Checklist

- [ ] 所有关联关系是否都已找到最强的可用证据？
- [ ] 是否已明确区分“硬性证据”和“逻辑推测”？
- [ ] 关联强度评分是否与证据强度匹配？
- [ ] 是否已为所有“待验证”的关联提供了清晰的验证路径？

## 7. Continuous Improvement

- 本次关联中最难验证的环节是什么？
- 是否有新的数据源可以提高关联的准确性？
- 下次进行类似事件的关联时，可以如何优化流程？
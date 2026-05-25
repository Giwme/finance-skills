---
name: thesis-tracker
description: 维护和更新持仓或观察名单的投资逻辑，追踪核心假设、关键数据点、催化剂、风险和信心变化。Use when the user asks to update thesis for a company, add a data point, review whether a thesis is intact, check position rationale, build a thesis scorecard, or run a portfolio thesis review.
---

# Thesis Tracker

## 使用原则

- 使用中文输出，结构清晰，优先使用 Markdown 标题、分段和表格。
- 分析必须可证伪：明确哪些事实会加强、削弱或推翻投资逻辑。
- 同等重视反证信息与确认信息，避免只收集支持原观点的数据。
- 结论仅供参考，不构成任何投资建议；在输出末尾保留风险提示。
- 如涉及当前行情、财报、公告或新闻，先用可用工具核验最新资料，并标注数据来源或时间。
- 将 thesis 数据保存为结构化文件，便于后续跨会话追踪。推荐路径：`theses/<ticker-or-company>.md`；如用户指定仓库或文件，以用户指定为准。

## 强制步骤标记

每当开始新的执行阶段，在该阶段开头单独输出一行：

```text
[STEP:阶段名称]
```

要求：

- 标记独占一行。
- 阶段名称不超过 8 个中文字符。
- 每次完整分析至少输出 3 个阶段标记。
- 示例：`[STEP:读取逻辑]`、`[STEP:更新记录]`、`[STEP:形成结论]`。

## 工作流

### 1. 定义或载入 Thesis

如果是新建 thesis，收集并记录：

- **公司**：公司名与 ticker。
- **方向**：Long / Short / Watchlist。
- **核心逻辑**：1-2 句概括主要投资假设。
- **关键支柱**：3-5 条支撑论点。
- **关键风险**：3-5 条可能推翻逻辑的风险。
- **催化剂**：可能验证或证伪逻辑的事件，如财报、产品发布、监管进展、行业数据。
- **目标价 / 估值框架**：逻辑兑现时的合理价值区间与主要假设。
- **止损或退出触发**：什么事实出现时应退出或显著降权。

如果是更新已有 thesis：

1. 先读取已有 thesis 文件或用户提供的原始逻辑。
2. 若缺少新数据点，向用户追问一个最关键问题：新发生了什么？
3. 若用户给出的信息足够，直接更新，不要求重复提供已有内容。

### 2. 记录更新日志

对每个新数据点记录：

| 字段 | 说明 |
|---|---|
| 日期 | 事件发生或披露日期 |
| 数据点 | 发生了什么变化 |
| 影响对象 | 影响哪个 thesis 支柱、风险或催化剂 |
| 逻辑影响 | Strengthen / Weaken / Neutral / Mixed |
| 操作建议 | No change / Increase / Trim / Exit / Watch |
| 更新后信心 | High / Medium / Low |

### 3. 更新 Thesis Scorecard

维护运行中的 scorecard：

| 支柱 | 原始预期 | 当前状态 | 趋势 |
|---|---|---|---|
| 收入增长 >20% | 维持高增 | 最近季度 22% | 稳定 |
| 利润率扩张 | 经营杠杆释放 | 利润率同比持平 | 需关注 |
| 新产品发布 | 按期上线 | 延迟至 Q2 | 转弱 |

趋势可使用：`改善`、`稳定`、`转弱`、`待验证`。

### 4. 更新催化剂日历

维护未来事件：

| 日期 | 事件 | 预期影响 | 关注点 |
|---|---|---|---|
|  |  |  |  |

如催化剂已发生，移动到更新日志，并说明是否验证了原始预期。

### 5. 形成输出

输出应适合：

- 晨会讨论
- 组合复盘
- 风险委员会汇报
- 单票逻辑追踪备忘

推荐结构：

```markdown
[STEP:读取逻辑]
## 当前 Thesis
- 公司：
- 方向：
- 核心逻辑：
- 当前信心：High / Medium / Low

[STEP:更新记录]
## 最新数据点
| 日期 | 数据点 | 影响 | 操作 | 信心 |
|---|---|---|---|---|

## Thesis Scorecard
| 支柱 | 原始预期 | 当前状态 | 趋势 |
|---|---|---|---|

[STEP:催化跟踪]
## 催化剂日历
| 日期 | 事件 | 预期影响 | 关注点 |
|---|---|---|---|

[STEP:形成结论]
## 结论
- Thesis 是否 intact：是 / 否 / 部分成立
- 关键变化：
- 需要继续验证：
- 建议动作：

> 分析仅供参考，不构成任何投资建议。
```

## 存储格式

若需要落盘，使用如下结构：

```markdown
# <Company> (<Ticker>) Thesis

## Metadata
- Direction:
- Current conviction:
- Last updated:

## Core Thesis

## Key Pillars

## Key Risks

## Valuation / Target

## Stop-loss / Exit Triggers

## Update Log

## Scorecard

## Catalyst Calendar
```

## 组合级复盘

当用户要求 review my positions / full portfolio thesis review：

1. 列出所有持仓或观察名单 thesis。
2. 按信心变化排序：显著增强、稳定、转弱、需退出。
3. 标记超过一个季度未更新的 thesis。
4. 汇总共性风险，如宏观、利率、监管、行业竞争、估值压缩。
5. 输出组合层面的优先跟踪清单。

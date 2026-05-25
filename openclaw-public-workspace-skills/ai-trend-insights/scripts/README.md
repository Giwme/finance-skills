# AI金融高管简报 - Scripts目录说明

## 目录结构

```
scripts/
├── generate.js           # PPT生成主脚本（排版逻辑）
├── content.example.json  # 文案配置示例
└── README.md            # 本文件
```

## 使用说明

### 文案与脚本分离原则

根据SKILL.md第8节要求，所有中文文案必须放在 `content.json` 中，`generate.js` 只负责排版逻辑。

### 运行流程

1. **语法检查（必须）**
   ```bash
   node --check generate.js
   ```

2. **生成PPT**
   ```bash
   node generate.js content.json 输出文件.pptx
   ```

### content.json 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 报告主标题 |
| subtitle | string | 否 | 副标题 |
| date | string | 是 | 报告日期 |
| author | string | 否 | 作者/团队 |
| slides | array | 是 | 幻灯片配置数组 |
| charts | array | 否 | 图表配置 |

### 幻灯片类型

- `cover` - 封面
- `summary` - 核心洞察摘要
- `model_evolution` - 模型能力演进
- `finance_application` - 金融应用生态
- `infrastructure` - 算力与工具链
- `recommendations` - 战略建议
- `end` - 结束页

## 错误处理

若 `node --check` 失败：
1. 自动修复一次并重试
2. 再失败则终止PPT生成
3. 保留文字稿并写入 `.done(status=failed)`

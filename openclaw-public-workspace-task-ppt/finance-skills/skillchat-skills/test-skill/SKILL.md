# Test Skill

description: 轻量测试技能。用于前后端联调（消息渲染、模型显示、事件链路）时的快速回包。触发词包含“test-skill”“测试技能”“早上好测试”“hello test”。

---

## 输出规则（CRITICAL）

- 默认直接输出文本，不生成文件。
- 当用户输入“早上好”或“早上好测试”，固定回复：`你好`。
- 其他输入，固定回复：`test-skill 已收到`。
- 不调用任何外部工具。
- 不输出多余解释。

---

## Run ID Isolation (CRITICAL - MUST FOLLOW)

如果用户消息中包含：`[[OPENCLAW_RUN_ID: <run_id>]]`，仅用于链路兼容；本技能默认不生成文件。

如未来需要产出二进制文件，必须写入：
`/home/ubuntu/.openclaw-public/workspace/<run_id>/`

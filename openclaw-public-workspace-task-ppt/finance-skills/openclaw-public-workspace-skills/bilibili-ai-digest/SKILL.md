# Bilibili AI Digest

## Run ID Isolation (CRITICAL - MUST FOLLOW)

**All file outputs MUST be isolated per request using run_id.**

### Run Context

User messages may contain a marker:

```
[[OPENCLAW_RUN_ID: <run_id>]]
```

**If present, you MUST:**

1. **Extract the run_id** from the marker
2. **When executing any script or generating files, always pass it as:**
   ```
   --run-id <run_id>
   ```
3. **All generated artifacts MUST be written under:**
   ```
   /home/ubuntu/.openclaw-public/workspace/<run_id>/
   ```

**NEVER write artifacts directly into the workspace root.**

### Implementation Pattern

```python
import re
import argparse
from pathlib import Path

# Extract run_id from conversation context
context = """{{user_input}}"""
match = re.search(r'\[\[OPENCLAW_RUN_ID:\s*([a-zA-Z0-9_-]+)\]\]', context)
run_id = match.group(1) if match else 'default'

# Create isolated output directory
workspace = Path("/home/ubuntu/.openclaw-public/workspace")
output_dir = workspace / run_id
output_dir.mkdir(parents=True, exist_ok=True)

# Write all files to this directory
output_file = output_dir / f"Bilibili_Digest_{date}.md"
```

### Completion Marker (REQUIRED)

After ALL files are generated:

```python
import json
from datetime import datetime

completed_files = [
    f.name for f in output_dir.iterdir()
    if f.is_file()
    and not f.name.startswith(".")
    and not f.name.endswith(".tmp")
    and f.suffix.lower() in [".xlsx", ".pptx", ".docx", ".pdf"]  # 只包含二进制文件，文本内容直接输出
]
```

- `--hours=N`：抓取最近 N 小时内发布的视频，默认 48 小时
- `--weekly`：周报模式，自动生成本周一至今的周报格式（含正确日期范围）
- 输出为 Markdown 格式，直接转发给用户

## UP 主配置（scripts/fetch_bilibili.py 顶部 UP_LIST）

| 博主 | UID | 状态 |
|------|-----|------|
| 硅谷101 | 508452265 | ✅ |
| AI深度研究员 | 3546710527707195 | ✅ |
| KrillinAI小林 | 242124650 | ✅ |
| 飞天闪客 | 325864133 | ✅ |
| 产品君 | 1845434732 | ✅ |

## 添加/修改 UP 主

编辑 `scripts/fetch_bilibili.py` 文件，修改 `UP_LIST` 变量：

```python
UP_LIST = [
    {"name": "博主名称", "uid": "数字UID", "note": "备注"},
    # 添加更多...
]
```

## 定时运行

建议通过 cron 或 systemd timer 设置定时任务：

```bash
# 每天上午 9 点推送
0 9 * * * cd /home/ubuntu/.openclaw-public/workspace && python3 skills/bilibili-ai-digest/scripts/fetch_bilibili.py --hours=24

# 或每周一上午 9 点推送周报
0 9 * * 1 cd /home/ubuntu/.openclaw-public/workspace && python3 skills/bilibili-ai-digest/scripts/fetch_bilibili.py --weekly
```

## OpenAI/Codex Tooling Guardrails (Shared)

Apply these rules when using runtime tools (especially with openai-codex/gpt-5.3-codex):

1. Python runtime
- Always use `python3`.
- Never use `python`.

2. web_search language
- For Chinese queries, use `search_lang: "zh-hans"`.
- Do not use `search_lang: "zh"`.
- If language is not critical, omit `search_lang`.

3. web_search execution strategy
- Run searches serially (avoid parallel bursts).
- Use minimum queries needed (typically 3-5).
- Add throttle between calls (~1.2-1.8s).

4. Error auto-recovery
- On 422 with invalid `search_lang`, retry once with `zh-hans`.
- On 429 RATE_LIMITED, back off (wait longer), reduce query count, then retry.

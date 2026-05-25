---
name: bilibili-ai-digest
description: 定时抓取 B站指定 AI 博主的最新视频并推送摘要。关注的 UP 主包括：硅谷101、AI深度研究员、KrillinAI小林、飞天山客、产品君。当用户提到"B站推送"、"B站视频更新"、"AI博主最新视频"、"bilibili digest"时触发。
---

# Bilibili AI Digest

定期抓取指定 UP 主的最新视频，格式化后推送给用户。

## 运行方式

```bash
python3 skills/bilibili-ai-digest/scripts/fetch_bilibili.py [--hours=48] [--weekly]
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

编辑 `scripts/fetch_bilibili.py` 中的 `UP_LIST` 字典，格式：
```python
"博主名称": UID数字,
```

查找 UID：访问 `https://space.bilibili.com/` 后跟主页 URL 中的数字。

## 定时推送

通过 cron job 定时执行本 skill：
- 每天早上 9:00（北京时间，即 UTC 01:00）推送一次
- cron 表达式：`0 1 * * *`
- 使用 `--weekly` 参数生成周报格式

## 注意事项

- Bilibili API 有频率限制，UP 主较多时请求间增加了 0.5s 延迟
- 若 API 返回频率限制错误，稍后重试即可
- `飞天山客` UID 尚未确认，需用户补充

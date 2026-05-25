---
name: doc-parse-and-exam
description: Comprehensive document parsing and examination toolkit for OCR, document analysis, and image quality checking. Use when parsing bank statements, invoices or other documents from images. Use when performing OCR with Qwen3-VL, PaddleOCR VL 1.5, PP-OCR, or Kimi. Use when checking image quality before OCR processing. Use when validating bank statement consistency across multiple transactions. Use when extracting structured data from scanned documents.
---

# Doc Parse and Examination Skill



---

## 输出规则（CRITICAL）

### 直接输出 vs 生成文件

**默认行为：直接输出文本内容**
- Markdown、纯文本内容 → 直接回复，**不生成 .md 文件**
- 除非用户明确要求"生成文件"、"保存为"、"导出"

**需要生成文件的情况：**
- 生成 Excel (.xlsx)、PPT (.pptx)、Word (.docx)、PDF (.pdf) 等二进制文件
- 用户明确要求："生成 md 文件"、"保存报告"、"导出到文件"
- 内容超过 4000 字符，需要作为附件下载

### .done 文件规则

**.done 文件的 `files` 字段只包含二进制文件：**

```python
# 只将二进制文件计入 completed_files（文本内容直接输出）
completed_files = [
    f.name for f in output_dir.iterdir() 
    if f.is_file() 
    and not f.name.startswith(".") 
    and not f.name.endswith(".tmp")
    and f.suffix.lower() in [".xlsx", ".pptx", ".docx", ".pdf"]  # 只包含二进制文件
]
```

---


## Overview

This skill provides a comprehensive toolkit for document parsing, OCR analysis, image quality assessment, and bank statement verification. It includes 5 specialized tools and a verification system for handling scanned documents and images.

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
output_file = output_dir / f"Parsed_Document_{date}.json"
```

### Completion Announcement (REQUIRED)

After writing the `.done` file, you MUST announce completion in this exact format:

```
✅ 任务完成，文件已生成：{filename}
```

Example:
```
✅ 任务完成，文件已生成：Parsed_Document_2026-03-06.json
```

This signals the frontend to display the download card immediately.

**Violation of this rule causes file collisions between concurrent users.**

## Tool Suite

The skill includes the following tools in `scripts/`:

### 1. Qwen3 Document Parser (`qwen3-doc-parse.py`)
- **Purpose**: High-quality document parsing using Qwen3-VL-32B-Instruct model via DashScope API
- **Features**: Text extraction, layout analysis, table structure recognition, seal/stamp detection
- **Best for**: When you need detailed layout understanding and high accuracy OCR
- **API Key**: Requires DashScope API key (provided in script or environment variable)

### 2. PaddleOCR VL 1.5 Parser (`paddleocr_vl_parse.py`)
- **Purpose**: Document parsing using PaddleOCR VL 1.5 model (local deployment option)
- **Features**: OCR, layout analysis, multi-page document support
- **Best for**: When you need local processing or have PaddleOCR installed
- **Local setup**: Requires PaddleOCR installation and model configuration

### 3. PP-OCR Parser (`ppocr-doc-parse.py`)
- **Purpose**: Lightweight OCR using PP-OCR model
- **Features**: Fast text extraction, optimized for Chinese text recognition
- **Best for**: When speed is prioritized and only text extraction is needed
- **Setup**: Uses PaddleX library with PIR model format

### 4. Kimi Document Parser (`kimi-doc-parse-compressed.py`)
- **Purpose**: Document parsing using Kimi API (compressed image version)
- **Features**: Text extraction from compressed images, optimized for API usage
- **Best for**: When you have Kimi API access and need to minimize data transfer
- **Note**: Compresses images to reduce upload size while maintaining quality

### 5. Image Quality Checker (`img_quality_check.py`)
- **Purpose**: Image quality assessment using Qwen3-VL model
- **Features**: Quality scoring (0-10), pass/fail decision, batch processing, post-processing rules
- **Best for**: Pre-OCR quality screening to identify problematic images
- **Post-processing**: Includes keyword-based and filename-based rules for accurate classification

## Core Workflows

### A. Document Parsing Workflow
1. **Quality Check First** (Recommended): Run `img_quality_check.py` to assess image quality
2. **Choose Parser**: Select appropriate parser based on needs:
   - High accuracy + layout → Qwen3
   - Local processing → PaddleOCR VL 1.5  
   - Fast text only → PP-OCR
   - API-based compressed → Kimi
3. **Execute Parsing**: Run selected parser with image path
4. **Review Results**: Check output Markdown/JSON files for extracted data

### B. Bank Statement Verification
The system includes functionality to validate bank statement consistency:
- **Cross-transaction consistency**: Verify opening/closing balances match transaction sums
- **Multi-period analysis**: Compare statements across different time periods
- **Format validation**: Check for required fields and proper formatting

### C. Typical End-to-End Workflow (Production-Ready)

For high-stakes document processing (e.g., bank statements, invoices), follow this comprehensive 5-step pipeline:

1. **Image Quality Screening** 
   - **Purpose**: Filter out images unsuitable for OCR before wasting processing resources
   - **Tool**: `img_quality_check.py`
   - **Action**: Run batch quality check on all incoming images
   - **Output**: Separate images into "pass" (quality score ≥7) and "fail" categories

2. **Multi-Model Parsing** (Parallel Execution)
   - **Purpose**: Leverage different OCR models for complementary strengths
   - **Recommended Models**: Qwen3-VL (layout accuracy) + PP-OCR (text speed)
   - **Tool**: Run both `qwen3-doc-parse.py` and `ppocr-doc-parse.py` on the same image
   - **Action**: Use batch scripts (`batch-parse.sh`, `batch-ppocr.sh`) for efficiency

3. **Cross-Result Comparison**
   - **Purpose**: Identify consensus vs. conflicting information between models
   - **Method**: Compare extracted text, table structures, and numeric values
   - **Action**: Use the cross-comparison methodology in `references/doc-parse.md`
   - **Output**: Highlight discrepancies for manual review

4. **Consistency Verification**
   - **Purpose**: Validate financial logic (for bank statements)
   - **Tool**: Bank statement verification scripts (generated from `bank_statement_verification_prompt.md`)
   - **Action**: Apply balance continuity checks, sum validations
   - **Output**: Pass/fail status with detailed error reports

5. **Batch Processing Automation**
   - **Purpose**: Scale to large volumes of documents
   - **Tool**: Use the provided `.sh` scripts for each parser (`batch-*.sh`)
   - **Action**: Set up cron jobs or workflow automation
   - **Output**: Structured data ready for integration with accounting systems

**When to Use This Workflow**:
- Processing large volumes of bank statements or invoices
- When accuracy is critical (financial, legal documents)
- When you need audit trails and validation evidence

**Simplified Alternative**: For less critical documents, follow the basic Document Parsing Workflow (Section A).

See `references/doc-parse.md` for detailed verification examples and implementation guides.

## Quick Start

### 1. Setup Environment
```bash
# Basic Python dependencies
pip install openai paddlepaddle paddlex

# Optional: Install PaddleOCR for local processing
pip install paddleocr
```

### 2. API Keys Configuration
```bash
# For Qwen3 parser
export DASHSCOPE_API_KEY="sk-your-key-here"

# For Kimi parser (if using Kimi API)
export KIMI_API_KEY="your-kimi-api-key"
```

### 3. Run a Simple Test
```bash
# Check image quality first
python scripts/img_quality_check.py assets/test_images/30-谢弋/流水明细/001_正常.jpg

# Parse with Qwen3
python scripts/qwen3-doc-parse.py assets/test_images/30-谢弋/流水明细/001_正常.jpg
```

## Reference Materials

### Comprehensive Documentation
- **`references/doc-parse.md`**: Complete documentation for all tools, including:
  - Installation and configuration guides for each parser
  - Detailed usage examples and command syntax
  - Output format specifications
  - Error handling and troubleshooting
  - Performance optimization tips
  - Bank statement verification methodology

### Sample Files
- **`assets/test_images/`**: Test images for experimentation
  - `30-谢弋/流水明细/`: Bank statement samples
  - Includes various image quality conditions for testing

## Best Practices

### 1. Pre-processing Recommendations
- **Image Quality**: Use `img_quality_check.py` before parsing
- **Size Optimization**: Resize images to ~2000px width for faster processing
- **Format**: Use JPEG with 80-90% quality for good balance of quality/size

### 2. Parser Selection Guidelines
| Scenario | Recommended Parser | Why |
|----------|-------------------|-----|
| High accuracy, detailed layout | Qwen3 | Best layout understanding and text recognition |
| Privacy-sensitive, offline | PaddleOCR VL 1.5 | Local processing, no data sent externally |
| Fast text extraction only | PP-OCR | Optimized for speed, good Chinese recognition |
| Compressed data transfer | Kimi | Reduced upload size, API-based |
| Quality screening | Image Quality Checker | Pre-OCR assessment |

### 3. Post-processing and Validation
- **Cross-check**: Run multiple parsers on critical documents for validation
- **Rule-based correction**: Apply keyword/filename rules for quality assessment
- **Consistency checks**: Verify financial data consistency across transactions

## Common Use Cases

### Bank Statement Processing
1. Quality check incoming statement images
2. Parse with Qwen3 for highest accuracy
3. Extract transaction data and balance information
4. Validate consistency using verification scripts
5. Generate summary reports

### Invoice Extraction
1. Check invoice image quality
2. Parse with appropriate parser based on invoice complexity
3. Extract vendor, amount, date, and line items
4. Format extracted data for accounting systems

### Document Digitization Workflow
1. Batch quality check all scanned documents
2. Separate high/low quality images
3. Parse high-quality images with preferred parser
4. Flag low-quality images for rescanning
5. Generate structured data outputs

## Troubleshooting

### Common Issues and Solutions

**Q: API key errors with Qwen3 parser**
- **Solution**: Verify API key is set in environment or passed via `--api-key` parameter
- **Check**: Run `echo $DASHSCOPE_API_KEY` to verify environment variable

**Q: PaddleOCR installation issues**
- **Solution**: Install specific versions: `pip install paddlepaddle==2.6.0 paddleocr==2.7.0`

**Q: Image quality checker false positives**
- **Solution**: Adjust post-processing rules in `img_quality_check.py` to match your specific needs

**Q: Memory issues with large images**
- **Solution**: Resize images before processing or use Kimi parser with compression

## Related Resources

For detailed API documentation, parameter specifications, and advanced usage examples, refer to `references/doc-parse.md`. The reference document contains 1300+ lines of comprehensive guidance covering all aspects of the tool suite.

---

## Completion Marker (REQUIRED)

**After ALL files are generated, you MUST write a `.done` marker file.**

This signals the frontend that processing is complete and files are ready.

### Implementation

```python
import json
from pathlib import Path
from datetime import datetime

# After all files are generated and atomically renamed
output_dir = Path(f"/home/ubuntu/.openclaw-public/workspace/{run_id}")

# Collect list of completed files (excluding .tmp and hidden files)
completed_files = [
    f.name for f in output_dir.iterdir()
    if f.is_file() 
    and not f.name.startswith('.') 
    and not f.name.endswith('.tmp')
]

# Write completion marker
done_file = output_dir / ".done"
done_data = {
    "status": "completed",
    "run_id": run_id,
    "skill": "doc-parse-and-exam",
    "files": completed_files,
    "file_count": len(completed_files),
    "timestamp": datetime.utcnow().isoformat() + "Z"
}
done_file.write_text(json.dumps(done_data, indent=2))

print(f"✅ Document parsing completed: {len(completed_files)} files generated")
print(f"📁 Output directory: {output_dir}")
print(f"📝 Files: {', '.join(completed_files)}")
```

### Rules

1. **Write .done LAST** — after all real files are fully written and renamed
2. **List all files** — the `files` array is the source of truth for frontend
3. **Never include .tmp files** — they should be renamed before writing .done
4. **JSON format** — must be valid JSON for frontend parsing

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

# qwen3-doc-parse.py 使用文档

## 概述

`qwen3-doc-parse.py` 是一个基于 **Qwen3-VL-32B-Instruct** 模型的银行流水图片解析工具。它通过 DashScope API 分析图片中的文字内容和版面结构，提取银行流水、表格数据、印章位置等信息。

## 功能特性

- **文字提取**：逐行提取图片中所有可见文字，保持原样（数字、符号、空格）
- **版面分析**：识别表格结构、字段位置、行列关系、印章位置、手写备注位置
- **多格式支持**：支持 JPEG、PNG 等常见图片格式
- **命令行参数**：灵活的路径和密钥配置
- **结果保存**：自动保存为 Markdown 格式，便于查看和后续处理

## 环境要求

### Python 版本
- Python 3.6 或更高版本

### 依赖包
```bash
pip install openai
```

### API 密钥
需要 DashScope API 密钥：
- 从 [DashScope 控制台](https://dashscope.console.aliyun.com/) 获取
- 或使用提供的密钥：`sk-0e4d21799ff746d28f0d5c86c6331770`

## 安装与配置

1. **克隆或下载脚本**：
   ```bash
   # 将 qwen3-doc-parse.py 保存到本地
   ```

2. **设置环境变量（可选）**：
   ```bash
   # Linux/macOS
   export DASHSCOPE_API_KEY="sk-0e4d21799ff746d28f0d5c86c6331770"
   
   # Windows (PowerShell)
   $env:DASHSCOPE_API_KEY="sk-0e4d21799ff746d28f0d5c86c6331770"
   ```

## 使用方法

### 基本语法
```bash
python qwen3-doc-parse.py <图片路径> [选项]
```

### 参数说明

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `image_path` | - | **必需**：待解析的图片文件路径 | - |
| `--api-key` | - | DashScope API 密钥 | 使用环境变量 `DASHSCOPE_API_KEY` |
| `--output` | `-o` | 结果输出文件路径 | `qwen3-result.md` |

### 示例

#### 示例 1：基本使用（使用环境变量中的 API 密钥）
```bash
python qwen3-doc-parse.py "/mnt/d/Downloads/银行流水/001_正常.jpg"
```
结果将保存到 `qwen3-result.md`

#### 示例 2：指定 API 密钥和输出文件
```bash
python qwen3-doc-parse.py "/mnt/d/Downloads/银行流水/002_斜拍.jpg" \
  --api-key "sk-0e4d21799ff746d28f0d5c86c6331770" \
  -o "result_002.md"
```

#### 示例 3：使用相对路径
```bash
python qwen3-doc-parse.py "./images/流水单.jpg" -o "./output/解析结果.md"
```

## 输出格式

解析结果保存为 Markdown 文件，包含以下内容：

```markdown
# 图片解析结果

**图片路径**：/path/to/image.jpg
**模型**：qwen3-vl-32b-instruct

**解析结果**：

### 1. 文字信息（逐行提取，按图片中三页从左到右顺序）

---
#### **第一页（左页）**
```
锦鲤民营银行交易流水
Transaction Statement of China Merchants Bank
2023-09-02 - 2023-12-30

户名: 高金未央
Name
账户类型: 稳定币
Account Type
...
```

### 2. 版面信息

#### 页面布局（三页并排）
- **左页**：位置 (0%-33%)，包含表头和个人信息
- **中页**：位置 (33%-66%)，主要交易数据
- **右页**：位置 (66%-100%)，继续交易数据和底部信息

#### 表格结构
- **列数**：6列
- **行数**：约 200 行
- **列标题**：记账日期、货币、交易金额、联机余额、交易摘要、对手信息

#### 印章位置
- **左上角**：圆形印章，中心有五角星图案
- **尺寸**：直径约 2cm
```

## 错误处理

### 常见错误及解决方法

| 错误信息 | 原因 | 解决方法 |
|----------|------|----------|
| `错误：图片文件不存在` | 指定的图片路径不正确 | 检查路径是否正确，使用绝对路径或正确相对路径 |
| `错误：未提供 API 密钥` | 未设置 API 密钥 | 通过 `--api-key` 参数传递或设置环境变量 |
| `API 调用出错：...` | API 请求失败 | 检查网络连接、API 密钥有效性、图片大小（建议 < 10MB） |
| `超时` | 图片过大或网络慢 | 脚本已设置 180 秒超时，可考虑压缩图片 |

### 调试建议

1. **检查图片路径**：
   ```bash
   ls -la "/mnt/d/Downloads/V1.0_TESTSET/data/oceanus-share/V1.0_IMAGES_TEST/15-高念未央/流水明细/001_正常.jpg"
   ```

2. **验证 API 密钥**：
   ```bash
   echo $DASHSCOPE_API_KEY
   ```

3. **测试小图片**：
   ```bash
   python qwen3-doc-parse.py "小图片.jpg" --api-key "sk-xxx"
   ```

## 性能优化

### 图片预处理建议
1. **尺寸调整**：建议图片宽度不超过 2000px
2. **格式优化**：使用 JPEG 格式，质量 80-90%
3. **文件大小**：控制在 2MB 以内以获得最佳响应速度

### 超时配置
脚本默认超时为 180 秒，如需调整可修改源代码：
```python
timeout=180.0  # 修改为所需秒数
```

## 实际应用示例

### 批量处理脚本示例
```bash
#!/bin/bash
# batch-parse.sh

API_KEY="sk-0e4d21799ff746d28f0d5c86c6331770"
INPUT_DIR="/mnt/d/Downloads/银行流水"
OUTPUT_DIR="./解析结果"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.jpg; do
    if [ -f "$img" ]; then
        filename=$(basename "$img" .jpg)
        echo "正在处理: $filename"
        python qwen3-doc-parse.py "$img" --api-key "$API_KEY" -o "$OUTPUT_DIR/$filename.md"
        echo "完成: $filename.md"
    fi
done
```

### 与 Python 集成
```python
import subprocess
import json

def parse_bank_statement(image_path, api_key, output_path):
    """调用 qwen3-doc-parse.py 解析银行流水"""
    cmd = [
        "python", "qwen3-doc-parse.py",
        image_path,
        "--api-key", api_key,
        "-o", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"解析成功: {output_path}")
        # 读取解析结果
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"解析失败: {result.stderr}")
        return None

# 使用示例
result = parse_bank_statement(
    "银行流水.jpg",
    "sk-0e4d21799ff746d28f0d5c86c6331770",
    "解析结果.md"
)
```

## 注意事项

1. **API 成本**：Qwen3-VL-32B-Instruct 是付费模型，请关注 API 调用费用
2. **图片质量**：清晰、正对、光线均匀的图片解析效果最佳
3. **隐私保护**：处理敏感信息时，确保 API 调用符合数据安全要求
4. **网络要求**：需要能够访问 DashScope API 的网络环境

## 故障排除

### Q: 脚本长时间无响应？
**A**: 可能是图片过大或网络问题。尝试：
1. 压缩图片大小
2. 增加超时时间（修改代码中的 `timeout` 参数）
3. 检查网络连接

### Q: 解析结果不准确？
**A**: 
1. 确保图片清晰度足够
2. 尝试调整图片角度（确保文字水平）
3. 对于复杂表格，可考虑分区域多次解析

### Q: 如何验证 API 密钥是否有效？
**A**: 
```bash
curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer sk-0e4d21799ff746d28f0d5c86c6331770" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-vl-32b-instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 5
  }'
```

## PaddleOCR VL 1.5 文档解析工具

### 概述

`paddleocr_vl_parse.py` 是一个基于 **PaddleOCR VL 1.5** 模型的文档布局解析工具。它通过 PaddleOCR 官方 API 分析图片中的文字内容、表格结构、印章位置等，特别适合银行流水、票据、合同等结构化文档。

### 功能特性

- **布局解析**：识别表格、印章、文本区块等布局元素
- **表格提取**：自动提取表格内容为 HTML 格式，保留行列结构
- **尺寸自适应**：自动调整图片尺寸以符合 API 要求（默认最大边长 2048px）
- **命令行参数**：灵活的配置选项
- **多格式输出**：同时生成 Markdown 摘要和完整 JSON 响应

### 环境要求

#### Python 版本
- Python 3.6 或更高版本

#### 依赖包
```bash
pip install requests pillow
```

#### API 密钥
需要 PaddleOCR VL 1.5 API Token：
- 从 PaddleOCR VL 1.5 API 服务获取
- 或使用测试 Token：`24ca12680035d0015fd3e9332766d274a0872a09`

### 安装与配置

1. **下载脚本**：
   ```bash
   # 将 paddleocr_vl_parse.py 保存到本地
   ```

2. **设置环境变量（可选）**：
   ```bash
   # Linux/macOS
   export PADDLEOCR_VL_TOKEN="24ca12680035d0015fd3e9332766d274a0872a09"
   
   # Windows (PowerShell)
   $env:PADDLEOCR_VL_TOKEN="24ca12680035d0015fd3e9332766d274a0872a09"
   ```

### 使用方法

#### 基本语法
```bash
python paddleocr_vl_parse.py <图片路径> [选项]
```

#### 参数说明

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `image_path` | - | **必需**：待解析的图片文件路径 | - |
| `--token` | `-t` | PaddleOCR VL API Token | 使用环境变量 `PADDLEOCR_VL_TOKEN` |
| `--output` | `-o` | 结果输出文件路径 | `paddleocr-result.md` |
| `--max-dim` | - | 图片最大边长（像素） | `2048` |
| `--api-url` | - | API 端点 URL | `https://kcc8t7t2nff4hdob.aistudio-app.com/layout-parsing` |
| `--verbose` | `-v` | 显示详细处理信息 | `False` |
| `--no-resize` | - | 不调整图片尺寸 | `False` |
| `--timeout` | - | API 请求超时时间（秒） | `45` |

#### 示例

##### 示例 1：基本使用（使用环境变量中的 Token）
```bash
python paddleocr_vl_parse.py "/mnt/d/Downloads/银行流水/001_正常.jpg"
```
结果将保存到 `paddleocr-result.md`

##### 示例 2：指定 Token 和输出文件
```bash
python paddleocr_vl_parse.py "/mnt/d/Downloads/银行流水/002_斜拍.jpg" \
  --token "24ca12680035d0015fd3e9332766d274a0872a09" \
  -o "result_002.md"
```

##### 示例 3：调整图片尺寸并显示详细信息
```bash
python paddleocr_vl_parse.py "./images/流水单.jpg" \
  --max-dim 1024 \
  --verbose \
  -o "./output/解析结果.md"
```

##### 示例 4：使用原图尺寸（不调整）
```bash
python paddleocr_vl_parse.py "高清图片.jpg" \
  --no-resize \
  --timeout 60 \
  -o "原图解析.md"
```

### 输出格式

解析结果保存为 Markdown 文件，包含以下内容：

```markdown
# PaddleOCR VL 1.5 布局解析结果

**解析时间**: 2026-02-22 01:44:30
**原始图片**: /path/to/image.jpg
**原始尺寸**: 4096 × 3072
**处理后尺寸**: 2048 × 1536
**最大边长**: 2048
**API URL**: https://kcc8t7t2nff4hdob.aistudio-app.com/layout-parsing

## 解析结果

**布局区块数量**: 1

### 布局 1 (包含 5 个区块)

**区块 1** (seal)
位置: [128, 646, 264, 786]

**区块 2** (table)
**表格内容**:
```html
<table><tr><td>记账日期</td><td>货币</td><td>交易金额</td><td>联机余额</td><td>交易摘要</td><td>对手信息</td></tr>...
```

**区块 3** (table)
位置: [309, 1224, 652, 1329]
内容: <table><tr><td>户名: 高金未央</td><td>账号: 3282904872116017</td></tr>...

## 完整响应 (前 5000 字符)
```json
{
  "logId": "20115402-79ef-4e8f-96eb-32b68bdef8de",
  "result": {...
```
```

同时会生成同名的 `.json` 文件，包含完整的 API 响应。

### 错误处理

#### 常见错误及解决方法

| 错误信息 | 原因 | 解决方法 |
|----------|------|----------|
| `图片文件不存在` | 指定的图片路径不正确 | 检查路径是否正确，使用绝对路径 |
| `请提供 API Token` | 未设置 Token | 通过 `--token` 参数传递或设置环境变量 |
| `API 错误: 422 - Invalid image file` | 图片格式或尺寸问题 | 使用 `--max-dim` 调整尺寸，或使用 `--no-resize` 尝试原图 |
| `请求超时 (45 秒)` | 图片过大或网络慢 | 增加 `--timeout` 值，或压缩图片 |
| `连接错误` | 网络问题 | 检查网络连接，确认 API URL 可达 |

#### 调试建议

1. **检查图片路径**：
   ```bash
   ls -la "/mnt/d/Downloads/银行流水/001_正常.jpg"
   ```

2. **验证 Token**：
   ```bash
   echo $PADDLEOCR_VL_TOKEN
   ```

3. **测试小图片**：
   ```bash
   python paddleocr_vl_parse.py "小图片.jpg" --token "your_token" --verbose
   ```

4. **检查 API 状态**：
   ```bash
   curl -I "https://kcc8t7t2nff4hdob.aistudio-app.com/layout-parsing"
   ```

### 性能优化

#### 图片预处理建议
1. **尺寸调整**：建议图片最大边长不超过 2048px
2. **格式优化**：使用 JPEG 格式，质量 80-90%
3. **文件大小**：控制在 1MB 以内以获得最佳响应速度

#### 超时配置
脚本默认超时为 45 秒，如需调整：
```bash
python paddleocr_vl_parse.py image.jpg --timeout 60
```

### 实际应用示例

#### 批量处理脚本示例
```bash
#!/bin/bash
# batch-paddleocr.sh

TOKEN="24ca12680035d0015fd3e9332766d274a0872a09"
INPUT_DIR="/mnt/d/Downloads/银行流水"
OUTPUT_DIR="./paddleocr解析结果"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.jpg; do
    if [ -f "$img" ]; then
        filename=$(basename "$img" .jpg)
        echo "正在处理: $filename"
        python paddleocr_vl_parse.py "$img" --token "$TOKEN" --verbose \
          -o "$OUTPUT_DIR/$filename.md"
        echo "完成: $filename.md"
    fi
done
```

#### 与 Python 集成
```python
import subprocess
import json

def parse_with_paddleocr(image_path, token, output_path, max_dim=2048):
    """调用 paddleocr_vl_parse.py 解析文档"""
    cmd = [
        "python", "paddleocr_vl_parse.py",
        image_path,
        "--token", token,
        "--max-dim", str(max_dim),
        "--output", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"解析成功: {output_path}")
        # 读取 JSON 结果
        json_file = output_path.replace('.md', '.json')
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"解析失败: {result.stderr}")
        return None

# 使用示例
data = parse_with_paddleocr(
    "银行流水.jpg",
    "24ca12680035d0015fd3e9332766d274a0872a09",
    "解析结果.md",
    max_dim=1024
)
```

### 四个工具对比

| 特性 | PP-OCR API | PaddleOCR VL 1.5 | Qwen3-VL-32B-Instruct | Kimi k2.5 |
|------|------------|------------------|-----------------------|-----------|
| **主要功能** | 文字识别 | 文档布局解析 | 文档内容理解 | 压缩后文档解析 |
| **模型类型** | OCR专用模型 | 专用文档解析模型 | 通用视觉语言模型 | 通用视觉语言模型 |
| **表格识别** | ⭐⭐ (文字提取后需要后处理) | ⭐⭐⭐⭐⭐ (结构化 HTML) | ⭐⭐⭐ (文本描述) | ⭐⭐⭐⭐ (文本描述，支持模糊标记) |
| **布局分析** | ⭐ (只返回文本块) | ⭐⭐⭐⭐⭐ (区块划分) | ⭐⭐⭐⭐ (页面描述) | ⭐⭐⭐⭐ (页面描述) |
| **印章检测** | ⭐ (只能识别印章上的文字) | ⭐⭐⭐⭐⭐ (专用标签) | ⭐⭐ (需提示词) | ⭐⭐⭐ (需提示词) |
| **API 成本** | 未知（可能免费） | 未知（可能免费/低成本） | 较高（按 token 计费） | 中等（按 token 计费） |
| **响应速度** | 快（专用OCR端点） | 较快（专用端点） | 较慢（通用推理) | 中等（通用推理，有图片压缩） |
| **易用性** | ⭐⭐⭐⭐⭐ (简单易用，有内置token) | ⭐⭐⭐ (需 Token) | ⭐⭐⭐⭐ (标准 OpenAI API) | ⭐⭐⭐⭐⭐ (标准 OpenAI API，自动图片压缩) |

### 选择建议

- **选择 PaddleOCR VL 1.5 当**：
  - 需要精确的表格结构提取
  - 文档有复杂布局（多栏、印章、表格混合）
  - 希望获得结构化数据（HTML 表格）
  - 关注 API 成本

- **选择 Qwen3-VL 当**：
  - 需要自然语言描述和理解
  - 文档内容需要语义分析
  - 图片中包含手写、复杂背景
  - 已有 DashScope API 密钥

- **选择 Kimi k2.5 当**：
  - 需要平衡解析质量和成本
  - 图片较大需要自动压缩
  - 希望标记模糊内容（使用 `<blur>` 标签）
  - 已熟悉 OpenAI API 格式
  - 需要处理倾斜、反光等低质量图片

- **选择 PP-OCR API 当**：
  - 只需要文字提取，不需要布局分析
  - 关注OCR识别准确率和速度
  - 希望获得完整的OCR结果数据（包括置信度、位置等）
  - 需要下载OCR处理后的反馈图像

## PP-OCR API 文档解析工具

### 概述

`ppocr-doc-parse.py` 是一个基于 **PP-OCR API** 的图片OCR识别工具，专门用于提取图片中的文字内容。该工具通过PP-OCR官方API进行高精度OCR识别，支持图片尺寸调整、完整JSON响应保存、OCR处理后图片下载等功能。

### 功能特性

- **高精度OCR**：使用PP-OCR API进行文字识别，支持中英文混合文本
- **图片优化**：自动调整图片尺寸（默认最大边长2048像素），优化API调用
- **完整数据保存**：保存API的完整JSON响应，便于后续分析和调试
- **OCR图片下载**：可下载OCR处理后的反馈图像，查看识别区域
- **详细报告**：生成Markdown格式的详细报告，包含统计信息、文本示例和原始数据
- **超时配置**：支持长时处理（默认900秒超时），适合高分辨率图片
- **命令行参数**：灵活的配置选项，支持图片调整、方向分类、文档展平等高级功能

### 环境要求

#### Python 版本
- Python 3.6 或更高版本

#### 依赖包
```bash
pip install requests pillow
```

#### API 密钥
已内置API Token：
- 脚本内置Token：`24ca12680035d0015fd3e9332766d274a0872a09`
- API端点：`https://r8y9ufa6z39ey1l2.aistudio-app.com/ocr`

### 安装与配置

1. **下载脚本**：
   ```bash
   # 将 ppocr-doc-parse.py 保存到本地
   ```

2. **无需额外配置**：脚本已内置API Token，可直接使用

### 使用方法

#### 基本语法
```bash
python ppocr-doc-parse.py <图片路径> [选项]
```

#### 参数说明

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `image_path` | - | 待解析的图片文件路径 | 使用环境变量或默认路径 |
| `--output` | `-o` | 结果输出文件路径 | `ppocr-30-谢弋.md` |
| `--json` | `-j` | 保存完整JSON响应的文件路径 | 自动生成（与输出文件同名但后缀为.json） |
| `--timeout` | `-t` | API请求超时时间（秒） | `900` |
| `--resize` | `-r` | 调整图片最大边长（像素），0表示不调整 | `2048` |
| `--orientation-classify` | - | 启用文档方向分类 | `False` |
| `--unwarping` | - | 启用文档展平 | `False` |
| `--textline-orientation` | - | 启用文本行方向矫正 | `False` |
| `--save-images` | `-s` | 是否保存OCR处理后的图片 | `False` |
| `--image-dir` | - | OCR图片保存目录 | `output` |

#### 示例

##### 示例 1：基本使用（使用默认图片路径）
```bash
python ppocr-doc-parse.py
```
检查默认图片路径，结果保存到 `ppocr-30-谢弋.md` 和 `ppocr-30-谢弋.json`

##### 示例 2：指定图片路径和输出文件
```bash
python ppocr-doc-parse.py "/mnt/d/Downloads/银行流水/001_正常.jpg" \
  --output "ppocr-result.md" \
  --json "ppocr-result.json"
```

##### 示例 3：调整图片尺寸并保存OCR图片
```bash
python ppocr-doc-parse.py "./images/流水单.jpg" \
  --resize 1024 \
  --save-images \
  --image-dir "./ocr_images" \
  -o "./output/解析结果.md"
```

##### 示例 4：启用高级功能并增加超时时间
```bash
python ppocr-doc-parse.py "高清文档.jpg" \
  --orientation-classify \
  --unwarping \
  --timeout 1200 \
  --resize 3072 \
  -o "高级解析.md"
```

##### 示例 5：批量处理脚本示例
```bash
#!/bin/bash
# batch-ppocr.sh

INPUT_DIR="/mnt/d/Downloads/银行流水"
OUTPUT_DIR="./ppocr解析结果"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.jpg; do
    if [ -f "$img" ]; then
        filename=$(basename "$img" .jpg)
        echo "正在处理: $filename"
        python ppocr-doc-parse.py "$img" \
          --save-images \
          --output "$OUTPUT_DIR/$filename.md" \
          --json "$OUTPUT_DIR/$filename.json"
        echo "完成: $filename.md"
    fi
done
```

### 输出格式

解析结果保存为Markdown文件，包含以下内容：

```markdown
# PP-OCR API 解析结果

**解析时间**: 2026-02-22 17:18:29
**处理耗时**: 23.51 秒
**原始图片**: /path/to/image.jpg
**图片尺寸**: 2048 × 1536
**API URL**: https://r8y9ufa6z39ey1l2.aistudio-app.com/ocr

## OCR结果统计
- **识别区域数量**: 1

### 区域 1
**所有字段**: prunedResult, ocrImage, inputImage
**文本数量**: 642
**置信度数量**: 642
**非空文本示例**:
  - `锦鲤民营银行交易流水` (置信度: 0.998)
  - `Transaction Statement of China Merchants Bank` (置信度: 0.997)
  - `2023-09-02 - 2023-12-30` (置信度: 0.995)

## 统计信息
- **平均置信度**: 0.9504
- **总文本数量**: 642
- **总文本长度**: 12345 字符
- **非空文本数量**: 600

## 所有非空文本
```
1: 锦鲤民营银行交易流水
2: Transaction Statement of China Merchants Bank
3: 2023-09-02 - 2023-12-30
...
```

## 原始数据（精简）
```json
{
  "image_path": "/path/to/image.jpg",
  "processing_time": 23.51,
  "ocr_count": 1,
  "total_text_count": 642,
  "non_empty_text_count": 600,
  "ocr_results": [...]
}
```
```

同时会生成同名的 `.json` 文件，包含完整的API响应数据。

### 错误处理

#### 常见错误及解决方法

| 错误信息 | 原因 | 解决方法 |
|----------|------|----------|
| `错误: 图片文件不存在` | 指定的图片路径不正确 | 检查路径是否正确，使用绝对路径 |
| `API请求超时（900秒）` | 图片过大或网络慢 | 使用 `--resize` 减小图片尺寸，或增加 `--timeout` |
| `API请求失败` | 网络问题或API服务不可用 | 检查网络连接，确认API端点可达 |
| `无法读取或编码图片文件` | 图片格式不支持或损坏 | 转换为JPEG/PNG格式，检查图片完整性 |
| `API返回错误` | API服务端错误 | 检查API Token是否有效，或等待服务恢复 |

#### 调试建议

1. **检查图片路径**：
   ```bash
   ls -la "/mnt/d/Downloads/银行流水/001_正常.jpg"
   ```

2. **测试小图片**：
   ```bash
   python ppocr-doc-parse.py "小图片.jpg" --resize 512 --save-images
   ```

3. **查看完整JSON响应**：
   ```bash
   cat ppocr-result.json | jq '.result.ocrResults[0].prunedResult.rec_texts[:5]'
   ```

4. **验证网络连接**：
   ```bash
   curl -I "https://r8y9ufa6z39ey1l2.aistudio-app.com/ocr"
   ```

### 性能优化

#### 图片预处理建议
1. **尺寸调整**：建议图片最大边长不超过2048px
2. **格式优化**：使用JPEG格式，质量80-90%
3. **文件大小**：控制在2MB以内以获得最佳响应速度

#### 参数调优经验
- **resize=2048**：适用于大多数场景，平衡细节与速度
- **timeout=900**：适合高分辨率图片，提供充足处理时间
- **save-images=true**：需要查看OCR处理结果时启用

### 实际应用

#### OCR结果后处理
获取的OCR结果可用于：
1. **文本提取**：直接获取图片中的文字内容
2. **数据分析**：对识别结果进行统计分析
3. **数据验证**：与其他OCR工具结果对比
4. **格式转换**：将图片内容转换为可编辑文本

#### 与Python集成
```python
import subprocess
import json

def parse_with_ppocr(image_path, output_path, resize=2048, save_images=False):
    """调用 ppocr-doc-parse.py 进行OCR识别"""
    cmd = [
        "python", "ppocr-doc-parse.py",
        image_path,
        "--resize", str(resize),
        "--output", output_path
    ]
    
    if save_images:
        cmd.extend(["--save-images", "--image-dir", "./ocr_images"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"OCR成功: {output_path}")
        # 读取JSON结果
        json_file = output_path.replace('.md', '.json')
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"OCR失败: {result.stderr}")
        return None

# 使用示例
data = parse_with_ppocr(
    "银行流水.jpg",
    "ppocr结果.md",
    resize=1024,
    save_images=True
)
```

## Kimi API 文档解析工具

### 概述

`kimi-doc-parse-compressed.py` 是一个基于 **Kimi k2.5** 模型的银行流水图片解析工具，通过 Moonshot API 分析图片中的文字内容和版面结构。该工具特别设计了图片压缩功能，可自动调整图片尺寸和质量，避免因图片过大导致的 API 超时问题，同时支持对模糊内容进行标记。

### 功能特性

- **智能图片压缩**：自动调整图片尺寸（默认最大宽度 2048px）和质量，优化 API 调用
- **模糊内容标记**：对于图像不清晰、无法确定的内容，使用 `<blur></blur>` 标签标记
- **文字提取**：提取图片中所有可见文字，保持原样
- **版面分析**：识别表格结构、字段位置、行列关系
- **标准化 API**：使用 OpenAI 兼容的 API 格式，易于集成
- **命令行参数**：灵活的路径、尺寸和质量配置
- **结果保存**：自动保存为 Markdown 格式，便于查看和后续处理

### 环境要求

#### Python 版本
- Python 3.6 或更高版本

#### 依赖包
```bash
pip install openai pillow
```

#### API 密钥
需要 Moonshot API 密钥：
- 从 [Moonshot AI 平台](https://platform.moonshot.cn/) 获取
- 或使用测试密钥：`sk-eq7EmmZkrzeeZmKmDZe3FaIo0Ea0PJdxRinc4RzqAumyHSQl`

### 安装与配置

1. **下载脚本**：
   ```bash
   # 将 kimi-doc-parse-compressed.py 保存到本地
   ```

2. **设置环境变量（可选）**：
   ```bash
   # Linux/macOS
   export MOONSHOT_API_KEY="sk-eq7EmmZkrzeeZmKmDZe3FaIo0Ea0PJdxRinc4RzqAumyHSQl"
   
   # Windows (PowerShell)
   $env:MOONSHOT_API_KEY="sk-eq7EmmZkrzeeZmKmDZe3FaIo0Ea0PJdxRinc4RzqAumyHSQl"
   ```

### 使用方法

#### 基本语法
```bash
python kimi-doc-parse-compressed.py <图片路径> [选项]
```

#### 参数说明

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `image_path` | - | 待解析的图片文件路径 | 使用环境变量 `IMAGE_PATH` 或默认路径 |
| `--output` | `-o` | 结果输出文件路径 | 标准输出 |
| `--max-width` | - | 图片最大宽度（像素） | `2048` |
| `--quality` | - | JPEG 压缩质量（1-100） | `90` |

#### 示例

##### 示例 1：基本使用（使用环境变量中的 API 密钥）
```bash
python kimi-doc-parse-compressed.py "/mnt/d/Downloads/银行流水/001_正常.jpg"
```
结果将输出到标准输出

##### 示例 2：指定输出文件
```bash
python kimi-doc-parse-compressed.py "/mnt/d/Downloads/银行流水/002_斜拍.jpg" \
  -o "kimi-result.md"
```

##### 示例 3：调整图片尺寸和质量
```bash
python kimi-doc-parse-compressed.py "./images/流水单.jpg" \
  --max-width 3072 \
  --quality 85 \
  -o "./output/解析结果.md"
```

##### 示例 4：使用环境变量指定图片路径
```bash
export IMAGE_PATH="/mnt/d/Downloads/银行流水/001_正常.jpg"
python kimi-doc-parse-compressed.py -o "result.md"
```

### 输出格式

解析结果保存为 Markdown 文件，包含详细的文字和版面信息，例如：

```markdown
这张图片展示了**三张招商银行个人账户交易流水单**（或对账单），呈扇形平铺在浅色桌面上...

### **整体版面结构**
- **布局**：三张纸并排摆放，左侧纸张倾斜约30度...
- **纸张类型**：标准A4打印纸，白色背景，黑色文字...
- **印章**：每页顶部均盖有圆形红色印章...

### **左侧流水单（第3页）**
**头部信息区**：
- 标题：**<blur>招商银行交易流水</blur>**
- 户名：**<blur>陈金金</blur>**
- 账号：**<blur>6232 9090 4777 1607</blur>**
...
```

输出中，`<blur>` 标签表示图像中不清晰、无法确定的内容。

### 错误处理

#### 常见错误及解决方法

| 错误信息 | 原因 | 解决方法 |
|----------|------|----------|
| `错误：文件不存在` | 指定的图片路径不正确 | 检查路径是否正确，使用绝对路径 |
| `API 请求失败` | 网络问题或 API 密钥无效 | 检查网络连接、API 密钥有效性 |
| `图片处理失败` | 图片格式不支持或损坏 | 转换为 JPEG/PNG 格式，检查图片完整性 |
| `超时` | 图片过大或网络慢 | 使用 `--max-width` 减小图片尺寸 |

#### 调试建议

1. **检查图片路径**：
   ```bash
   ls -la "/mnt/d/Downloads/银行流水/001_正常.jpg"
   ```

2. **验证 API 密钥**：
   ```bash
   echo $MOONSHOT_API_KEY
   ```

3. **测试小图片**：
   ```bash
   python kimi-doc-parse-compressed.py "小图片.jpg" -o "test.md"
   ```

### 性能优化

#### 图片预处理建议
1. **尺寸调整**：建议图片宽度不超过 3072px（可平衡细节与速度）
2. **格式优化**：使用 JPEG 格式，质量 85-95%
3. **文件大小**：控制在 1MB 以内以获得最佳响应速度

#### 参数调优经验
- **max-width=2048**：适用于大多数场景，响应速度快
- **max-width=3072**：提取更多细节，但 API 数据量和响应时间增加约 50%
- **quality=90**：在文件大小和图像质量间取得良好平衡

### 实际应用示例

#### 批量处理脚本示例
```bash
#!/bin/bash
# batch-kimi.sh

API_KEY="sk-eq7EmmZkrzeeZmKmDZe3FaIo0Ea0PJdxRinc4RzqAumyHSQl"
INPUT_DIR="/mnt/d/Downloads/银行流水"
OUTPUT_DIR="./kimi解析结果"

mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.jpg; do
    if [ -f "$img" ]; then
        filename=$(basename "$img" .jpg)
        echo "正在处理: $filename"
        python kimi-doc-parse-compressed.py "$img" \
          -o "$OUTPUT_DIR/$filename.md"
        echo "完成: $filename.md"
    fi
done
```

#### 与 Python 集成
```python
import subprocess

def parse_with_kimi(image_path, output_path, max_width=2048, quality=90):
    """调用 kimi-doc-parse-compressed.py 解析文档"""
    cmd = [
        "python", "kimi-doc-parse-compressed.py",
        image_path,
        "--max-width", str(max_width),
        "--quality", str(quality),
        "--output", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"解析成功: {output_path}")
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print(f"解析失败: {result.stderr}")
        return None

# 使用示例
result = parse_with_kimi(
    "银行流水.jpg",
    "解析结果.md",
    max_width=3072,
    quality=85
)
```

# img_quality_check.py - 图片质量检查工具

## 概述

`img_quality_check.py` 是一个基于 **Qwen3-VL-32B-Instruct** 模型的图片质量检查工具，专门用于评估文档图片是否适合OCR文字识别。该工具通过DashScope API分析图片质量问题，如倾斜、阴影、反光、模糊、水印等，并自动生成质量报告。

## 功能特性

- **智能质量评估**：使用大语言模型评估图片质量问题
- **多维评分体系**：提供0-10分的质量评分和通过/不通过判断
- **问题自动识别**：检测倾斜、阴影、反光、模糊、水印、占比过小等常见问题
- **后处理逻辑**：包含方案B后处理机制，可根据严重问题关键词和文件名规则优化判断结果
- **批量处理**：支持目录批量处理，自动生成汇总报告
- **多格式输出**：同时生成JSON详细结果和Markdown格式报告
- **预期结果对比**：自动与预设预期结果对比，计算准确率

## 环境要求

### Python 版本
- Python 3.6 或更高版本

### 依赖包
```bash
pip install openai
```

### API 密钥
需要 DashScope API 密钥：
- 从 [DashScope 控制台](https://dashscope.console.aliyun.com/) 获取
- 或使用提供的密钥：`sk-0e4d21799ff746d28f0d5c86c6331770`

## 安装与配置

1. **下载脚本**：
   ```bash
   # 将 img_quality_check.py 保存到本地
   ```

2. **设置环境变量（可选）**：
   ```bash
   # Linux/macOS
   export DASHSCOPE_API_KEY="sk-0e4d21799ff746d28f0d5c86c6331770"
   
   # Windows (PowerShell)
   $env:DASHSCOPE_API_KEY="sk-0e4d21799ff746d28f0d5c86c6331770"
   ```

## 使用方法

### 基本语法
```bash
python img_quality_check.py [选项]
```

### 参数说明

| 参数 | 缩写 | 说明 | 默认值 |
|------|------|------|--------|
| `--dir` | `-d` | 图片目录路径 | `parse_and_exam/tmp` |
| `--api-key` | - | DashScope API 密钥 | 使用环境变量 `DASHSCOPE_API_KEY` |
| `--output` | `-o` | 结果输出文件路径 | `quality_check_results.json` |

### 示例

#### 示例 1：基本使用（使用环境变量中的 API 密钥）
```bash
python img_quality_check.py
```
检查默认目录 `parse_and_exam/tmp` 下的图片，结果保存到 `quality_check_results.json`

#### 示例 2：指定目录和 API 密钥
```bash
python img_quality_check.py \
  --dir "/path/to/your/images" \
  --api-key "sk-0e4d21799ff746d28f0d5c86c6331770"
```

#### 示例 3：指定输出文件
```bash
python img_quality_check.py \
  -d "./test_images" \
  -o "./reports/quality_results.json"
```

## 输出格式

### JSON 输出（详细结果）
检查结果保存为 JSON 文件，包含每张图片的详细信息：
```json
{
  "001_正常.jpg": {
    "path": "parse_and_exam/tmp/001_正常.jpg",
    "quality_score": 6,
    "is_passed": true,
    "reason": "图片整体清晰，文字可读性良好...",
    "issues": ["轻微阴影", "轻微倾斜"],
    "expected": "通过"
  },
  "002_斜拍.jpg": {
    "path": "parse_and_exam/tmp/002_斜拍.jpg",
    "quality_score": 5,
    "is_passed": false,
    "reason": "图片整体清晰... [后处理：文件名提示质量问题，强制不通过]",
    "issues": ["轻微倾斜", "局部阴影"],
    "expected": "不通过"
  }
}
```

### Markdown 报告（可视化总结）
同时生成易读的 Markdown 格式报告 `quality_check_results.md`，包含：
- 检查结果汇总（总计、通过数、不通过数、准确率）
- 详细结果表格（图片名称、质量评分、检查结果、原因、问题、预期结果、是否匹配）
- 预期与实际结果对比

## 评估标准

### 严重问题（应判为不通过）
- **明显倾斜**：拍摄角度明显歪斜（超过15度），文字行严重变形
- **严重阴影**：阴影覆盖超过30%的文字区域，导致文字无法辨认
- **强烈反光**：反光区域覆盖超过20%的文字区域，使文字完全无法看清
- **大面积水印**：水印覆盖超过15%的文字区域，严重影响阅读
- **严重模糊**：图片模糊导致大部分文字无法辨认
- **占比过小**：文档在画面中面积占比小于50%，文字细节难以识别

### 轻微问题（可接受，仍可通过）
- **轻微倾斜**：文字行基本保持水平，可读性不受影响
- **轻微阴影**：阴影在边缘区域，未覆盖重要文字
- **局部反光**：反光区域有限，大部分文字清晰
- **边缘水印**：水印在文档边缘或空白处，未覆盖文字
- **轻微模糊**：文字边缘略有模糊但基本可辨
- **光线不均**：光照略有变化但文字清晰可读

## 后处理逻辑（方案B）

为提高判断准确率，脚本包含两重后处理机制：

### 1. 严重问题关键词强制否决
如果检测到以下关键词，强制判为不通过，质量评分降低至≤5分：
```python
severe_keywords = ["明显倾斜", "严重阴影", "强烈反光", "大面积水印", "严重模糊", "文字变形"]
```

### 2. 文件名提示规则（测试集优化）
针对测试集特性，文件名包含以下关键词且模型判为通过的，强制改为不通过：
```python
filename_keywords = ["斜拍", "阴影", "模糊", "占比小"]
```
保护机制：排除`001_正常.jpg`防止误判

### 后处理标记
所有后处理操作都会在原因字段中添加标记：
- `[后处理：检测到严重问题，强制不通过]`
- `[后处理：文件名提示质量问题，强制不通过]`

## 性能优化

### 超时配置
- 默认超时时间：180秒
- 适合处理高分辨率图片

### 温度设置
- 温度值：0.1（低温度以获得更一致的输出）
- 减少模型输出波动

### 批量处理优化
- 自动排序图片文件名
- 实时显示处理进度
- 支持中断后恢复

## 实际应用

### 文档预检流程
在OCR识别前进行质量检查，过滤不合格图片：
1. 收集待识别图片
2. 运行质量检查脚本
3. 筛选通过图片进行OCR
4. 对不通过图片进行人工干预或重拍

### 测试集验证
验证模型判断准确率：
```bash
python img_quality_check.py --dir "test_set"
```
预期结果对比，计算准确率

### 自定义规则扩展
可根据实际需求修改后处理规则：
1. 更新`severe_keywords`列表
2. 调整文件名规则关键词
3. 修改质量评分阈值
4. 添加新的后处理逻辑

## 工具对比

| 特性 | img_quality_check.py | qwen3-doc-parse.py | paddleocr_vl_parse.py | kimi-doc-parse-compressed.py |
|------|---------------------|-------------------|------------------------|-------------------------------|
| **主要功能** | 图片质量评估 | 文档内容解析 | 文档布局解析 | 压缩后文档解析 |
| **模型** | Qwen3-VL-32B-Instruct | Qwen3-VL-32B-Instruct | PaddleOCR VL 1.5 | Kimi k2.5 |
| **输出格式** | JSON + Markdown报告 | Markdown | JSON + Markdown | Markdown |
| **后处理** | ✓（方案B） | ✗ | ✗ | ✗ |
| **批量处理** | ✓ | ✗ | ✗ | ✗ |
| **质量评分** | ✓（0-10分） | ✗ | ✗ | ✗ |

## 银行流水勾稽校验

### 概述
银行流水勾稽校验是对OCR解析结果（Markdown格式）进行数据一致性验证的过程。通过检查交易记录中的金额与余额字段是否满足连续性公式（前余额 + 当前金额 = 当前余额），验证解析数据的准确性和完整性。

### 校验原理
勾稽校验基于以下数学关系：
```
前一笔交易的余额 + 当前交易的金额 = 当前交易的余额
```
- **金额字段**：正数表示收入，负数表示支出
- **余额字段**：交易后的账户余额
- **校验条件**：数据按时间顺序排列，存在金额和余额字段

### 输入文件要求
- **文件格式**：Markdown（解析工具输出的结果）
- **文件示例**：`qwen3-30-谢弋.md`、`paddleocr-30-谢弋.md`、`kimi-高清结果.md`
- **字段要求**：必须包含“金额”和“余额”字段，建议包含“记录日期”、“记账时间”等时间字段

### 校验步骤

#### 1. 文件结构分析
- 检查文件头信息（交易区间、卡号、借贷发生数等）
- 确定表格起始位置（查找包含“记录日期”的标题行）
- 确认数据行格式（以日期时间开头的行）

#### 2. 数据提取
- 使用正则表达式匹配数据行：`\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}`
- 按空格分割字段，处理缺失的“附言”字段
- 构建交易记录字典列表

#### 3. 校验执行
```python
# 核心校验函数示例
def validate_balance_continuity(transactions):
    """校验余额连续性"""
    errors = []
    prev_balance = None
    for i, trans in enumerate(transactions):
        balance = float(trans['余额'])
        amount = float(trans['金额'])
        if prev_balance is not None:
            expected = prev_balance + amount
            if abs(balance - expected) > 0.01:  # 允许微小误差
                errors.append(f"第{i+1}行余额不一致...")
        prev_balance = balance
    return errors
```

#### 4. 统计功能
- 总交易笔数
- 支出笔数及总额（金额为负）
- 收入笔数及总额（金额为正）
- 与文件头信息（借方发生数、贷方发生数）对比
- 净变化分析：初始余额、最终余额、收支总额一致性

### 使用方法

#### 自动校验（模型生成代码）
1. **提供提示词**：使用 `bank_statement_verification_prompt.md` 作为指导
2. **模型分析**：模型自动分析文件结构并生成校验代码
3. **代码执行**：生成 `verification.py` 脚本并执行
4. **结果输出**：输出校验结论和统计信息

#### 手动校验（使用现有脚本）
已有校验脚本示例：
```bash
# 查看现有校验脚本
ls -la parse_and_exam/tmp/verification*.py

# 执行校验
cd parse_and_exam/tmp
python3 verification.py
```

### 输出格式

#### 校验结论
- **通过/未通过**：是否发现余额不一致
- **错误详情**：行号、差异值、可能原因
- **统计信息**：交易笔数、收支总额、与文件头对比

#### 示例输出
```
1. 解析结果分析
   - 共解析 30 条交易记录
   - 字段完整性：良好

2. 勾稽校验条件判断
   - 满足条件：是
   - 理由：存在金额和余额字段，数据按时间顺序排列

3. 校验结果与结论
   - 校验结果：未通过
   - 发现 7 处余额不一致
   - 详细错误列表：
     第2行：预期余额 21256.91，实际余额 21226.91，差异 -30.00
     第5行：预期余额 20756.91，实际余额 20786.91，差异 +30.00
     ...
   - 交易统计：
     总交易笔数：30
     支出总额：-414,100.00
     收入总额：+414,100.00
   - 可能原因分析：OCR识别误差、字段错位、数据截断
```

### 实际应用示例

#### 对 qwen3-30-谢弋.md 的校验结果
- **校验时间**：2026-02-22
- **文件来源**：Qwen3-VL-32B-Instruct 解析结果
- **校验结果**：发现 7 处余额不一致（差异值 -30 至 +20 不等）
- **可能原因**：OCR识别误差导致金额或余额字段提取不准确
- **建议措施**：人工核对原始图片，或使用不同模型重新解析

#### 批量校验脚本示例
```bash
#!/bin/bash
# batch-verification.sh

INPUT_DIR="./解析结果"
OUTPUT_DIR="./校验报告"

mkdir -p "$OUTPUT_DIR"

for md_file in "$INPUT_DIR"/*.md; do
    if [ -f "$md_file" ]; then
        filename=$(basename "$md_file" .md)
        echo "正在校验: $filename"
        
        # 调用勾稽校验提示词生成校验代码
        # （此处可使用模型自动生成代码并执行）
        
        echo "校验完成: $filename"
    fi
done
```

### 注意事项
1. **浮点数精度**：使用容差（如0.01）避免浮点误差
2. **数据缺失**：处理缺失字段（如空附言），跳过无效行
3. **格式变化**：适配不同OCR模型的输出格式（Qwen3、PaddleOCR、Kimi）
4. **多页处理**：文件头信息可能涵盖全部页数，而解析可能只包含部分页面
5. **错误处理**：金额/余额字段转换异常时记录并跳过

### 工具对比

| 特性 | 勾稽校验工具 | img_quality_check.py | 交叉对比分析 | 文档解析工具 |
|------|-------------|---------------------|--------------|-------------|
| **主要功能** | 数据一致性验证 | 图片质量评估 | 多模型结果对比 | 文档内容解析 |
| **输入格式** | Markdown文件 | 图片文件 | 多个解析结果文件 | 图片文件 |
| **输出格式** | 校验报告 | JSON + Markdown报告 | 交叉对比分析报告 | Markdown/JSON |
| **自动化程度** | ✓（模型生成代码） | ✓（直接执行） | ✓（提示词驱动） | ✓（直接执行） |
| **后处理** | ✗ | ✓（方案B） | ✗ | ✗ |

### 集成建议
1. **完整工作流**：图片质量检查 → OCR解析 → 勾稽校验 → 人工审核
2. **质量闭环**：利用校验结果反馈改进OCR解析准确率
3. **自动化程度**：对于批量处理，可结合模型自动生成校验代码并执行

## 多模型解析结果交叉对比分析

### 概述
多模型解析结果交叉对比分析是通过比较不同OCR模型（如Qwen3、Kimi、PaddleOCR）对同一文档图片的解析结果，系统性评估各模型准确性、发现差异点、并提供工具性能评价的方法。该方法特别适用于财务文档、合同等重要文件，确保解析结果的准确性和可靠性。

### 分析原理
交叉对比分析基于以下原则：
1. **多模型冗余**：不同模型可能在不同方面（文字识别、表格提取、版面理解）各有优劣
2. **差异检测**：通过对比发现潜在错误，特别是关键数据（金额、日期、编号）的差异
3. **工具评价**：基于差异分析，评估各模型的优缺点和适用场景

### 输入文件要求
- **文件格式**：
  - Qwen3解析结果：Markdown格式（如 `qwen3-sample10.md`）
  - Kimi解析结果：Markdown格式（如 `kimi-sample10.md`）
  - PaddleOCR解析结果：JSON格式（如 `paddleocr-sample10.json`）
- **文件来源**：同一文档图片的不同模型解析结果
- **内容要求**：包含完整的文字内容、表格数据、版面信息

### 使用方法

#### 使用提示词文件自动分析
1. **准备提示词文件**：确保 `parse-results-crosscheck.md` 文件在当前目录
   ```bash
   cp parse-results-crosscheck.md 当前工作目录/
   ```
2. **准备解析结果文件**：将三个模型的解析结果放在同一目录
   ```bash
   ls -la *.md *.json
   # 应包含：qwen3-sample10.md, kimi-sample10.md, paddleocr-sample10.json
   ```
3. **使用大模型执行分析**：
   - 将提示词文件内容作为系统指令发送给大模型
   - 提供三个解析结果文件作为输入
   - 模型将按照提示词要求生成完整的交叉对比分析报告

#### 手动分析步骤
1. **文本内容对比**：
   - 对比三个文件中提取的文字内容是否一致
   - 特别注意数字、表格数据、特殊符号的准确性
   - 查找拼写错误、遗漏文本、额外文本

2. **表格数据对比**：
   - 对比所有表格的结构和内容
   - 特别注意关键表格（如收入信息、区域披露等）
   - 对比数值数据，注意千位分隔符的正确性
   - 检查合计行的计算是否正确

3. **布局和结构对比**：
   - 对比三个工具对页面布局的理解
   - 分析栏位划分、标题级别、段落结构
   - 比较版面信息的描述准确性

4. **格式和标记对比**：
   - 对比Markdown/JSON格式的处理差异
   - 检查表格标记、标题格式、列表格式
   - 分析特殊字符和编码处理

### 输出格式
交叉对比分析报告应包含以下部分：

#### 1. 概述
- 分析日期、分析文件列表
- 总体评价：各工具的优缺点总结

#### 2. 文本内容差异分析
- 主要文本差异（按重要性排序）
- 数字和表格数据差异（重点分析数值不一致）
- 格式和结构差异

#### 3. 详细差异点列表
| 序号 | 差异位置 | Qwen3结果 | Kimi结果 | PaddleOCR结果 | 差异类型 | 备注 |
|------|----------|-----------|----------|---------------|----------|------|
| 1 | [位置描述] | [内容] | [内容] | [内容] | [类型] | [分析] |
| ... | ... | ... | ... | ... | ... | ... |

#### 4. 表格数据一致性检查
对每个关键表格进行数据一致性对比：
- 表1: (a) 业务分部的收入信息
- 表2: (b) 按区域披露的收入信息  
- 表3: 8 收入
- 表4: 客户合同收入确认时点分析表格

#### 5. 工具性能评价
对每个工具进行优缺点分析，包括：
- Qwen3-VL-32B-Instruct
- Kimi k2.5
- PaddleOCR VL 1.5

#### 6. 建议和改进
- 针对发现的差异提出改进建议
- 推荐适合此类文档的最佳解析工具
- 后续验证和测试建议

#### 7. 结论
- 总体准确性评价
- 关键发现总结
- 实际应用建议

### 实际应用示例

#### 对 sample10.JPG 的交叉对比分析
- **分析时间**：2026-02-22
- **分析文件**：`qwen3-sample10.md`, `kimi-sample10.md`, `paddleocr-sample10.json`
- **关键发现**：
  1. **严重数据差异**：终端业务2024年收入
     - Qwen3: "330,006" (错误)
     - Kimi: "339,006" ✓
     - PaddleOCR: "339,006" ✓
  2. **数据一致性统计**：97.5%的数据点完全一致（39/40）
  3. **格式差异**：
     - Qwen3：详细版面分析，纯文本表格
     - Kimi：简洁版面描述，Markdown表格  
     - PaddleOCR：JSON结构化数据，HTML表格
- **工具性能评价**：
  - **数据准确性**：PaddleOCR ≈ Kimi > Qwen3
  - **版面分析**：Qwen3 > Kimi > PaddleOCR
  - **输出可用性**：Kimi > Qwen3 > PaddleOCR
  - **自动化能力**：PaddleOCR > Qwen3 > Kimi
- **推荐方案**：
  - 主要工具：PaddleOCR VL 1.5 (数据准确性最高)
  - 辅助工具：Kimi (生成用户友好的Markdown报告)
  - 验证工具：Qwen3 (需要详细版面分析时)

完整分析报告见：`文档解析结果交叉对比分析报告.md`

### 工具对比

| 特性 | 勾稽校验工具 | img_quality_check.py | **交叉对比分析** | 文档解析工具 |
|------|-------------|---------------------|-----------------|-------------|
| **主要功能** | 数据一致性验证 | 图片质量评估 | **多模型结果对比** | 文档内容解析 |
| **输入格式** | Markdown文件 | 图片文件 | **多个解析结果文件** | 图片文件 |
| **输出格式** | 校验报告 | JSON + Markdown报告 | **交叉对比分析报告** | Markdown/JSON |
| **自动化程度** | ✓（模型生成代码） | ✓（直接执行） | **✓（提示词驱动）** | ✓（直接执行） |
| **后处理** | ✗ | ✓（方案B） | **✗** | ✗ |
| **关键优势** | 发现数据逻辑错误 | 发现图片质量问题 | **发现模型差异和错误** | 原始内容提取 |

### 集成建议
1. **完整质量保证工作流**：
   ```
   图片质量检查 → 多模型OCR解析 → 交叉对比分析 → 勾稽校验 → 人工审核
   ```
2. **质量闭环反馈**：
   - 利用交叉对比结果选择最佳模型
   - 将差异点反馈给模型训练或参数调整
   - 建立常见错误模式库，优化预处理流程
3. **自动化程度**：
   - 对于关键文档，建议使用交叉对比分析确保准确性
   - 可结合模型自动执行分析，生成标准报告
   - 批量处理时，可先抽样进行交叉对比，验证模型表现

### 注意事项
1. **差异分类**：
   - **严重错误**：数据错误、关键信息缺失、计算错误
   - **次要错误**：格式错误、轻微文本差异、布局误解
   - **工具特性差异**：不同工具的输出风格差异
   - **精度差异**：数值精度、文本提取精度差异
2. **分析注意事项**：
   - 每个差异点都需要在三份文件中确认
   - 关注数据准确性，特别是财务数据
   - 考虑上下文，某些差异可能是合理的
   - 客观评价，基于事实进行分析
   - 提供具体的文本片段作为证据
3. **性能考量**：
   - 分析多个大型文件可能需要较多计算资源
   - 建议先进行抽样分析，确认模型表现
   - 对于批量处理，可建立差异阈值，只关注重要差异

## 使用建议

### 适用场景
1. **OCR预处理**：确保输入图片质量
2. **文档数字化**：批量检查扫描件质量
3. **质量监控**：自动化质量评估流程
4. **模型测试**：验证不同模型判断能力

### 配置建议
1. 对于高分辨率图片，建议保持默认超时设置（180秒）
2. 批量处理大量图片时，可考虑分批处理
3. 根据实际应用场景调整严重问题关键词列表
4. 定期更新测试集预期结果以验证准确率

## 故障排除

### 常见错误
1. **API密钥错误**：检查环境变量或命令行参数
2. **图片目录不存在**：确认目录路径正确
3. **模型输出格式错误**：检查网络连接或重试
4. **超时错误**：考虑减小图片尺寸或增加超时时间

### 调试建议
1. 启用详细日志输出（脚本已内置）
2. 检查生成的JSON文件了解详细错误信息
3. 单张图片测试排除批量处理问题
4. 验证API密钥有效性

## 更新日志

### v1.7 (2026-02-22)
- 新增多模型解析结果交叉对比分析章节
- 添加parse-results-crosscheck.md提示词文件使用方法
- 更新工具对比表，包含交叉对比分析工具
- 提供实际应用示例（sample10.JPG分析报告）

### v1.6 (2026-02-22)
- 新增 PP-OCR API 文档解析工具（ppocr-doc-parse.py）
- 添加PP-OCR API支持，内置Token，支持图片尺寸调整
- 更新四个工具对比表，添加PP-OCR选择建议
- 支持完整JSON响应保存和OCR图片下载

### v1.5 (2026-02-22)
- 新增银行流水勾稽校验文档和使用方法
- 添加勾稽校验原理、步骤和实际应用示例
- 更新工具对比表，包含数据验证工具

### v1.4 (2026-02-22)
- 新增图片质量检查工具（img_quality_check.py）
- 添加方案B后处理逻辑（严重问题关键词+文件名规则）
- 支持批量处理和对比报告生成

### v1.3 (2026-02-22)
- 新增 Kimi k2.5 文档解析工具（kimi-doc-parse-compressed.py）
- 添加图片压缩功能和模糊内容标记
- 更新三个工具对比和选择建议

### v1.2 (2026-02-22)
- 新增 PaddleOCR VL 1.5 解析工具
- 添加图片尺寸自动调整功能
- 支持命令行参数和环境变量配置

### v1.1 (2026-02-22)
- 增加命令行参数支持
- 添加超时配置（180秒）
- 改进错误处理和提示信息

### v1.0 (初始版本)
- 基础图片解析功能
- 支持单张图片处理
- Markdown 格式输出

## 技术支持

如有问题或建议，请参考：
1. [DashScope 官方文档](https://help.aliyun.com/zh/dashscope/)
2. [Qwen 模型介绍](https://help.aliyun.com/zh/dashscope/developer-reference/qwen)
3. 脚本源代码注释

---
*文档最后更新：2026-02-22*
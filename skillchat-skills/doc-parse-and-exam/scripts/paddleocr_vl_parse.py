#!/usr/bin/env python3
"""
PaddleOCR VL 1.5 文档解析工具
基于 PaddleOCR VL 1.5 布局解析 API，支持银行流水、表格、印章等识别
"""

import base64
import os
import sys
import argparse
import requests
import time
import io
import json
from PIL import Image

# 默认配置
DEFAULT_API_URL = "https://kcc8t7t2nff4hdob.aistudio-app.com/layout-parsing"
DEFAULT_MAX_DIMENSION = 2048
DEFAULT_OUTPUT = "paddleocr-result.md"
ENV_TOKEN = "PADDLEOCR_VL_TOKEN"

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="PaddleOCR VL 1.5 文档解析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""示例:
  %(prog)s /path/to/image.jpg
  %(prog)s /path/to/image.jpg --token YOUR_TOKEN --output result.md
  %(prog)s /path/to/image.jpg --max-dim 1024 --verbose
  %(prog)s /path/to/image.jpg --api-url {DEFAULT_API_URL}

环境变量:
  {ENV_TOKEN}: 可替代 --token 参数
"""
    )
    
    parser.add_argument(
        "image_path",
        help="待解析的图片文件路径"
    )
    
    parser.add_argument(
        "--token", "-t",
        help=f"PaddleOCR VL API Token（可从 {DEFAULT_API_URL} 获取）。"
             f"如未提供，将使用环境变量 {ENV_TOKEN}"
    )
    
    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT,
        help=f"结果输出文件路径（默认：{DEFAULT_OUTPUT}）"
    )
    
    parser.add_argument(
        "--max-dim",
        type=int,
        default=DEFAULT_MAX_DIMENSION,
        help=f"图片最大边长（像素），超过将自动缩放（默认：{DEFAULT_MAX_DIMENSION}）"
    )
    
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"API 端点 URL（默认：{DEFAULT_API_URL}）"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细处理信息"
    )
    
    parser.add_argument(
        "--no-resize",
        action="store_true",
        help="不调整图片尺寸（使用原图，可能因尺寸过大失败）"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=45,
        help="API 请求超时时间（秒，默认：45）"
    )
    
    return parser.parse_args()

def check_file(image_path):
    """检查图片文件是否存在且可读"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            f.read(100)  # 测试读取
    except Exception as e:
        raise IOError(f"无法读取图片文件: {e}")

def resize_image_if_needed(image_path, max_dimension, no_resize=False, verbose=False):
    """
    加载图片并按需调整尺寸
    
    返回: (base64编码字符串, 原始尺寸, 调整后尺寸)
    """
    try:
        img = Image.open(image_path)
        orig_size = img.size
        orig_mode = img.mode
        
        if verbose:
            print(f"原始图片: {orig_size[0]} × {orig_size[1]}, 模式: {orig_mode}")
        
        # 检查是否需要调整尺寸
        width, height = orig_size
        if no_resize or (width <= max_dimension and height <= max_dimension):
            if verbose:
                print("保持原尺寸")
            new_size = orig_size
        else:
            # 计算调整后的尺寸，保持宽高比
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            
            new_size = (new_width, new_height)
            if verbose:
                print(f"调整尺寸: {new_size[0]} × {new_size[1]}")
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # 确保 RGB 模式
        if img.mode != 'RGB':
            if verbose:
                print(f"转换模式: {img.mode} → RGB")
            img = img.convert('RGB')
        
        # 保存到内存
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=90)
        buffer.seek(0)
        file_bytes = buffer.read()
        
        if verbose:
            print(f"处理后图片大小: {len(file_bytes)} 字节")
        
        # Base64 编码
        encoded = base64.b64encode(file_bytes).decode('ascii')
        if verbose:
            print(f"Base64 长度: {len(encoded)} 字符")
        
        return encoded, orig_size, new_size
        
    except Exception as e:
        raise RuntimeError(f"图片处理失败: {e}")

def call_paddleocr_api(api_url, token, file_data, timeout=45, verbose=False):
    """调用 PaddleOCR VL 1.5 布局解析 API"""
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "file": file_data,
        "fileType": 1,  # 图片文件
        "useDocOrientationClassify": False,
        "useDocUnwarping": False,
        "useChartRecognition": False,
    }
    
    if verbose:
        print(f"API URL: {api_url}")
        print(f"Token: {token[:8]}...")
        print(f"超时: {timeout} 秒")
        print("发送请求...")
    
    start_time = time.time()
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=timeout)
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"响应时间: {elapsed:.2f} 秒")
            print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            if verbose:
                print("API 调用成功")
            return response.json()
        else:
            error_msg = f"API 错误: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('errorMsg', response.text[:200])}"
                except:
                    error_msg += f" - {response.text[:200]}"
            raise RuntimeError(error_msg)
            
    except requests.exceptions.Timeout:
        raise RuntimeError(f"请求超时 ({timeout} 秒)")
    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"连接错误: {e}")
    except Exception as e:
        raise RuntimeError(f"请求异常: {e}")

def save_results(result, args, orig_size, resized_size):
    """保存解析结果"""
    output_file = args.output
    verbose = args.verbose
    
    try:
        # 保存为 Markdown
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# PaddleOCR VL 1.5 布局解析结果\n\n")
            f.write(f"**解析时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**原始图片**: {args.image_path}\n")
            f.write(f"**原始尺寸**: {orig_size[0]} × {orig_size[1]}\n")
            f.write(f"**处理后尺寸**: {resized_size[0]} × {resized_size[1]}\n")
            f.write(f"**最大边长**: {args.max_dim}\n")
            f.write(f"**API URL**: {args.api_url}\n\n")
            
            if not result:
                f.write("## API 调用失败\n")
                f.write("未获得有效响应。\n")
            else:
                f.write("## 解析结果\n\n")
                
                # 提取结构化信息
                if isinstance(result, dict):
                    # 检查布局解析结果
                    if "result" in result and "layoutParsingResults" in result["result"]:
                        layout_results = result["result"]["layoutParsingResults"]
                        f.write(f"**布局区块数量**: {len(layout_results)}\n\n")
                        
                        for layout_idx, layout in enumerate(layout_results):
                            if "prunedResult" in layout and "parsing_res_list" in layout["prunedResult"]:
                                blocks = layout["prunedResult"]["parsing_res_list"]
                                f.write(f"### 布局 {layout_idx+1} (包含 {len(blocks)} 个区块)\n\n")
                                
                                for block_idx, block in enumerate(blocks):
                                    label = block.get("block_label", "unknown")
                                    content = block.get("block_content", "")
                                    bbox = block.get("block_bbox", [])
                                    
                                    f.write(f"**区块 {block_idx+1}** ({label})\n")
                                    if bbox:
                                        f.write(f"位置: {bbox}\n")
                                    
                                    # 处理不同类型的内容
                                    if label == "table" and content:
                                        # 表格内容（通常是 HTML）
                                        if "<table>" in content:
                                            f.write("**表格内容**:\n")
                                            f.write("```html\n")
                                            f.write(content[:1000])
                                            if len(content) > 1000:
                                                f.write("\n... (已截断)")
                                            f.write("\n```\n")
                                        else:
                                            f.write(f"表格内容: {content[:200]}...\n")
                                    elif content and len(content.strip()) > 0:
                                        # 其他文本内容
                                        f.write(f"内容: {content[:200]}")
                                        if len(content) > 200:
                                            f.write("...")
                                        f.write("\n")
                                    
                                    f.write("\n")
                    
                    # 保存完整 JSON（部分）
                    f.write("## 完整响应 (前 5000 字符)\n")
                    f.write("```json\n")
                    json_str = json.dumps(result, ensure_ascii=False, indent=2)
                    if len(json_str) > 5000:
                        f.write(json_str[:5000])
                        f.write("\n... (已截断)\n")
                    else:
                        f.write(json_str)
                    f.write("\n```\n")
                else:
                    f.write("## 原始响应\n")
                    f.write("```\n")
                    f.write(str(result)[:5000])
                    f.write("\n```\n")
        
        if verbose:
            print(f"结果已保存到: {output_file}")
        
        # 同时保存原始 JSON
        json_file = output_file.replace('.md', '.json')
        if not json_file.endswith('.json'):
            json_file += '.json'
        
        if result is not None:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            if verbose:
                print(f"原始 JSON 已保存到: {json_file}")
        
        return True
        
    except Exception as e:
        raise RuntimeError(f"保存结果失败: {e}")

def main():
    """主函数"""
    args = parse_arguments()
    
    if args.verbose:
        print("=== PaddleOCR VL 1.5 文档解析工具 ===")
        print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"图片: {args.image_path}")
        print(f"输出: {args.output}")
        print(f"最大边长: {args.max_dim}")
        print(f"API URL: {args.api_url}")
        print("-" * 50)
    
    try:
        # 1. 检查文件
        if args.verbose:
            print("1. 检查图片文件...")
        check_file(args.image_path)
        
        # 2. 获取 API Token
        token = args.token or os.environ.get(ENV_TOKEN)
        if not token:
            raise ValueError(
                f"请提供 API Token:\n"
                f"  1. 使用 --token 参数\n"
                f"  2. 或设置环境变量 {ENV_TOKEN}\n"
                f"  例如: export {ENV_TOKEN}='your_token_here'"
            )
        
        if args.verbose:
            print(f"2. 使用 Token: {token[:8]}...")
        
        # 3. 调整图片尺寸并编码
        if args.verbose:
            print("3. 处理图片...")
        file_data, orig_size, resized_size = resize_image_if_needed(
            args.image_path, args.max_dim, args.no_resize, args.verbose
        )
        
        # 4. 调用 API
        if args.verbose:
            print("4. 调用 API...")
        result = call_paddleocr_api(
            args.api_url, token, file_data, args.timeout, args.verbose
        )
        
        # 5. 保存结果
        if args.verbose:
            print("5. 保存结果...")
        save_results(result, args, orig_size, resized_size)
        
        if args.verbose:
            print("-" * 50)
            print("处理完成！")
            print(f"结果文件: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        if not args.verbose:
            print("使用 --verbose 参数查看详细处理信息", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
PP-OCR API 文档解析脚本

使用 PP-OCR API 对图片进行OCR识别，并将结果保存为Markdown格式。
支持超时设置（默认15分钟）和错误重试，可保存完整的API JSON响应。

使用方法：
    python3 ppocr-doc-parse.py [图片路径] [--output 输出文件] [--json JSON文件] [--timeout 超时秒数]

示例：
    python3 ppocr-doc-parse.py /path/to/image.jpg --output result.md --json result.json
    python3 ppocr-doc-parse.py /path/to/image.jpg --output result.md  # 自动生成result.json
"""

import os
import sys
import base64
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Any

import requests

# API配置
API_URL = "https://r8y9ufa6z39ey1l2.aistudio-app.com/ocr"
TOKEN = "24ca12680035d0015fd3e9332766d274a0872a09"

# 默认超时时间（秒）
DEFAULT_TIMEOUT = 900  # 15分钟

def encode_image_to_base64(file_path: str, max_size: int = None) -> str:
    """将图片文件编码为base64字符串，可选调整大小"""
    try:
        # 如果指定了max_size，尝试调整图片大小
        if max_size and max_size > 0:
            try:
                from PIL import Image
                img = Image.open(file_path)
                width, height = img.size
                
                if max(width, height) > max_size:
                    if width > height:
                        new_width = max_size
                        new_height = int(height * (max_size / width))
                    else:
                        new_height = max_size
                        new_width = int(width * (max_size / height))
                    
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    print(f"   图片已调整: {width}x{height} -> {new_width}x{new_height}")
                    
                    # 保存到临时文件
                    import tempfile
                    temp_fd, temp_path = tempfile.mkstemp(suffix='.jpg')
                    os.close(temp_fd)
                    img.save(temp_path, "JPEG", quality=90)
                    
                    with open(temp_path, "rb") as f:
                        file_bytes = f.read()
                    
                    # 清理临时文件
                    os.unlink(temp_path)
                    
                    return base64.b64encode(file_bytes).decode("ascii")
            except Exception as pil_error:
                print(f"   警告: 调整图片大小失败，使用原图: {pil_error}")
        
        # 未调整大小或调整失败，使用原图
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        return base64.b64encode(file_bytes).decode("ascii")
    except Exception as e:
        raise ValueError(f"无法读取或编码图片文件: {e}")

def call_ppocr_api(file_data: str, file_type: int = 1, timeout: int = DEFAULT_TIMEOUT,
                   use_doc_orientation_classify: bool = False,
                   use_doc_unwarping: bool = False,
                   use_textline_orientation: bool = False) -> Dict[str, Any]:
    """调用PP-OCR API进行OCR识别"""
    headers = {
        "Authorization": f"token {TOKEN}",
        "Content-Type": "application/json"
    }
    
    required_payload = {
        "file": file_data,
        "fileType": file_type  # 1表示图片，0表示PDF
    }
    
    # 可选参数
    optional_payload = {
        "useDocOrientationClassify": use_doc_orientation_classify,
        "useDocUnwarping": use_doc_unwarping,
        "useTextlineOrientation": use_textline_orientation,
    }
    
    payload = {**required_payload, **optional_payload}
    
    try:
        response = requests.post(
            API_URL, 
            json=payload, 
            headers=headers, 
            timeout=timeout
        )
        response.raise_for_status()  # 检查HTTP错误
        
        result = response.json()
        
        # 检查API返回的错误
        if "error" in result:
            raise RuntimeError(f"API返回错误: {result['error']}")
        
        return result
        
    except requests.exceptions.Timeout:
        raise RuntimeError(f"API请求超时（{timeout}秒）")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API请求失败: {e}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"API响应JSON解析失败: {e}")

def save_ocr_images(result: Dict[str, Any], input_filename: str, output_dir: str = "output") -> List[str]:
    """保存OCR处理后的图片"""
    saved_files = []
    
    if "result" not in result or "ocrResults" not in result["result"]:
        return saved_files
    
    os.makedirs(output_dir, exist_ok=True)
    
    for i, res in enumerate(result["result"]["ocrResults"]):
        image_url = res.get("ocrImage")
        if image_url:
            try:
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    filename = f"{output_dir}/{input_filename}_{i}.jpg"
                    with open(filename, "wb") as f:
                        f.write(img_response.content)
                    saved_files.append(filename)
                    print(f"  已保存OCR图片: {filename}")
                else:
                    print(f"  警告: 无法下载图片 {image_url}, 状态码: {img_response.status_code}")
            except Exception as e:
                print(f"  警告: 下载图片失败: {e}")
    
    return saved_files

def format_ocr_result_to_markdown(result: Dict[str, Any], image_path: str, processing_time: float) -> str:
    """将OCR结果格式化为Markdown文档"""
    if "result" not in result:
        return "# PP-OCR API 解析结果\n\n**错误**: 结果格式异常，未找到'result'字段\n"
    
    ocr_results = result["result"].get("ocrResults", [])
    
    # 获取图片信息
    try:
        import PIL.Image
        from PIL import Image
        img = Image.open(image_path)
        width, height = img.size
        img_info = f"{width} × {height}"
    except Exception:
        img_info = "未知尺寸"
    
    # 构建Markdown内容
    md_content = []
    md_content.append("# PP-OCR API 解析结果\n")
    md_content.append(f"**解析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_content.append(f"**处理耗时**: {processing_time:.2f} 秒\n")
    md_content.append(f"**原始图片**: {os.path.abspath(image_path)}\n")
    md_content.append(f"**图片尺寸**: {img_info}\n")
    md_content.append(f"**API URL**: {API_URL}\n")
    
    md_content.append("\n## OCR结果统计\n")
    md_content.append(f"- **识别区域数量**: {len(ocr_results)}\n")
    
    total_text_count = 0
    total_text_length = 0
    total_confidence = 0.0
    confidence_count = 0
    all_texts = []
    
    # 处理每个OCR结果
    for i, res in enumerate(ocr_results):
        md_content.append(f"\n### 区域 {i+1}\n")
        
        # 显示所有字段
        md_content.append(f"**所有字段**: {', '.join(res.keys())}\n")
        
        # 处理prunedResult（可能是字典或字符串）
        if "prunedResult" in res:
            pruned = res["prunedResult"]
            if isinstance(pruned, dict):
                # 提取识别文本和置信度
                texts = pruned.get("rec_texts", [])
                scores = pruned.get("rec_scores", [])
                polys = pruned.get("rec_polys", [])
                
                md_content.append(f"**文本数量**: {len(texts)}\n")
                md_content.append(f"**置信度数量**: {len(scores)}\n")
                
                # 显示部分文本
                non_empty_texts = [t for t in texts if t and t.strip()]
                if non_empty_texts:
                    md_content.append(f"**非空文本示例**:\n")
                    for j, text in enumerate(non_empty_texts[:10]):
                        score = scores[j] if j < len(scores) else None
                        score_str = f" (置信度: {score:.3f})" if score is not None else ""
                        md_content.append(f"  - `{text}`{score_str}\n")
                    
                    if len(non_empty_texts) > 10:
                        md_content.append(f"  ... 还有 {len(non_empty_texts) - 10} 个文本\n")
                
                # 统计
                total_text_count += len(texts)
                for text in texts:
                    if text:
                        total_text_length += len(text)
                        all_texts.append(text)
                
                for score in scores:
                    total_confidence += score
                    confidence_count += 1
                
                # 显示其他字段
                other_keys = [k for k in pruned.keys() if k not in ["rec_texts", "rec_scores", "rec_polys", "dt_polys"]]
                if other_keys:
                    md_content.append(f"**其他字段**: {', '.join(other_keys)}\n")
                
                # 显示检测多边形数量
                if "dt_polys" in pruned:
                    md_content.append(f"**检测多边形数量**: {len(pruned['dt_polys'])}\n")
                    
            else:
                # prunedResult是字符串
                text = str(pruned)
                md_content.append(f"**识别文本**: {text}\n")
                total_text_length += len(text)
                all_texts.append(text)
        
        # 置信度信息
        if "score" in res:
            confidence = res["score"]
            md_content.append(f"**区域置信度**: {confidence:.4f}\n")
            total_confidence += confidence
            confidence_count += 1
        
        # 位置信息
        if "location" in res:
            location = res["location"]
            md_content.append(f"**位置坐标**: {location}\n")
        
        # 图片URL
        if "ocrImage" in res:
            md_content.append(f"**OCR图片URL**: {res['ocrImage']}\n")
    
    # 统计信息
    if confidence_count > 0:
        avg_confidence = total_confidence / confidence_count
        md_content.append(f"\n## 统计信息\n")
        md_content.append(f"- **平均置信度**: {avg_confidence:.4f}\n")
        md_content.append(f"- **总文本数量**: {total_text_count}\n")
        md_content.append(f"- **总文本长度**: {total_text_length} 字符\n")
        md_content.append(f"- **非空文本数量**: {len([t for t in all_texts if t and t.strip()])}\n")
    
    # 所有非空文本
    non_empty_texts = [t for t in all_texts if t and t.strip()]
    if non_empty_texts:
        md_content.append(f"\n## 所有非空文本\n")
        md_content.append("```\n")
        for i, text in enumerate(non_empty_texts[:100]):  # 限制前100个
            md_content.append(f"{i+1}: {text}\n")
        if len(non_empty_texts) > 100:
            md_content.append(f"... 还有 {len(non_empty_texts) - 100} 个文本未显示\n")
        md_content.append("```\n")
    
    # 原始JSON数据（精简版）
    md_content.append("\n## 原始数据（精简）\n")
    md_content.append("```json\n")
    
    # 创建精简版的JSON数据
    simplified_result = {
        "image_path": image_path,
        "processing_time": processing_time,
        "ocr_count": len(ocr_results),
        "total_text_count": total_text_count,
        "non_empty_text_count": len(non_empty_texts),
        "ocr_results": []
    }
    
    for i, res in enumerate(ocr_results[:3]):  # 只显示前3个结果
        simplified_res = {}
        if "prunedResult" in res:
            pruned = res["prunedResult"]
            if isinstance(pruned, dict):
                texts = pruned.get("rec_texts", [])
                simplified_res["text_count"] = len(texts)
                if texts:
                    simplified_res["sample_texts"] = [t for t in texts[:3] if t and t.strip()]
            else:
                simplified_res["text"] = str(pruned)[:100]
        if "score" in res:
            simplified_res["score"] = res["score"]
        simplified_result["ocr_results"].append(simplified_res)
    
    if len(ocr_results) > 3:
        simplified_result["_note"] = f"共{len(ocr_results)}个结果，此处显示前3个"
    
    md_content.append(json.dumps(simplified_result, indent=2, ensure_ascii=False))
    md_content.append("\n```\n")
    
    md_content.append("\n---\n")
    md_content.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    return "\n".join(md_content)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="使用PP-OCR API解析图片文档")
    parser.add_argument("image_path", nargs="?", default="", help="图片文件路径")
    parser.add_argument("--output", "-o", default="ppocr-30-谢弋.md", help="输出Markdown文件路径")
    parser.add_argument("--timeout", "-t", type=int, default=DEFAULT_TIMEOUT, 
                       help=f"API请求超时时间（秒，默认{DEFAULT_TIMEOUT}）")
    parser.add_argument("--resize", "-r", type=int, default=2048,
                       help="调整图片最大边长（像素），0表示不调整，默认2048")
    parser.add_argument("--orientation-classify", action="store_true",
                       help="启用文档方向分类（useDocOrientationClassify）")
    parser.add_argument("--unwarping", action="store_true",
                       help="启用文档展平（useDocUnwarping）")
    parser.add_argument("--textline-orientation", action="store_true",
                       help="启用文本行方向矫正（useTextlineOrientation）")
    parser.add_argument("--save-images", "-s", action="store_true", 
                       help="是否保存OCR处理后的图片")
    parser.add_argument("--image-dir", default="output", help="OCR图片保存目录")
    parser.add_argument("--json", "-j", help="保存完整JSON响应的文件路径（默认：与输出文件同名但后缀为.json）")
    
    args = parser.parse_args()
    
    # 如果没有提供图片路径，使用默认路径
    if not args.image_path:
        default_image = "/mnt/d/Downloads/V1.0_TESTSET/data/oceanus-share/V1.0_IMAGES_TEST/30-谢弋/流水明细/001_正常.jpg"
        if os.path.exists(default_image):
            args.image_path = default_image
            print(f"使用默认图片路径: {default_image}")
        else:
            print("错误: 未提供图片路径且默认图片不存在")
            print(f"默认路径: {default_image}")
            sys.exit(1)
    
    # 检查图片文件
    if not os.path.exists(args.image_path):
        print(f"错误: 图片文件不存在: {args.image_path}")
        sys.exit(1)
    
    print(f"开始处理图片: {args.image_path}")
    print(f"输出文件: {args.output}")
    print(f"超时设置: {args.timeout} 秒")
    
    try:
        # 1. 编码图片
        print("1. 编码图片...")
        if args.resize > 0:
            print(f"   调整图片大小，最大边长: {args.resize} 像素")
        start_time = time.time()
        file_data = encode_image_to_base64(args.image_path, max_size=args.resize if args.resize > 0 else None)
        encode_time = time.time() - start_time
        print(f"   编码完成，耗时: {encode_time:.2f} 秒")
        print(f"   Base64数据长度: {len(file_data)} 字符")
        
        # 2. 调用API
        print("2. 调用PP-OCR API...")
        api_start_time = time.time()
        result = call_ppocr_api(file_data, file_type=1, timeout=args.timeout)
        api_time = time.time() - api_start_time
        print(f"   API调用成功，耗时: {api_time:.2f} 秒")
        
        # 2.5. 保存完整JSON响应
        print("2.5. 保存完整JSON响应...")
        if args.json:
            json_path = args.json
        else:
            # 使用输出文件的路径，但将后缀改为.json
            base_name = os.path.splitext(args.output)[0]
            json_path = f"{base_name}.json"
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"   完整JSON响应已保存到: {os.path.abspath(json_path)}")
        
        # 3. 保存OCR图片（可选）
        if args.save_images:
            print("3. 保存OCR图片...")
            input_filename = os.path.splitext(os.path.basename(args.image_path))[0]
            saved_images = save_ocr_images(result, input_filename, args.image_dir)
            print(f"   已保存 {len(saved_images)} 张OCR图片到 '{args.image_dir}' 目录")
        
        # 4. 生成Markdown报告
        print("4. 生成Markdown报告...")
        total_time = time.time() - start_time
        md_content = format_ocr_result_to_markdown(result, args.image_path, total_time)
        
        # 5. 保存报告
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"✅ 解析完成!")
        print(f"   总耗时: {total_time:.2f} 秒")
        print(f"   结果已保存到: {os.path.abspath(args.output)}")
        
        # 显示摘要信息
        if "result" in result and "ocrResults" in result["result"]:
            ocr_count = len(result["result"]["ocrResults"])
            print(f"   识别区域数量: {ocr_count}")
            
            # 显示部分文本
            for i, res in enumerate(result["result"]["ocrResults"][:3]):
                if "prunedResult" in res:
                    pruned = res["prunedResult"]
                    if isinstance(pruned, dict):
                        # 从字典中提取文本
                        texts = pruned.get("rec_texts", [])
                        non_empty = [t for t in texts if t and t.strip()]
                        if non_empty:
                            preview = non_empty[0][:50] + ("..." if len(non_empty[0]) > 50 else "")
                            print(f"   区域 {i+1}: {preview} (共{len(texts)}文本)")
                        else:
                            print(f"   区域 {i+1}: [无文本] (共{len(texts)}文本)")
                    else:
                        # 字符串类型
                        text = str(pruned)
                        preview = text[:50] + ("..." if len(text) > 50 else "")
                        print(f"   区域 {i+1}: {preview}")
            
            if ocr_count > 3:
                print(f"   ... 还有 {ocr_count - 3} 个区域")
        
        return 0
        
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        
        # 保存错误信息
        error_content = f"""# PP-OCR API 解析失败

**错误时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**图片路径**: {args.image_path}
**错误信息**: {str(e)}

## 错误详情
```python
{type(e).__name__}: {e}
```

## 建议
1. 检查网络连接
2. 确认API token有效
3. 检查图片格式是否支持
4. 尝试减小图片尺寸
5. 增加超时时间（当前: {args.timeout}秒）

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(error_content)
            print(f"   错误信息已保存到: {args.output}")
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()
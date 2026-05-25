#!/usr/bin/env python3
"""
kimi-doc-parse-compressed.py
压缩图片后调用 kimi k2.5 模型解析，避免 API 超时。
"""

import os
import sys
import base64
import argparse
import tempfile
from pathlib import Path
from PIL import Image
from openai import OpenAI

def compress_image(image_path, max_width=2048, quality=90):
    """压缩图片，返回临时文件路径"""
    with Image.open(image_path) as img:
        # 转换为 RGB（如果透明）
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 调整大小
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"图片已缩放: {img.width}x{img.height} (原图 {img.width}x{img.height})", file=sys.stderr)
        else:
            print(f"图片尺寸未变: {img.width}x{img.height}", file=sys.stderr)
        
        # 保存到临时文件
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(temp_file.name, 'JPEG', quality=quality, optimize=True)
        print(f"临时文件: {temp_file.name} (大小: {os.path.getsize(temp_file.name)} 字节)", file=sys.stderr)
        return temp_file.name

def main():
    parser = argparse.ArgumentParser(description='压缩图片后解析文字和版面信息')
    parser.add_argument('image_path', nargs='?', default='',
                        help='图片路径，默认为空，使用环境变量 IMAGE_PATH 或默认路径')
    parser.add_argument('--output', '-o', default='',
                        help='输出文件路径，默认为标准输出')
    parser.add_argument('--max-width', type=int, default=2048,
                        help='最大宽度像素（默认 2048）')
    parser.add_argument('--quality', type=int, default=90,
                        help='JPEG 质量（默认 90）')
    args = parser.parse_args()

    image_path = args.image_path
    if not image_path:
        image_path = os.environ.get('IMAGE_PATH', '')
    if not image_path:
        image_path = "/mnt/d/Downloads/V1.0_TESTSET/data/oceanus-share/V1.0_IMAGES_TEST/15-高念未央/流水明细/001_正常.jpg"
    
    if not os.path.exists(image_path):
        print(f"错误：文件不存在 - {image_path}", file=sys.stderr)
        sys.exit(1)
    
    api_key = os.environ.get("MOONSHOT_API_KEY")
    if not api_key:
        api_key = "sk-eq7EmmZkrzeeZmKmDZe3FaIo0Ea0PJdxRinc4RzqAumyHSQl"
    
    print(f"原始图片路径: {image_path}", file=sys.stderr)
    print(f"原始文件大小: {os.path.getsize(image_path)} 字节", file=sys.stderr)
    
    # 压缩图片
    compressed_path = compress_image(image_path, max_width=args.max_width, quality=args.quality)
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1",
            timeout=120.0,
        )
        
        with open(compressed_path, "rb") as f:
            image_data = f.read()
        
        image_url = f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
        print(f"压缩图片 base64 长度: {len(image_url)}", file=sys.stderr)
        
        print("发送请求到 Kimi API...", file=sys.stderr)
        completion = client.chat.completions.create(
            model="kimi-k2.5",
            messages=[
                {
                    "role": "system",
                    "content": "你是 Kimi。请严格遵循用户指令：解析图片中的所有信息，包括文字信息和版面信息。尽可能准确地提取所有可见信息。对于图像不清晰、无法确定的内容，使用 `<blur></blur>` 标签标记该部分，例如：`<blur>可能为张三</blur>`。确保解析的信息与图像信息完全一致，不要做任何修改、加工、推理或补充，但可以对模糊内容进行标记。"
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                        {
                            "type": "text",
                            "text": "请解析这张图片中的所有信息，包括文字信息和版面信息（例如文字的位置、布局、表格结构等）。要求：尽可能准确地提取所有可见信息。对于图像不清晰、无法确定的内容，使用 `<blur></blur>` 标签标记该部分。直接输出解析结果。",
                        },
                    ],
                },
            ],
            timeout=300.0,
        )
        
        result = completion.choices[0].message.content
        print(f"收到响应，长度: {len(result)} 字符", file=sys.stderr)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"结果已写入: {args.output}", file=sys.stderr)
        else:
            print(result)
            
    except Exception as e:
        print(f"API 请求失败: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # 清理临时文件
        try:
            os.unlink(compressed_path)
            print(f"已删除临时文件: {compressed_path}", file=sys.stderr)
        except:
            pass

if __name__ == "__main__":
    main()
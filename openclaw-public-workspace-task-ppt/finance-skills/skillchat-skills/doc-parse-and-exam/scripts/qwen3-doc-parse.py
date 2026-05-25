#!/usr/bin/env python3
"""
解析银行流水图片，提取文字和版面信息。
使用 qwen3-vl-32b-instruct 模型，通过 DashScope API。
支持命令行参数指定图片路径和 API 密钥。
"""

import os
import base64
import argparse
from openai import OpenAI

def encode_image_to_base64(image_path):
    """将本地图片文件编码为 base64 数据 URI"""
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

def main():
    parser = argparse.ArgumentParser(description="使用 qwen3-vl-32b-instruct 解析银行流水图片")
    parser.add_argument("image_path", help="待解析的图片文件路径")
    parser.add_argument("--api-key", help="DashScope API 密钥（如未提供，则使用环境变量 DASHSCOPE_API_KEY）")
    parser.add_argument("--output", "-o", default="qwen3-result.md", help="结果输出文件路径（默认：qwen3-result.md）")
    args = parser.parse_args()

    image_path = args.image_path
    if not os.path.exists(image_path):
        print(f"错误：图片文件不存在 {image_path}")
        return

    # 确定 API 密钥
    api_key = args.api_key or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误：未提供 API 密钥。请通过 --api-key 参数或设置环境变量 DASHSCOPE_API_KEY 指定。")
        return

    # 初始化 DashScope 客户端
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        timeout=180.0,  # 请求超时（秒）
    )

    # 构建用户消息
    image_url = encode_image_to_base64(image_path)
    prompt = """请解析这张银行流水图片中的所有信息，包括：
1. 文字信息：所有可见的文字内容，按原样逐行提取。
2. 版面信息：表格结构、字段位置、行列关系、印章位置、手写备注位置等。

要求：
- 完全按照图片中的信息输出，不要修改、加工或补充任何内容。
- 文字部分保持原样，包括数字、符号、空格。
- 版面信息描述清晰，指出各元素在图片中的相对位置。
"""

    try:
        print(f"正在解析图片：{image_path}")
        completion = client.chat.completions.create(
            model="qwen3-vl-32b-instruct",  # DashScope 视觉语言模型
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        result = completion.choices[0].message.content
        print("解析完成，正在保存结果...")
        
        # 保存到文件
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"# 图片解析结果\n\n")
            f.write(f"**图片路径**：{image_path}\n\n")
            f.write(f"**模型**：qwen3-vl-32b-instruct\n\n")
            f.write(f"**解析结果**：\n\n")
            f.write(result)
        
        print(f"结果已保存至 {args.output}")
        print("\n--- 解析结果预览（前500字符） ---")
        print(result[:500] + ("..." if len(result) > 500 else ""))
        
    except Exception as e:
        print(f"API 调用出错：{e}")

if __name__ == "__main__":
    main()
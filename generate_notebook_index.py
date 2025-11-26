#!/usr/bin/env python3
"""
扫描文件夹中所有 Jupyter Notebook 的 markdown cell，生成 INDEX.md 索引文件。

用法：
    python generate_notebook_index.py [目录路径]
    
如果不指定目录，默认扫描当前目录。
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def extract_markdown_cells(notebook_path):
    """从 notebook 中提取所有 markdown cell 的内容"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    
    cells = nb.get('cells', [])
    markdown_contents = []
    
    for cell in cells:
        if cell.get('cell_type') == 'markdown':
            source = cell.get('source', [])
            if isinstance(source, list):
                content = ''.join(source).strip()
            else:
                content = source.strip()
            if content:
                markdown_contents.append(content)
    
    return markdown_contents


def format_all_markdown_cells(markdown_cells):
    """格式化所有 markdown cells"""
    if not markdown_cells:
        return "_（无 markdown 描述）_"
    
    formatted = []
    for i, cell in enumerate(markdown_cells, 1):
        # 清理每个cell的内容
        lines = cell.strip().split('\n')
        formatted.append(f"**Cell {i}:**\n{cell.strip()}")
    
    return '\n\n'.join(formatted)


def scan_notebooks(directory):
    """扫描目录中的所有 notebook"""
    directory = Path(directory)
    notebooks = []
    
    for nb_path in sorted(directory.glob('**/*.ipynb')):
        # 跳过 checkpoint 文件
        if '.ipynb_checkpoints' in str(nb_path):
            continue
        
        relative_path = nb_path.relative_to(directory)
        markdown_cells = extract_markdown_cells(nb_path)
        
        if markdown_cells is not None:
            notebooks.append({
                'path': relative_path,
                'name': nb_path.stem,
                'markdown_cells': markdown_cells,
                'formatted_content': format_all_markdown_cells(markdown_cells),
                'cell_count': len(markdown_cells)
            })
    
    return notebooks


def generate_index(notebooks, directory):
    """生成 INDEX.md 内容"""
    lines = [
        f"# Notebook 索引",
        f"",
        f"_自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        f"",
        f"共 {len(notebooks)} 个 notebook",
        f"",
        "---",
        ""
    ]
    
    for nb in notebooks:
        lines.append(f"## 📓 {nb['name']}")
        lines.append(f"")
        lines.append(f"**文件**: `{nb['path']}` | **Markdown cells**: {nb['cell_count']}")
        lines.append(f"")
        # 直接展示所有 markdown cells 内容
        lines.append(nb['formatted_content'])
        lines.append(f"")
        lines.append("---")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    # 获取目标目录
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = '.'
    
    directory = Path(directory).resolve()
    
    if not directory.exists():
        print(f"错误：目录不存在 - {directory}")
        sys.exit(1)
    
    print(f"扫描目录: {directory}")
    
    # 扫描 notebooks
    notebooks = scan_notebooks(directory)
    
    if not notebooks:
        print("未找到任何 Jupyter Notebook 文件")
        sys.exit(0)
    
    print(f"找到 {len(notebooks)} 个 notebook")
    
    # 生成索引
    index_content = generate_index(notebooks, directory)
    
    # 写入文件
    output_path = directory / 'INDEX.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"索引已生成: {output_path}")
    
    # 简单预览
    print("\n--- 预览 ---")
    for nb in notebooks:
        print(f"  • {nb['name']}: {nb['cell_count']} 个 markdown cells")


if __name__ == '__main__':
    main()

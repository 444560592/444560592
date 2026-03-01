"""
SVG 批量排版工具 / SVG Batch Layout Tool

将多个 SVG 文件按网格排列并合并为一个 SVG 文件。
Arrange multiple SVG files in a grid and merge them into a single SVG file.

用法 / Usage:
    python svg_layout.py input_dir/ -o output.svg --cols 4 --padding 10
    python svg_layout.py a.svg b.svg c.svg -o grid.svg --cols 3
"""

import os
import math
import copy
import argparse
from xml.etree import ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"

# Register namespace prefixes so the output does not use ns0, ns1 …
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_length(value):
    """Convert an SVG length string (e.g. '100px', '50.5') to a float."""
    if value is None:
        return None
    value = str(value).strip()
    for unit in ("px", "pt", "mm", "cm", "in", "em", "rem", "%"):
        if value.endswith(unit):
            value = value[: -len(unit)]
            break
    try:
        return float(value)
    except ValueError:
        return None


def parse_svg_dimensions(root):
    """
    Extract (width, height) from an SVG root element.

    Falls back to the viewBox attribute when explicit width/height are absent.
    Returns (width, height) as floats, defaulting to 100×100 if nothing is found.
    """
    width = _parse_length(root.get("width"))
    height = _parse_length(root.get("height"))

    viewbox = root.get("viewBox")
    if viewbox:
        parts = viewbox.split()
        if len(parts) == 4:
            if width is None:
                width = float(parts[2])
            if height is None:
                height = float(parts[3])

    return (width or 100.0), (height or 100.0)


def load_svg(filepath):
    """
    Load an SVG file.

    Returns (root_element, width, height).
    """
    tree = ET.parse(filepath)
    root = tree.getroot()
    w, h = parse_svg_dimensions(root)
    return root, w, h


def collect_svg_files(paths):
    """
    Expand a list of file/directory paths into a sorted list of .svg file paths.
    """
    svg_files = []
    for path in paths:
        if os.path.isdir(path):
            for fname in sorted(os.listdir(path)):
                if fname.lower().endswith(".svg"):
                    svg_files.append(os.path.join(path, fname))
        elif os.path.isfile(path) and path.lower().endswith(".svg"):
            svg_files.append(path)
    return svg_files


# ---------------------------------------------------------------------------
# Core layout
# ---------------------------------------------------------------------------

def batch_layout(svg_files, output_file, cols=4, padding=10,
                 show_labels=True, cell_width=None, cell_height=None):
    """
    Arrange multiple SVG files in a grid and write the result to output_file.

    Parameters
    ----------
    svg_files   : list of paths to input SVG files.
    output_file : destination path for the combined SVG.
    cols        : number of grid columns.
    padding     : spacing (px) between cells and around the canvas border.
    show_labels : when True, render each file's stem as a caption below its cell.
    cell_width  : uniform cell width in px; defaults to the widest source SVG.
    cell_height : uniform cell height in px; defaults to the tallest source SVG.

    Returns
    -------
    str : the path of the written output file.
    """
    if not svg_files:
        raise ValueError("SVG 文件列表为空 / No SVG files provided")

    # Load all source SVGs
    items = []
    for filepath in svg_files:
        root, w, h = load_svg(filepath)
        name = os.path.splitext(os.path.basename(filepath))[0]
        items.append((name, root, w, h))

    # Uniform cell dimensions
    if cell_width is None:
        cell_width = max(w for _, _, w, h in items)
    if cell_height is None:
        cell_height = max(h for _, _, w, h in items)

    cols = min(cols, len(items))
    rows = math.ceil(len(items) / cols)
    label_h = 18 if show_labels else 0

    canvas_w = cols * cell_width + (cols + 1) * padding
    canvas_h = rows * (cell_height + label_h) + (rows + 1) * padding

    # Root <svg> element
    output_root = ET.Element(
        f"{{{SVG_NS}}}svg",
        {
            "width": str(canvas_w),
            "height": str(canvas_h),
            "viewBox": f"0 0 {canvas_w} {canvas_h}",
        },
    )

    # White background
    ET.SubElement(
        output_root,
        f"{{{SVG_NS}}}rect",
        {"width": str(canvas_w), "height": str(canvas_h), "fill": "white"},
    )

    for idx, (name, src_root, w, h) in enumerate(items):
        col = idx % cols
        row = idx // cols

        cell_x = padding + col * (cell_width + padding)
        cell_y = padding + row * (cell_height + label_h + padding)

        # Scale uniformly to fit inside the cell
        scale = min(cell_width / w, cell_height / h) if w and h else 1.0
        offset_x = cell_x + (cell_width - w * scale) / 2
        offset_y = cell_y + (cell_height - h * scale) / 2

        # Group with transform for this SVG
        g = ET.SubElement(
            output_root,
            f"{{{SVG_NS}}}g",
            {
                "transform": (
                    f"translate({offset_x:.4f},{offset_y:.4f})"
                    f" scale({scale:.6f})"
                ),
                "data-source": name,
            },
        )

        # Copy source children into the group
        for child in src_root:
            g.append(copy.deepcopy(child))

        # Caption below the cell
        if show_labels:
            ET.SubElement(
                output_root,
                f"{{{SVG_NS}}}text",
                {
                    "x": str(cell_x + cell_width / 2),
                    "y": str(cell_y + cell_height + label_h * 0.8),
                    "text-anchor": "middle",
                    "font-size": "12",
                    "font-family": "sans-serif",
                    "fill": "#555",
                },
            ).text = name

    ET.indent(output_root, space="  ")
    ET.ElementTree(output_root).write(
        output_file, encoding="unicode", xml_declaration=False
    )

    print(
        f"已生成 / Generated: {output_file}"
        f"  ({len(items)} 文件/files, {rows}×{cols} 网格/grid)"
    )
    return output_file


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="SVG 批量排版工具 / SVG Batch Layout Tool"
    )
    parser.add_argument(
        "input",
        nargs="+",
        help="输入 SVG 文件或目录 / Input SVG files or directories",
    )
    parser.add_argument(
        "-o", "--output",
        default="output.svg",
        help="输出文件路径 / Output file path (default: output.svg)",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=4,
        help="列数 / Number of columns (default: 4)",
    )
    parser.add_argument(
        "--padding",
        type=float,
        default=10,
        help="单元格间距 px / Padding between cells in px (default: 10)",
    )
    parser.add_argument(
        "--no-labels",
        action="store_true",
        help="隐藏文件名标签 / Hide filename labels",
    )
    parser.add_argument(
        "--cell-width",
        type=float,
        default=None,
        help="固定单元格宽度 px / Fixed cell width in px",
    )
    parser.add_argument(
        "--cell-height",
        type=float,
        default=None,
        help="固定单元格高度 px / Fixed cell height in px",
    )

    args = parser.parse_args()
    svg_files = collect_svg_files(args.input)

    if not svg_files:
        print("未找到 SVG 文件 / No SVG files found")
        return 1

    batch_layout(
        svg_files,
        args.output,
        cols=args.cols,
        padding=args.padding,
        show_labels=not args.no_labels,
        cell_width=args.cell_width,
        cell_height=args.cell_height,
    )
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

# 简单计算器 / Simple Calculator

一个用 Python 编写的命令行计算器程序，支持加、减、乘、除运算。

A command-line calculator program written in Python, supporting addition, subtraction, multiplication, and division.

## 使用方法 / Usage

```bash
python main.py
```

按提示输入表达式，例如：

Enter expressions as prompted, e.g.:

```
3 + 4
10 - 2.5
6 * 7
9 / 3
```

输入 `q` 退出程序。Enter `q` to quit.

## 功能 / Features

- 加法 / Addition (`+`)
- 减法 / Subtraction (`-`)
- 乘法 / Multiplication (`*`)
- 除法 / Division (`/`)
- 除零保护 / Division-by-zero protection

---

# SVG 批量排版工具 / SVG Batch Layout Tool

将多个 SVG 文件按网格排列并合并为一个 SVG 文件的命令行工具。

A command-line tool that arranges multiple SVG files in a grid and merges them into a single SVG file.

## 使用方法 / Usage

```bash
# 将目录中所有 SVG 排列成 4 列网格 / Arrange all SVGs in a directory into a 4-column grid
python svg_layout.py icons/ -o output.svg --cols 4

# 指定具体文件 / Specify individual files
python svg_layout.py a.svg b.svg c.svg -o grid.svg --cols 3

# 隐藏文件名标签 / Hide filename labels
python svg_layout.py icons/ -o output.svg --no-labels

# 自定义单元格大小和间距 / Custom cell size and padding
python svg_layout.py icons/ -o output.svg --cell-width 120 --cell-height 120 --padding 20
```

## 参数说明 / Options

| 参数 / Option | 默认值 / Default | 说明 / Description |
|---|---|---|
| `input` | — | SVG 文件或目录 / SVG files or directories |
| `-o / --output` | `output.svg` | 输出文件路径 / Output file path |
| `--cols` | `4` | 列数 / Number of columns |
| `--padding` | `10` | 间距 px / Padding in px |
| `--no-labels` | off | 隐藏文件名标签 / Hide filename labels |
| `--cell-width` | 自动 / auto | 固定格宽 px / Fixed cell width |
| `--cell-height` | 自动 / auto | 固定格高 px / Fixed cell height |
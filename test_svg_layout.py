"""
Unit tests for svg_layout.py
"""

import os
import math
import unittest
import tempfile
from xml.etree import ElementTree as ET

from svg_layout import (
    _parse_length,
    parse_svg_dimensions,
    load_svg,
    collect_svg_files,
    batch_layout,
)

SVG_NS = "http://www.w3.org/2000/svg"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_svg(width, height, content="", viewbox=False):
    vb = f' viewBox="0 0 {width} {height}"' if viewbox else ""
    return (
        f'<svg xmlns="{SVG_NS}" width="{width}" height="{height}"{vb}>'
        f"{content}</svg>"
    )


def _write_svg(path, width, height, color="red", viewbox=False):
    content = f'<rect width="{width}" height="{height}" fill="{color}"/>'
    path.write_text(_make_svg(width, height, content, viewbox=viewbox))
    return str(path)


# ---------------------------------------------------------------------------
# _parse_length
# ---------------------------------------------------------------------------

class TestParseLength(unittest.TestCase):
    def test_plain_number(self):
        self.assertEqual(_parse_length("100"), 100.0)

    def test_px_unit(self):
        self.assertEqual(_parse_length("64px"), 64.0)

    def test_float(self):
        self.assertAlmostEqual(_parse_length("12.5"), 12.5)

    def test_none_input(self):
        self.assertIsNone(_parse_length(None))

    def test_non_numeric(self):
        self.assertIsNone(_parse_length("auto"))


# ---------------------------------------------------------------------------
# parse_svg_dimensions
# ---------------------------------------------------------------------------

class TestParseSvgDimensions(unittest.TestCase):
    def test_explicit_width_height(self):
        root = ET.fromstring(f'<svg xmlns="{SVG_NS}" width="150" height="80"/>')
        w, h = parse_svg_dimensions(root)
        self.assertEqual(w, 150.0)
        self.assertEqual(h, 80.0)

    def test_viewbox_fallback(self):
        root = ET.fromstring(f'<svg xmlns="{SVG_NS}" viewBox="0 0 300 200"/>')
        w, h = parse_svg_dimensions(root)
        self.assertEqual(w, 300.0)
        self.assertEqual(h, 200.0)

    def test_explicit_overrides_viewbox(self):
        root = ET.fromstring(
            f'<svg xmlns="{SVG_NS}" width="50" height="50" viewBox="0 0 300 200"/>'
        )
        w, h = parse_svg_dimensions(root)
        self.assertEqual(w, 50.0)
        self.assertEqual(h, 50.0)

    def test_defaults_when_nothing(self):
        root = ET.fromstring(f'<svg xmlns="{SVG_NS}"/>')
        w, h = parse_svg_dimensions(root)
        self.assertEqual(w, 100.0)
        self.assertEqual(h, 100.0)

    def test_px_unit_stripped(self):
        root = ET.fromstring(f'<svg xmlns="{SVG_NS}" width="200px" height="100px"/>')
        w, h = parse_svg_dimensions(root)
        self.assertEqual(w, 200.0)
        self.assertEqual(h, 100.0)


# ---------------------------------------------------------------------------
# load_svg
# ---------------------------------------------------------------------------

class TestLoadSvg(unittest.TestCase):
    def test_load_returns_root_and_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "test.svg")
            with open(path, "w") as f:
                f.write(_make_svg(64, 32))
            root, w, h = load_svg(path)
            self.assertIsNotNone(root)
            self.assertEqual(w, 64.0)
            self.assertEqual(h, 32.0)


# ---------------------------------------------------------------------------
# collect_svg_files
# ---------------------------------------------------------------------------

class TestCollectSvgFiles(unittest.TestCase):
    def test_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("b.svg", "a.svg", "c.txt"):
                open(os.path.join(tmp, name), "w").close()
            files = collect_svg_files([tmp])
            basenames = [os.path.basename(f) for f in files]
            self.assertEqual(basenames, ["a.svg", "b.svg"])

    def test_explicit_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = os.path.join(tmp, "a.svg")
            open(a, "w").close()
            files = collect_svg_files([a])
            self.assertEqual(files, [a])

    def test_non_svg_file_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "file.png")
            open(p, "w").close()
            files = collect_svg_files([p])
            self.assertEqual(files, [])


# ---------------------------------------------------------------------------
# batch_layout
# ---------------------------------------------------------------------------

class TestBatchLayout(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmpdir = self.tmp.name
        from pathlib import Path
        specs = [(100, 100, "red"), (200, 100, "blue"), (100, 200, "green")]
        self.svg_files = [
            _write_svg(Path(self.tmpdir) / f"shape{i + 1}.svg", w, h, color)
            for i, (w, h, color) in enumerate(specs)
        ]
        self.output = os.path.join(self.tmpdir, "out.svg")

    def tearDown(self):
        self.tmp.cleanup()

    def test_creates_output_file(self):
        batch_layout(self.svg_files, self.output, cols=2)
        self.assertTrue(os.path.exists(self.output))

    def test_raises_on_empty_list(self):
        with self.assertRaises(ValueError):
            batch_layout([], self.output)

    def test_output_is_valid_svg(self):
        batch_layout(self.svg_files, self.output, cols=2)
        tree = ET.parse(self.output)
        root = tree.getroot()
        self.assertIn("svg", root.tag)

    def test_canvas_dimensions(self):
        cell_w, cell_h, pad = 100.0, 100.0, 10.0
        cols = 2
        batch_layout(
            self.svg_files, self.output,
            cols=cols, padding=pad,
            show_labels=False,
            cell_width=cell_w, cell_height=cell_h,
        )
        root = ET.parse(self.output).getroot()
        rows = math.ceil(len(self.svg_files) / cols)
        expected_w = cols * cell_w + (cols + 1) * pad
        expected_h = rows * cell_h + (rows + 1) * pad
        self.assertAlmostEqual(float(root.get("width")), expected_w)
        self.assertAlmostEqual(float(root.get("height")), expected_h)

    def test_labels_present_by_default(self):
        batch_layout(self.svg_files, self.output, cols=2)
        content = open(self.output).read()
        self.assertIn("shape1", content)

    def test_no_labels_when_disabled(self):
        batch_layout(self.svg_files, self.output, cols=2, show_labels=False)
        root = ET.parse(self.output).getroot()
        ns = {"svg": SVG_NS}
        texts = root.findall(".//svg:text", ns)
        self.assertEqual(texts, [])

    def test_single_file(self):
        batch_layout([self.svg_files[0]], self.output, cols=4)
        self.assertTrue(os.path.exists(self.output))

    def test_returns_output_path(self):
        result = batch_layout(self.svg_files, self.output)
        self.assertEqual(result, self.output)


if __name__ == "__main__":
    unittest.main()

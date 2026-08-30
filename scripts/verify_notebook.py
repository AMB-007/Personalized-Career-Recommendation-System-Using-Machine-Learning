import nbformat
from pathlib import Path

nb_path = Path("model_training/notebook.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

print(f"Total Notebook Cells: {len(nb.cells)}")
code_cells = [c for c in nb.cells if c.cell_type == "code"]
md_cells = [c for c in nb.cells if c.cell_type == "markdown"]
print(f"Code Cells: {len(code_cells)} | Markdown Cells: {len(md_cells)}")

cells_with_output = [c for c in code_cells if len(c.get("outputs", [])) > 0]
print(f"Code cells with live populated outputs: {len(cells_with_output)} / {len(code_cells)}")

size_kb = nb_path.stat().st_size / 1024
print(f"Notebook File Size: {size_kb:.1f} KB")

for i, cell in enumerate(code_cells):
    outs = cell.get("outputs", [])
    out_types = [o.get("output_type") for o in outs]
    has_image = any("image/png" in o.get("data", {}) for o in outs if o.get("output_type") == "display_data")
    img_str = " (Has inline PNG graph)" if has_image else ""
    print(f"  Code Cell {i+1:2d} -> Outputs: {len(outs):2d} | Types: {out_types}{img_str}")

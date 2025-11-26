# notebook-mapper
Generate a markdown index from Jupyter notebook markdown cells.




## Installation

```bash
git clone https://github.com/ddzs1234/notebook-mapper.git
```

Or just download `generate_notebook_index.py` directly.

## Usage

```bash
# Scan current directory
python generate_notebook_index.py

# Scan a specific directory
python generate_notebook_index.py /path/to/your/notebooks
```

This will generate an `INDEX.md` file in the target directory.

## Example Output

```markdown
# Notebook 索引

共 3 个 notebook

---

## 📓 01_data_analysis

**文件**: `01_data_analysis.ipynb` | **Markdown cells**: 2

**Cell 1:**
# Data Analysis
Loading data from FITS files...

**Cell 2:**
## Results
Found 3400 sources...

---
```

## Requirements

Python 3.6+ (no external dependencies)

## License

MIT

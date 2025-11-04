# Iris plotting helper

This workspace contains a small helper to plot the `iris.csv` dataset.

Files of interest
- `plot_iris.py` — script to create plots (scatter, pairplot, histogram). Supports CLI flags.
- `notebook.ipynb` — small notebook that displays the scatter inline.
- `plots/` — directory where PNGs are written (created by the script).

Quick examples

Create the default scatter (auto-detects column names like `sepal.length` or `sepal_length`):

```bash
python3 plot_iris.py
```

Create all plots (scatter, pairplot, hist):

```bash
python3 plot_iris.py --plot all
```

Specify columns and output path:

```bash
python3 plot_iris.py --x "sepal.length" --y "sepal.width" --hue variety --out plots/my_scatter.png
```

Open generated plots in VS Code Explorer by clicking `plots/*.png`.

Notebook

Open `notebook.ipynb` in VS Code or run it with Jupyter to see the scatter inline.

Dependencies

Install required Python packages:

```bash
python3 -m pip install --user pandas matplotlib seaborn
```

If you want, I can also add a `requirements.txt` or convert this into a small package.
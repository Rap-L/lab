#!/usr/bin/env python3
"""Simple script to plot iris.csv and save a scatter plot.

Saves output to ./plots/iris_scatter.png
"""
import os
import sys
from typing import Optional, List

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
except Exception as e:
    print("Missing dependency:", e)
    print("Install dependencies with: python3 -m pip install pandas matplotlib seaborn")
    sys.exit(1)


def norm(s: str) -> str:
    return s.strip().lower().replace('.', '_').replace(' ', '_')


def detect_columns(df: pd.DataFrame):
    col_map = {norm(c): c for c in df.columns}
    # desired normalized names
    x_norm = 'sepal_length'
    y_norm = 'sepal_width'
    hue_candidates = ['species', 'variety', 'class', 'target']

    x_col = None
    y_col = None
    if x_norm in col_map and y_norm in col_map:
        x_col = col_map[x_norm]
        y_col = col_map[y_norm]
    else:
        # fallback: substring matching
        for k, v in col_map.items():
            if 'sepal' in k and 'length' in k and x_col is None:
                x_col = v
            if 'sepal' in k and 'width' in k and y_col is None:
                y_col = v

    hue_col = None
    for cand in hue_candidates:
        if cand in col_map:
            hue_col = col_map[cand]
            break

    return x_col, y_col, hue_col


def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, hue_col: Optional[str], out_path: str):
    sns.set(style='whitegrid')
    plt.figure(figsize=(8, 6))
    if hue_col and hue_col in df.columns:
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col, palette='deep', s=60)
    else:
        plt.scatter(df[x_col], df[y_col], c='tab:blue')

    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'{os.path.basename(out_path)}')
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved scatter to {out_path}")


def plot_pairplot(df: pd.DataFrame, out_path: str, hue_col: Optional[str]):
    cols = df.select_dtypes(include=['number']).columns.tolist()
    if not cols:
        print('No numeric columns available for pairplot. Skipping.')
        return
    pp = sns.pairplot(df[cols + ([hue_col] if hue_col and hue_col in df.columns else [])], hue=hue_col)
    pp.savefig(out_path)
    plt.close()
    print(f"Saved pairplot to {out_path}")


def plot_hist(df: pd.DataFrame, out_path: str, columns: Optional[List[str]] = None):
    cols = columns or df.select_dtypes(include=['number']).columns.tolist()
    if not cols:
        print('No numeric columns available for histogram. Skipping.')
        return
    sns.set(style='white')
    df[cols].hist(figsize=(4 * min(3, len(cols)), 3 * ((len(cols) + 2) // 3)), bins=15)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved histogram(s) to {out_path}")


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser(description='Plot iris.csv (scatter/pairplot/hist).')
    parser.add_argument('--csv', default=os.path.join(os.path.dirname(__file__), 'iris.csv'), help='Path to iris CSV')
    parser.add_argument('--x', help='X column for scatter')
    parser.add_argument('--y', help='Y column for scatter')
    parser.add_argument('--hue', help='Hue/label column')
    parser.add_argument('--plot', choices=['scatter', 'pairplot', 'hist', 'all'], default='scatter', help='Which plot to create')
    parser.add_argument('--out', help='Output path for saved plot (file for scatter/hist, file for pairplot)')
    args = parser.parse_args(argv)

    csv_path = args.csv
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Make sure the file exists.")
        return

    df = pd.read_csv(csv_path)

    auto_x, auto_y, auto_hue = detect_columns(df)

    x_col = args.x or auto_x
    y_col = args.y or auto_y
    hue_col = args.hue or auto_hue

    if args.plot in ('scatter', 'all'):
        if not x_col or not y_col:
            print('Scatter plot requires x and y columns. Found:', list(df.columns))
        else:
            out_dir = os.path.join(os.path.dirname(__file__), 'plots')
            os.makedirs(out_dir, exist_ok=True)
            out_path = args.out or os.path.join(out_dir, 'iris_scatter.png')
            plot_scatter(df, x_col, y_col, hue_col, out_path)

    if args.plot in ('pairplot', 'all'):
        out_dir = os.path.join(os.path.dirname(__file__), 'plots')
        os.makedirs(out_dir, exist_ok=True)
        out_path = args.out or os.path.join(out_dir, 'iris_pairplot.png')
        plot_pairplot(df, out_path, hue_col)

    if args.plot in ('hist', 'all'):
        out_dir = os.path.join(os.path.dirname(__file__), 'plots')
        os.makedirs(out_dir, exist_ok=True)
        out_path = args.out or os.path.join(out_dir, 'iris_hist.png')
        plot_hist(df, out_path)


if __name__ == '__main__':
    main()

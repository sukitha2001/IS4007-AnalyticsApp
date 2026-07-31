#!/usr/bin/env python3
"""
Assemble the analytics notebook from module cell definitions.
Combines setup cells + Module 1 + Module 2 into a single .ipynb file.
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


def make_cell(cell_type, source):
    """Create a notebook cell dict in nbformat v4 format."""
    lines = source.rstrip('\n').split('\n')
    formatted = [line + '\n' for line in lines[:-1]] + [lines[-1]]
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": formatted
    }
    if cell_type == "code":
        cell["outputs"] = []
        cell["execution_count"] = None
    return cell


def get_setup_cells():
    """Return the notebook setup and data loading cells."""
    return [
        {
            "cell_type": "markdown",
            "source": (
                "# 📊 Revenue Analytics & Customer Intelligence Notebook\n"
                "\n"
                "---\n"
                "\n"
                "**Dataset**: Synthetic revenue data (Jan 2023 – Dec 2024)  \n"
                "**Transactions**: ~12,900 | **Customers**: 120 | **Products**: 30 | **Campaigns**: 10\n"
                "\n"
                "This notebook provides a comprehensive analytical framework organised into two modules:\n"
                "\n"
                "| Module | Focus |\n"
                "|---|---|\n"
                "| **Module 1** | Executive Revenue Dashboard — KPIs, trends, category/channel/branch breakdowns, margins, campaign impact |\n"
                "| **Module 2** | Customer Analytics — segmentation, RFM, CLV, repeat behaviour, inactive detection, cohort analysis |\n"
                "\n"
                "A **Statistical Analysis** appendix follows with OLS & logistic regressions, ANOVA, chi-square tests, "
                "seasonal decomposition, and full diagnostic outputs.\n"
                "\n"
                "---"
            )
        },
        {
            "cell_type": "markdown",
            "source": "## ⚙️ Setup & Data Loading"
        },
        {
            "cell_type": "code",
            "source": (
                "# ── Imports ─────────────────────────────────────────────────────────────\n"
                "import pandas as pd\n"
                "import numpy as np\n"
                "import matplotlib.pyplot as plt\n"
                "import matplotlib.patches as mpatches\n"
                "import matplotlib.ticker as mticker\n"
                "import seaborn as sns\n"
                "from scipy import stats\n"
                "import statsmodels.api as sm\n"
                "from statsmodels.formula.api import ols as smf_ols, logit as smf_logit\n"
                "from statsmodels.stats.outliers_influence import variance_inflation_factor\n"
                "from statsmodels.stats.diagnostic import het_breuschpagan\n"
                "from statsmodels.stats.multicomp import pairwise_tukeyhsd\n"
                "from statsmodels.tsa.seasonal import seasonal_decompose\n"
                "from sklearn.cluster import KMeans\n"
                "from sklearn.preprocessing import StandardScaler, LabelEncoder\n"
                "from sklearn.metrics import classification_report, roc_curve, auc, confusion_matrix\n"
                "from sklearn.model_selection import train_test_split\n"
                "import warnings\n"
                "warnings.filterwarnings('ignore')\n"
                "\n"
                "# ── Light Theme Visual Style ────────────────────────────────────────────\n"
                "plt.rcParams.update({\n"
                "    'figure.facecolor': '#FFFFFF',\n"
                "    'axes.facecolor': '#F7F7FA',\n"
                "    'axes.edgecolor': '#D1D5DB',\n"
                "    'axes.labelcolor': '#1F2937',\n"
                "    'text.color': '#1F2937',\n"
                "    'xtick.color': '#4B5563',\n"
                "    'ytick.color': '#4B5563',\n"
                "    'grid.color': '#E5E7EB',\n"
                "    'grid.alpha': 0.8,\n"
                "    'font.family': 'sans-serif',\n"
                "    'font.size': 11,\n"
                "    'axes.titlesize': 14,\n"
                "    'axes.titleweight': 'bold',\n"
                "    'figure.titlesize': 16,\n"
                "    'figure.titleweight': 'bold',\n"
                "    'axes.spines.top': False,\n"
                "    'axes.spines.right': False,\n"
                "})\n"
                "sns.set_style('whitegrid', {\n"
                "    'axes.facecolor': '#F7F7FA',\n"
                "    'grid.color': '#E5E7EB',\n"
                "})\n"
                "sns.set_context('notebook', font_scale=1.1)\n"
                "\n"
                "COLORS = {\n"
                "    'primary': '#4361EE',\n"
                "    'secondary': '#E63946',\n"
                "    'accent': '#2EC4B6',\n"
                "    'success': '#06D6A0',\n"
                "    'warning': '#FFB703',\n"
                "    'danger': '#EF476F',\n"
                "    'bg_dark': '#FFFFFF',\n"
                "    'bg_card': '#F0F4FF',\n"
                "    'text': '#1F2937',\n"
                "    'text_muted': '#6B7280',\n"
                "    'gradient': ['#4361EE', '#7209B7', '#E63946', '#FFB703', '#2EC4B6', '#06D6A0'],\n"
                "    'pastel': ['#A8DADC', '#F1FAEE', '#FFD6A5', '#CAFFBF', '#BDB2FF', '#FFC6FF'],\n"
                "    'category_palette': ['#4361EE', '#E63946', '#2EC4B6', '#FFB703', '#7209B7', '#06D6A0'],\n"
                "}\n"
                "\n"
                "print('✅ All libraries loaded and light visual style configured.')"
            )
        },
        {
            "cell_type": "code",
            "source": (
                "# ── Load Data ───────────────────────────────────────────────────────────\n"
                "sales = pd.read_csv('../generated_data/sales_transactions.csv', parse_dates=['transaction_date'])\n"
                "customers = pd.read_csv('../generated_data/customers.csv', parse_dates=['customer_since'])\n"
                "products = pd.read_csv('../generated_data/products.csv')\n"
                "campaigns = pd.read_csv('../generated_data/campaigns.csv', parse_dates=['start_date', 'end_date'])\n"
                "\n"
                "# ── Enriched Dataset (merge sales + customers + products) ────────────\n"
                "df = sales.merge(customers, on='customer_id', how='left').merge(products, on='product_id', how='left', suffixes=('', '_prod'))\n"
                "\n"
                "# ── Reference date for recency calculations ─────────────────────────\n"
                "analysis_date = pd.Timestamp('2024-12-31')\n"
                "\n"
                "# ── Quick Data Overview ─────────────────────────────────────────────\n"
                "print(f'📦 Sales Transactions : {len(sales):,} rows × {sales.shape[1]} cols')\n"
                "print(f'👥 Customers          : {len(customers):,} rows × {customers.shape[1]} cols')\n"
                "print(f'📦 Products           : {len(products):,} rows × {products.shape[1]} cols')\n"
                "print(f'📣 Campaigns          : {len(campaigns):,} rows × {campaigns.shape[1]} cols')\n"
                "print(f'🔗 Merged DataFrame   : {len(df):,} rows × {df.shape[1]} cols')\n"
                "print(f'\\n📅 Date Range: {sales.transaction_date.min().date()} → {sales.transaction_date.max().date()}')\n"
                "print(f'\\n── Column types ──')\n"
                "print(sales.dtypes.to_string())"
            )
        },
        {
            "cell_type": "code",
            "source": (
                "# ── Data Quality Check ──────────────────────────────────────────────────\n"
                "print('══════════════════════════════════════════════════')\n"
                "print('           DATA QUALITY ASSESSMENT')\n"
                "print('══════════════════════════════════════════════════')\n"
                "\n"
                "print('\\n── Missing Values ──')\n"
                "for name, frame in [('sales', sales), ('customers', customers), ('products', products), ('campaigns', campaigns)]:\n"
                "    missing = frame.isnull().sum()\n"
                "    missing = missing[missing > 0]\n"
                "    if len(missing) > 0:\n"
                "        print(f'\\n{name}:')\n"
                "        print(missing.to_string())\n"
                "    else:\n"
                "        print(f'{name}: ✅ No missing values')\n"
                "\n"
                "print('\\n── Duplicate Transactions ──')\n"
                "dupes = sales.duplicated(subset='transaction_id').sum()\n"
                "print(f'Duplicate transaction_ids: {dupes}')\n"
                "\n"
                "print('\\n── Value Ranges ──')\n"
                "print(f'Net Revenue  : ${sales.net_revenue.min():,.2f} – ${sales.net_revenue.max():,.2f}')\n"
                "print(f'Discount %   : {sales.discount_percentage.min()}% – {sales.discount_percentage.max()}%')\n"
                "print(f'Quantity     : {sales.quantity.min()} – {sales.quantity.max()}')\n"
                "print(f'Gross Margin : ${sales.gross_margin.min():,.2f} – ${sales.gross_margin.max():,.2f}')\n"
                "\n"
                "print('\\n── Interpretation ──')\n"
                "print('The dataset is clean with no missing values or duplicate transaction IDs.')\n"
                "print('Some transactions show negative gross margins, indicating products sold at a loss')\n"
                "print('(likely due to heavy discounting exceeding the product margin). This warrants further investigation.')"
            )
        }
    ]


def build_notebook():
    """Build the complete notebook."""
    from module1_cells import get_module1_cells
    from module2_cells import get_module2_cells

    all_cells = []
    for cell_def in get_setup_cells():
        all_cells.append(make_cell(cell_def["cell_type"], cell_def["source"]))
    for cell_def in get_module1_cells():
        all_cells.append(make_cell(cell_def["cell_type"], cell_def["source"]))
    for cell_def in get_module2_cells():
        all_cells.append(make_cell(cell_def["cell_type"], cell_def["source"]))

    notebook = {
        "cells": all_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbformat_minor": 5,
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    output_path = os.path.join(os.path.dirname(__file__), 'analytics_notebook.ipynb')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print(f'✅ Notebook generated: {output_path}')
    print(f'   Total cells: {len(all_cells)}')
    code_cells = sum(1 for c in all_cells if c["cell_type"] == "code")
    md_cells = sum(1 for c in all_cells if c["cell_type"] == "markdown")
    print(f'   Code cells: {code_cells}, Markdown cells: {md_cells}')


if __name__ == '__main__':
    build_notebook()

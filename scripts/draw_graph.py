#!/usr/bin/env python3
"""
数据可视化脚本
支持平台：macOS, Windows, Linux
用途：绘制数据趋势图

使用方法：
python draw_graph.py [data_file] [output_file]

参数说明：
data_file: 数据文件路径（CSV格式，包含date和value列）
output_file: 输出文件路径（支持PNG、JPG、PDF格式）

"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional
from scripts.utils import get_logger

logger = get_logger(__name__)

sns.set_style("whitegrid")
plt.rcParams["font.sans-serif"] = ["SimHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.figsize"] = [12, 6]
plt.rcParams["figure.dpi"] = 300
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 12
plt.rcParams["legend.fontsize"] = 10


def load_data(file_path: Path) -> pd.DataFrame:
    """
    加载数据文件

    Args:
        file_path: 数据文件路径

    Returns:
        加载的DataFrame
    """
    logger.info(f"开始读取数据文件：{file_path}")

    if not file_path.exists():
        raise FileNotFoundError(f"数据文件不存在：{file_path}")

    if file_path.suffix == '.csv':
        data = pd.read_csv(file_path)
    elif file_path.suffix in ['.xlsx', '.xls']:
        data = pd.read_excel(file_path)
    else:
        raise ValueError(f"不支持的文件格式：{file_path.suffix}，仅支持CSV和Excel格式")

    logger.info(f"成功读取数据文件，共 {len(data)} 行")
    logger.info(f"数据列名：{list(data.columns)}")
    logger.info(f"数据预览：\n{data.head()}")
    logger.info(f"数据统计信息：\n{data.describe()}")

    return data


def validate_data(data: pd.DataFrame) -> tuple:
    """
    验证数据格式并返回日期列和值列

    Args:
        data: 数据DataFrame

    Returns:
        (日期列名, 值列名)
    """
    date_col = None
    value_col = None

    if 'date' in data.columns:
        date_col = 'date'
    elif '日期' in data.columns:
        date_col = '日期'
    else:
        logger.warning("数据中未找到日期列，将使用默认索引")
        data = data.copy()
        data['date'] = pd.date_range(start='2023-01-01', periods=len(data), freq='M')
        date_col = 'date'

    if 'value' in data.columns:
        value_col = 'value'
    elif '指标值' in data.columns:
        value_col = '指标值'
    else:
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            value_col = numeric_cols[0]
        else:
            raise ValueError("数据中必须包含至少一个数值列")

    logger.info(f"使用日期列：{date_col}")
    logger.info(f"使用值列：{value_col}")

    return date_col, value_col


def create_trend_chart(data: pd.DataFrame, date_col: str, value_col: str,
                       title: Optional[str] = None,
                       xlabel: Optional[str] = None,
                       ylabel: Optional[str] = None) -> plt.Figure:
    """
    创建趋势图

    Args:
        data: 数据DataFrame
        date_col: 日期列名
        value_col: 值列名
        title: 图表标题
        xlabel: X轴标签
        ylabel: Y轴标签

    Returns:
        matplotlib图表对象
    """
    logger.info("开始创建趋势图")

    fig, ax = plt.subplots(figsize=(12, 6))

    data[date_col] = pd.to_datetime(data[date_col])
    data = data.sort_values(by=date_col)

    ax.plot(data[date_col], data[value_col],
            marker='o',
            markersize=4,
            linewidth=2,
            label=value_col,
            color='#1f77b4')

    ax.fill_between(data[date_col], data[value_col],
                    alpha=0.3,
                    color='#1f77b4')

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    else:
        ax.set_title('数据趋势图', fontsize=14, fontweight='bold', pad=20)

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    else:
        ax.set_xlabel('日期', fontsize=12)

    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    else:
        ax.set_ylabel('指标值', fontsize=12)

    ax.legend(loc='best', frameon=True, shadow=True)
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    logger.info("成功创建趋势图")
    return fig


def create_comparison_chart(data: pd.DataFrame, date_col: str, value_col: str,
                            show_growth: bool = True) -> plt.Figure:
    """
    创建对比图（包含增长趋势）

    Args:
        data: 数据DataFrame
        date_col: 日期列名
        value_col: 值列名
        show_growth: 是否显示增长率

    Returns:
        matplotlib图表对象
    """
    logger.info("开始创建对比图")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    data[date_col] = pd.to_datetime(data[date_col])
    data = data.sort_values(by=date_col)

    ax1.plot(data[date_col], data[value_col],
             marker='s',
             markersize=5,
             linewidth=2,
             label=value_col,
             color='#2ca02c')

    ax1.fill_between(data[date_col], data[value_col],
                     alpha=0.2,
                     color='#2ca02c')

    ax1.set_title('指标值趋势', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('指标值', fontsize=12)
    ax1.legend(loc='best', frameon=True, shadow=True)
    ax1.grid(True, linestyle='--', alpha=0.7)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    if show_growth and len(data) > 1:
        data['growth'] = data[value_col].pct_change() * 100

        colors = ['#d62728' if x < 0 else '#2ca02c' for x in data['growth'].fillna(0)]
        ax2.bar(data[date_col], data['growth'].fillna(0),
                color=colors,
                alpha=0.7,
                edgecolor='black',
                linewidth=0.5)

        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        ax2.set_title('环比增长率 (%)', fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('日期', fontsize=12)
        ax2.set_ylabel('增长率 (%)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7, axis='y')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    logger.info("成功创建对比图")
    return fig


def save_chart(fig: plt.Figure, output_path: Path) -> None:
    """
    保存图表到文件

    Args:
        fig: matplotlib图表对象
        output_path: 输出文件路径
    """
    logger.info(f"开始保存图表到文件：{output_path}")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path,
                format=output_path.suffix[1:] if output_path.suffix else 'png',
                bbox_inches='tight',
                dpi=300)

    logger.info(f"成功将图表保存到文件：{output_path}")

    plt.close(fig)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("开始数据可视化程序")
    logger.info("=" * 60)

    try:
        if len(sys.argv) < 3:
            logger.error("参数不足")
            print("用法: python draw_graph.py [数据文件] [输出文件]")
            print("示例: python draw_graph.py data.csv output.png")
            print("      python draw_graph.py data.xlsx output.pdf")
            sys.exit(1)

        data_file = sys.argv[1]
        output_file = sys.argv[2]

        logger.info(f"输入数据文件：{data_file}")
        logger.info(f"输出文件：{output_file}")

        data = load_data(Path(data_file))

        date_col, value_col = validate_data(data)

        chart_type = sys.argv[3] if len(sys.argv) > 3 else 'trend'

        if chart_type == 'comparison' or chart_type == 'compare':
            fig = create_comparison_chart(data, date_col, value_col, show_growth=True)
        else:
            fig = create_trend_chart(data, date_col, value_col)

        save_chart(fig, Path(output_file))

        logger.info("=" * 60)
        logger.info("数据可视化完成！")
        logger.info("=" * 60)
        sys.exit(0)

    except FileNotFoundError as e:
        logger.error(f"文件错误：{e}")
        logger.error("请确保数据文件存在，并且路径正确")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"数据格式错误：{e}")
        logger.error("请检查数据文件的格式是否符合要求")
        sys.exit(1)
    except Exception as e:
        logger.error(f"未知错误：{e}")
        logger.exception("程序执行过程中发生错误")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
数据分析脚本
支持平台：macOS, Windows, Linux
用途：分析数据，计算同比增长、环比增长等指标

使用方法：
python analyze.py [data_file] [output_file]

data_file：输入数据文件，格式为CSV/Excel，包含日期、指标值等列
output_file：输出结果文件，格式为CSV/Excel，包含日期、同比增长、环比增长等指标
"""
import sys
import pandas as pd
from pathlib import Path
from typing import Optional
from scripts.utils import get_logger

logger = get_logger(__name__)


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


def validate_data(data: pd.DataFrame) -> bool:
    """
    验证数据格式

    Args:
        data: 数据DataFrame

    Returns:
        验证是否通过
    """
    if 'date' not in data.columns and '日期' not in data.columns:
        logger.warning("数据中未找到日期列，将使用默认索引")
        return False

    date_col = 'date' if 'date' in data.columns else '日期'
    logger.info(f"使用日期列：{date_col}")

    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    if not numeric_cols:
        logger.error("数据中没有数值列")
        raise ValueError("数据中必须包含至少一个数值列")

    logger.info(f"数值列：{numeric_cols}")
    return True


def analyze_data(data: pd.DataFrame, value_column: Optional[str] = None) -> pd.DataFrame:
    """
    分析数据，计算同比、环比等指标

    Args:
        data: 原始数据
        value_column: 值列名称，如果为None则自动选择第一个数值列

    Returns:
        分析后的数据
    """
    logger.info("开始数据处理和分析")

    if 'date' in data.columns:
        date_col = 'date'
    elif '日期' in data.columns:
        date_col = '日期'
    else:
        logger.warning("未找到日期列，将使用默认索引")
        data = data.copy()
        data['date'] = pd.date_range(start='2023-01-01', periods=len(data), freq='M')
        date_col = 'date'

    data[date_col] = pd.to_datetime(data[date_col])
    logger.info(f"成功将日期列转换为datetime类型")

    data = data.set_index(date_col)

    if value_column:
        if value_column not in data.columns:
            raise ValueError(f"指定的列 '{value_column}' 不存在")
        data = data[[value_column]]

    data = data.resample("M").mean()
    logger.info(f"成功将数据按月进行平均值计算")

    data['last_month'] = data['value'].shift(1)
    data['last_year'] = data['value'].shift(12)
    data['same_month_last_year'] = data['value'].shift(12)

    logger.info(f"成功将数据进行时序处理")

    data['same_month_last_year'] = data['same_month_last_year'].fillna(0)
    data['same_month_last_year'] = data['same_month_last_year'].apply(lambda x: x if x > 0 else 0)
    data['same_month_last_year'] = data['same_month_last_year'].fillna(0)

    logger.info(f"成功将缺失值和零值进行处理")

    data['yoy_growth'] = ((data['value'] - data['same_month_last_year']) /
                          data['same_month_last_year'] * 100)
    data['mom_growth'] = ((data['value'] - data['last_month']) /
                          data['last_month'] * 100)

    data['yoy_growth'] = data['yoy_growth'].replace([float('inf'), float('-inf')], 0).fillna(0)
    data['mom_growth'] = data['mom_growth'].replace([float('inf'), float('-inf')], 0).fillna(0)

    logger.info(f"成功计算同比增长和环比增长指标")

    data = data.reset_index()
    logger.info(f"成功将数据处理为最终结果")

    return data


def save_results(data: pd.DataFrame, output_path: Path) -> None:
    """
    保存分析结果

    Args:
        data: 分析后的数据
        output_path: 输出文件路径
    """
    logger.info(f"开始保存结果到文件：{output_path}")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix == '.csv':
        data.to_csv(output_path, index=False, encoding='utf-8-sig')
    elif output_path.suffix in ['.xlsx', '.xls']:
        data.to_excel(output_path, index=False)
    else:
        data.to_csv(output_path.with_suffix('.csv'), index=False, encoding='utf-8-sig')
        output_path = output_path.with_suffix('.csv')

    logger.info(f"成功将数据保存到文件：{output_path}")
    logger.info(f"输出文件包含 {len(data)} 行数据")


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("开始数据分析程序")
    logger.info("=" * 60)

    try:
        data_file = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
        output_file = sys.argv[2] if len(sys.argv) > 2 else "output.csv"

        logger.info(f"输入数据文件：{data_file}")
        logger.info(f"输出结果文件：{output_file}")

        data = load_data(Path(data_file))

        validate_data(data)

        analyzed_data = analyze_data(data)

        save_results(analyzed_data, Path(output_file))

        logger.info("=" * 60)
        logger.info("数据分析完成！")
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

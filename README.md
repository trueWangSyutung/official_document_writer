# 党政公文写作助手

基于 GB/T 9704-2012 国家标准的党政公文写作与格式化工具。

## 功能特性

### 📄 公文生成
- 支持多种公文类型：请示、报告、通知、决定、通报、函等
- 自动生成符合政治要求的公文内容
- 支持自定义发文单位、标题、关键词等元数据

### 🎨 红头标识
- 自动生成规范的红头标识
- 包含单位名称、文件标题、文件编号、日期等核心要素
- 采用红色系配色方案，庄重的黑体/宋体字体

### 🔄 文档格式化
- 严格遵循 GB/T 9704-2012 国家标准
- 自动设置页面布局、字体、行间距等格式
- 支持表格格式化

### 📊 数据分析
- 支持同比增长、环比增长分析
- 生成趋势图、对比图等可视化图表
- 支持 CSV、Excel 数据格式

## 快速开始

### 环境要求
- Python 3.8+
- macOS / Windows / Linux

### 安装依赖

```bash
pip install -r requirements.txt
```

### 字体安装

为确保文档显示正确，建议安装以下字体：
- **方正小标宋简体**：用于公文标题和红头
- **仿宋_GB2312**：用于正文
- **黑体**：用于红头单位名称

## 使用方法

### 1. 格式化 Word 文档

```bash
python scripts/format.py input.docx output.docx
```

### 2. 添加红头标识

```bash
python scripts/format.py input.docx output.docx --red-head \
    --org "发文单位名称" \
    --title "文件标题" \
    --number "文件编号" \
    --date "发文日期"
```

**示例**：
```bash
python scripts/format.py draft.docx official.docx --red-head \
    --org "国央企" \
    --title "关于加强数据安全管理的通知" \
    --number "国央企〔2024〕5号" \
    --date "2024年1月15日"
```

### 3. 数据分析

```bash
python scripts/analyze.py data.csv output.csv
```

### 4. 数据可视化

```bash
# 生成趋势图
python scripts/draw_graph.py data.csv trend.png trend

# 生成对比图
python scripts/draw_graph.py data.csv comparison.png comparison
```

## GB/T 9704-2012 规范要点

### 页面设置
- 纸张：A4（210mm × 297mm）
- 页边距：上3.7cm，下3.5cm，左2.8cm，右2.6cm

### 字体规范
- 标题：方正小标宋简体，二号字，居中
- 正文：仿宋_GB2312，三号字
- 红头单位名称：黑体，二号字，红色

### 段落格式
- 行间距：固定值28磅
- 首行缩进：2字符

## 项目结构

```
├── scripts/
│   ├── format.py      # Word文档格式化工具
│   ├── analyze.py     # 数据分析工具
│   ├── draw_graph.py  # 数据可视化工具
│   └── utils.py       # 通用工具函数
├── references/
│   ├── title-templates.md    # 公文标题模板
│   ├── write.pdf             # 公文基础知识
│   ├── format.pdf            # Word排版规范
│   └── 党政机关公文格式.pdf  # GB/T 9704-2012标准
├── requirements.txt   # Python依赖包
├── SKILL.md           # 技能说明文档
└── README.md          # 项目说明文档
```

## 命令行参数说明

### format.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 输入文件路径 | 必需 |
| output_file | 输出文件路径 | 必需 |
| --red-head | 添加红头标识 | False |
| --org | 单位名称 | 国央企 |
| --title | 文件标题 | 空 |
| --number | 文件编号 | 空 |
| --date | 发文日期 | 空 |

## 示例输出

### 红头格式示例

```
                    国央企

            关于加强数据安全管理的通知

国央企〔2024〕5号
2024年1月15日

────────────────────────────────────────

正文内容...
```

## 注意事项

1. 确保系统已安装所需字体（方正小标宋简体、仿宋_GB2312、黑体）
2. 处理前建议备份原始文档
3. 红头标识仅添加到文档首页顶部
4. 数据分析功能需要输入文件包含日期和数值列

## 故障排除

### Q: 运行脚本时提示 "ModuleNotFoundError"？
A: 缺少必要的Python包，运行 `pip install -r requirements.txt`

### Q: Word文档字体显示不正确？
A: 确保系统已安装方正小标宋简体、仿宋_GB2312、黑体字体

### Q: 红头颜色显示异常？
A: 确保使用的是支持RGB颜色的Word版本

## 许可证

本项目遵循相关开源许可证。

## 联系方式

如有问题或建议，请联系项目作者。
# 课程资料自动整理工具

## 功能
- 按文件**关键字**（作业、练习、实验、任务）优先归类到 `homework/`
- 否则按**后缀**归入 `slides/`、`code/`、`data/`、`documents/`、`images/`、`others/`
- 支持**复制**（默认）或**移动**（`--mode move`）
- **安全**：目标目录已有同名文件时自动重命名（`_1`, `_2`, ...）
- **预览**：`--dry-run` 只显示计划，不操作
- **递归**：`--recursive` 处理子目录
- **过滤**：`--include` / `--exclude` 指定后缀
- **报告**：生成 `整理报告.txt` 或 `整理报告.csv`

## 使用方法
```bash
# 预览整理计划
python main.py --source sample_materials --target organized_materials --dry-run

# 执行整理（默认复制）
python main.py --source sample_materials --target organized_materials

# 移动文件
python main.py --source sample_materials --target organized_materials --mode move

# 递归整理子目录，仅处理 .py 和 .pdf，排除 .txt
python main.py --source sample_materials --target organized_materials --recursive --include .py .pdf --exclude .txt

# 生成 CSV 报告
python main.py --source sample_materials --target organized_materials --csv
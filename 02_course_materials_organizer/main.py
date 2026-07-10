# main.py
import argparse
from pathlib import Path
from course_organizer.core import generate_plan, execute_plan, generate_report

def main():
    parser = argparse.ArgumentParser(description="课程资料自动整理工具")
    parser.add_argument("--source", required=True, help="原始资料目录")
    parser.add_argument("--target", required=True, help="目标整理目录")
    parser.add_argument("--dry-run", action="store_true", help="仅预览整理计划，不实际执行")
    parser.add_argument("--mode", choices=['copy', 'move'], default='copy', help="操作模式：复制或移动")
    parser.add_argument("--recursive", action="store_true", help="递归处理子目录")
    parser.add_argument("--include", nargs='+', help="仅整理指定后缀（如 .py .pdf）")
    parser.add_argument("--exclude", nargs='+', help="排除指定后缀")
    parser.add_argument("--csv", action="store_true", help="整理报告保存为 CSV 格式")
    args = parser.parse_args()

    source = Path(args.source)
    target = Path(args.target)

    # 生成计划
    plan = generate_plan(
        source_dir=source,
        target_dir=target,
        recursive=args.recursive,
        include=args.include,
        exclude=args.exclude
    )

    # 执行
    execute_plan(plan, mode=args.mode, dry_run=args.dry_run)

    # 生成报告（仅当非 dry-run）
    if not args.dry_run and plan:
        generate_report(plan, args.mode, target, csv=args.csv)
        print(f"整理完成！报告已生成在 {target / ('整理报告.csv' if args.csv else '整理报告.txt')}")

if __name__ == "__main__":
    main()
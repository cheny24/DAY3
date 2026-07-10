# course_organizer/core.py
import shutil
from pathlib import Path
from typing import List, Tuple, Optional, Set
from .rules import get_category

def _normalize_ext(ext_list: Optional[List[str]]) -> Optional[Set[str]]:
    """将命令行传入的后缀列表统一为带点的小写集合"""
    if ext_list is None:
        return None
    return {e if e.startswith('.') else f'.{e}' for e in map(str.lower, ext_list)}

def collect_files(
    source_dir: Path,
    recursive: bool = False,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None
) -> List[Path]:
    """收集源目录下所有文件，并按 include/exclude 过滤"""
    if not source_dir.exists():
        raise FileNotFoundError(f"源目录不存在: {source_dir}")
    
    if recursive:
        all_files = list(source_dir.rglob('*'))
    else:
        all_files = list(source_dir.glob('*'))
    
    files = [f for f in all_files if f.is_file()]
    
    include_set = _normalize_ext(include)
    exclude_set = _normalize_ext(exclude)
    
    if include_set:
        files = [f for f in files if f.suffix.lower() in include_set]
    if exclude_set:
        files = [f for f in files if f.suffix.lower() not in exclude_set]
    
    return files

def get_unique_path(target_dir: Path, filename: str) -> Path:
    """
    在 target_dir 下生成唯一的文件路径。
    若文件名已存在，则在 stem 后加 _1, _2, ...
    """
    dest = target_dir / filename
    if not dest.exists():
        return dest
    
    stem = dest.stem
    suffix = dest.suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_dest = target_dir / new_name
        if not new_dest.exists():
            return new_dest
        counter += 1

def generate_plan(
    source_dir: Path,
    target_dir: Path,
    recursive: bool = False,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None
) -> List[Tuple[Path, Path]]:
    """
    生成整理计划：每个元素为 (源文件路径, 目标文件路径)
    注意：目标路径会确保唯一性，不会覆盖已有文件。
    """
    files = collect_files(source_dir, recursive, include, exclude)
    plan = []
    for src in files:
        category = get_category(src.name)
        dest_dir = target_dir / category
        dest_path = get_unique_path(dest_dir, src.name)
        plan.append((src, dest_path))
    return plan

def execute_plan(plan: List[Tuple[Path, Path]], mode: str = 'copy', dry_run: bool = False):
    """
    执行整理计划。
    mode: 'copy' 或 'move'
    dry_run: 若为 True，仅打印计划，不执行实际操作。
    """
    if dry_run:
        print("[Dry Run] 以下为整理计划：")
        for src, dst in plan:
            print(f"  {src} -> {dst}")
        print(f"共 {len(plan)} 个文件")
        return

    # 实际执行
    action = shutil.copy2 if mode == 'copy' else shutil.move
    for src, dst in plan:
        dst.parent.mkdir(parents=True, exist_ok=True)
        action(src, dst)

def generate_report(
    plan: List[Tuple[Path, Path]],
    mode: str,
    target_dir: Path,
    csv: bool = False
) -> None:
    """
    在目标目录生成整理报告。
    若 csv=True，生成 CSV 格式；否则生成文本格式。
    """
    if not plan:
        return  # 无文件则不生成报告

    target_dir.mkdir(parents=True, exist_ok=True)
    report_path = target_dir / ('整理报告.csv' if csv else '整理报告.txt')
    
    # 统计每个类别文件数
    from collections import Counter
    categories = [dst.parent.name for _, dst in plan]
    counter = Counter(categories)

    lines = []
    if csv:
        lines.append("源路径,目标路径,类别")
        for src, dst in plan:
            lines.append(f"{src},{dst},{dst.parent.name}")
        lines.append("")
        lines.append("类别统计")
        for cat, cnt in counter.items():
            lines.append(f"{cat},{cnt}")
    else:
        lines.append(f"本次执行的是: {mode}")
        lines.append(f"整理文件总数: {len(plan)}\n")
        lines.append("每个文件的来源与去向：")
        for src, dst in plan:
            lines.append(f"  {src} -> {dst}")
        lines.append("\n各类别文件数量：")
        for cat, cnt in counter.items():
            lines.append(f"  {cat}: {cnt}")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
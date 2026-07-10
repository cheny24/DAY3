# course_organizer/rules.py
from pathlib import Path

# 关键字（优先级最高）
KEYWORDS = ['作业', '练习', '实验', '任务']

# 后缀 → 目标子目录
EXT_RULES = {
    '.ppt': 'slides',
    '.pptx': 'slides',
    '.key': 'slides',
    '.py': 'code',
    '.ipynb': 'code',
    '.c': 'code',
    '.cpp': 'code',
    '.java': 'code',
    '.csv': 'data',
    '.xlsx': 'data',
    '.json': 'data',
    '.pdf': 'documents',
    '.doc': 'documents',
    '.docx': 'documents',
    '.txt': 'documents',
    '.md': 'documents',
    '.png': 'images',
    '.jpg': 'images',
    '.jpeg': 'images',
    '.gif': 'images',
}

def get_category(filename: str) -> str:
    """
    根据文件名决定目标子目录。
    优先检查关键字，其次按后缀匹配，最后归入 'others'。
    """
    for kw in KEYWORDS:
        if kw in filename:
            return 'homework'
    ext = Path(filename).suffix.lower()
    return EXT_RULES.get(ext, 'others')
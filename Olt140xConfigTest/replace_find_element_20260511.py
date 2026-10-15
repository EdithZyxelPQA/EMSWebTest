import re
import os
from pathlib import Path

# 定義所有替換規則
REPLACEMENTS = [
    (r'find_element_by_class_name\(', 'find_element(By.CLASS_NAME, '),
    (r'find_elements_by_class_name\(', 'find_elements(By.CLASS_NAME, '),
    (r'find_element_by_id\(', 'find_element(By.ID, '),
    (r'find_elements_by_id\(', 'find_elements(By.ID, '),
    (r'find_element_by_xpath\(', 'find_element(By.XPATH, '),
    (r'find_elements_by_xpath\(', 'find_elements(By.XPATH, '),
    (r'find_element_by_name\(', 'find_element(By.NAME, '),
    (r'find_elements_by_name\(', 'find_elements(By.NAME, '),
    (r'find_element_by_css_selector\(', 'find_element(By.CSS_SELECTOR, '),
    (r'find_elements_by_css_selector\(', 'find_elements(By.CSS_SELECTOR, '),
    (r'find_element_by_tag_name\(', 'find_element(By.TAG_NAME, '),
    (r'find_elements_by_tag_name\(', 'find_elements(By.TAG_NAME, '),
    (r'find_element_by_link_text\(', 'find_element(By.LINK_TEXT, '),
    (r'find_elements_by_link_text\(', 'find_elements(By.LINK_TEXT, '),
    (r'find_element_by_partial_link_text\(', 'find_element(By.PARTIAL_LINK_TEXT, '),
    (r'find_elements_by_partial_link_text\(', 'find_elements(By.PARTIAL_LINK_TEXT, '),
]

def migrate_file(filepath: Path, dry_run=True):
    original = filepath.read_text(encoding='utf-8')
    result = original

    for pattern, replacement in REPLACEMENTS:
        result = re.sub(pattern, replacement, result)

    if result == original:
        return False  # 沒有變更

    if dry_run:
        print(f"[DRY RUN] 會修改: {filepath}")
    else:
        filepath.write_text(result, encoding='utf-8')
        print(f"已修改: {filepath}")
    return True

def migrate_project(root_dir='.', dry_run=True):
    root = Path(root_dir)
    changed = []

    for py_file in root.rglob('*.py'):
        if migrate_file(py_file, dry_run=dry_run):
            changed.append(py_file)

    print(f"\n{'[DRY RUN] ' if dry_run else ''}共 {len(changed)} 個檔案{'需要' if dry_run else '已'}修改")
    return changed

# 先 dry run 確認影響範圍
#migrate_project('.', dry_run=True)

# # 確認沒問題後，改成 False 正式執行
migrate_project('.', dry_run=False)



BY_IMPORT = 'from selenium.webdriver.common.by import By\n'

for py_file in Path('.').rglob('*.py'):
    content = py_file.read_text(encoding='utf-8')
    if 'find_element(By.' in content and BY_IMPORT.strip() not in content:
        py_file.write_text(BY_IMPORT + content, encoding='utf-8')
        print(f"補 import: {py_file}")
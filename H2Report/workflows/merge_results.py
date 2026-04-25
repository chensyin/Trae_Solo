import json
import sys
from urllib.parse import urlparse

def normalize_entry(entry):
    """标准化条目结构，统一字段名"""
    # 检查是哪种格式
    if 'url' in entry:
        url = entry['url']
        keywords = entry.get('keywords', [])
    elif 'link' in entry:
        url = entry['link']
        keywords = entry.get('keyword_tags', [])
    else:
        raise ValueError(f"未知的条目格式: {entry}")
    
    # 确保URL格式一致（可选：去除片段和查询参数）
    parsed = urlparse(url)
    normalized_url = parsed._replace(fragment='', query='').geturl()
    
    return {
        'url': normalized_url,
        'original_url': url,  # 保留原始URL用于参考
        'title': entry.get('title', ''),
        'summary': entry.get('summary', ''),
        'publish_date': entry.get('publish_date', ''),
        'keywords': keywords if isinstance(keywords, list) else []
    }

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        return json.load(f)

def main():
    # 文件路径
    file1 = 'search-results-round1-cleaned.json'
    file2 = 'search-results-round2.json'
    
    # 加载数据
    data1 = load_json_file(file1)
    data2 = load_json_file(file2)
    
    # 标准化所有条目
    normalized_entries = []
    for entry in data1:
        normalized_entries.append(normalize_entry(entry))
    for entry in data2:
        normalized_entries.append(normalize_entry(entry))
    
    # 基于URL去重
    seen_urls = set()
    unique_entries = []
    for entry in normalized_entries:
        url = entry['url']
        if url not in seen_urls:
            seen_urls.add(url)
            unique_entries.append(entry)
    
    # 重新分配ID（可选）
    for idx, entry in enumerate(unique_entries):
        entry['id'] = idx + 1
    
    # 输出合并后的JSON
    output_file = 'search-results-merged.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_entries, f, ensure_ascii=False, indent=2)
    
    print(f"合并完成，共 {len(unique_entries)} 个唯一条目，已保存到 {output_file}")
    
    # 打印一些统计信息
    print(f"原始条目数: round1={len(data1)}, round2={len(data2)}, 总计={len(data1)+len(data2)}")
    print(f"去重后条目数: {len(unique_entries)}")

if __name__ == '__main__':
    main()
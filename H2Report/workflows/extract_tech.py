import json
import sys
import os

def extract_technology_entries(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 定义技术相关关键词
    tech_keywords = ['技术', '制氢', '储氢', '运氢', '加氢', '用氢', '突破', '专利', '研发', '创新', '成果', '项目', '系统', '设备', '装置', '电解', '催化剂', '膜', '电池', '燃料电池', '储运', '加注', '应用']
    
    tech_entries = []
    
    for entry in data:
        # 检查分类
        category = entry.get('category', '')
        title = entry.get('title', '')
        summary = entry.get('summary', '')
        keywords = entry.get('keywords', [])
        
        # 判断是否与技术相关
        is_tech = False
        
        # 如果分类是"重要信息"或包含"技术"关键词
        if '技术' in category:
            is_tech = True
        elif '重要信息' in category or '其他相关信息' in category:
            # 检查标题、摘要、关键词中是否包含技术关键词
            text = title + ' ' + summary + ' ' + ' '.join(keywords)
            for kw in tech_keywords:
                if kw in text:
                    is_tech = True
                    break
        else:
            # 对于政策解读，只保留明确提及技术突破的
            text = title + ' ' + summary + ' ' + ' '.join(keywords)
            tech_mention = any(kw in text for kw in ['技术', '突破', '研发', '创新', '专利'])
            if tech_mention:
                is_tech = True
        
        if is_tech:
            tech_entries.append(entry)
    
    return tech_entries

def main():
    json_file = 'search-results-merged.json'
    if not os.path.exists(json_file):
        print(f"文件 {json_file} 不存在")
        sys.exit(1)
    
    tech_entries = extract_technology_entries(json_file)
    
    print(f"共找到 {len(tech_entries)} 个技术相关条目")
    
    # 输出到控制台供检查
    for i, entry in enumerate(tech_entries):
        print(f"\n{i+1}. ID: {entry.get('id')}")
        print(f"   标题: {entry.get('title')}")
        print(f"   分类: {entry.get('category')}")
        print(f"   关键词: {entry.get('keywords')}")
        print(f"   摘要: {entry.get('summary')[:100]}...")
    
    # 保存到新JSON文件以便后续处理
    output_file = 'technology-entries.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tech_entries, f, ensure_ascii=False, indent=2)
    
    print(f"\n技术相关条目已保存到 {output_file}")

if __name__ == '__main__':
    main()
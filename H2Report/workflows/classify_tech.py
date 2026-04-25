import json
import os
from collections import defaultdict

def classify_entries(entries):
    categories = {
        '制氢': [],
        '储氢': [],
        '运氢': [],
        '加氢': [],
        '用氢': [],
        '其他技术': []
    }
    
    # 定义每个类别的关键词
    category_keywords = {
        '制氢': ['制氢', '电解', '电解水', '电解槽', '碱性电解水', 'PEM', 'AEM', '海水制氢', '绿氢生产', '制氢装备', '制氢系统', '制氢成本', '制氢技术'],
        '储氢': ['储氢', '储运', '固态储氢', '储氢罐', '储氢技术'],
        '运氢': ['运氢', '运输', '输氢', '管道', '输送'],
        '加氢': ['加氢', '加注', '加氢站'],
        '用氢': ['用氢', '应用', '氢能重卡', '燃料电池', '航空发动机', '液氢航空发动机', '工业用氢', '氢能车', '氢能商业化']
    }
    
    for entry in entries:
        title = entry.get('title', '')
        summary = entry.get('summary', '')
        keywords = entry.get('keywords', [])
        
        text = title + ' ' + summary + ' ' + ' '.join(keywords)
        
        # 检查每个类别
        matched_categories = []
        for category, kw_list in category_keywords.items():
            for kw in kw_list:
                if kw in text:
                    matched_categories.append(category)
                    break  # 每个类别匹配一次即可
        
        # 去重
        matched_categories = list(set(matched_categories))
        
        if matched_categories:
            # 如果匹配到多个类别，选择第一个（或全部保留？这里我们分配到一个主要类别）
            # 这里我们分配到所有匹配的类别，但为了简化，只分配到一个主要类别
            # 我们选择第一个匹配的类别
            main_category = matched_categories[0]
        else:
            main_category = '其他技术'
        
        # 添加到对应类别
        categories[main_category].append(entry)
    
    return categories

def extract_breakthrough_info(entries):
    breakthrough_entries = []
    for entry in entries:
        title = entry.get('title', '')
        summary = entry.get('summary', '')
        keywords = entry.get('keywords', [])
        
        text = title + ' ' + summary + ' ' + ' '.join(keywords)
        
        # 检查突破性关键词
        breakthrough_keywords = ['突破', '首次', '首创', '里程碑', '重大', '革命', '革新', '创新', '领先', '领先技术']
        for kw in breakthrough_keywords:
            if kw in text:
                breakthrough_entries.append(entry)
                break
    
    return breakthrough_entries

def generate_markdown(categories, breakthrough_entries, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('# 氢能技术信息汇总\n\n')
        f.write('基于 `workflows/search-results-merged.json` 文件提取的技术相关信息，按氢能产业链环节分类整理。\n\n')
        
        f.write('## 概述\n\n')
        f.write(f'- 总计技术相关条目: {sum(len(v) for v in categories.values())}\n')
        for category, entries in categories.items():
            f.write(f'- {category}: {len(entries)} 条\n')
        f.write(f'- 突破性技术条目: {len(breakthrough_entries)} 条\n\n')
        
        f.write('## 一、制氢技术\n\n')
        if categories['制氢']:
            for entry in categories['制氢']:
                f.write(f'### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无相关信息\n\n')
        
        f.write('## 二、储氢技术\n\n')
        if categories['储氢']:
            for entry in categories['储氢']:
                f.write(f'### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无相关信息\n\n')
        
        f.write('## 三、运氢技术\n\n')
        if categories['运氢']:
            for entry in categories['运氢']:
                f.write(f'### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无相关信息\n\n')
        
        f.write('## 四、加氢技术\n\n')
        if categories['加氢']:
            for entry in categories['加氢']:
                f.write(f'### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无相关信息\n\n')
        
        f.write('## 五、用氢技术\n\n')
        if categories['用氢']:
            for entry in categories['用氢']:
                f.write(f'### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无相关信息\n\n')
        
        f.write('## 六、其他相关技术\n\n')
        if categories['其他技术']:
            for entry in categories['其他技术']:
                f.write(f'### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无相关信息\n\n')
        
        f.write('## 七、突破性技术与专利信息\n\n')
        if breakthrough_entries:
            f.write('以下条目涉及突破性技术或重要技术进展：\n\n')
            for entry in breakthrough_entries:
                f.write(f'### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无明确的突破性技术或专利信息\n\n')
        
        f.write('---\n')
        f.write('*最后更新: 2026-04-18*\n')
        f.write('*数据来源: workflows/search-results-merged.json*\n')

def main():
    input_file = 'technology-entries.json'
    if not os.path.exists(input_file):
        print(f"文件 {input_file} 不存在")
        return
    
    with open(input_file, 'r', encoding='utf-8') as f:
        entries = json.load(f)
    
    print(f"共读取 {len(entries)} 个技术相关条目")
    
    # 分类
    categories = classify_entries(entries)
    
    # 统计
    for category, entries_list in categories.items():
        print(f"{category}: {len(entries_list)} 条")
    
    # 提取突破性技术
    breakthrough_entries = extract_breakthrough_info(entries)
    print(f"突破性技术条目: {len(breakthrough_entries)} 条")
    
    # 生成markdown
    output_file = 'technology-summary.md'
    generate_markdown(categories, breakthrough_entries, output_file)
    print(f"技术信息汇总已保存到 {output_file}")

if __name__ == '__main__':
    main()
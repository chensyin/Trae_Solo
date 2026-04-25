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
    
    # 定义每个类别的关键词和优先级
    # 每个条目可以匹配多个类别，我们选择匹配度最高的
    category_keywords = {
        '制氢': ['制氢', '电解', '电解水', '电解槽', '碱性电解水', 'PEM', 'AEM', '海水制氢', '绿氢生产', '制氢装备', '制氢系统', '制氢成本', '制氢技术', '电解槽新增订单', '兆瓦级制氢系统'],
        '储氢': ['储氢', '储运', '固态储氢', '储氢罐', '储氢技术', '储氢罐'],
        '运氢': ['运氢', '运输', '输氢', '管道', '输送', '出海', '运送', '物流'],
        '加氢': ['加氢', '加注', '加氢站', '加注站'],
        '用氢': ['用氢', '应用', '氢能重卡', '燃料电池', '航空发动机', '液氢航空发动机', '工业用氢', '氢能车', '氢能商业化', '氢能综合应用试点', '氢能全产业链', '氢能产业化', '氢能展会', '氢能展']
    }
    
    for entry in entries:
        title = entry.get('title', '')
        summary = entry.get('summary', '')
        keywords = entry.get('keywords', [])
        
        text = title + ' ' + summary + ' ' + ' '.join(keywords)
        
        # 计算每个类别的匹配分数
        scores = {category: 0 for category in categories.keys()}
        
        for category, kw_list in category_keywords.items():
            for kw in kw_list:
                if kw in text:
                    scores[category] += 1
        
        # 找出最高分数的类别
        max_score = max(scores.values())
        if max_score == 0:
            main_category = '其他技术'
        else:
            # 如果有多个类别分数相同，按优先级选择：制氢 > 储氢 > 运氢 > 加氢 > 用氢
            priority_order = ['制氢', '储氢', '运氢', '加氢', '用氢']
            for category in priority_order:
                if scores[category] == max_score:
                    main_category = category
                    break
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
        breakthrough_keywords = ['突破', '首次', '首创', '里程碑', '重大', '革命', '革新', '创新', '领先', '领先技术', '技术突破', '全链条突破']
        for kw in breakthrough_keywords:
            if kw in text:
                breakthrough_entries.append(entry)
                break
    
    return breakthrough_entries

def extract_patent_info(entries):
    patent_entries = []
    for entry in entries:
        title = entry.get('title', '')
        summary = entry.get('summary', '')
        keywords = entry.get('keywords', [])
        
        text = title + ' ' + summary + ' ' + ' '.join(keywords)
        
        # 检查专利关键词
        patent_keywords = ['专利', '知识产权', '发明专利', '实用新型', '专利授权']
        for kw in patent_keywords:
            if kw in text:
                patent_entries.append(entry)
                break
    
    return patent_entries

def generate_markdown(categories, breakthrough_entries, patent_entries, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('# 氢能技术信息汇总\n\n')
        f.write('基于 `workflows/search-results-merged.json` 文件提取的技术相关信息，按氢能产业链环节分类整理。\n\n')
        
        f.write('## 概述\n\n')
        f.write(f'- 总计技术相关条目: {sum(len(v) for v in categories.values())}\n')
        for category, entries in categories.items():
            f.write(f'- {category}: {len(entries)} 条\n')
        f.write(f'- 突破性技术条目: {len(breakthrough_entries)} 条\n')
        f.write(f'- 专利相关信息条目: {len(patent_entries)} 条\n\n')
        
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
        
        f.write('### 突破性技术\n\n')
        if breakthrough_entries:
            f.write('以下条目涉及突破性技术或重要技术进展：\n\n')
            for entry in breakthrough_entries:
                f.write(f'#### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('暂无明确的突破性技术信息\n\n')
        
        f.write('### 专利信息\n\n')
        if patent_entries:
            f.write('以下条目涉及专利或知识产权信息：\n\n')
            for entry in patent_entries:
                f.write(f'#### {entry.get("title")}\n')
                f.write(f'- **ID**: {entry.get("id")}\n')
                f.write(f'- **发布时间**: {entry.get("publish_date")}\n')
                f.write(f'- **关键词**: {", ".join(entry.get("keywords", []))}\n')
                f.write(f'- **摘要**: {entry.get("summary")}\n')
                f.write(f'- **来源**: {entry.get("url")}\n\n')
        else:
            f.write('本次收集的数据中未发现明确的专利信息。\n\n')
        
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
    
    # 提取专利信息
    patent_entries = extract_patent_info(entries)
    print(f"专利信息条目: {len(patent_entries)} 条")
    
    # 生成markdown
    output_file = 'technology-summary.md'
    generate_markdown(categories, breakthrough_entries, patent_entries, output_file)
    print(f"技术信息汇总已保存到 {output_file}")

if __name__ == '__main__':
    main()
import json

def categorize_entry(entry):
    """根据标题、摘要和关键词对条目进行分类"""
    title = entry.get('title', '').lower()
    summary = entry.get('summary', '').lower()
    keywords = [k.lower() for k in entry.get('keywords', [])]
    
    # 政策解读类别关键词
    policy_keywords = ['政策', '通知', '试点', '解读', '报告', '分析', '研究', '补贴', '奖励', '财政', '部署', '工作方案', '揭榜挂帅', '以奖代补']
    policy_keywords_en = ['policy', 'notification', 'pilot', 'interpretation', 'report', 'analysis', 'research', 'subsidy', 'reward']
    
    # 重要信息类别关键词
    important_keywords = ['突破', '首例', '首个', '首次', '重大', '重要', '关键', '里程碑', '成就', '成功', '完成', '签约', '合作', '投资', '融资', '订单', '成本降', '价格降', '氢价', '运行超', '小时', '量产', '商业化', '规模']
    important_keywords_en = ['breakthrough', 'first', 'major', 'key', 'milestone', 'achievement', 'success', 'complete', 'sign', 'cooperation', 'investment', 'financing', 'order', 'cost reduction', 'price reduction']
    
    # 检查是否属于政策解读
    text = title + ' ' + summary
    for kw in policy_keywords + policy_keywords_en:
        if kw in text:
            return '政策解读'
    
    # 检查是否属于重要信息
    for kw in important_keywords + important_keywords_en:
        if kw in text:
            return '重要信息'
    
    # 默认归类为其他相关信息
    return '其他相关信息'

def main():
    # 读取合并后的JSON文件
    merged_file = 'search-results-merged.json'
    with open(merged_file, 'r', encoding='utf-8-sig') as f:
        entries = json.load(f)
    
    # 为每个条目添加分类
    for entry in entries:
        entry['category'] = categorize_entry(entry)
    
    # 更新合并后的JSON文件（添加分类字段）
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    
    print(f"已为 {len(entries)} 个条目添加分类，并更新了 {merged_file}")
    
    # 创建分类索引的Markdown文件
    categorized_file = 'search-results-categorized.md'
    with open(categorized_file, 'w', encoding='utf-8') as f:
        f.write('# 氢能政策与市场信息分类索引\n\n')
        f.write('根据报告结构初步分类：重要信息、其他相关信息、政策解读。\n\n')
        
        # 按类别分组
        categories = {}
        for entry in entries:
            cat = entry['category']
            categories.setdefault(cat, []).append(entry)
        
        # 定义类别顺序
        category_order = ['重要信息', '政策解读', '其他相关信息']
        for cat in category_order:
            if cat not in categories:
                continue
            f.write(f'## {cat}\n\n')
            for entry in categories[cat]:
                # 格式化条目
                f.write(f'### {entry["title"]}\n')
                f.write(f'- **URL**: [{entry["original_url"]}]({entry["original_url"]})\n')
                f.write(f'- **发布日期**: {entry["publish_date"]}\n')
                f.write(f'- **关键词**: {", ".join(entry["keywords"])}\n')
                f.write(f'- **摘要**: {entry["summary"]}\n')
                f.write(f'- **ID**: {entry["id"]}\n')
                f.write('\n')
        
        # 统计信息
        f.write('## 统计信息\n\n')
        f.write(f'- 总条目数: {len(entries)}\n')
        for cat in category_order:
            if cat in categories:
                f.write(f'- {cat}: {len(categories[cat])} 条\n')
    
    print(f"分类索引已保存到 {categorized_file}")
    
    # 打印分类统计
    print("\n分类统计:")
    for cat, items in categories.items():
        print(f"  {cat}: {len(items)} 条")

if __name__ == '__main__':
    main()
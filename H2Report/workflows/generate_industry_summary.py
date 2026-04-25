import json
import os

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_industry_items(data):
    """筛选类别为'重要信息'和'其他相关信息'的条目"""
    target_categories = ['重要信息', '其他相关信息']
    return [item for item in data if item.get('category') in target_categories]

def categorize_by_industry_chain(items):
    """按产业链环节分类"""
    categories = {
        '制氢': [],
        '储运': [],
        '加注': [],
        '应用（交通）': [],
        '应用（工业）': [],
        '应用（发电）': [],
        '设备制造': [],
        '材料与部件': [],
        '研发与标准': [],
        '产业政策与市场': [],
        '其他': []
    }
    
    keywords_mapping = {
        '制氢': ['制氢', '电解', '电解槽', '电解水', 'PEM', 'AEM', '碱性', '海水制氢', '工厂化海水制氢', '绿氢', '灰氢', '蓝氢', '煤炭制氢', '天然气制氢', '甲醇制氢', '丙烷制氢'],
        '储运': ['储氢', '储运', '运输', '储罐', '固态储氢', '液氢', '输氢', '管道', '储氢罐', '集装箱', '出海'],
        '加注': ['加氢', '加注', '加氢站'],
        '应用（交通）': ['氢能车', '燃料电池汽车', '氢能重卡', '氢能汽车', '氢能船舶', '氢能航空', '航空发动机', '液氢航空'],
        '应用（工业）': ['工业用氢', '化工', '炼化', '合成氨', '甲醇', '钢铁', '工业'],
        '应用（发电）': ['发电', '燃料电池', '热电联产'],
        '设备制造': ['设备', '装备', '电解槽', '制氢系统', '制氢装备', '燃料电池', '发动机'],
        '材料与部件': ['材料', '部件', '电极', '膜', '催化剂', '质子交换膜'],
        '研发与标准': ['研发', '标准', '技术突破', '创新', '科研', '验证', '实验'],
        '产业政策与市场': ['政策', '市场', '补贴', '试点', '规划', '产业', '产业链', '商业化', '展览', '展会', '报告', '规模', '产能', '成本', '价格', '投资']
    }
    
    for item in items:
        title = item.get('title', '')
        summary = item.get('summary', '')
        keywords = item.get('keywords', [])
        text = title + ' ' + summary + ' ' + ' '.join(keywords)
        assigned = False
        
        for category, keywords_list in keywords_mapping.items():
            if any(keyword in text for keyword in keywords_list):
                categories[category].append(item)
                assigned = True
                break
        if not assigned:
            categories['其他'].append(item)
    
    return categories

def extract_project_info(items):
    """提取项目信息（立项、审批、招标、建设、验收等）"""
    projects = []
    for item in items:
        title = item.get('title', '')
        summary = item.get('summary', '')
        stages = []
        if any(word in title+summary for word in ['立项', '启动', '揭榜挂帅', '试点']):
            stages.append('立项')
        if any(word in title+summary for word in ['审批', '批准', '批复', '备案']):
            stages.append('审批')
        if any(word in title+summary for word in ['招标', '中标', '订单', '签约', '合同']):
            stages.append('招标')
        if any(word in title+summary for word in ['建设', '建造', '施工', '安装', '工程']):
            stages.append('建设')
        if any(word in title+summary for word in ['验收', '运行', '运营', '投产', '完成', '成功', '稳定运行', '验证', '测试']):
            stages.append('验收/运行')
        if stages:
            projects.append({
                'item': item,
                'stages': stages
            })
    return projects

def extract_company_dynamics(items):
    """提取企业动态（合作、签约、融资、发布产品等）"""
    company_items = []
    for item in items:
        title = item.get('title', '')
        summary = item.get('summary', '')
        if any(word in title+summary for word in ['合作', '签约', '联手', '合资', '联盟', '合作', '协议', '战略合作']):
            company_items.append((item, '合作'))
        if any(word in title+summary for word in ['融资', '投资', '募资', '上市']):
            company_items.append((item, '融资'))
        if any(word in title+summary for word in ['发布', '推出', '新产品', '新设备', '新系统']):
            company_items.append((item, '产品发布'))
        if any(word in title+summary for word in ['突破', '首创', '首次', '领先']):
            company_items.append((item, '技术突破'))
    return company_items

def generate_markdown(categorized, projects, company_dynamics):
    """生成Markdown内容"""
    lines = []
    lines.append('# 氢能产业信息汇总')
    lines.append('')
    lines.append('> 基于 `workflows/search-results-merged.json` 文件提取，筛选分类为"重要信息"和"其他相关信息"的产业相关条目。')
    lines.append('')
    lines.append('## 概述')
    lines.append('')
    total_items = sum(len(items) for items in categorized.values())
    lines.append(f'- **总条目数**: {total_items}条（重要信息+其他相关信息）')
    lines.append(f'- **项目信息**: {len(projects)}个')
    lines.append(f'- **企业动态**: {len(company_dynamics)}条')
    lines.append('')
    
    lines.append('## 一、按产业链环节分类')
    lines.append('')
    for category, items in categorized.items():
        if items:
            lines.append(f'### {category} ({len(items)}条)')
            lines.append('')
            for item in items:
                lines.append(f'#### {item["title"]}')
                lines.append('')
                lines.append(f'- **ID**: {item["id"]}')
                lines.append(f'- **分类**: {item["category"]}')
                lines.append(f'- **发布时间**: {item["publish_date"]}')
                lines.append(f'- **原文链接**: [{item["url"][:50]}...]({item["url"]})')
                lines.append(f'- **关键词**: {", ".join(item["keywords"])}')
                lines.append(f'- **内容摘要**: {item["summary"]}')
                lines.append('')
    lines.append('')
    
    lines.append('## 二、项目信息（按阶段分类）')
    lines.append('')
    stage_groups = {}
    for proj in projects:
        for stage in proj['stages']:
            if stage not in stage_groups:
                stage_groups[stage] = []
            stage_groups[stage].append(proj['item'])
    
    for stage, items in stage_groups.items():
        lines.append(f'### {stage} ({len(items)}个)')
        lines.append('')
        for item in items:
            lines.append(f'- **{item["title"]}** (ID:{item["id"]})')
            lines.append(f'  - 摘要: {item["summary"][:100]}...')
            lines.append('')
    lines.append('')
    
    lines.append('## 三、企业动态')
    lines.append('')
    dyn_groups = {}
    for item, dyn_type in company_dynamics:
        if dyn_type not in dyn_groups:
            dyn_groups[dyn_type] = []
        dyn_groups[dyn_type].append(item)
    
    for dyn_type, items in dyn_groups.items():
        lines.append(f'### {dyn_type} ({len(items)}条)')
        lines.append('')
        for item in items:
            lines.append(f'- **{item["title"]}** (ID:{item["id"]})')
            lines.append(f'  - 摘要: {item["summary"][:100]}...')
            lines.append('')
    lines.append('')
    
    lines.append('## 四、主要企业动态汇总')
    lines.append('')
    companies = set()
    all_items = sum(categorized.values(), [])
    known_companies = ['稳石氢能', '国富氢能', '昊臻氢能', '航天工程', '东方电气', '中石化', '深圳大学', '四川大学', '青岛炼化', '中信证券', '中国航发', '上海外高桥', '中国氢能联盟', '中国石化', '中国石油', '马来西亚国家石油公司', '陕西理谷新能源', '上海外高桥港区']
    for item in all_items:
        text = item['title'] + item['summary']
        for company in known_companies:
            if company in text:
                companies.add(company)
    
    for company in sorted(companies):
        lines.append(f'### {company}')
        lines.append('')
        related_items = []
        for item in all_items:
            if company in item['title'] or company in item['summary']:
                related_items.append(item)
        for item in related_items:
            lines.append(f'- **{item["title"]}** (ID:{item["id"]})')
            lines.append(f'  - 发布时间: {item["publish_date"]}')
            lines.append(f'  - 摘要: {item["summary"][:80]}...')
            lines.append('')
    lines.append('')
    
    lines.append('---')
    lines.append('*生成时间: 2026-04-18*')
    lines.append('*数据源: search-results-merged.json*')
    
    return '\n'.join(lines)

def main():
    json_path = r'y:\Trae_Solo\H2Report\workflows\search-results-merged.json'
    if not os.path.exists(json_path):
        print("JSON文件不存在")
        return
    
    data = load_json(json_path)
    print(f"总共 {len(data)} 条条目")
    
    industry_items = filter_industry_items(data)
    print(f"筛选出 {len(industry_items)} 条产业相关条目（重要信息+其他相关信息）")
    
    categorized = categorize_by_industry_chain(industry_items)
    projects = extract_project_info(industry_items)
    company_dynamics = extract_company_dynamics(industry_items)
    
    md_content = generate_markdown(categorized, projects, company_dynamics)
    
    output_path = r'y:\Trae_Solo\H2Report\workflows\industry-summary.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"产业信息汇总已保存到: {output_path}")

if __name__ == '__main__':
    main()
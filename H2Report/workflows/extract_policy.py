import json
import re

def extract_agency_from_url(url):
    """从URL中提取发布机构"""
    if 'xinhuanet.com' in url:
        return '新华网'
    elif 'mof.gov.cn' in url:
        return '财政部'
    elif 'gmw.cn' in url:
        return '光明网'
    elif 'cnr.cn' in url:
        return '央广网'
    elif 'jxt.hubei.gov.cn' in url:
        return '湖北省经济和信息化厅'
    elif 'toutiao.com' in url:
        return '今日头条'
    elif 'baike.com' in url:
        return '快懂百科'
    elif 'caifuhao.eastmoney.com' in url:
        return '东方财富'
    elif 'chinanews.ai' in url:
        return '中新网'
    elif 'dialogue.earth' in url:
        return 'Dialogue Earth'
    elif 'xueqiu.com' in url:
        return '雪球'
    elif '36kr.com' in url:
        return '36氪'
    elif 'citics.com' in url:
        return '中信证券'
    elif 'people.cn' in url:
        return '人民网'
    elif 'cctv.com' in url:
        return '央视网'
    elif '163.com' in url:
        return '网易'
    elif 'sina.cn' in url:
        return '新浪'
    elif 'ccin.com.cn' in url:
        return '中化新网'
    elif 'metal.com' in url:
        return '上海金属网'
    elif 'hydrogenenergyexpo.cn' in url:
        return '中国国际氢能及燃料电池产业展览会'
    else:
        # 尝试从域名提取
        match = re.search(r'https?://(?:www\.)?([^/]+)', url)
        if match:
            domain = match.group(1)
            # 去掉常见后缀
            domain = domain.replace('.com', '').replace('.cn', '').replace('.gov', '').replace('.org', '')
            return domain
        return '未知'

def main():
    with open('search-results-merged.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    policy_items = [item for item in data if item.get('category') == '政策解读']
    print(f'找到 {len(policy_items)} 条政策解读条目')
    
    # 准备Markdown内容
    md_lines = []
    md_lines.append('# 氢能政策信息汇总')
    md_lines.append('')
    md_lines.append('## 一、现有政策解读条目')
    md_lines.append('')
    md_lines.append('| 序号 | 标题 | 原文链接 | 发布时间 | 发布机构 | 关键内容摘要 |')
    md_lines.append('|------|------|----------|----------|----------|--------------|')
    
    for idx, item in enumerate(policy_items, 1):
        title = item['title']
        url = item['url']
        publish_date = item['publish_date']
        agency = extract_agency_from_url(url)
        summary = item['summary'].replace('\n', ' ').strip()
        
        md_lines.append(f'| {idx} | {title} | [{url}]({url}) | {publish_date} | {agency} | {summary} |')
    
    md_lines.append('')
    md_lines.append('## 二、补充收集的政策信息')
    md_lines.append('')
    md_lines.append('### 2.1 中国国家层面政策')
    md_lines.append('待补充')
    md_lines.append('')
    md_lines.append('### 2.2 省级和地区层面政策')
    md_lines.append('待补充')
    md_lines.append('')
    md_lines.append('### 2.3 全球其他政府及国际组织政策')
    md_lines.append('待补充')
    
    # 写入文件
    with open('policy-summary.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print('已生成 policy-summary.md 文件')

if __name__ == '__main__':
    main()
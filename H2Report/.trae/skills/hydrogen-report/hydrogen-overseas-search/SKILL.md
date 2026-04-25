---
name: hydrogen-overseas-search
description: >
  氢能海外维度信息搜索。Use when searching for global hydrogen news,
  海外氢能动态, Chinese hydrogen companies overseas, overseas
  dimension search, or when user asks to collect international
  hydrogen information for monthly report. Executes ≥30 searches
  covering global policy, Chinese companies overseas, international
  technology, and professional media.
---

# 氢能海外维度搜索

## 概述

海外维度负责采集全球氢能动态信息，包括：
- 全球氢能综合动态
- 重点国家/地区政策与项目
- 中国企业出海动态
- 海外技术动态
- 国际组织与权威机构
- 海外专业媒体

**搜索次数要求**：≥30次

---

## 第一层：全球氢能综合动态（3次）

| # | 搜索语句 | 覆盖范围 |
|---|---------|---------|
| O1 | `hydrogen energy policy project investment breakthrough [月份英文] [年份]` lr="en" | 全球氢能综合动态 |
| O2 | `green hydrogen green ammonia green methanol project [月份英文] [年份]` lr="en" | 绿氢衍生物全球项目 |
| O3 | `hydrogen energy news [月份英文] [年份]` lr="en" num=10 | 全球氢能新闻汇总 |

---

## 第二层：重点国家/地区定点搜索（12次）

### 2.1 欧洲（4次）

| # | 搜索语句 | 覆盖范围 |
|---|---------|---------|
| O4 | `hydrogen policy subsidy (EU OR Europe) [月份英文] [年份]` lr="en" | 欧盟政策/补贴 |
| O5 | `hydrogen project investment (Germany OR Denmark OR Netherlands) [年份]` lr="en" | 欧洲核心国家项目 |
| O6 | `hydrogen policy project (UK OR France OR Spain) [年份]` lr="en" | 欧洲大国项目 |
| O7 | `hydrogen pipeline infrastructure Europe [年份]` lr="en" | 欧洲氢能管道/基础设施 |

### 2.2 亚太（3次）

| # | 搜索语句 | 覆盖范围 |
|---|---------|---------|
| O8 | `hydrogen policy project Japan Korea [月份英文] [年份]` lr="en" | 日韩（技术领先） |
| O9 | `hydrogen policy project India Australia [年份]` lr="en" | 印度/澳大利亚 |
| O10 | `hydrogen electrolyzer manufacturing Asia [年份]` lr="en" | 亚洲电解槽制造 |

### 2.3 中东+非洲+美洲（3次）

| # | 搜索语句 | 覆盖范围 |
|---|---------|---------|
| O11 | `hydrogen project investment (Saudi Arabia OR Oman OR UAE OR Middle East) [年份]` lr="en" | 中东大型出口项目 |
| O12 | `hydrogen project (USA OR Canada) [年份]` lr="en" | 北美 |
| O13 | `hydrogen project (Africa OR Brazil OR Chile OR Colombia) [年份]` lr="en" | 新兴市场 |

### 2.4 海外技术动态（2次）

| # | 搜索语句 | 覆盖范围 |
|---|---------|---------|
| O14 | `hydrogen technology breakthrough (Toyota OR Hyundai OR Cummins OR Siemens) [月份英文] [年份]` lr="en" | 海外龙头企业技术动态 |
| O15 | `hydrogen (SOEC OR PEM electrolyzer) breakthrough [月份英文] [年份]` lr="en" | 海外电解槽技术 |

---

## 第三层：中国企业出海（6次）

| # | 搜索语句 | 覆盖范围 |
|---|---------|---------|
| O16 | `氢能 (出口 OR 海外 OR 出海 OR 国际合作) [月份] [年份]` lr="zh" | 中文媒体报道的中国企业出海 |
| O17 | `Chinese hydrogen electrolyzer export overseas project [年份]` lr="en" | 英文报道的中国企业出海 |
| O18 | `(电解槽 OR 燃料电池 OR 储氢设备) 出口 (海外 OR 国际) [月份] [年份]` | 按设备类型搜索出口 |
| O19 | `(隆基氢能 OR 阳光氢能 OR 三一氢能 OR 国富氢能) 出口 OR 海外 [月份] [年份]` | 按企业搜索出海 |
| O20 | `Chinese hydrogen (Africa OR Middle East OR Southeast Asia OR Europe) project [年份]` lr="en" | 按目的地区分 |
| O21 | `氢能 (一带一路 OR 海外项目 OR 国际工程) [月份] [年份]` | 一带一路框架下出海 |

---

## 第四层：国际组织与权威机构（3次）

| # | 搜索语句 | 覆盖范围 |
|---|---------|---------|
| O22 | `hydrogen (IEA OR IRENA OR Hydrogen Council) report policy [年份]` lr="en" | 国际组织报告 |
| O23 | `hydrogen energy news site:reuters.com [月份英文] [年份]` lr="en" | 路透社 |
| O24 | `hydrogen energy news site:ft.com OR site:bloomberg.com [年份]` lr="en" | 金融时报/彭博 |

---

## 第五层：海外专业媒体（4次）

| # | 搜索语句 | 媒体 |
|---|---------|------|
| O25 | `hydrogen project investment [月份英文] [年份] site:rechargenews.com` lr="en" | Recharge News |
| O26 | `hydrogen energy [月份英文] [年份] site:energyvoice.com` lr="en" | Energy Voice |
| O27 | `hydrogen news [月份英文] [年份] site:hydrogeninsight.com` lr="en" | Hydrogen Insight |
| O28 | `green hydrogen project [年份] site:h2-view.com` lr="en" | H2 View |

---

## 第六层：海外维度补充搜索（2-4次）

| # | 搜索语句 | 补充方向 |
|---|---------|---------|
| O29 | `hydrogen (IPO OR funding OR investment) startup [月份英文] [年份]` lr="en" | 海外氢能创业投资 |
| O30 | `hydrogen (safety OR accident OR incident) [年份]` lr="en" | 海外氢能安全事件 |
| O31 | `hydrogen (CfD OR subsidy OR incentive) [年份]` lr="en" | 各国补贴机制 |
| O32 | `hydrogen shipping vessel maritime [年份]` lr="en" | 氢能航运 |

---

## 海外维度评分标准

| 评分 | 标准 | 来源类型 |
|------|------|---------|
| **5分** | 外国政府官网政策原文/国际组织权威报告 | gov.au/gov.uk/IEA/IRENA |
| **5分** | 中国企业海外项目的官方公告（含合同金额/规模） | 企业官网/交易所公告 |
| **4分** | 国际权威媒体深度报道（路透社/金融时报等） | Reuters/FT/Bloomberg |
| **4分** | 海外专业媒体的详细报道 | Recharge/H2 View/Energy Voice |
| **3分** | 一般英文媒体的氢能新闻 | 综合英文媒体 |
| **2分** | 内容泛泛、缺乏具体数据 | 低质量来源 |
| **1分** | 无关内容 | 广告 |

---

## 海外维度"充分"标准

| 检查项 | 充分标准 |
|--------|---------|
| 全球政策/项目 | ≥3条（来自≥3个不同国家） |
| 中国企业出海 | ≥2条（含具体出口/海外项目信息） |
| 海外技术动态 | ≥2条（海外企业技术突破/新产品） |
| 区域覆盖 | 至少覆盖3个不同区域（欧洲/亚太/中东等） |
| 信息来源 | 至少有3条来自非中文来源 |

---

## 海外维度sub_category枚举

| 枚举值 | 说明 |
|--------|------|
| `global_policy` | 全球政策动态 |
| `chinese_overseas` | 中国企业出海 |
| `overseas_technology` | 海外技术动态 |
| `international_org` | 国际组织报告 |

---

## 海外维度key_info字段

```json
{
  "key_info": {
    "country": "德国",
    "company": "隆基氢能",
    "event_description": "交付欧洲首台套5MW碱性电解槽",
    "scale": "5MW"
  }
}
```

---

## 来源偏好规则（海外维度专用）

```
⚠️ 海外维度的URL优先级：

第1优先：中国企业的中文报道
  - 国内媒体对中国企业出海的报道
  - 企业官网中文新闻稿

第2优先：国际权威媒体
  - reuters.com（路透社）
  - ft.com（金融时报）
  - bloomberg.com（彭博）

第3优先：海外专业媒体
  - h2-view.com
  - rechargenews.com
  - energyvoice.com
  - hydrogeninsight.com

禁止：
  - 企业官网首页（如 https://nghc.com/）
```

---

## 弹性搜索（按需触发）

> **触发条件**：当基础搜索（O1-O32）完成后，覆盖度评估显示"不足"时，按以下优先级补充搜索。每轮补充1-3次，最多3轮。连续3轮无新增≥3分结果则标记"已搜尽"。

### 补充搜索优先级

| 优先级 | 补充方向 | 搜索语句模板 |
|--------|---------|-------------|
| 1 | 按热点深挖 | `"[热点关键词英文]" (policy OR project OR investment) [月份英文] [年份]` lr="en" |
| 2 | 按未覆盖国家补充 | `hydrogen (policy OR project) [未搜索国家名] [年份]` lr="en" |
| 3 | 按中国企业出海补充 | `Chinese hydrogen [设备类型] [未搜索目的地区] [年份]` lr="en" |
| 4 | 按海外媒体补充 | `hydrogen [月份英文] [年份] site:[未搜索媒体域名]` lr="en" |
| 5 | 换词重搜 | 将"project"→"investment"/"breakthrough"/"pilot"等同义词替换后重搜 |

### 换词原则

- 更换同义词：`project`→`investment`→`breakthrough`→`pilot`→`initiative`
- 更换国家：`Germany`→`Denmark`→`Netherlands`→`UK`→`France`→`Spain`
- 更换媒体：`h2-view.com`→`rechargenews.com`→`energyvoice.com`→`hydrogeninsight.com`

---

## 搜索结果记录格式

每次搜索后立即记录：

```json
{
  "search_id": "O1",
  "query": "hydrogen energy policy project investment breakthrough March 2026",
  "result_count": 10,
  "results": [
    {
      "rank": 1,
      "title": "EU Hydrogen Bank second auction results announced",
      "url": "https://ec.europa.eu/xxx",
      "snippet": "...",
      "score": 5,
      "dimension": "overseas",
      "sub_category": "global_policy",
      "is_duplicate": false
    }
  ]
}
```

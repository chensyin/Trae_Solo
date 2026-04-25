---
name: hydrogen-search
description: >
  氢能行业月度信息采集主入口。Use when user asks to execute 氢能搜索,
  collect hydrogen industry information, run 搜索模块提示词, generate
  monthly hydrogen report, or perform comprehensive hydrogen information
  collection. Performs base search to identify hotspots, then orchestrates
  5 dimension searches (policy/industry/technology/project/overseas).
---

# 氢能行业月度信息采集

## 概述

本Skill是氢能行业信息采集的主入口，负责：
1. 确定目标月份和停止条件
2. 执行基底搜索（3次），识别当月热点
3. 编排调用5个维度Skill执行深度搜索
4. 调用输出Skill进行质量评估和JSON汇总

## 执行流程

```
┌─────────────────────────────────────┐
│  第1步：确定目标月份和停止条件        │
│  - 动态参数替换                      │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  第2步：执行基底搜索（3次）           │
│  - 中文综合搜索                      │
│  - 中文事件搜索                      │
│  - 英文国际搜索                      │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  第3步：识别当月热点（≥1个）          │
│  - 动态生成协同搜索语句               │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  第4步：并行调用5个维度Skill          │
│  - 传入动态参数                      │
│  - 各维度弹性搜索（按需触发）         │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  第5步：调用hydrogen-fetch           │
│  - 对高分URL执行WebFetch             │
│  - 二次验证与评分更新                 │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  第6步：调用hydrogen-search-output   │
│  - 质量评估与去重                    │
│  - 覆盖度评估与补充搜索              │
│  - JSON格式输出                     │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│  第7步：调用hydrogen-report          │
│  - 从JSON提取URL生成月报             │
│  - 输出MD+Word格式                  │
└─────────────────────────────────────┘
```

---

## 第1步：确定目标月份和停止条件

### 1.1 目标月份确定

**优先级规则**：
1. 用户明确指定月份 → 使用指定月份
2. 用户未指定 → 使用当前月份的上月（如当前2026年4月，则搜索2026年3月）

### 1.2 动态参数替换

确定目标月份后，生成以下参数供所有维度Skill使用：

| 参数 | 示例值 | 说明 |
|------|--------|------|
| `TARGET_MONTH_CN` | `3月` | 中文月份 |
| `TARGET_MONTH_EN` | `March` | 英文月份 |
| `TARGET_YEAR` | `2026` | 年份 |
| `TARGET_DATE_CN` | `3月 2026` | 中文日期（用于中文搜索） |
| `TARGET_DATE_EN` | `March 2026` | 英文日期（用于英文搜索） |
| `TARGET_YM` | `2026-03` | 年月（用于文件命名） |

**替换规则**：所有维度Skill中的 `[月份]`、`[年份]`、`[月份英文]` 占位符，在执行前统一替换为上述参数值。

**示例**：
```
原始模板：`"氢能" site:gov.cn [月份] [年份]`
替换后：  `"氢能" site:gov.cn 3月 2026`

原始模板：`hydrogen energy policy [月份英文] [年份]`
替换后：  `hydrogen energy policy March 2026`
```

### 1.3 热点驱动的动态搜索语句生成

识别出当月热点后，按以下模板动态生成协同搜索语句：

```python
# 伪代码
for hotspot in identified_hotspots:
    for dimension in ["policy", "industry", "technology", "project", "overseas"]:
        query = generate_cross_search_query(hotspot, dimension, TARGET_DATE_CN)
        execute_search(query)
```

**通用协同搜索模板**（按热点关键词动态填充）：

| 维度 | 搜索语句模板 |
|------|-------------|
| 政策 | `"[HOTSPOT_KEYWORD]" (配套 OR 细则 OR 申报指南) [月份] [年份]` |
| 产业 | `"[HOTSPOT_KEYWORD]" (企业反应 OR 机会 OR 布局 OR 签约) [月份] [年份]` |
| 技术 | `"[HOTSPOT_KEYWORD]" (技术路线 OR 技术要求 OR 指标) [月份] [年份]` |
| 项目 | `"[HOTSPOT_KEYWORD]" (申报 OR 项目储备 OR 落地) [月份] [年份]` |
| 海外 | `"[HOTSPOT_KEYWORD_EN]" (comparison OR benchmark) [年份]` lr="en" |

### 1.4 停止条件

搜索循环在以下**任一条件**满足时停止：

| 条件 | 标准 |
|------|------|
| **总搜索次数** | ≥200次 |
| **各维度充分性** | 政策+产业+技术+项目+海外5个维度均达到"充分"标准 |
| **连续无新增** | 连续3轮补充搜索均无新增≥3分结果 |

### 1.3 输出要求

最终输出为JSON格式文件：`[月份]_信息采集结果.json`

---

## 第2步：基底搜索（3次）

> **目的**：快速扫描当月氢能领域综合动态，识别热点事件，为后续维度搜索和协同搜索提供方向。

| # | 搜索语句 | 参数 | 目的 |
|---|---------|------|------|
| B1 | `氢能 (政策 OR 项目 OR 技术 OR 投资 OR 签约 OR 投产) [月份] [年份]` | num=10, lr="zh" | 获取当月氢能领域综合动态，识别热点事件 |
| B2 | `氢能 (展会 OR 论坛 OR 签约 OR 开工 OR 投产 OR 突破) [月份] [年份]` | num=10, lr="zh" | 聚焦当月重大事件（展会、签约、投产等） |
| B3 | `hydrogen energy (policy OR project OR investment OR breakthrough) [月份英文] [年份]` | num=10, lr="en" | 获取国际氢能动态，识别海外热点 |

### 2.4 基底搜索结果记录

每次搜索后，立即记录返回的每一条结果：

```json
{
  "search_id": "B1",
  "query": "氢能 (政策 OR 项目 OR 技术 OR 投资 OR 签约 OR 投产) 3月 2026",
  "result_count": 10,
  "results": [
    {
      "rank": 1,
      "title": "三部门联合发布氢能综合应用试点政策",
      "url": "https://m.mof.gov.cn/xxx",
      "snippet": "...",
      "score": 5,
      "is_hotspot_candidate": true
    }
  ]
}
```

---

## 第3步：识别当月热点

### 3.1 热点识别标准

从基底搜索结果中识别热点，标准如下：

| 热点类型 | 识别标准 | 示例 |
|---------|---------|------|
| **政策热点** | 国家级政策发布、重大补贴政策、试点政策 | 三部门氢能试点政策 |
| **展会热点** | 大型行业展会、论坛 | CIHC中国氢能展 |
| **项目热点** | 重大签约、开工、投产 | 万吨级绿氢项目投产 |
| **技术热点** | 重大技术突破、首发产品 | 海水制氢突破1000小时 |
| **海外热点** | 中国企业重大出海项目 | 隆基氢能交付欧洲5MW电解槽 |

### 3.2 热点记录格式

```json
{
  "hotspots": [
    {
      "name": "氢能综合应用试点政策发布",
      "trigger_date": "2026-03-16",
      "related_dimensions": ["policy", "industry", "technology", "project", "overseas"],
      "cross_search_count": 5
    }
  ]
}
```

### 3.3 热点与维度关联

识别出的每个热点，标注其关联的维度，用于触发协同搜索：

| 热点 | 关联维度 |
|------|---------|
| 政策发布 | policy + industry + technology + project |
| 展会 | industry + technology + project + overseas |
| 项目投产 | project + industry + technology |
| 技术突破 | technology + industry + project |
| 企业出海 | overseas + industry + project |

---

## 第4步：调用维度Skill

### 4.1 并行调用策略

使用Task工具并行调用5个维度Skill（最多3个并行）：

**第一批**：
- hydrogen-policy-search
- hydrogen-industry-search
- hydrogen-tech-search

**第二批**：
- hydrogen-project-search
- hydrogen-overseas-search

### 4.2 传递给维度Skill的参数

每个维度Skill需要接收以下参数：
- `target_month`: 目标月份（如"2026-03"）
- `hotspots`: 识别出的热点列表
- `base_results`: 基底搜索结果（用于避免重复）

### 4.3 各维度Skill返回结果

每个维度Skill返回JSON格式的搜索结果：

```json
{
  "dimension": "policy",
  "search_count": 35,
  "results": [
    {
      "id": "P0-1",
      "title": "...",
      "url": "...",
      "score": 5,
      "dimension": "policy",
      "sub_category": "national_policy"
    }
  ],
  "coverage_status": "sufficient"
}
```

---

## 第5步：调用输出Skill

### 5.1 传递给输出Skill的参数

- `dimension_results`: 5个维度Skill返回的所有结果
- `hotspots`: 识别出的热点列表
- `target_month`: 目标月份

### 5.2 输出Skill执行内容

1. **质量评估与去重**：统一评分、标记重复
2. **覆盖度评估**：检查各维度是否达到充分标准
3. **补充搜索**：对不足维度执行补充搜索
4. **WebFetch并行抓取**：获取全文内容
5. **JSON格式输出**：生成最终汇总文件

---

## 附录：网站列表和关键词池

详见 [reference.md](reference.md)，包含：
- 附录A：中央政府网站列表
- 附录B：地方政府网站列表
- 附录C：权威新闻媒体网站列表
- 附录D：关键词池（产业/技术/项目/海外）

---

## 依赖Skill

- `hydrogen-policy-search`：政策维度搜索
- `hydrogen-industry-search`：产业维度搜索
- `hydrogen-tech-search`：技术维度搜索
- `hydrogen-project-search`：项目维度搜索
- `hydrogen-overseas-search`：海外维度搜索
- `hydrogen-fetch`：深度抓取与URL验证
- `hydrogen-search-output`：质量评估与JSON输出
- `hydrogen-report`：月报生成（MD+Word）

---
name: hydrogen-fetch
description: >
  氢能搜索结果深度抓取与验证。Use after dimension searches complete,
  or when user asks to fetch hydrogen article full text, verify URL
  accessibility, validate search result content, or perform WebFetch
  on high-value hydrogen URLs. Scores URLs, extracts key paragraphs,
  and updates quality ratings.
---

# 氢能搜索结果深度抓取与验证

## 概述

本Skill对搜索结果中的高价值URL执行WebFetch深度抓取，提取全文关键段落，验证URL可访问性和内容相关性，并二次更新评分。

---

## 第1步：URL筛选与优先级排序

### 1.1 自动抓取条件

| 条件 | 说明 |
|------|------|
| 评分 ≥ 4分 | 必须抓取 |
| 评分 = 3分 且 信息缺口大 | 视情况抓取 |
| 评分 ≤ 2分 | 不抓取 |

### 1.2 抓取优先级

| 优先级 | URL类型 | 抓取理由 |
|--------|---------|---------|
| P0 | 政府官网政策原文（gov.cn/miit.gov.cn等） | 最权威来源，需提取完整政策条款 |
| P1 | 交易所公告原文（sse.com.cn/szse.cn等） | 包含具体财务数据 |
| P2 | 国际组织报告（IEA/IRENA） | 权威数据和分析 |
| P3 | 行业媒体深度报道 | 包含具体项目/企业/金额信息 |
| P4 | 英文权威媒体（Reuters/FT/Bloomberg） | 国际视角 |

### 1.3 最大抓取数量

- 单维度最多抓取 **15个URL**
- 全部维度合计最多抓取 **50个URL**
- 超出限制时按评分从高到低截断

---

## 第2步：分批并行抓取

### 2.1 分批策略

```
每批最多5个并行WebFetch调用。
按维度分组，同一维度的URL放在同一批。
优先抓取P0-P1级别的URL。
```

### 2.2 批次安排

| 批次 | 内容 | URL数量 |
|------|------|---------|
| 第1批 | 政策维度P0-P1级别URL | ≤5个 |
| 第2批 | 产业维度交易所公告+行业媒体 | ≤5个 |
| 第3批 | 技术维度科研机构+学术论文 | ≤5个 |
| 第4批 | 项目维度政府审批平台 | ≤5个 |
| 第5批 | 海外维度国际组织+权威媒体 | ≤5个 |
| 第6批 | 各维度剩余高分URL | ≤5个 |
| ... | 按需继续 | 每批≤5个 |

---

## 第3步：信息提取格式

### 3.1 提取字段

从每个URL的页面中提取以下信息：

```json
{
  "id": "P0-1",
  "title": "页面实际标题（从页面<title>或<h1>中提取，不得编造）",
  "source": "网站/媒体名称",
  "url": "搜索阶段实际返回的完整URL（不得修改）",
  "publish_date": "2026-03-16（从页面中提取，格式YYYY-MM-DD，如无则填null）",
  "full_text_snippet": "正文关键段落摘录（200-500字，保留核心数据和事实）",
  "quality": "high / medium / low",
  "key_info": {
    "按维度提取结构化字段，见各维度定义"
  }
}
```

### 3.2 各维度key_info提取规则

**政策维度**：
```json
{
  "key_info": {
    "issuer": "发布机构全称",
    "doc_number": "文号（如：工信部联节〔2026〕59号）",
    "core_content": "核心内容一句话概括",
    "details": ["要点1", "要点2", "要点3"],
    "effective_date": "生效日期"
  }
}
```

**产业维度**：
```json
{
  "key_info": {
    "company": "相关企业",
    "event_type": "事件类型（订单/签约/中标/融资等）",
    "amount": "金额/规模",
    "details": ["细节1", "细节2"]
  }
}
```

**技术维度**：
```json
{
  "key_info": {
    "research_entity": "研发主体",
    "tech_route": "技术路线",
    "key_metrics": ["指标1：数值", "指标2：数值"],
    "research_stage": "basic_research / tech_breakthrough / lab_scale / pilot / industrialization"
  }
}
```

**项目维度**：
```json
{
  "key_info": {
    "project_name": "项目全称",
    "location": "项目所在地",
    "investment": "投资金额",
    "capacity": "产能规模",
    "stage": "项目阶段",
    "participants": ["参与方1", "参与方2"]
  }
}
```

**海外维度**：
```json
{
  "key_info": {
    "country": "国家/地区",
    "company": "相关企业",
    "event_description": "事件描述",
    "scale": "规模/金额"
  }
}
```

---

## 第4步：二次验证与评分更新

### 4.1 内容相关性验证

| 检查项 | 通过条件 | 不通过处理 |
|--------|---------|-----------|
| 标题匹配 | 页面标题与搜索结果标题相关度 ≥ 70% | `score` 降1分 |
| 内容匹配 | 页面正文包含搜索关键词 | `score` 降1分 |
| 时效性 | 页面发布日期在目标月份 ± 1个月内 | `score` 降2分 |
| 内容量 | 正文有效内容 ≥ 100字 | `quality` 标记为 `"low"` |

### 4.2 URL有效性验证

| 检查项 | 通过条件 | 不通过处理 |
|--------|---------|-----------|
| 可访问性 | WebFetch成功返回内容 | `url` 标记为 `null`，`score` 降为1分 |
| 页面类型 | 指向具体文章/公告页面 | `score` 降为1分，`url` 标记为 `null` |
| 非首页 | URL路径包含文章标识（日期/ID/GUID等） | 如指向首页则降分 |

### 4.3 评分更新规则

```
原评分 → 二次验证后评分：

5分 + 验证通过 → 保持5分
5分 + 标题不匹配 → 降为4分
5分 + 内容不匹配 → 降为3分
5分 + URL指向首页 → 降为1分，url=null

4分 + 验证通过 → 保持4分
4分 + 内容量不足 → 降为3分，quality="low"

3分 + 验证通过 → 保持3分
3分 + 非当月内容 → 降为2分
```

---

## 第5步：输出更新后的JSON

### 5.1 输出文件

将抓取和验证后的结果更新到原始JSON文件中，新增以下字段：

```json
{
  "id": "P0-1",
  "title": "更新后的标题（从页面实际提取）",
  "url": "原始URL（不得修改）",
  "publish_date": "从页面提取的发布日期",
  "full_text_snippet": "正文关键段落（200-500字）",
  "quality": "high / medium / low",
  "fetch_status": "success / failed / skipped",
  "fetch_notes": "抓取备注（如：标题与搜索结果不完全匹配）"
}
```

### 5.2 抓取统计

```json
{
  "fetch_stats": {
    "total_urls": 50,
    "fetched": 45,
    "failed": 3,
    "skipped": 2,
    "score_upgraded": 0,
    "score_downgraded": 8,
    "url_nullified": 2
  }
}
```

---

## 依赖

- 搜索结果JSON文件（`/data/user/work/search_results_*.json`）
- WebFetch工具

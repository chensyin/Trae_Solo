---
name: hydrogen-report
description: >
  根据氢能搜索结果JSON文件生成月度行业动态报告。Use when user asks to
  generate 氢能月报, monthly hydrogen report, create report from JSON
  search results, or write 双碳新能源领域月度行业动态. Reads JSON files
  to extract URLs and key_info, outputs both MD and Word formats following
  the template structure. Enforces URL integrity, key_info injection,
  minimum item counts, and fixed subcategory names.
---

# 氢能月报生成

## 概述

本Skill从JSON搜索结果文件中提取信息，按照标准模板格式生成月度行业动态报告。

**核心原则**：
- **必须先读取JSON文件**提取URL和key_info，严禁从子代理传递的文本中直接复制
- 每条信息必须附带来自JSON的真实URL，**零容忍"暂无链接"**
- 每条信息的描述必须注入JSON中的key_info具体数据，**零容忍泛化描述**
- 趋势研判类内容必须引用独立来源URL，**零容忍复用前文URL**
- 政策类信息优先引用gov.cn来源

---

## 第1步：读取JSON搜索结果文件

### 1.1 文件位置

JSON文件保存在 `/data/user/work/` 目录下，命名规则：

| 文件名 | 内容 |
|--------|------|
| `search_results_pi_[月份].json` | 政策+产业维度搜索结果 |
| `search_results_tp_[月份].json` | 技术+项目维度搜索结果 |
| `search_results_os_[月份].json` | 海外维度搜索结果 |

### 1.2 读取方法

```
⚠️ 强制要求：必须使用Read工具逐个读取上述3个JSON文件的完整内容。
不得仅读取部分内容或依赖其他子代理传递的摘要。
```

### 1.3 提取字段清单

从每条JSON结果中必须提取以下**全部字段**：

| 字段 | 用途 | 是否必填 |
|------|------|---------|
| `title` | 信息标题 | ✅ 必填 |
| `url` | 来源链接 | ✅ 必填（null的条目不得使用） |
| `snippet` | 搜索摘要 | ✅ 必填 |
| `score` | 评分（1-5） | ✅ 必填 |
| `dimension` | 维度 | ✅ 必填 |
| `sub_category` | 子分类 | ✅ 必填 |
| `key_info` | 结构化关键数据 | ✅ 必填（注入描述） |
| `full_text_snippet` | 全文摘录 | ⚠️ 有则用 |
| `publish_date` | 发布日期 | ⚠️ 有则用 |

---

## 第2步：信息筛选与分类

### 2.1 重要性评级

| 报告位置 | 筛选标准 | 数量 |
|---------|---------|------|
| 一、重要信息 | `score ≥ 4` 且影响重大 | **精确3条** |
| 二、其他相关信息 | `score ≥ 3` 的剩余条目 | 按子分类分配 |

### 2.2 固定子分类名称（禁止修改）

```
⚠️ 以下9个子分类名称和顺序为固定模板，子代理不得自行调整、合并或重命名：

（一）研发动态
（二）项目前期
（三）项目建设
（四）市场和销售
（五）合作投资重组
（六）海外项目
（七）国内政策风向
（八）市场和成本数据
（九）趋势研判
```

### 2.3 子分类映射规则

| 报告子分类 | 对应JSON维度+子分类 |
|-----------|-------------------|
| （一）研发动态 | dimension=technology, sub_category∈{domestic_research, english_academic, testing_validation, patent} |
| （二）项目前期 | dimension=project, sub_category=pre_project |
| （三）项目建设 | dimension=project, sub_category=post_project |
| （四）市场和销售 | dimension=industry, sub_category∈{supply_chain, market_data, enterprise} |
| （五）合作投资重组 | dimension=industry, sub_category∈{exchange_announcement, soe_bidding, financial_media} |
| （六）海外项目 | dimension=overseas, sub_category∈{global_policy, chinese_overseas, overseas_technology} |
| （七）国内政策风向 | dimension=policy, sub_category∈{national_policy, local_policy, policy_interpretation, policy_impact} |
| （八）市场和成本数据 | dimension=industry, sub_category=market_data + dimension=technology 成本相关 + dimension=project 投资规模 |
| （九）趋势研判 | 基于所有数据的编辑分析（**必须使用独立来源URL**） |

### 2.4 强制最低条数

```
⚠️ 以下为强制最低条数，低于此数则报告不合格，必须补充：

| 子分类 | 最低条数 | 建议条数 | 硬性下限 |
|--------|---------|---------|---------|
| 一、重要信息 | 3条 | 3条 | 3条（精确） |
| （一）研发动态 | 4条 | 5条 | 4条 |
| （二）项目前期 | 4条 | 5条 | 4条 |
| （三）项目建设 | 4条 | 5条 | 4条 |
| （四）市场和销售 | 4条 | 5条 | 4条 |
| （五）合作投资重组 | 4条 | 5条 | 4条 |
| （六）海外项目 | 5条 | 6条 | 5条 |
| （七）国内政策风向 | 4条 | 5条 | 4条 |
| （八）市场和成本数据 | 4条 | 5条 | 4条 |
| （九）趋势研判 | 5条 | 5条 | 5条（精确） |
| **合计** | **≥45条** | **≥48条** | **45条** |

如果某子分类条数不足最低要求：
1. 优先从JSON中该维度剩余条目补充
2. 如果JSON中该维度条目已用完，从相邻维度借用
3. 如果仍然不足，标注"[补充搜索建议：需要补充XX维度搜索]"
```

---

## 第3步：key_info注入规则

### 3.1 什么是key_info注入

```
⚠️ 核心规则：每条信息的描述中必须包含来自JSON key_info字段的具体数据。

❌ 错误示例（泛化描述）：
"某企业获得了一笔大额订单，将推动氢能产业发展。"

✅ 正确示例（key_info注入）：
"隆基氢能获得中石化10亿元电解槽采购订单（来源：上交所公告601868_20251217），
将交付50台1000Nm³/h碱性电解槽，预计2026年Q2完成全部交付。"
```

### 3.2 各维度key_info必填字段

每条信息的描述中**必须包含**以下对应维度的具体数据：

**政策维度**：
- 发布机构（如"工信部/财政部/发改委"）
- 文号（如"工信部联节〔2026〕59号"）
- 核心内容（一句话概括）
- 具体条款/要点（至少2个）

**产业维度**：
- 企业名称（如"隆基氢能"）
- 事件类型（如"订单交付/中标/融资"）
- 金额/规模（如"10亿元"/"50台"）
- 合作方/客户（如有）

**技术维度**：
- 研发主体（如"中科院大连化物所"）
- 技术路线（如"PEM电解槽"）
- 关键技术指标（如"电流密度3A/cm²"、"能耗4.3kWh/Nm³"）
- 研究阶段（如"中试示范"）

**项目维度**：
- 项目全称
- 所在地（如"内蒙古鄂尔多斯"）
- 投资金额（如"32亿元"）
- 产能规模（如"年产绿氨30万吨"）
- 参与方（至少2个）

**海外维度**：
- 国家/地区
- 企业名称
- 事件描述
- 规模/金额

### 3.3 禁止的描述方式

```
❌ 禁止使用以下泛化表述（除非JSON中确实没有具体数据）：
- "某企业" → 必须使用企业全称
- "大额订单" → 必须写明具体金额
- "取得了突破" → 必须写明具体技术指标
- "某项目" → 必须写明项目全称
- "近日" → 必须写明具体日期（如"12月16日"）
- "数亿元" → 必须写明确切金额
- "多个" → 必须写明具体数量
```

---

## 第4步：报告格式模板

```markdown
# "双碳"新能源领域月度行业动态
## （[年份]年[月份]）

---

## 一、重要信息

### 1. [信息标题]

[第1段：事件概述，包含时间、地点、参与方等5W1H要素]
[第2段：具体数据，包含key_info中的金额/规模/指标等]
[第3段：影响分析，包含对行业/市场/技术的影响]

来源：[来源描述](URL)

---

### 2. [信息标题]

[同上结构]

来源：[来源描述](URL)

---

### 3. [信息标题]

[同上结构]

来源：[来源描述](URL)

---

## 二、其他相关信息

### （一）研发动态

**1. [信息标题]**

[第1段：研发主体+技术路线+关键指标]
[第2段：技术细节+研究阶段+应用前景]

来源：[来源描述](URL)

**2. [信息标题]**

[同上结构]

来源：[来源描述](URL)

（每个子分类4-5条，结构同上）

### （二）项目前期
### （三）项目建设
### （四）市场和销售
### （五）合作投资重组
### （六）海外项目
### （七）国内政策风向
### （八）市场和成本数据
### （九）趋势研判
```

---

## 第5步：强制URL核对

### 5.1 逐条URL核对流程

```
⚠️ 生成报告后，必须执行以下逐条核对流程：

1. 提取报告中所有"来源：[描述](URL)"行
2. 对每条URL执行以下检查：
   a. URL是否以http://或https://开头？
   b. URL是否来自JSON文件（与JSON中的url字段完全匹配）？
   c. URL是否指向具体文章页面（非首页/列表页/搜索结果页）？
   d. 趋势研判类URL是否与前文所有URL均不重复？
3. 如果发现不合格URL：
   a. 回查JSON文件，找到该条信息对应的真实URL
   b. 如果JSON中该条url为null，则从同事件的其他搜索结果中找到替代URL
   c. 如果确实无可用URL，删除该条信息，用JSON中其他条目补充
4. 核对完成后，统计：
   - 总信息条数（必须 ≥ 45条）
   - 有URL条数（必须 = 总条数）
   - 无URL条数（必须 = 0）
   - 趋势研判独立URL数（必须 = 5条）
```

### 5.2 URL黑名单

```
以下URL模式为黑名单，发现后必须替换：

❌ 企业首页：
   https://www.sinopec.com.cn/
   https://www.longi.com/
   https://nghc.com/

❌ 政府首页：
   https://www.ndrc.gov.cn/
   https://www.gov.cn/

❌ 列表页/搜索结果页：
   https://www.h2-view.com/category/europe
   https://h2.china-nengyuan.com/news/?keyword=制氢
   https://search.mof.gov.cn/was5/web/search?...

❌ 跳转页/短链接：
   https://cj.sina.cn/article/norm_detail?url=...
   http://2fwww.tanjiaoyi.com/

❌ "综合搜索结果"标记（v2版问题，v3版禁止出现）
```

### 5.3 来源偏好规则

```
政策维度（dimension=policy）：
  第1优先：政府部门官网（gov.cn/miit.gov.cn/ndrc.gov.cn/nea.gov.cn/mee.gov.cn等）
  第2优先：权威中文媒体（xinhuanet.com/people.com.cn/ce.cn）
  第3优先：行业专业媒体（in-en.com/china-nengyuan.com等）

非政策维度：
  第1优先：中文来源
  第2优先：中文行业媒体
  第3优先：英文来源（仅在中文来源确实不存在时使用）

海外维度（dimension=overseas）：
  第1优先：中国企业的中文报道
  第2优先：国际权威媒体（reuters.com/ft.com/bloomberg.com）
  第3优先：海外专业媒体（h2-view.com/rechargenews.com等）
```

---

## 第6步：强制自检清单

```
⚠️ 生成报告后，必须逐项确认以下检查全部通过。
任何一项不通过，必须修正后才能输出最终报告。

### 数量检查
- [ ] 总信息条数 ≥ 45条
- [ ] 重要信息精确3条
- [ ] 趋势研判精确5条
- [ ] 每个子分类 ≥ 4条（海外≥5条）

### URL检查
- [ ] 每条信息都有URL（"暂无链接"数量 = 0）
- [ ] 所有URL来自JSON文件（非编造）
- [ ] 无企业首页/政府首页URL
- [ ] 无列表页/搜索结果页URL
- [ ] 无"综合搜索结果"标记
- [ ] 趋势研判5条URL均与前文不重复

### 内容质量检查
- [ ] 每条描述包含key_info中的具体数据
- [ ] 无"某企业"/"大额"/"近日"等泛化表述
- [ ] 政策类信息包含发布机构+文号+核心内容
- [ ] 技术类信息包含具体技术指标（数值+单位）
- [ ] 项目类信息包含投资金额+产能规模+所在地
- [ ] 产业类信息包含企业名称+事件类型+金额

### 来源检查
- [ ] 政策类信息优先引用了gov.cn来源
- [ ] 非政策类信息优先引用中文来源
- [ ] 所有URL域名可识别（非乱码/截断）
```

---

## 第7步：输出文件

### 7.1 MD文件

保存路径：`/workspace/双碳新能源领域月度行业动态_[年份]年[月份].md`

### 7.2 Word文件

使用docx-js将MD转换为Word文档：
- 中文字体：Microsoft YaHei
- A4纸张，1英寸页边距
- URL保留为蓝色超链接
- 生成后运行sanitize.py检查

保存路径：`/workspace/双碳新能源领域月度行业动态_[年份]年[月份].docx`

---

## 依赖

- JSON搜索结果文件（`/data/user/work/search_results_*.json`）
- docx Skill（Word文档生成）

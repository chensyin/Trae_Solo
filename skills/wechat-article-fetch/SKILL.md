---
name: wechat-article-fetch
description: 使用 requests + BeautifulSoup 直接抓取微信公众号文章链接内容，对公众号页面噪音做专用清洗，输出干净的 Markdown 或 JSON。轻量方案，无需浏览器依赖。
version: 1.0.0
author: SOLO Agent
license: MIT
metadata:
  tags: [wechat, mp.weixin.qq.com, extraction, markdown, json, beautifulsoup]
  related_skills: [wechat-article-camofox]
---

# 微信公众号文章抓取（轻量版）

当你要获取 **微信公众号文章链接**（`mp.weixin.qq.com/s/...`）的正文内容时，使用这个 skill。

它通过 `requests` 直接获取文章 HTML，再用 `BeautifulSoup` 解析页面结构，对公众号页面噪音做专用清洗，输出干净的 Markdown 或 JSON。

## 与 camofox-browser 方案的区别

| 维度 | 本方案（轻量版） | camofox-browser 方案 |
|------|------------------|---------------------|
| 依赖 | Python 3 + requests + beautifulsoup4 | Python 3 + git + Node.js 18+ + camofox-browser |
| 安装成本 | pip install 两个包即可 | 需 clone 仓库 + npm install + 下载浏览器二进制（~100MB） |
| 反爬能力 | 依赖 requests 的 User-Agent 伪装 | 使用 CamouFox 反检测浏览器，更难被拦截 |
| 适用场景 | 大多数可公开访问的公众号文章 | 需要更强反爬能力的场景 |
| 速度 | 快（单次 HTTP 请求） | 较慢（需启动浏览器服务） |

**建议**：优先尝试本方案；如果遇到文章被拦截或返回空白内容，再切换到 camofox-browser 方案。

## 适用场景

- 抓取微信公众号文章正文
- 输出 Markdown 或 JSON
- 批量保存公众号文章
- 后续需要将内容导入其他系统（飞书、Notion 等）
- 不想安装重量级浏览器依赖的场景

## 前提条件

1. 本机已安装 Python 3.9+
2. 能正常访问 `mp.weixin.qq.com`

依赖安装（脚本首次运行时会自动安装）：

```bash
pip install requests beautifulsoup4
```

## 文件结构

```
wechat-article-fetch/
├── SKILL.md                  # 本文档
├── fetch_wechat.py           # 核心抓取脚本
├── requirements.txt          # Python 依赖
└── templates/
    └── article_urls.example.txt  # 批量抓取示例
```

## 最常用用法

### 1）抓取为 Markdown（直接打印）

```bash
python3 fetch_wechat.py "https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxx"
```

### 2）抓取为 JSON

```bash
python3 fetch_wechat.py "https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxx" --format json
```

### 3）保存到本地文件

```bash
python3 fetch_wechat.py "https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxx" --save /tmp/article.md
```

### 4）附带图片信息一起输出

```bash
python3 fetch_wechat.py "https://mp.weixin.qq.com/s/xxxxxxxxxxxxxxxx" \
  --format json \
  --include-images \
  --save /tmp/article.json
```

### 5）批量抓取

```bash
while IFS= read -r url; do
  [ -z "$url" ] && continue
  python3 fetch_wechat.py "$url" --save "/tmp/articles/$(basename $url).md"
done < templates/article_urls.example.txt
```

## 输出说明

### Markdown

默认输出：

- 标题（一级标题）
- 作者 / 发布时间（斜体元信息行）
- 文章描述（引用块，如有）
- 清洗后的正文
- 按正文顺序排列的图片

### JSON

输出字段：

- `url`：原始文章链接
- `title`：文章标题
- `author`：公众号名称
- `published_at`：发布时间
- `description`：文章描述
- `content_markdown`：清洗后的 Markdown 全文
- `images`：图片列表（需 `--include-images`）
  - `src`：图片 URL
  - `alt`：图片描述
  - `width` / `height`：图片尺寸
- `source`：固定为 `requests_beautifulsoup`

## 提取策略

### 第一步：获取 HTML

```python
requests.get(url, headers=HEADERS, timeout=30)
```

- 使用桌面 Chrome 的 User-Agent
- 设置 Referer 为 `mp.weixin.qq.com`
- 自动检测编码

### 第二步：提取元信息

从 HTML `<head>` 和页面顶部元素中提取：

| 字段 | 提取来源（优先级从高到低） |
|------|--------------------------|
| 标题 | `<meta property="og:title">` → `<h1 id="activity-name">` |
| 作者 | `<a id="js_name">` → `<span class="rich_media_meta_nickname">` |
| 发布时间 | `<em id="publish_time">` → `<span id="publish_time">` |
| 描述 | `<meta property="og:description">` |

### 第三步：定位正文区域

```python
soup.find("div", id="js_content")
  or soup.find("div", class_="rich_media_content")
  or soup.find("div", class_="rich_media_area_primary")
```

### 第四步：递归清洗 HTML → Markdown

清洗规则：

1. **跳过噪音区域**（按 class 名过滤）：
   - `rich_media_tool`、`rich_media_extra`、`rich_media_footer`
   - `rich_media_comment`、`rich_media_reward`、`rich_media_operation`
   - `rich_media_bottom_tool`、`rich_media_global_like`
   - `activity-meta`、`rich_media_meta_list`、`profile_nickname` 等

2. **跳过噪音文本**（按关键词匹配）：
   - 底部操作栏：关注、赞、推荐、收藏、分享视频
   - 互动区：写留言、暂无留言、已无更多数据
   - 提示语：微信扫一扫、轻触阅读原文、预览时标签不可点
   - 视频控件：倍速播放中、切换到横屏模式、退出全屏

3. **HTML 标签转换规则**：

   | HTML 标签 | Markdown 输出 |
   |-----------|--------------|
   | `<h1>` ~ `<h6>` | `#` ~ `######` 标题 |
   | `<p>` | 段落文本 + 空行 |
   | `<strong>` / `<b>` | `**加粗**` |
   | `<em>` / `<i>` | `*斜体*` |
   | `<blockquote>` | `> 引用` |
   | `<ul>` / `<ol>` | `- 列表项` |
   | `<a>` | `[文本](链接)` |
   | `<img>` | `![alt](src)` |
   | `<hr>` | `---` |
   | `<section>` | 递归处理子元素 |
   | `<figure>` | 图片 + 可选 figcaption |

4. **图片处理**：
   - 优先取 `data-src`（公众号延迟加载属性），其次取 `src`
   - 自动补全 `//` 开头的协议
   - 过滤 `res.wx.qq.com/op_res/` 下的资源图标

5. **列表清洗**：
   - 去除列表项开头的装饰符号（`•·▪◦‣∙●○■□◆`）

6. **后处理**：
   - 合并连续空行为单个空行
   - 去除首尾空行

## 已知边界

- 这是"公众号正文提取器"，不是通用网页抽取器
- 部分文章如果页面结构特殊（如嵌套小程序、复杂卡片），清洗规则可能需要补充
- 纯文本方案无法处理需要 JavaScript 渲染的动态内容
- 如果遇到反爬拦截（返回验证码或空白页），建议切换到 camofox-browser 方案
- 图片链接来自微信 CDN（`mmbiz.qpic.cn`），可能有访问时效限制
- 公众号全文有时会分段加载，本方案只抓取首次加载的内容

## 何时优先使用这个 skill

当用户提到：

- 微信公众号文章
- 公众号链接抓取
- mp.weixin.qq.com
- 提取公众号正文
- 微信文章转 Markdown / JSON
- 批量保存公众号文章

## 何时切换到 camofox-browser 方案

当遇到以下情况：

- 文章返回空白内容或验证码
- 需要处理需要 JavaScript 渲染的动态页面
- 对反爬能力有更高要求

camofox-browser 方案参考：`https://github.com/dracohu2025-cloud/draco-skills-collection/tree/main/wechat-article-camofox`

## 一句话总结

**用 requests 获取 HTML，用 BeautifulSoup 解析结构，用公众号专用规则清洗噪音，输出干净的 Markdown / JSON —— 轻量、快速、零浏览器依赖。**

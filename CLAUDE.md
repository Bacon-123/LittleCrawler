# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

## 项目规则
1. 善用Task agent工具来完成每一步规划，执行规划步骤时也应当善用Task agent工具
2. 所有代码修改都必须通过测试，确保构建成功
3. 保证所有输出都是中文
4. 本CLUADE.md文档尽可能保持300行以内，超过300行时需要进行压缩，如果需要有其余规则，可引用.claude/rules/目录下的规则文件，每一个规则文件限制在300行以内
5. 所有任务遵循"先规划，再写代码"的原则
6. 没有权限执行，请使用sudo
7. 目前设置内存最大设置为8G，尽可能不要一次性解析过多的文件，导致内存溢出。

## 项目概述

LittleCrawler 是一个基于 Python 3.11+ asyncio 构建的多平台社交媒体爬虫框架。支持从小红书、知乎和闲鱼平台抓取数据。项目结合了强大的核心爬虫引擎和现代化的 Web 管理界面（FastAPI + Next.js）。

## 开发命令

**依赖管理：**
```bash
uv sync                              # 安装依赖（推荐）
pip install -r requirements.txt      # 使用 pip 安装
playwright install chromium          # 安装浏览器
```

**运行爬虫：**
```bash
uv run python main.py                                   # 使用 config/base_config.py 默认配置运行
uv run python main.py --platform xhs --type search     # 指定平台和类型
uv run python main.py --init-db sqlite                 # 初始化数据库
```

**Web 界面：**
```bash
cd web && npm run build                                # 构建前端到 api/ui/
uv run uvicorn api.main:app --port 8080 --reload       # 启动完整服务（API + 前端）
API_ONLY=1 uv run uvicorn api.main:app --port 8080     # 仅启动 API
cd web && npm run dev                                  # 前端开发模式
```

**测试：**
```bash
uv run pytest tests/                                   # 运行测试
```

**工具命令：**
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +   # 清除 Python 缓存
```

## 核心架构

### 双工厂模式

**CrawlerFactory** (`main.py:26-38`): 注册并创建平台特定的爬虫
```python
CrawlerFactory.CRAWLERS = {"xhs": XiaoHongShuCrawler, "zhihu": ZhihuCrawler}
```

**StoreFactory** (`src/storage/{platform}/__init__.py`): 创建存储后端（csv, db, json, sqlite, mongodb, excel）

### 抽象基类 (`src/core/base_crawler.py`)

| 基类 | 必须实现的方法 |
|------|---------------|
| `AbstractCrawler` | `start()`, `search()`, `launch_browser()` |
| `AbstractLogin` | `begin()`, `login_by_qrcode()`, `login_by_mobile()`, `login_by_cookies()` |
| `AbstractStore` | `store_content()`, `store_comment()`, `store_creator()` |
| `AbstractApiClient` | `request()`, `update_cookies()` |

### 平台模块结构 (`src/platforms/{platform}/`)

```
core.py      # 爬虫主入口，继承 AbstractCrawler
client.py    # API 客户端，带有 ProxyRefreshMixin 实现自动代理刷新
login.py     # 登录实现（扫码、手机、Cookie）
field.py     # 平台枚举类型（SearchSortType 等）
help.py      # 工具函数（URL 解析、签名等）
```

### 上下文变量模式 (`src/core/var.py`)

线程安全的异步上下文用于配置传递：
```python
crawler_type_var.set(config.CRAWLER_TYPE)  # 设置爬虫类型
source_keyword_var.set(keyword)            # 设置搜索关键词
```

### 浏览器模式

**CDP 模式** (`config.ENABLE_CDP_MODE=True`): 通过 DevTools Protocol 使用现有的 Chrome/Edge 浏览器，具有更好的反检测能力

**Playwright 模式** (`config.ENABLE_CDP_MODE=False`): 使用隐身脚本管理的浏览器实例 (`libs/stealth.min.js`)

### 人工行为模拟 (`src/utils/human_behavior.py`)

爬虫使用 `HumanBehavior` 类模拟真实用户行为，提供多种延迟策略：
- `page_view_delay()` - 页面浏览延迟（模拟阅读时间）
- `action_delay()` - 操作间隔延迟（模拟鼠标点击/滚动）
- `comment_crawl_delay()` - 评论爬取延迟
- `session_break_delay()` - 会话休息延迟
- `random_delay(min, max)` - 随机延迟

配置项在 `config/base_config.py`：
```python
ENABLE_HUMAN_BEHAVIOR = True    # 总开关
PAGE_VIEW_MIN_SEC = 2.0         # 页面浏览延迟区间
PAGE_VIEW_MAX_SEC = 5.0
ACTION_INTERVAL_MIN_SEC = 0.5   # 操作间隔延迟区间
ACTION_INTERVAL_MAX_SEC = 1.5
SESSION_BREAK_INTERVAL = 30      # 会话休息间隔（操作次数）
COMMENT_CRAWL_MIN_SEC = 1.0     # 评论爬取延迟区间
COMMENT_CRAWL_MAX_SEC = 2.5
```

## 配置 (`config/base_config.py`)

| 选项 | 可选值 | 说明 |
|------|--------|------|
| `PLATFORM` | `xhs`, `zhihu`, `xhy` | 目标平台 |
| `CRAWLER_TYPE` | `search`, `detail`, `creator` | 爬取模式 |
| `LOGIN_TYPE` | `qrcode`, `phone`, `cookie` | 登录方式 |
| `SAVE_DATA_OPTION` | `csv`, `json`, `db`, `sqlite`, `mongodb`, `excel` | 存储后端 |
| `ENABLE_CDP_MODE` | `True`, `False` | CDP 浏览器模式 |
| `ENABLE_IP_PROXY` | `True`, `False` | 启用代理池 |
| `ENABLE_HUMAN_BEHAVIOR` | `True`, `False` | 启用人工行为模拟 |

## 数据流

```
配置 → CrawlerFactory → 启动浏览器 → 身份认证 →
数据采集 → StoreFactory → 持久化 → Web UI/API
```

## 添加新平台

1. 创建 `src/platforms/{platform}/` 目录，包含 core.py, client.py, login.py, field.py, help.py
2. 创建 `src/storage/{platform}/__init__.py`，包含 StoreFactory 和 6 种存储实现
3. 在 `src/storage/base/models.py` 中添加 ORM 模型
4. 在 `src/models/m_{platform}.py` 中添加 Pydantic 模型
5. 创建 `config/{platform}_config.py` 配置文件
6. 在 `main.py::CrawlerFactory.CRAWLERS` 中注册

## 重要模式

- **全异步 I/O**: 所有地方使用 `async/await`
- **日志记录**: 从 `src.utils.utils import logger` 导入
- **重试机制**: 使用 tenacity 的 `@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))`
- **导入规范**: 核心代码使用 `from src.xxx import ...` 格式
- **数据去重**: DB 存储模式基于 note_id 内置去重功能
- **编码处理**: main.py 强制 UTF-8 编码处理 stdout/stderr 以支持中文字符

## Web API

默认凭据: `admin` / `admin123`

| 类别 | 路径 | 需要认证 |
|------|------|---------|
| 身份认证 | `/api/auth` | 否 |
| 爬虫控制 | `/api/crawler` | 是 |
| 数据管理 | `/api/data` | 是 |
| WebSocket | `/api/ws` | 否 |

---

## 📋 当前任务：数据展示平台重构

> 详细计划见：[docs/重构计划.md](docs/重构计划.md)
>
> **规则**：每完成一个任务必须验证通过，再进行下一个

### 任务状态跟踪

- [x] **1.1** 更新 `web/src/app/globals.css` - 配色方案 ✅
- [x] **1.2** 更新 `web/tailwind.config.ts` - 自定义颜色 ✅
- [x] **1.3** 更新 `web/src/components/Sidebar.tsx` - 导航栏样式 ✅
- [x] **1.4** 更新 `web/src/app/layout.tsx` - 整体布局 ✅
- [x] **2.1** 移除 `api/routers/crawler.py` ✅
- [x] **2.2** 移除 `api/services/crawler_manager.py` ✅
- [x] **2.3** 移除 `api/routers/websocket.py` ✅
- [x] **2.4** 更新 `api/main.py` - 移除路由注册 ✅
- [x] **2.5** 重构 `web/src/app/dashboard/page.tsx` - 移除爬虫配置 ✅
- [ ] **3.1** 创建 `api/services/data_service.py` - 数据库查询服务
- [ ] **3.2** 修改 `api/routers/data.py` - 添加数据路由
- [ ] **3.3** 修改 `api/schemas/crawler.py` - 添加响应模型
- [ ] **4.1** 创建 `web/src/lib/api.ts` - API 请求函数
- [ ] **4.2** 创建 `web/src/lib/api.types.ts` - TypeScript 类型
- [ ] **4.3** 创建 `web/src/app/dashboard/data/page.tsx` - 数据列表页
- [ ] **4.4** 创建 `web/src/components/DataTable.tsx` - 表格组件
- [ ] **5.1** 创建 `web/src/app/dashboard/data/notes/[noteId]/page.tsx` - 详情页
- [ ] **5.2** 创建 `web/src/components/CommentList.tsx` - 评论列表
- [ ] **5.3** 创建 `web/src/components/CommentItem.tsx` - 评论项

### 当前进度

```
阶段一：清理爬虫模块   [░░░░░░░░░░] 0%
阶段二：UI 风格重构     [░░░░░░░░░░] 0%
阶段三：后端 API 开发   [░░░░░░░░░░] 0%
阶段四：数据列表页     [░░░░░░░░░░] 0%
阶段五：笔记详情页     [░░░░░░░░░░] 0%
```

### 完成记录

<!-- 每个任务完成后，在此记录验证结果 -->

| 任务 | 完成时间 | 验证方式 | 状态 |
|------|----------|----------|------|
| 1.1 更新 globals.css | 2026-01-18 | CSS 语法检查通过 | ✅ |
| 1.2 更新 tailwind.config.ts | 2026-01-18 | TypeScript 配置检查通过 | ✅ |
| 1.3 更新 Sidebar.tsx | 2026-01-18 | 代码验证通过 | ✅ |
| 1.4 更新 layout.tsx | 2026-01-18 | 代码验证通过 | ✅ |
| 2.1 移除 crawler.py | 2026-01-18 | 文件删除 | ✅ |
| 2.2 移除 crawler_manager.py | 2026-01-18 | 文件删除 | ✅ |
| 2.3 移除 websocket.py | 2026-01-18 | 文件删除 | ✅ |
| 2.4 更新 main.py | 2026-01-18 | Python 语法检查通过 | ✅ |

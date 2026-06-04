# SimulatedBank

**[B站视频演示](https://www.bilibili.com/video/BV1k4VB6LEjF/?spm_id_from=333.1387.list.card_archive.click&vd_source=beaa4cb33880f51ae2a1246c529f75ca)** — 3分钟快速了解项目功能

一个模拟真实银行核心账务系统的个人理财项目。采用 SQL 数据库 + 复式记账（Double-Entry Ledger） 架构，不直接存储账户余额，而是通过所有交易流水实时计算得出，确保每一笔资金变动都有完整的借贷对应记录。集成 AI API 提供基于个人收支数据的智能理财建议。支持按月查看收支总览、分类支出统计、当前余额及最近五笔交易明细。

---

## 项目简介

本项目是一个基于FastAPI构建的模拟银行电子系统，使用MySQL作为数据存储，通过Jinja2模板渲染前端页面。核心设计理念借鉴真实银行系统：

- **余额实时计算**：不存储静态余额字段，所有账户余额通过聚合交易流水（`SUM(amount)`）动态计算，模拟真实银行核心账务处理。
- **AI 智能理财**：调用 Groq API（`openai/gpt-oss-20b`），根据用户当月收支数据生成个性化理财建议。
- **按月账单查询**：支持选择任意月份，展示该月收入、支出、余额、分类支出汇总及最近 5 笔交易记录。

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI |
| 数据库 | MySQL (PyMySQL) |
| 模板引擎 | Jinja2 |
| AI 接口 | Groq OpenAI API |
| 前端 | HTML + CSS (原生) |

---

## 项目结构

```
simulatedbank/
├── server.py              # FastAPI 主服务，路由与业务逻辑
├── SqlDataCreation.sql    # 数据库初始化脚本（表结构 + 示例数据）
├── templates/
│   ├── page0.html         # 银行首页（欢迎页）
│   ├── customer0.html     # 客户登录页
│   └── customer1.html     # 客户仪表盘（账单/AI建议/交易记录）
└── README.md
```

---

## 快速开始

### 1. 环境准备

确保已安装：
- Python
- MySQL数据库或其他SQL数据库
- 必要的Python依赖：

### 2. 数据库初始化

在 MySQL 中执行初始化脚本SqlDataCreation.sql，该脚本会：

- 创建 `simulated_bank` 数据库
- 创建 `transactions`（交易流水表）和 `cus_info`（客户信息表）
- 插入 2 个示例用户（`100001` / `100002`）及 2026 年 1-2 月的模拟交易数据

### 3. 配置服务

修改 `server.py` 开头的两处配置（或使用其他AI API或SQL数据库连接）：

```python
# AI API 配置（Groq）
client_ai = OpenAI(
    api_key="YOUR_GROQ_API_KEY",      # 填入你的 Groq API Key
    base_url="https://api.groq.com/openai/v1"
)

# MySQL 连接配置
def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",   # 填入你的 MySQL 密码
        database="simulated_bank",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
```

### 4. 启动服务

```bash
uvicorn server:app --reload
```

访问 `http://localhost:8000`（或你设置的localhost地址）即可使用。

---

## 功能说明

### 登录系统
- 客户 ID + 密码验证
- 示例账号：`100001` / `123456`（Tom Lee），`100002` / `123456`（Chen Yu）

### 仪表盘功能
- **月份选择**：通过 `type="month"` 选择任意月份（默认当前月）
- **收支总览**：实时计算并展示当月余额、总收入、总支出
- **分类支出**：按类型（工资/房租/购物/交通/转账）聚合展示
- **AI 理财建议**：基于当月收支数据，由 AI 生成 5 句话以内的中文建议
- **最近 5 笔交易**：按时间倒序展示最近交易记录

---

## 核心设计亮点

### Double-Entry Ledger 模拟

```sql
-- 余额实时计算，不存储余额字段
SELECT SUM(amount) FROM transactions WHERE account_id = '100001';
```

所有资金变动（收入为正、支出为负）以流水形式记录，余额通过聚合计算得出。这与真实银行核心系统一致：账户余额是派生数据，而非存储数据。

### AI 理财建议生成

系统通过 `get_financial_tip()` 函数将用户当月收支数据注入 Prompt，调用 Groq API 实时生成个性化中文理财建议，控制在 5 句话以内。

---

##

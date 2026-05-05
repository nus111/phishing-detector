<div align="center">

# 🛡️ 钓鱼检测器

**基于AI的钓鱼与欺诈检测系统**

[![CI](https://github.com/nus111/phishing-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/nus111/phishing-detector/actions/workflows/ci.yml)

**🌐 [English](README.md) | [中文](README_zh.md) | [Bahasa Melayu](README_ms.md) | [தமிழ்](README_ta.md)**

</div>

---

## 项目概述

一个基于多语言AI的实时钓鱼与欺诈消息检测系统，重点关注保护马来西亚非英语弱势群体（难民、外籍劳工、国际学生）。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React + Next.js + Tailwind CSS |
| 后端 | Python FastAPI |
| 数据库 | PostgreSQL |
| AI/ML | XLM-RoBERTa (Hugging Face Transformers) |
| 部署 | Docker + Docker Compose |

## 功能特性

- 🔍 **实时消息分析** — 粘贴任意消息即可检测钓鱼指标
- 🌍 **多语言支持** — English、中文、Bahasa Melayu、தமிழ்
- ⚠️ **风险评估** — 颜色分级风险（低/中/高）+ 详细解释
- 📚 **安全教育** — 提示、文章和测验，提升防钓鱼意识
- 📊 **管理后台** — 威胁趋势、语言分布、用户分析
- 🤖 **AI驱动** — XLM-RoBERTa 深度学习模型精准检测

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/nus111/phishing-detector.git
cd phishing-detector

# 复制环境配置
cp .env.example .env
# 编辑 .env 填入你的配置

# 启动所有服务
docker-compose up -d

# 访问：
# 前端：      http://localhost:3000
# 后端：      http://localhost:8000
# ML服务：    http://localhost:8001
# API文档：   http://localhost:8000/docs
```

## 项目结构

```
phishing-detector/
├── frontend/          # Next.js 前端（React + Tailwind + 国际化）
├── backend/           # FastAPI 后端（REST API + JWT 认证）
├── ml/                # ML 模型训练与推理服务
├── docs/              # API、模型、部署文档
├── docker-compose.yml # 服务编排
└── .env.example       # 环境变量模板
```

## API 接口

| 方法 | 端点 | 说明 | 认证 |
|------|------|------|------|
| POST | `/api/v1/auth/register` | 注册 | ❌ |
| POST | `/api/v1/auth/login` | 登录 | ❌ |
| GET | `/api/v1/auth/me` | 当前用户信息 | 🔒 |
| POST | `/api/v1/analyze` | 分析消息 | 🔒 |
| GET | `/api/v1/analyze/history` | 分析历史 | 🔒 |
| GET | `/api/v1/education` | 教育内容 | ❌ |
| POST | `/api/v1/education/quiz/submit` | 提交测验 | 🔒 |
| GET | `/api/v1/admin/dashboard` | 管理统计 | 👑 |

> 完整API文档请访问 `http://localhost:8000/docs`（Swagger UI）

## 团队成员

| 姓名 | 角色 | 职责 |
|------|------|------|
| 杨金涛 | 组长、前端开发 | UI/UX设计、网站开发、项目管理 |
| 林宇博 | 安全与后端工程师 | REST API、数据库、安全、部署 |
| 刘泽宇 | 首席数据工程师 | 数据预处理、特征提取、模型评估 |
| 李浩 | 数据工程师 | 数据收集、清洗、AI模型调优 |
| 杨俊熙 | ML/AI工程师 | 模型选择、微调、错误分析 |

## 指导老师

**Dr. Arafat Mohammed Rashad Al-dhaqm**
泰莱大学计算机科学学院

## 许可证

本项目为学术用途 — 泰莱大学毕业设计（PRJ63504）。

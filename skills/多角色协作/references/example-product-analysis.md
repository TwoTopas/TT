# 产品模式分析示例

用户说"产品模式"时，输出结构参考。

## 示例场景：设计一个任务管理应用

### 角色 1：产品经理
- **用户需求**: 个人和小团队需要轻量级任务管理，比 Trello 简单，比 Todoist 灵活
- **核心功能**:
  - 看板视图 + 列表视图
  - 任务依赖关系
  - 简单的权限（所有者/协作者）
- **MVP 范围**: 看板 + 列表 + 基础协作，排除 Gantt 图和自动化

### 角色 2：架构师
- **前端**: React + Tailwind CSS，响应式设计
- **后端**: Node.js + Express + SQLite（MVP），后续 PostgreSQL
- **API**: RESTful，OpenAPI 3.0 文档
- **部署**: Docker Compose，单机部署

### 角色 3：开发者
- **数据模型**: Board → List → Card
- **API 端点**: CRUD /boards, /lists, /cards
- **前端组件**: BoardView, ListColumn, CardItem, DragHandle

### 总结
MVP 以看板为核心，三人团队开发周期约 4 周。

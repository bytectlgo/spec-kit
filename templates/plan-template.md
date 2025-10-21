# 实现计划：[功能]

**分支**：`[###-feature-name]` | **日期**：[日期] | **规范**：[链接]
**输入**：来自 `/specs/[###-feature-name]/spec.md` 的功能规范

**注意**：此模板由 `/speckit.plan` 命令填充。有关执行工作流，请参见 `.specify/templates/commands/plan.md`。

## 摘要

[从功能规范中提取：来自研究的主要需求 + 技术方法]

## 技术上下文

<!--
  需要行动：用项目的技术详细信息替换本节中的内容。
  此处的结构以咨询身份呈现，以指导迭代过程。
-->

**语言/版本**：[例如 Python 3.11、Swift 5.9、Rust 1.75 或需要澄清]  
**主要依赖项**：[例如 FastAPI、UIKit、LLVM 或需要澄清]  
**存储**：[如果适用，例如 PostgreSQL、CoreData、文件或 N/A]  
**测试**：[例如 pytest、XCTest、cargo test 或需要澄清]  
**目标平台**：[例如 Linux 服务器、iOS 15+、WASM 或需要澄清]
**项目类型**：[单个/web/移动 - 确定源结构]  
**性能目标**：[特定于领域，例如 1000 请求/秒、10k 行/秒、60 fps 或需要澄清]  
**约束**：[特定于领域，例如 <200ms p95、<100MB 内存、离线能力或需要澄清]  
**规模/范围**：[特定于领域，例如 10k 用户、1M LOC、50 个屏幕或需要澄清]

## 宪章检查

*门控：必须在第 0 阶段研究之前通过。在第 1 阶段设计后重新检查。*

[根据宪章文件确定的门控]

## 项目结构

### 文档（此功能）

```
specs/[###-feature]/
├── plan.md              # 此文件（/speckit.plan 命令输出）
├── research.md          # 第 0 阶段输出（/speckit.plan 命令）
├── data-model.md        # 第 1 阶段输出（/speckit.plan 命令）
├── quickstart.md        # 第 1 阶段输出（/speckit.plan 命令）
├── contracts/           # 第 1 阶段输出（/speckit.plan 命令）
└── tasks.md             # 第 2 阶段输出（/speckit.tasks 命令 - 不是由 /speckit.plan 创建）
```

### 源代码（仓库根目录）
<!--
  需要行动：用此功能的具体布局替换下面的占位符树。
  删除未使用的选项并扩展所选结构，包含真实路径
  （例如 apps/admin、packages/something）。交付的计划不得
  包含选项标签。
-->

```
# [如果未使用则删除] 选项 1：单个项目（默认）
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [如果未使用则删除] 选项 2：Web 应用程序（当检测到"前端"+"后端"时）
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [如果未使用则删除] 选项 3：移动 + API（当检测到"iOS/Android"时）
api/
└── [与上面的后端相同]

ios/ or android/
└── [特定于平台的结构：功能模块、UI 流程、平台测试]
```

**结构决策**：[记录所选结构并引用上面捕获的真实目录]

## 复杂性跟踪

*仅当宪章检查有必须证明的违规行为时才填写*

| 违规 | 为什么需要 | 拒绝更简单替代方案的原因 |
|-----------|------------|-------------------------------------|
| [例如第 4 个项目] | [当前需求] | [为什么 3 个项目不够] |
| [例如仓库模式] | [特定问题] | [为什么直接 DB 访问不够] |

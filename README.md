<div align="center">
    <img src="./media/logo_small.webp"/>
    <h1>🌱 Spec Kit</h1>
    <h3><em>更快地构建高质量软件</em></h3>
</div>

<p align="center">
    <strong>一个开源工具包，让你专注于产品场景和可预测的结果，而不是从头开始凭感觉编写每一段代码。</strong>
</p>

<p align="center">
    <a href="https://github.com/github/spec-kit/actions/workflows/release.yml"><img src="https://github.com/github/spec-kit/actions/workflows/release.yml/badge.svg" alt="Release"/></a>
    <a href="https://github.com/github/spec-kit/stargazers"><img src="https://img.shields.io/github/stars/github/spec-kit?style=social" alt="GitHub stars"/></a>
    <a href="https://github.com/github/spec-kit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/github/spec-kit" alt="License"/></a>
    <a href="https://github.github.io/spec-kit/"><img src="https://img.shields.io/badge/docs-GitHub_Pages-blue" alt="Documentation"/></a>
</p>

---

## 目录

- [🤔 什么是规范驱动开发？](#-什么是规范驱动开发)
- [⚡ 快速开始](#-快速开始)
- [📽️ 视频概览](#️-视频概览)
- [🤖 支持的 AI 代理](#-支持的-ai-代理)
- [🔧 Specify CLI 参考](#-specify-cli-参考)
- [📚 核心理念](#-核心理念)
- [🌟 开发阶段](#-开发阶段)
- [🎯 实验目标](#-实验目标)
- [🔧 前置要求](#-前置要求)
- [📖 了解更多](#-了解更多)
- [📋 详细流程](#-详细流程)
- [🔍 故障排除](#-故障排除)
- [👥 维护者](#-维护者)
- [💬 支持](#-支持)
- [🙏 致谢](#-致谢)
- [📄 许可证](#-许可证)

## 🤔 什么是规范驱动开发？

规范驱动开发（Spec-Driven Development）**改变了**传统软件开发的规则。几十年来，代码一直是王道——规范只是我们搭建然后在"真正的编码工作"开始后就丢弃的脚手架。规范驱动开发改变了这一点：**规范变得可执行**，直接生成可工作的实现，而不仅仅是指导它们。

## ⚡ 快速开始

### 1. 安装 Specify CLI

选择您首选的安装方法：

#### 选项 1：持久安装（推荐）

一次安装，到处使用：

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

然后直接使用工具：

```bash
specify init <PROJECT_NAME>
specify check
```

升级 specify 运行：

```bash
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git
```

#### 选项 2：一次性使用

直接运行而无需安装：

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

**持久安装的好处：**

- 工具保持安装状态并在 PATH 中可用
- 无需创建 shell 别名
- 使用 `uv tool list`、`uv tool upgrade`、`uv tool uninstall` 更好地管理工具
- 更简洁的 shell 配置

### 2. 建立项目原则

在项目目录中启动您的 AI 助手。助手中可以使用 `/speckit.*` 命令。

使用 **`/speckit.constitution`** 命令创建项目的管理原则和开发指南，这将指导所有后续开发。

```bash
/speckit.constitution 创建关注代码质量、测试标准、用户体验一致性和性能要求的原则
```

### 3. 创建规范

使用 **`/speckit.specify`** 命令描述您想要构建什么。专注于**做什么**和**为什么**，而不是技术栈。

```bash
/speckit.specify 构建一个可以帮助我将照片组织到单独相册中的应用程序。相册按日期分组，可以在主页上拖放重新组织。相册不会嵌套在其他相册中。在每个相册内，照片以类似瓷砖的界面预览。
```

### 4. 创建技术实现计划

使用 **`/speckit.plan`** 命令提供您的技术栈和架构选择。

```bash
/speckit.plan 应用程序使用 Vite，库的数量最少。尽可能使用原生 HTML、CSS 和 JavaScript。图片不会上传到任何地方，元数据存储在本地 SQLite 数据库中。
```

### 5. 分解为任务

使用 **`/speckit.tasks`** 从实现计划创建可操作的任务列表。

```bash
/speckit.tasks
```

### 6. 执行实现

使用 **`/speckit.implement`** 执行所有任务并根据计划构建您的功能。

```bash
/speckit.implement
```

有关详细的分步说明，请参阅我们的[综合指南](./spec-driven.md)。

## 📽️ 视频概览

想看看 Spec Kit 的实际效果吗？观看我们的[视频概览](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)！

[![Spec Kit 视频标题](/media/spec-kit-video-header.jpg)](https://www.youtube.com/watch?v=a9eR1xsfvHg&pp=0gcJCckJAYcqIYzv)

## 🤖 支持的 AI 代理

| 代理                                                     | 支持 | 说明                                             |
|-----------------------------------------------------------|---------|---------------------------------------------------|
| [Claude Code](https://www.anthropic.com/claude-code)      | ✅ |                                                   |
| [GitHub Copilot](https://code.visualstudio.com/)          | ✅ |                                                   |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | ✅ |                                                   |
| [Cursor](https://cursor.sh/)                              | ✅ |                                                   |
| [Qwen Code](https://github.com/QwenLM/qwen-code)          | ✅ |                                                   |
| [opencode](https://opencode.ai/)                          | ✅ |                                                   |
| [Windsurf](https://windsurf.com/)                         | ✅ |                                                   |
| [Kilo Code](https://github.com/Kilo-Org/kilocode)         | ✅ |                                                   |
| [Auggie CLI](https://docs.augmentcode.com/cli/overview)   | ✅ |                                                   |
| [CodeBuddy CLI](https://www.codebuddy.ai/cli)             | ✅ |                                                   |
| [Roo Code](https://roocode.com/)                          | ✅ |                                                   |
| [Codex CLI](https://github.com/openai/codex)              | ✅ |                                                   |
| [Amazon Q Developer CLI](https://aws.amazon.com/developer/learning/q-developer-cli/) | ⚠️ | Amazon Q Developer CLI [不支持](https://github.com/aws/amazon-q-developer-cli/issues/3064)斜杠命令的自定义参数。 |

## 🔧 Specify CLI 参考

`specify` 命令支持以下选项：

### 命令

| 命令     | 描述                                                    |
|-------------|----------------------------------------------------------------|
| `init`      | 从最新模板初始化新的 Specify 项目      |
| `check`     | 检查已安装的工具（`git`、`claude`、`gemini`、`code`/`code-insiders`、`cursor-agent`、`windsurf`、`qwen`、`opencode`、`codex`） |

### `specify init` 参数和选项

| 参数/选项        | 类型     | 描述                                                                  |
|------------------------|----------|------------------------------------------------------------------------------|
| `<project-name>`       | 参数 | 新项目目录的名称（如果使用 `--here` 则可选，或使用 `.` 表示当前目录） |
| `--ai`                 | 选项   | 要使用的 AI 助手：`claude`、`gemini`、`copilot`、`cursor-agent`、`qwen`、`opencode`、`codex`、`windsurf`、`kilocode`、`auggie`、`roo`、`codebuddy` 或 `q` |
| `--script`             | 选项   | 要使用的脚本变体：`sh`（bash/zsh）或 `ps`（PowerShell）                 |
| `--ignore-agent-tools` | 标志     | 跳过对 AI 代理工具（如 Claude Code）的检查                             |
| `--no-git`             | 标志     | 跳过 git 仓库初始化                                          |
| `--here`               | 标志     | 在当前目录初始化项目而不是创建新目录   |
| `--force`              | 标志     | 在当前目录初始化时强制合并/覆盖（跳过确认） |
| `--skip-tls`           | 标志     | 跳过 SSL/TLS 验证（不推荐）                                 |
| `--debug`              | 标志     | 启用详细调试输出以进行故障排除                            |
| `--github-token`       | 选项   | 用于 API 请求的 GitHub token（或设置 GH_TOKEN/GITHUB_TOKEN 环境变量）  |

### 示例

```bash
# 基本项目初始化
specify init my-project

# 使用特定 AI 助手初始化
specify init my-project --ai claude

# 使用 Cursor 支持初始化
specify init my-project --ai cursor-agent

# 使用 Windsurf 支持初始化
specify init my-project --ai windsurf

# 使用 PowerShell 脚本初始化（Windows/跨平台）
specify init my-project --ai copilot --script ps

# 在当前目录初始化
specify init . --ai copilot
# 或使用 --here 标志
specify init --here --ai copilot

# 强制合并到当前（非空）目录而不确认
specify init . --force --ai copilot
# 或 
specify init --here --force --ai copilot

# 跳过 git 初始化
specify init my-project --ai gemini --no-git

# 启用调试输出以进行故障排除
specify init my-project --ai claude --debug

# 使用 GitHub token 进行 API 请求（对企业环境有帮助）
specify init my-project --ai claude --github-token ghp_your_token_here

# 检查系统要求
specify check
```

### 可用的斜杠命令

运行 `specify init` 后，您的 AI 编码代理将可以访问这些用于结构化开发的斜杠命令：

#### 核心命令

规范驱动开发工作流的基本命令：

| 命令                  | 描述                                                           |
|--------------------------|-----------------------------------------------------------------------|
| `/speckit.constitution`  | 创建或更新项目管理原则和开发指南 |
| `/speckit.specify`       | 定义您想要构建什么（需求和用户故事）        |
| `/speckit.plan`          | 使用您选择的技术栈创建技术实现计划     |
| `/speckit.tasks`         | 生成实现的可操作任务列表                     |
| `/speckit.implement`     | 执行所有任务以根据计划构建功能         |

#### 可选命令

用于增强质量和验证的其他命令：

| 命令              | 描述                                                           |
|----------------------|-----------------------------------------------------------------------|
| `/speckit.clarify`   | 澄清未充分指定的领域（建议在 `/speckit.plan` 之前；以前称为 `/quizme`） |
| `/speckit.analyze`   | 跨工件一致性和覆盖率分析（在 `/speckit.tasks` 之后、`/speckit.implement` 之前运行） |
| `/speckit.checklist` | 生成自定义质量检查清单，验证需求的完整性、清晰度和一致性（类似于"英语的单元测试"） |

### 环境变量

| 变量         | 描述                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| `SPECIFY_FEATURE` | 覆盖非 Git 仓库的功能检测。设置为功能目录名称（例如 `001-photo-albums`）以在不使用 Git 分支时处理特定功能。<br/>**必须在使用 `/speckit.plan` 或后续命令之前在您正在使用的代理的上下文中设置。 |

## 📚 核心理念

规范驱动开发是一个结构化流程，强调：

- **意图驱动开发**，其中规范在"_如何_"之前定义"_做什么_"
- **使用护栏和组织原则创建丰富的规范**
- **多步骤细化**而不是从提示一次性生成代码
- **大量依赖**高级 AI 模型功能进行规范解释

## 🌟 开发阶段

| 阶段 | 重点 | 关键活动 |
|-------|-------|----------------|
| **0-to-1 开发**（"绿地"） | 从头开始生成 | <ul><li>从高级需求开始</li><li>生成规范</li><li>计划实现步骤</li><li>构建生产就绪的应用程序</li></ul> |
| **创意探索** | 并行实现 | <ul><li>探索多样化的解决方案</li><li>支持多种技术栈和架构</li><li>实验 UX 模式</li></ul> |
| **迭代增强**（"棕地"） | 棕地现代化 | <ul><li>迭代添加功能</li><li>现代化遗留系统</li><li>适应流程</li></ul> |

## 🎯 实验目标

我们的研究和实验重点是：

### 技术独立性

- 使用多样化的技术栈创建应用程序
- 验证规范驱动开发是一个不依赖于特定技术、编程语言或框架的流程的假设

### 企业约束

- 演示关键任务应用程序开发
- 整合组织约束（云提供商、技术栈、工程实践）
- 支持企业设计系统和合规要求

### 以用户为中心的开发

- 为不同的用户群体和偏好构建应用程序
- 支持各种开发方法（从凭感觉编码到 AI 原生开发）

### 创意和迭代流程

- 验证并行实现探索的概念
- 提供强大的迭代功能开发工作流
- 扩展流程以处理升级和现代化任务

## 🔧 前置要求

- **Linux/macOS/Windows**
- [支持的](#-支持的-ai-代理) AI 编码代理。
- [uv](https://docs.astral.sh/uv/) 用于包管理
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

如果您在使用代理时遇到问题，请提交 issue，以便我们改进集成。

## 📖 了解更多

- **[完整的规范驱动开发方法论](./spec-driven.md)** - 深入了解完整流程
- **[详细演练](#-详细流程)** - 分步实现指南

---

## 📋 详细流程

<details>
<summary>点击展开详细的分步演练</summary>

您可以使用 Specify CLI 引导您的项目，它将在您的环境中引入所需的工件。运行：

```bash
specify init <project_name>
```

或在当前目录初始化：

```bash
specify init .
# 或使用 --here 标志
specify init --here
# 当目录已有文件时跳过确认
specify init . --force
# 或
specify init --here --force
```

![Specify CLI 在终端中引导新项目](./media/specify_cli.gif)

系统将提示您选择正在使用的 AI 代理。您也可以直接在终端中主动指定它：

```bash
specify init <project_name> --ai claude
specify init <project_name> --ai gemini
specify init <project_name> --ai copilot

# 或在当前目录：
specify init . --ai claude
specify init . --ai codex

# 或使用 --here 标志
specify init --here --ai claude
specify init --here --ai codex

# 强制合并到非空的当前目录
specify init . --force --ai claude

# 或
specify init --here --force --ai claude
```

CLI 将检查您是否安装了 Claude Code、Gemini CLI、Cursor CLI、Qwen CLI、opencode、Codex CLI 或 Amazon Q Developer CLI。如果您没有安装，或者您希望获取模板而不检查正确的工具，请在命令中使用 `--ignore-agent-tools`：

```bash
specify init <project_name> --ai claude --ignore-agent-tools
```

### **步骤 1：** 建立项目原则

进入项目文件夹并运行您的 AI 代理。在我们的示例中，我们使用 `claude`。

![引导 Claude Code 环境](./media/bootstrap-claude-code.gif)

如果您看到 `/speckit.constitution`、`/speckit.specify`、`/speckit.plan`、`/speckit.tasks` 和 `/speckit.implement` 命令可用，就说明配置正确了。

第一步应该是使用 `/speckit.constitution` 命令建立项目的管理原则。这有助于确保在所有后续开发阶段中做出一致的决策：

```text
/speckit.constitution 创建关注代码质量、测试标准、用户体验一致性和性能要求的原则。包括关于这些原则应如何指导技术决策和实现选择的治理。
```

此步骤创建或更新 `.specify/memory/constitution.md` 文件，其中包含 AI 代理在规范、计划和实现阶段将参考的项目基础指南。

### **步骤 2：** 创建项目规范

建立项目原则后，您现在可以创建功能规范。使用 `/speckit.specify` 命令，然后提供您想要开发的项目的具体需求。

>[!IMPORTANT]
>尽可能明确地说明您想要构建_什么_以及_为什么_。**此时不要关注技术栈**。

示例提示：

```text
开发 Taskify，一个团队生产力平台。它应该允许用户创建项目、添加团队成员、
分配任务、评论并以看板风格在看板之间移动任务。在这个功能的初始阶段，
我们称之为"创建 Taskify"，让我们有多个用户，但用户将提前声明，预定义。
我想要五个用户，分为两个不同的类别，一个产品经理和四个工程师。让我们创建三个
不同的示例项目。让我们为每个任务的状态设置标准的看板列，例如"待办"、
"进行中"、"审核中"和"完成"。此应用程序将没有登录功能，因为这只是第一个
测试性的东西，以确保我们的基本功能已设置。对于任务卡的 UI 中的每个任务，
您应该能够在看板工作板的不同列之间更改任务的当前状态。
您应该能够为特定卡片留下无限数量的评论。您应该能够从该任务
卡中分配一个有效用户。当您首次启动 Taskify 时，它将为您提供五个用户的列表供选择。
不需要密码。当您单击用户时，您将进入主视图，该视图显示项目列表。当您单击项目时，您将打开该项目的看板。您将看到各列。
您将能够在不同的列之间拖放卡片。您将看到分配给您（当前登录的用户）的任何卡片以不同的颜色显示，
与所有其他卡片不同，这样您就可以快速看到您的卡片。您可以编辑您所做的任何评论，但不能编辑其他人的评论。您可以
删除您所做的任何评论，但不能删除其他人的评论。
```

输入此提示后，您应该会看到 Claude Code 启动计划和规范起草过程。Claude Code 还将触发一些内置脚本来设置仓库。

此步骤完成后，您应该有一个新创建的分支（例如 `001-create-taskify`），以及 `specs/001-create-taskify` 目录中的新规范。

生成的规范应包含一组用户故事和功能需求，如模板中所定义。

在此阶段，您的项目文件夹内容应类似于以下内容：

```text
└── .specify
    ├── memory
    │	 └── constitution.md
    ├── scripts
    │	 ├── check-prerequisites.sh
    │	 ├── common.sh
    │	 ├── create-new-feature.sh
    │	 ├── setup-plan.sh
    │	 └── update-claude-md.sh
    ├── specs
    │	 └── 001-create-taskify
    │	     └── spec.md
    └── templates
        ├── plan-template.md
        ├── spec-template.md
        └── tasks-template.md
```

### **步骤 3：** 功能规范澄清（计划前必需）

有了基线规范后，您可以继续澄清第一次尝试中未正确捕获的任何需求。

您应该在创建技术计划**之前**运行结构化的澄清工作流，以减少下游的返工。

首选顺序：
1. 使用 `/speckit.clarify`（结构化）- 顺序的、基于覆盖率的提问，将答案记录在澄清部分。
2. 如果某些内容仍然感觉模糊，可以选择跟进自由形式的细化。

如果您有意想跳过澄清（例如尖峰或探索性原型），请明确说明，以便代理不会因缺少澄清而阻塞。

示例自由形式细化提示（在 `/speckit.clarify` 之后，如果仍然需要）：

```text
对于您创建的每个示例项目或项目，应该有 5 到 15 个
任务的可变数量，随机分布到不同的完成状态。确保至少有
每个完成阶段至少有一个任务。
```

您还应该要求 Claude Code 验证**审核和验收清单**，勾选通过需求/验证的项目，并将未通过的项目留空。可以使用以下提示：

```text
阅读审核和验收清单，如果功能规范满足标准，则勾选清单中的每个项目。如果不满足，则留空。
```

重要的是要利用与 Claude Code 的交互作为澄清和询问有关规范的问题的机会 - **不要将其第一次尝试视为最终版本**。

### **步骤 4：** 生成计划

您现在可以具体说明技术栈和其他技术要求。您可以使用项目模板中内置的 `/speckit.plan` 命令，提示如下：

```text
我们将使用 .NET Aspire 生成此内容，使用 Postgres 作为数据库。前端应该使用
Blazor 服务器，具有拖放任务板、实时更新。应该使用 REST API 创建项目 API、
任务 API 和通知 API。
```

此步骤的输出将包括许多实现细节文档，您的目录树类似于：

```text
.
├── CLAUDE.md
├── memory
│	 └── constitution.md
├── scripts
│	 ├── check-prerequisites.sh
│	 ├── common.sh
│	 ├── create-new-feature.sh
│	 ├── setup-plan.sh
│	 └── update-claude-md.sh
├── specs
│	 └── 001-create-taskify
│	     ├── contracts
│	     │	 ├── api-spec.json
│	     │	 └── signalr-spec.md
│	     ├── data-model.md
│	     ├── plan.md
│	     ├── quickstart.md
│	     ├── research.md
│	     └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

检查 `research.md` 文档以确保根据您的说明使用了正确的技术栈。如果任何组件突出，您可以要求 Claude Code 进行改进，或者甚至让它检查您想要使用的平台/框架的本地安装版本（例如 .NET）。

此外，如果选择的技术栈是快速变化的东西（例如 .NET Aspire、JS 框架），您可能想要求 Claude Code 研究有关该技术栈的详细信息，使用如下提示：

```text
我希望您查看实现计划和实现细节，寻找可能
受益于额外研究的领域，因为 .NET Aspire 是一个快速变化的库。对于您识别的需要
进一步研究的领域，我希望您使用有关我们将在此 Taskify 应用程序中使用的特定
版本的额外详细信息更新研究文档，并生成并行研究任务以使用网络研究澄清
任何细节。
```

在此过程中，您可能会发现 Claude Code 卡在研究错误的东西上 - 您可以帮助它朝正确的方向推动，使用如下提示：

```text
我认为我们需要将其分解为一系列步骤。首先，确定您在实现过程中需要执行的任务列表，
这些任务您不确定或将受益于进一步研究。写下这些任务的列表。然后对于这些任务中的每一个，
我希望您启动一个单独的研究任务，以便最终结果是我们并行研究
所有这些非常具体的任务。我看到您所做的是看起来您正在研究 .NET Aspire 的一般内容，我认为这对我们没有太大帮助。
那太笼统的研究了。研究需要帮助您解决特定的针对性问题。
```

>[!NOTE]
>Claude Code 可能过于热情，添加您没有要求的组件。要求它澄清变更的理由和来源。

### **步骤 5：** 让 Claude Code 验证计划

有了计划后，您应该让 Claude Code 检查它，以确保没有遗漏的部分。您可以使用如下提示：

```text
现在我希望您检查实现计划和实现细节文件。
仔细阅读，以确定是否有您需要执行的明显任务序列。因为我不知道这里是否足够。例如，
当我查看核心实现时，有用的是在实现
细节中的适当位置引用，在那里它可以在核心实现或细化中的每个步骤中找到信息。
```

这有助于改进实现计划，并帮助您避免 Claude Code 在计划周期中遗漏的潜在盲点。初步改进完成后，在进入实现之前再次要求 Claude Code 检查清单。

您还可以要求 Claude Code（如果安装了 [GitHub CLI](https://docs.github.com/en/github-cli/github-cli)）从当前分支创建一个拉取请求到 `main`，并提供详细描述，以确保正确跟踪工作。

>[!NOTE]
>在让代理实现之前，还值得提示 Claude Code 交叉检查细节，看看是否有任何过度工程化的部分（记住 - 它可能过于热情）。如果存在过度工程化的组件或决策，您可以要求 Claude Code 解决它们。确保 Claude Code 遵循[宪章](base/memory/constitution.md)作为它在建立计划时必须遵守的基础部分。

### **步骤 6：** 使用 /speckit.tasks 生成任务分解

验证实现计划后，您现在可以将计划分解为可以按正确顺序执行的具体可操作任务。使用 `/speckit.tasks` 命令从实现计划自动生成详细的任务分解：

```text
/speckit.tasks
```

此步骤在您的功能规范目录中创建一个 `tasks.md` 文件，其中包含：

- **按用户故事组织的任务分解** - 每个用户故事成为一个单独的实现阶段，具有自己的任务集
- **依赖管理** - 任务按顺序排列以尊重组件之间的依赖关系（例如模型在服务之前，服务在端点之前）
- **并行执行标记** - 可以并行运行的任务用 `[P]` 标记以优化开发工作流
- **文件路径规范** - 每个任务包括应发生实现的确切文件路径
- **测试驱动开发结构** - 如果请求测试，则包括测试任务并按顺序排列在实现之前编写
- **检查点验证** - 每个用户故事阶段包括检查点以验证独立功能

生成的 tasks.md 为 `/speckit.implement` 命令提供了清晰的路线图，确保系统实现以保持代码质量并允许逐步交付用户故事。

### **步骤 7：** 实现

准备就绪后，使用 `/speckit.implement` 命令执行实现计划：

```text
/speckit.implement
```

`/speckit.implement` 命令将：
- 验证所有先决条件是否就绪（宪章、规范、计划和任务）
- 从 `tasks.md` 解析任务分解
- 按正确顺序执行任务，尊重依赖关系和并行执行标记
- 遵循任务计划中定义的 TDD 方法
- 提供进度更新并适当处理错误

>[!IMPORTANT]
>AI 代理将执行本地 CLI 命令（例如 `dotnet`、`npm` 等）- 确保您的计算机上安装了所需的工具。

实现完成后，测试应用程序并解决 CLI 日志中可能不可见的任何运行时错误（例如浏览器控制台错误）。您可以将此类错误复制并粘贴回您的 AI 代理以进行解决。

</details>

---

## 🔍 故障排除

### Linux 上的 Git Credential Manager

如果您在 Linux 上遇到 Git 身份验证问题，可以安装 Git Credential Manager：

```bash
#!/usr/bin/env bash
set -e
echo "下载 Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "安装 Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "配置 Git 使用 GCM..."
git config --global credential.helper manager
echo "清理..."
rm gcm-linux_amd64.2.6.1.deb
```

## 👥 维护者

- Den Delimarsky ([@localden](https://github.com/localden))
- John Lam ([@jflam](https://github.com/jflam))

## 💬 支持

如需支持，请提交 [GitHub issue](https://github.com/github/spec-kit/issues/new)。我们欢迎错误报告、功能请求和关于使用规范驱动开发的问题。

## 🙏 致谢

该项目深受 [John Lam](https://github.com/jflam) 的工作和研究的影响和基础。

## 📄 许可证

该项目根据 MIT 开源许可证的条款授权。请参阅 [LICENSE](./LICENSE) 文件了解完整条款。

## 为 Spec Kit 做贡献

你好！我们很高兴你想为 Spec Kit 做贡献。对该项目的贡献根据[项目的开源许可证](LICENSE)向公众[发布](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license)。

请注意，该项目发布时附有[贡献者行为准则](CODE_OF_CONDUCT.md)。参与该项目即表示您同意遵守其条款。

## 运行和测试代码的前置条件

这些是一次性安装，需要能够在本地测试您的更改作为拉取请求（PR）提交流程的一部分。

1. 安装 [Python 3.11+](https://www.python.org/downloads/)
1. 安装 [uv](https://docs.astral.sh/uv/) 用于包管理
1. 安装 [Git](https://git-scm.com/downloads)
1. 拥有一个[可用的 AI 编码代理](README.md#-支持的-ai-代理)

<details>
<summary><b>💡 如果您使用 <code>VSCode</code> 或 <code>GitHub Codespaces</code> 作为 IDE 的提示</b></summary>

<br>

如果您的计算机上安装了 [Docker](https://docker.com)，您可以通过此 [VSCode 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)利用 [Dev Containers](https://containers.dev) 轻松设置开发环境，得益于 `.devcontainer/devcontainer.json` 文件（位于项目根目录），上述工具已经安装和配置。

为此，只需：

- 检出仓库
- 使用 VSCode 打开
- 打开[命令面板](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette)并选择"Dev Containers: Open Folder in Container..."

在 [GitHub Codespaces](https://github.com/features/codespaces) 上更简单，因为它在打开代码空间时会自动利用 `.devcontainer/devcontainer.json`。

</details>

## 提交拉取请求

>[!NOTE]
>如果您的拉取请求引入了重大更改，会对 CLI 或仓库的其余部分的工作产生实质性影响（例如，您正在引入新模板、参数或其他重大更改），请确保项目维护者已**讨论并同意**。未经事先对话和协议的包含重大更改的拉取请求将被关闭。

1. Fork 并克隆仓库
1. 配置并安装依赖项：`uv sync`
1. 确保 CLI 在您的机器上工作：`uv run specify --help`
1. 创建一个新分支：`git checkout -b my-branch-name`
1. 进行更改，添加测试，并确保一切仍然正常工作
1. 如果相关，使用示例项目测试 CLI 功能
1. 推送到您的 fork 并提交拉取请求
1. 等待您的拉取请求被审核和合并。

以下几点可以增加您的拉取请求被接受的可能性：

- 遵循项目的编码约定。
- 为新功能编写测试。
- 如果您的更改影响面向用户的功能，请更新文档（`README.md`、`spec-driven.md`）。
- 尽可能保持更改的重点。如果您想进行多个不相互依赖的更改，请考虑将它们作为单独的拉取请求提交。
- 编写[良好的提交消息](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)。
- 使用规范驱动开发工作流测试您的更改以确保兼容性。

## 开发工作流

在 spec-kit 上工作时：

1. 在您选择的编码代理中使用 `specify` CLI 命令（`/speckit.specify`、`/speckit.plan`、`/speckit.tasks`）测试更改
2. 验证 `templates/` 目录中的模板是否正常工作
3. 测试 `scripts/` 目录中的脚本功能
4. 如果进行了重大流程更改，请确保更新内存文件（`memory/constitution.md`）

## Spec Kit 中的 AI 贡献

> [!IMPORTANT]
>
> 如果您使用**任何类型的 AI 辅助**为 Spec Kit 做贡献，
> 必须在拉取请求或 issue 中披露。

我们欢迎并鼓励使用 AI 工具来帮助改进 Spec Kit！许多有价值的贡献都通过 AI 辅助在代码生成、问题检测和功能定义方面得到了增强。

话虽如此，如果您在为 Spec Kit 做贡献时使用任何类型的 AI 辅助（例如代理、ChatGPT），
**必须在拉取请求或 issue 中披露**，以及 AI 辅助的使用程度（例如文档注释与代码生成）。

如果您的 PR 响应或评论是由 AI 生成的，也请披露。

作为例外，无关紧要的间距或拼写错误修复不需要披露，只要更改仅限于代码的小部分或短语。

示例披露：

> 此 PR 主要由 GitHub Copilot 编写。

或更详细的披露：

> 我咨询了 ChatGPT 以了解代码库，但解决方案
> 完全由我自己手动编写。

未披露这一点首先对拉取请求另一端的人类操作员不礼貌，而且还使得
难以确定应对贡献应用多少审查。

在理想的世界中，AI 辅助将产生与任何人类相同或更高质量的工作。这不是我们今天生活的世界，在大多数情况下，
如果人类监督或专业知识不在循环中，它会生成无法合理维护或演变的代码。

### 我们正在寻找什么

提交 AI 辅助的贡献时，请确保它们包括：

- **明确披露 AI 使用** - 您对 AI 使用以及您在贡献中使用它的程度保持透明
- **人类理解和测试** - 您已亲自测试了更改并理解它们的作用
- **清晰的理由** - 您可以解释为什么需要更改以及它如何适合 Spec Kit 的目标  
- **具体证据** - 包括测试用例、场景或演示改进的示例
- **您自己的分析** - 分享您对端到端开发人员体验的想法

### 我们将关闭什么

我们保留关闭以下贡献的权利：

- 未经验证提交的未测试更改
- 不针对特定 Spec Kit 需求的通用建议
- 显示没有人工审查或理解的批量提交

### 成功指南

关键是证明您理解并验证了您提议的更改。如果维护者可以轻松判断贡献完全由 AI 生成而没有人工输入或测试，则它可能需要在提交前进行更多工作。

持续提交低质量 AI 生成更改的贡献者可能会根据维护者的决定被限制进一步贡献。

请尊重维护者并披露 AI 辅助。

## 资源

- [规范驱动开发方法论](./spec-driven.md)
- [如何为开源做贡献](https://opensource.guide/how-to-contribute/)
- [使用拉取请求](https://help.github.com/articles/about-pull-requests/)
- [GitHub 帮助](https://help.github.com)

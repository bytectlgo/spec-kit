# 更新日志

<!-- markdownlint-disable MD024 -->

Specify CLI 和模板的所有显著更改都在此记录。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，
本项目遵循[语义化版本](https://semver.org/spec/v2.0.0.html)。

## [0.0.20] - 2025-10-14

### 新增

- **智能分支命名**：`create-new-feature` 脚本现在支持 `--short-name` 参数用于自定义分支名称
  - 当提供 `--short-name` 时：直接使用自定义名称（清理和格式化后）
  - 当省略时：使用停用词过滤和基于长度的过滤自动生成有意义的名称
  - 过滤掉常见的停用词（I、want、to、the、for 等）
  - 删除短于 3 个字符的单词（除非它们是大写首字母缩略词）
  - 从描述中提取 3-4 个最有意义的单词
  - **强制执行 GitHub 的 244 字节分支名称限制**，带有自动截断和警告
  - 示例：
    - "I want to create user authentication" → `001-create-user-authentication`
    - "Implement OAuth2 integration for API" → `001-implement-oauth2-integration-api`
    - "Fix payment processing bug" → `001-fix-payment-processing`
    - 非常长的描述会在单词边界自动截断以保持在限制内
  - 设计用于 AI 代理提供语义短名称，同时保持独立可用性

### 更改

- 增强了 `create-new-feature.sh` 和 `create-new-feature.ps1` 脚本的帮助文档，添加了示例
- 分支名称现在根据 GitHub 的 244 字节限制进行验证，如果需要会自动截断

## [0.0.19] - 2025-10-10

### 新增

- 支持 CodeBuddy（感谢 [@lispking](https://github.com/lispking) 的贡献）。
- 您现在可以在 Specify CLI 中看到来自 Git 的错误。

### 更改

- 修复了 `plan.md` 中宪章的路径（感谢 [@lyzno1](https://github.com/lyzno1) 发现）。
- 修复了为 Gemini 生成的 TOML 文件中的反斜杠转义（感谢 [@hsin19](https://github.com/hsin19) 的贡献）。
- 实现命令现在确保添加正确的忽略文件（感谢 [@sigent-amazon](https://github.com/sigent-amazon) 的贡献）。

## [0.0.18] - 2025-10-06

### 新增

- 支持在 `specify init .` 命令中使用 `.` 作为当前目录的简写，等同于 `--here` 标志，但对用户来说更直观。
- 使用 `/speckit.` 命令前缀轻松发现 Spec Kit 相关命令。
- 重构提示和模板以简化其功能和跟踪方式。不再在不需要时用测试污染内容。
- 确保每个用户故事创建任务（简化测试和验证）。
- 添加对 Visual Studio Code 提示快捷方式和自动脚本执行的支持。

### 更改

- 所有命令文件现在以 `speckit.` 为前缀（例如 `speckit.specify.md`、`speckit.plan.md`），以便在 IDE/CLI 命令面板和文件资源管理器中更好地发现和区分

## [0.0.17] - 2025-09-22

### 新增

- 新的 `/clarify` 命令模板，用于为现有规范提出最多 5 个有针对性的澄清问题，并将答案持久化到规范的澄清部分。
- 新的 `/analyze` 命令模板，提供非破坏性的跨工件差异和对齐报告（规范、澄清、计划、任务、宪章），插入在 `/tasks` 之后和 `/implement` 之前。
	- 注意：宪章规则明确被视为不可协商的；任何冲突都是需要工件修复的关键发现，而不是削弱原则。

## [0.0.16] - 2025-09-22

### 新增

- `init` 命令的 `--force` 标志，在非空目录中使用 `--here` 时绕过确认并继续合并/覆盖文件。

## [0.0.15] - 2025-09-21

### 新增

- 支持 Roo Code。

## [0.0.14] - 2025-09-21

### 更改

- 错误消息现在一致地显示。

## [0.0.13] - 2025-09-21

### 新增

- 支持 Kilo Code。感谢 [@shahrukhkhan489](https://github.com/shahrukhkhan489) 的 [#394](https://github.com/github/spec-kit/pull/394)。
- 支持 Auggie CLI。感谢 [@hungthai1401](https://github.com/hungthai1401) 的 [#137](https://github.com/github/spec-kit/pull/137)。
- 项目配置完成后显示代理文件夹安全通知，警告用户某些代理可能会在其代理文件夹中存储凭证或身份验证令牌，并建议将相关文件夹添加到 `.gitignore` 以防止意外泄露凭证。

### 更改

- 显示警告以确保人们知道他们可能需要将代理文件夹添加到 `.gitignore`。
- 清理了 `check` 命令输出。

## [0.0.12] - 2025-09-21

### 更改

- 为 OpenAI Codex 用户添加了额外的上下文 - 他们需要设置额外的环境变量，如 [#417](https://github.com/github/spec-kit/issues/417) 中所述。

## [0.0.11] - 2025-09-20

### 新增

- Codex CLI 支持（感谢 [@honjo-hiroaki-gtt](https://github.com/honjo-hiroaki-gtt) 在 [#14](https://github.com/github/spec-kit/pull/14) 中的贡献）
- Codex 感知的上下文更新工具（Bash 和 PowerShell），因此功能计划会刷新 `AGENTS.md`，与现有助手一起，无需手动编辑。

## [0.0.10] - 2025-09-20

### 修复

- 解决了 [#378](https://github.com/github/spec-kit/issues/378)，当 GitHub token 为空时可能会附加到请求的问题。

## [0.0.9] - 2025-09-19

### 更改

- 改进了代理选择器 UI，对代理键使用青色高亮，对全名使用灰色括号

## [0.0.8] - 2025-09-19

### 新增

- Windsurf IDE 支持作为额外的 AI 助手选项（感谢 [@raedkit](https://github.com/raedkit) 在 [#151](https://github.com/github/spec-kit/pull/151) 中的工作）
- GitHub token 支持 API 请求以处理企业环境和速率限制（由 [@zryfish](https://github.com/@zryfish) 在 [#243](https://github.com/github/spec-kit/pull/243) 中贡献）

### 更改

- 更新了 README，添加了 Windsurf 示例和 GitHub token 使用
- 增强了发布工作流以包含 Windsurf 模板

## [0.0.7] - 2025-09-18

### 更改

- 更新了 CLI 中的命令说明。
- 清理了代码，在通用时不渲染代理特定信息。


## [0.0.6] - 2025-09-17

### 新增

- 支持 opencode 作为额外的 AI 助手选项

## [0.0.5] - 2025-09-17

### 新增

- 支持 Qwen Code 作为额外的 AI 助手选项

## [0.0.4] - 2025-09-14

### 新增

- 通过 `httpx[socks]` 依赖项为企业环境提供 SOCKS 代理支持

### 修复

无

### 更改

无

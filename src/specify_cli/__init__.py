#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
Specify CLI - Specify 项目的设置工具

用法：
    uvx specify-cli.py init <project-name>
    uvx specify-cli.py init .
    uvx specify-cli.py init --here

或全局安装：
    uv tool install --from specify-cli.py specify-cli
    specify init <project-name>
    specify init .
    specify init --here
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from pathlib import Path
from typing import Optional, Tuple

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# 跨平台键盘输入
import readchar
import ssl
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def _github_token(cli_token: str | None = None) -> str | None:
    """返回清理后的 GitHub 令牌（CLI 参数优先）或 None。"""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None

def _github_auth_headers(cli_token: str | None = None) -> dict:
    """仅当存在非空令牌时返回 Authorization 头字典。"""
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}

# 代理配置，包含名称、文件夹、安装 URL 和 CLI 工具要求
AGENT_CONFIG = {
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "install_url": None,  # 基于 IDE，无需 CLI 检查
        "requires_cli": False,
    },
    "claude": {
        "name": "Claude Code",
        "folder": ".claude/",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini/",
        "install_url": "https://github.com/google-gemini/gemini-cli",
        "requires_cli": True,
    },
    "cursor-agent": {
        "name": "Cursor",
        "folder": ".cursor/",
        "install_url": None,  # 基于 IDE
        "requires_cli": False,
    },
    "qwen": {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    },
    "opencode": {
        "name": "opencode",
        "folder": ".opencode/",
        "install_url": "https://opencode.ai",
        "requires_cli": True,
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex/",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    },
    "windsurf": {
        "name": "Windsurf",
        "folder": ".windsurf/",
        "install_url": None,  # 基于 IDE
        "requires_cli": False,
    },
    "kilocode": {
        "name": "Kilo Code",
        "folder": ".kilocode/",
        "install_url": None,  # 基于 IDE
        "requires_cli": False,
    },
    "auggie": {
        "name": "Auggie CLI",
        "folder": ".augment/",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    },
    "codebuddy": {
        "name": "CodeBuddy",
        "folder": ".codebuddy/",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    },
    "roo": {
        "name": "Roo Code",
        "folder": ".roo/",
        "install_url": None,  # 基于 IDE
        "requires_cli": False,
    },
    "q": {
        "name": "Amazon Q Developer CLI",
        "folder": ".amazonq/",
        "install_url": "https://aws.amazon.com/developer/learning/q-developer-cli/",
        "requires_cli": True,
    },
}

SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}

CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"

BANNER = """
███████╗██████╗ ███████╗ ██████╗██╗███████╗██╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔════╝╚██╗ ██╔╝
███████╗██████╔╝█████╗  ██║     ██║█████╗   ╚████╔╝ 
╚════██║██╔═══╝ ██╔══╝  ██║     ██║██╔══╝    ╚██╔╝  
███████║██║     ███████╗╚██████╗██║██║        ██║   
╚══════╝╚═╝     ╚══════╝ ╚═════╝╚═╝╚═╝        ╚═╝   
"""

TAGLINE = "GitHub Spec Kit - 规范驱动开发工具包"
class StepTracker:
    """跟踪和渲染分层步骤，不使用表情符号，类似于 Claude Code 树形输出。
    支持通过附加的刷新回调进行实时自动刷新。
    """
    def __init__(self, title: str):
        self.title = title
        self.steps = []  # 字典列表：{key, label, status, detail}
        self.status_order = {"pending": 0, "running": 1, "done": 2, "error": 3, "skipped": 4}
        self._refresh_cb = None  # 用于触发 UI 刷新的可调用对象

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return

        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                # Entire line light gray (pending)
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                # Label white, detail (if any) light gray in parentheses
                if detail_text:
                    line = f"{symbol} [white]{label}[/white] [bright_black]({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree

def get_key():
    """使用 readchar 以跨平台方式获取单个按键。"""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return 'up'
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return 'down'

    if key == readchar.key.ENTER:
        return 'enter'

    if key == readchar.key.ESC:
        return 'escape'

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key

def select_with_arrows(options: dict, prompt_text: str = "选择一个选项", default_key: str = None) -> str:
    """
    使用箭头键进行交互式选择，带有 Rich Live 显示。
    
    参数：
        options: 选项键作为键、描述作为值的字典
        prompt_text: 在选项上方显示的文本
        default_key: 默认开始的选项键
        
    返回：
        选中的选项键
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """创建带有当前选择高亮的选择面板。"""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]使用 ↑/↓ 导航，回车选择，Esc 取消[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2)
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(create_selection_panel(), console=console, transient=True, auto_refresh=False) as live:
            while True:
                try:
                    key = get_key()
                    if key == 'up':
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == 'down':
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == 'enter':
                        selected_key = option_keys[selected_index]
                        break
                    elif key == 'escape':
                        console.print("\n[yellow]选择已取消[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]选择已取消[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]选择失败。[/red]")
        raise typer.Exit(1)

    return selected_key

console = Console()

class BannerGroup(TyperGroup):
    """自定义组，在帮助之前显示横幅。"""

    def format_help(self, ctx, formatter):
        # 在帮助之前显示横幅
        show_banner()
        super().format_help(ctx, formatter)


app = typer.Typer(
    name="specify",
    help="Specify 规范驱动开发项目的设置工具",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)

def show_banner():
    """显示 ASCII 艺术横幅。"""
    banner_lines = BANNER.strip().split('\n')
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()

@app.callback()
def callback(ctx: typer.Context):
    """在未提供子命令时显示横幅。"""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]运行 'specify --help' 获取使用信息[/dim]"))
        console.print()

def run_command(cmd: list[str], check_return: bool = True, capture: bool = False, shell: bool = False) -> Optional[str]:
    """运行 shell 命令并可选地捕获输出。"""
    try:
        if capture:
            result = subprocess.run(cmd, check=check_return, capture_output=True, text=True, shell=shell)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]运行命令时出错：[/red] {' '.join(cmd)}")
            console.print(f"[red]退出代码：[/red] {e.returncode}")
            if hasattr(e, 'stderr') and e.stderr:
                console.print(f"[red]错误输出：[/red] {e.stderr}")
            raise
        return None

def check_tool(tool: str, tracker: StepTracker = None) -> bool:
    """检查工具是否已安装。可选地更新跟踪器。
    
    参数：
        tool: 要检查的工具名称
        tracker: 可选的 StepTracker 用于更新结果
        
    返回：
        如果找到工具则返回 True，否则返回 False
    """
    # 对 Claude CLI 在 `claude migrate-installer` 后的特殊处理
    # 参见：https://github.com/bytectlgo/spec-kit/issues/123
    # migrate-installer 命令从 PATH 中删除原始可执行文件
    # 并在 ~/.claude/local/claude 创建别名
    # 此路径应优先于 PATH 中的其他 claude 可执行文件
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            if tracker:
                tracker.complete(tool, "available")
            return True
    
    found = shutil.which(tool) is not None
    
    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")
    
    return found

def is_git_repo(path: Path = None) -> bool:
    """检查指定路径是否在 git 仓库内。"""
    if path is None:
        path = Path.cwd()
    
    if not path.is_dir():
        return False

    try:
        # 使用 git 命令检查是否在工作树内
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo(project_path: Path, quiet: bool = False) -> Tuple[bool, Optional[str]]:
    """在指定路径初始化 git 仓库。
    
    参数：
        project_path: 要在其中初始化 git 仓库的路径
        quiet: 如果为 True 则抑制控制台输出（跟踪器处理状态）
    
    返回：
        (success: bool, error_message: Optional[str]) 的元组
    """
    try:
        original_cwd = Path.cwd()
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]正在初始化 git 仓库...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from Specify template"], check=True, capture_output=True, text=True)
        if not quiet:
            console.print("[green]✓[/green] Git 仓库已初始化")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"命令：{' '.join(e.cmd)}\n退出代码：{e.returncode}"
        if e.stderr:
            error_msg += f"\n错误：{e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\n输出：{e.stdout.strip()}"
        
        if not quiet:
            console.print(f"[red]初始化 git 仓库时出错：[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)

def handle_vscode_settings(sub_item, dest_file, rel_path, verbose=False, tracker=None) -> None:
    """处理 .vscode/settings.json 文件的合并或复制。"""
    def log(message, color="green"):
        if verbose and not tracker:
            console.print(f"[{color}]{message}[/] {rel_path}")

    try:
        with open(sub_item, 'r', encoding='utf-8') as f:
            new_settings = json.load(f)

        if dest_file.exists():
            merged = merge_json_files(dest_file, new_settings, verbose=verbose and not tracker)
            with open(dest_file, 'w', encoding='utf-8') as f:
                json.dump(merged, f, indent=4)
                f.write('\n')
            log("已合并：", "green")
        else:
            shutil.copy2(sub_item, dest_file)
            log("已复制（不存在 settings.json）：", "blue")

    except Exception as e:
        log(f"警告：无法合并，改为复制：{e}", "yellow")
        shutil.copy2(sub_item, dest_file)

def merge_json_files(existing_path: Path, new_content: dict, verbose: bool = False) -> dict:
    """将新的 JSON 内容合并到现有 JSON 文件中。

    执行深度合并：
    - 添加新键
    - 保留现有键，除非被新内容覆盖
    - 递归合并嵌套字典
    - 替换（不合并）列表和其他值

    参数：
        existing_path: 现有 JSON 文件的路径
        new_content: 要合并的新 JSON 内容
        verbose: 是否打印合并详细信息

    返回：
        合并后的 JSON 内容，作为字典
    """
    try:
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件不存在或无效，则仅使用新内容
        return new_content

    def deep_merge(base: dict, update: dict) -> dict:
        """递归地将 update 字典合并到 base 字典中。"""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # 递归合并嵌套字典
                result[key] = deep_merge(result[key], value)
            else:
                # 添加新键或替换现有值
                result[key] = value
        return result

    merged = deep_merge(existing_content, new_content)

    if verbose:
        console.print(f"[cyan]已合并 JSON 文件：[/cyan] {existing_path.name}")

    return merged

def download_template_from_github(ai_assistant: str, download_dir: Path, *, script_type: str = "sh", verbose: bool = True, show_progress: bool = True, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Tuple[Path, dict]:
    repo_owner = "bytectlgo"
    repo_name = "spec-kit"
    if client is None:
        client = httpx.Client(verify=ssl_context)

    if verbose:
        console.print("[cyan]正在获取最新发布信息...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            msg = f"GitHub API 为 {api_url} 返回 {status}"
            if debug:
                msg += f"\n响应头：{response.headers}\n正文（截断 500）：{response.text[:500]}"
            raise RuntimeError(msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"解析发布 JSON 失败：{je}\n原始内容（截断 400）：{response.text[:400]}")
    except Exception as e:
        console.print(f"[red]获取发布信息时出错[/red]")
        console.print(Panel(str(e), title="获取错误", border_style="red"))
        raise typer.Exit(1)

    assets = release_data.get("assets", [])
    pattern = f"spec-kit-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets
        if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(f"[red]未找到匹配的发布资产[/red] 对于 [bold]{ai_assistant}[/bold]（期望模式：[bold]{pattern}[/bold]）")
        asset_names = [a.get('name', '?') for a in assets]
        console.print(Panel("\n".join(asset_names) or "（无资产）", title="可用资产", border_style="yellow"))
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]找到模板：[/cyan] {filename}")
        console.print(f"[cyan]大小：[/cyan] {file_size:,} 字节")
        console.print(f"[cyan]发布：[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print(f"[cyan]正在下载模板...[/cyan]")

    try:
        with client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                body_sample = response.text[:400]
                raise RuntimeError(f"下载失败，状态码 {response.status_code}\n头部：{response.headers}\n正文（截断）：{body_sample}")
            total_size = int(response.headers.get('content-length', 0))
            with open(zip_path, 'wb') as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[progress.description]{task.description}"),
                            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                            console=console,
                        ) as progress:
                            task = progress.add_task("正在下载...", total=total_size)
                            downloaded = 0
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                                downloaded += len(chunk)
                                progress.update(task, completed=downloaded)
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
    except Exception as e:
        console.print(f"[red]下载模板时出错[/red]")
        detail = str(e)
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(detail, title="下载错误", border_style="red"))
        raise typer.Exit(1)
    if verbose:
        console.print(f"已下载：{filename}")
    metadata = {
        "filename": filename,
        "size": file_size,
        "release": release_data["tag_name"],
        "asset_url": download_url
    }
    return zip_path, metadata

def download_and_extract_template(project_path: Path, ai_assistant: str, script_type: str, is_current_dir: bool = False, *, verbose: bool = True, tracker: StepTracker | None = None, client: httpx.Client = None, debug: bool = False, github_token: str = None) -> Path:
    """下载最新发布并提取以创建新项目。
    返回 project_path。如果提供则使用 tracker（键：fetch、download、extract、cleanup）
    """
    current_dir = Path.cwd()

    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta['filename'])
    except Exception as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    zip_ref.extractall(temp_path)

                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print(f"[cyan]Found nested directory structure[/cyan]")

                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                for sub_item in item.rglob('*'):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        # Special handling for .vscode/settings.json - merge instead of overwrite
                                        if dest_file.name == "settings.json" and dest_file.parent.name == ".vscode":
                                            handle_vscode_settings(sub_item, dest_file, rel_path, verbose, tracker)
                                        else:
                                            shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print(f"[cyan]Template files merged into current directory[/cyan]")
            else:
                zip_ref.extractall(project_path)

                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"

                    shutil.move(str(nested_dir), str(temp_move_dir))

                    project_path.rmdir()

                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print(f"[cyan]Flattened nested directory structure[/cyan]")

    except Exception as e:
        if tracker:
            tracker.error("extract", str(e))
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")

        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path


def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """确保 .specify/scripts 下的 POSIX .sh 脚本（递归）具有执行权限（Windows 上为空操作）。"""
    if os.name == "nt":
        return  # Windows：静默跳过
    scripts_root = project_path / ".specify" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except Exception:
                continue
            st = script.stat(); mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400: new_mode |= 0o100
            if mode & 0o040: new_mode |= 0o010
            if mode & 0o004: new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except Exception as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]")
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for f in failures:
                console.print(f"  - {f}")

@app.command()
def init(
    project_name: str = typer.Argument(None, help="新项目目录的名称（如果使用 --here 则可选，或使用 '.' 表示当前目录）"),
    ai_assistant: str = typer.Option(None, "--ai", help="要使用的 AI 助手：claude、gemini、copilot、cursor-agent、qwen、opencode、codex、windsurf、kilocode、auggie、codebuddy 或 q"),
    script_type: str = typer.Option(None, "--script", help="要使用的脚本类型：sh 或 ps"),
    ignore_agent_tools: bool = typer.Option(False, "--ignore-agent-tools", help="跳过对 AI 代理工具（如 Claude Code）的检查"),
    no_git: bool = typer.Option(False, "--no-git", help="跳过 git 仓库初始化"),
    here: bool = typer.Option(False, "--here", help="在当前目录初始化项目，而不是创建新目录"),
    force: bool = typer.Option(False, "--force", help="使用 --here 时强制合并/覆盖（跳过确认）"),
    skip_tls: bool = typer.Option(False, "--skip-tls", help="跳过 SSL/TLS 验证（不推荐）"),
    debug: bool = typer.Option(False, "--debug", help="显示网络和提取失败的详细诊断输出"),
    github_token: str = typer.Option(None, "--github-token", help="用于 API 请求的 GitHub 令牌（或设置 GH_TOKEN 或 GITHUB_TOKEN 环境变量）"),
):
    """
    从最新模板初始化新的 Specify 项目。
    
    此命令将：
    1. 检查所需工具是否已安装（git 是可选的）
    2. 让您选择 AI 助手
    3. 从 GitHub 下载适当的模板
    4. 将模板提取到新项目目录或当前目录
    5. 初始化一个新的 git 仓库（如果不是 --no-git 且没有现有仓库）
    6. 可选地设置 AI 助手命令
    
    示例：
        specify init my-project
        specify init my-project --ai claude
        specify init my-project --ai copilot --no-git
        specify init --ignore-agent-tools my-project
        specify init . --ai claude         # 在当前目录初始化
        specify init .                     # 在当前目录初始化（交互式 AI 选择）
        specify init --here --ai claude    # 当前目录的替代语法
        specify init --here --ai codex
        specify init --here --ai codebuddy
        specify init --here
        specify init --here --force  # 当前目录不为空时跳过确认
    """

    show_banner()

    if project_name == ".":
        here = True
        project_name = None  # Clear project_name to use existing validation logic

    if here and project_name:
        console.print("[red]错误：[/red] 不能同时指定项目名称和 --here 标志")
        raise typer.Exit(1)

    if not here and not project_name:
        console.print("[red]错误：[/red] 必须指定项目名称、使用 '.' 表示当前目录或使用 --here 标志")
        raise typer.Exit(1)

    if here:
        project_name = Path.cwd().name
        project_path = Path.cwd()

        existing_items = list(project_path.iterdir())
        if existing_items:
            console.print(f"[yellow]警告：[/yellow] 当前目录不为空（{len(existing_items)} 个项目）")
            console.print("[yellow]模板文件将与现有内容合并，可能会覆盖现有文件[/yellow]")
            if force:
                console.print("[cyan]已提供 --force：跳过确认并继续合并[/cyan]")
            else:
                response = typer.confirm("您要继续吗？")
                if not response:
                    console.print("[yellow]操作已取消[/yellow]")
                    raise typer.Exit(0)
    else:
        project_path = Path(project_name).resolve()
        if project_path.exists():
            error_panel = Panel(
                f"目录 '[cyan]{project_name}[/cyan]' 已存在\n"
                "请选择不同的项目名称或删除现有目录。",
                title="[red]目录冲突[/red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print()
            console.print(error_panel)
            raise typer.Exit(1)

    current_dir = Path.cwd()

    setup_lines = [
        "[cyan]Specify 项目设置[/cyan]",
        "",
        f"{'项目':<15} [green]{project_path.name}[/green]",
        f"{'工作路径':<15} [dim]{current_dir}[/dim]",
    ]

    if not here:
        setup_lines.append(f"{'目标路径':<15} [dim]{project_path}[/dim]")

    console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

    should_init_git = False
    if not no_git:
        should_init_git = check_tool("git")
        if not should_init_git:
            console.print("[yellow]未找到 Git - 将跳过仓库初始化[/yellow]")

    if ai_assistant:
        if ai_assistant not in AGENT_CONFIG:
            console.print(f"[red]错误：[/red] 无效的 AI 助手 '{ai_assistant}'。请从以下选择：{', '.join(AGENT_CONFIG.keys())}")
            raise typer.Exit(1)
        selected_ai = ai_assistant
    else:
        # 创建选择选项字典（agent_key: display_name）
        ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
        selected_ai = select_with_arrows(
            ai_choices, 
            "选择您的 AI 助手：", 
            "copilot"
        )

    if not ignore_agent_tools:
        agent_config = AGENT_CONFIG.get(selected_ai)
        if agent_config and agent_config["requires_cli"]:
            install_url = agent_config["install_url"]
            if not check_tool(selected_ai):
                error_panel = Panel(
                    f"[cyan]{selected_ai}[/cyan] 未找到\n"
                    f"从以下位置安装：[cyan]{install_url}[/cyan]\n"
                    f"需要 {agent_config['name']} 才能继续此项目类型。\n\n"
                    "提示：使用 [cyan]--ignore-agent-tools[/cyan] 跳过此检查",
                    title="[red]代理检测错误[/red]",
                    border_style="red",
                    padding=(1, 2)
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)

    if script_type:
        if script_type not in SCRIPT_TYPE_CHOICES:
            console.print(f"[red]错误：[/red] 无效的脚本类型 '{script_type}'。请从以下选择：{', '.join(SCRIPT_TYPE_CHOICES.keys())}")
            raise typer.Exit(1)
        selected_script = script_type
    else:
        default_script = "ps" if os.name == "nt" else "sh"

        if sys.stdin.isatty():
            selected_script = select_with_arrows(SCRIPT_TYPE_CHOICES, "选择脚本类型（或按回车）", default_script)
        else:
            selected_script = default_script

    console.print(f"[cyan]选择的 AI 助手：[/cyan] {selected_ai}")
    console.print(f"[cyan]选择的脚本类型：[/cyan] {selected_script}")

    tracker = StepTracker("初始化 Specify 项目")

    sys._specify_tracker_active = True

    tracker.add("precheck", "检查所需工具")
    tracker.complete("precheck", "ok")
    tracker.add("ai-select", "选择 AI 助手")
    tracker.complete("ai-select", f"{selected_ai}")
    tracker.add("script-select", "选择脚本类型")
    tracker.complete("script-select", selected_script)
    for key, label in [
        ("fetch", "获取最新发布"),
        ("download", "下载模板"),
        ("extract", "提取模板"),
        ("zip-list", "存档内容"),
        ("extracted-summary", "提取摘要"),
        ("chmod", "确保脚本可执行"),
        ("cleanup", "清理"),
        ("git", "初始化 git 仓库"),
        ("final", "完成")
    ]:
        tracker.add(key, label)

    # 在 Live 上下文之外跟踪 git 错误消息，以便它持久存在
    git_error_message = None

    with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
        tracker.attach_refresh(lambda: live.update(tracker.render()))
        try:
            verify = not skip_tls
            local_ssl_context = ssl_context if verify else False
            local_client = httpx.Client(verify=local_ssl_context)

            download_and_extract_template(project_path, selected_ai, selected_script, here, verbose=False, tracker=tracker, client=local_client, debug=debug, github_token=github_token)

            ensure_executable_scripts(project_path, tracker=tracker)

            if not no_git:
                tracker.start("git")
                if is_git_repo(project_path):
                    tracker.complete("git", "existing repo detected")
                elif should_init_git:
                    success, error_msg = init_git_repo(project_path, quiet=True)
                    if success:
                        tracker.complete("git", "initialized")
                    else:
                        tracker.error("git", "init failed")
                        git_error_message = error_msg
                else:
                    tracker.skip("git", "git not available")
            else:
                tracker.skip("git", "--no-git flag")

            tracker.complete("final", "项目已就绪")
        except Exception as e:
            tracker.error("final", str(e))
            console.print(Panel(f"初始化失败：{e}", title="失败", border_style="red"))
            if debug:
                _env_pairs = [
                    ("Python", sys.version.split()[0]),
                    ("平台", sys.platform),
                    ("当前目录", str(Path.cwd())),
                ]
                _label_width = max(len(k) for k, _ in _env_pairs)
                env_lines = [f"{k.ljust(_label_width)} → [bright_black]{v}[/bright_black]" for k, v in _env_pairs]
                console.print(Panel("\n".join(env_lines), title="调试环境", border_style="magenta"))
            if not here and project_path.exists():
                shutil.rmtree(project_path)
            raise typer.Exit(1)
        finally:
            pass

    console.print(tracker.render())
    console.print("\n[bold green]项目已就绪。[/bold green]")
    
    # 如果初始化失败，显示 git 错误详细信息
    if git_error_message:
        console.print()
        git_error_panel = Panel(
            f"[yellow]警告：[/yellow] Git 仓库初始化失败\n\n"
            f"{git_error_message}\n\n"
            f"[dim]您可以稍后手动初始化 git：[/dim]\n"
            f"[cyan]cd {project_path if not here else '.'}[/cyan]\n"
            f"[cyan]git init[/cyan]\n"
            f"[cyan]git add .[/cyan]\n"
            f"[cyan]git commit -m \"Initial commit\"[/cyan]",
            title="[red]Git 初始化失败[/red]",
            border_style="red",
            padding=(1, 2)
        )
        console.print(git_error_panel)

    # 代理文件夹安全通知
    agent_config = AGENT_CONFIG.get(selected_ai)
    if agent_config:
        agent_folder = agent_config["folder"]
        security_notice = Panel(
            f"某些代理可能会在项目的代理文件夹中存储凭据、身份验证令牌或其他识别和私有工件。\n"
            f"考虑将 [cyan]{agent_folder}[/cyan]（或其部分）添加到 [cyan].gitignore[/cyan] 以防止意外泄露凭据。",
            title="[yellow]代理文件夹安全[/yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print()
        console.print(security_notice)

    steps_lines = []
    if not here:
        steps_lines.append(f"1. 进入项目文件夹：[cyan]cd {project_name}[/cyan]")
        step_num = 2
    else:
        steps_lines.append("1. 您已在项目目录中！")
        step_num = 2

    # 如果需要，添加 Codex 特定的设置步骤
    if selected_ai == "codex":
        codex_path = project_path / ".codex"
        quoted_path = shlex.quote(str(codex_path))
        if os.name == "nt":  # Windows
            cmd = f"setx CODEX_HOME {quoted_path}"
        else:  # Unix-like systems
            cmd = f"export CODEX_HOME={quoted_path}"
        
        steps_lines.append(f"{step_num}. 在运行 Codex 之前设置 [cyan]CODEX_HOME[/cyan] 环境变量：[cyan]{cmd}[/cyan]")
        step_num += 1

    steps_lines.append(f"{step_num}. 开始在您的 AI 代理中使用斜杠命令：")

    steps_lines.append("   2.1 [cyan]/speckit.constitution[/] - 建立项目原则")
    steps_lines.append("   2.2 [cyan]/speckit.specify[/] - 创建基线规范")
    steps_lines.append("   2.3 [cyan]/speckit.plan[/] - 创建实现计划")
    steps_lines.append("   2.4 [cyan]/speckit.tasks[/] - 生成可操作的任务")
    steps_lines.append("   2.5 [cyan]/speckit.implement[/] - 执行实现")

    steps_panel = Panel("\n".join(steps_lines), title="下一步", border_style="cyan", padding=(1,2))
    console.print()
    console.print(steps_panel)

    enhancement_lines = [
        "可用于规范的可选命令 [bright_black]（提高质量和信心）[/bright_black]",
        "",
        f"○ [cyan]/speckit.clarify[/] [bright_black]（可选）[/bright_black] - 在计划前提出结构化问题以降低模糊区域的风险（如果使用则在 [cyan]/speckit.plan[/] 之前运行）",
        f"○ [cyan]/speckit.analyze[/] [bright_black]（可选）[/bright_black] - 跨工件一致性和对齐报告（在 [cyan]/speckit.tasks[/] 之后，[cyan]/speckit.implement[/] 之前）",
        f"○ [cyan]/speckit.checklist[/] [bright_black]（可选）[/bright_black] - 生成质量检查清单以验证需求的完整性、清晰度和一致性（在 [cyan]/speckit.plan[/] 之后）"
    ]
    enhancements_panel = Panel("\n".join(enhancement_lines), title="增强命令", border_style="cyan", padding=(1,2))
    console.print()
    console.print(enhancements_panel)

@app.command()
def check():
    """检查所有必需的工具是否已安装。"""
    show_banner()
    console.print("[bold]正在检查已安装的工具...[/bold]\n")

    tracker = StepTracker("检查可用工具")

    tracker.add("git", "Git 版本控制")
    git_ok = check_tool("git", tracker=tracker)

    agent_results = {}
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]
        requires_cli = agent_config["requires_cli"]

        tracker.add(agent_key, agent_name)

        if requires_cli:
            agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
        else:
            # 基于 IDE 的代理 - 跳过 CLI 检查并标记为可选
            tracker.skip(agent_key, "基于 IDE，无 CLI 检查")
            agent_results[agent_key] = False  # 不将 IDE 代理计为"找到"

    # 检查 VS Code 变体（不在代理配置中）
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", tracker=tracker)

    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]Specify CLI 已准备好使用！[/bold green]")

    if not git_ok:
        console.print("[dim]提示：安装 git 以进行仓库管理[/dim]")

    if not any(agent_results.values()):
        console.print("[dim]提示：安装 AI 助手以获得最佳体验[/dim]")

def main():
    app()

if __name__ == "__main__":
    main()


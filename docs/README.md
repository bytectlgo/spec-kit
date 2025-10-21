# 文档

此文件夹包含 Spec Kit 的文档源文件，使用 [DocFX](https://dotnet.github.io/docfx/) 构建。

## 本地构建

要本地构建文档：

1. 安装 DocFX：
   ```bash
   dotnet tool install -g docfx
   ```

2. 构建文档：
   ```bash
   cd docs
   docfx docfx.json --serve
   ```

3. 在浏览器中打开 `http://localhost:8080` 查看文档。

## 结构

- `docfx.json` - DocFX 配置文件
- `index.md` - 主文档首页
- `toc.yml` - 目录配置
- `installation.md` - 安装指南
- `quickstart.md` - 快速入门指南
- `_site/` - 生成的文档输出（git 忽略）

## 部署

当更改推送到 `main` 分支时，文档会自动构建并部署到 GitHub Pages。工作流在 `.github/workflows/docs.yml` 中定义。

# Git 分支推拉取操作说明

## 1. 概念澄清：`origin`、`main`、`dev` 分别是什么

- `main`、`dev` 是分支名。
- `origin` 是远程仓库别名（remote name），不是分支名。
- `origin/main`、`origin/dev` 的含义是：远程仓库 `origin` 上的 `main`、`dev` 分支。

常用检查命令：

```bash
git remote -v
git branch -a
```

## 2. 场景一：本地有文件更新，推送本地指定分支到远程指定分支

### 2.1 采用的命令

```bash
git switch <本地分支>
git status
git add .
git commit -m "your commit message"
git push origin <本地分支>:<远程分支>
```

### 2.2 对应每条命令的解释

1. `git switch <本地分支>`：切换到要推送的本地分支（如 `dev`）。
2. `git status`：确认有哪些文件变更待提交。
3. `git add .`：将当前变更加入暂存区（也可按文件精确 `git add <文件>`）。
4. `git commit -m "..."`：把暂存区变更提交到本地分支。
5. `git push origin <本地分支>:<远程分支>`：把本地指定分支推送到远程指定分支。

示例：

```bash
# 同名分支推送
git push origin dev:dev

# 不同名分支推送（把本地 feature-x 推到远程 dev）
git push origin feature-x:dev
```

## 3. 场景二：远程指定分支有更新，拉取到本地指定分支

### 3.1 采用的命令

```bash
git switch <本地分支>
git fetch origin
git pull --ff-only origin <远程分支>
```

### 3.2 对应每条命令的解释

1. `git switch <本地分支>`：先切换到要更新的本地分支（如 `dev`）。
2. `git fetch origin`：从远程获取最新提交信息，不直接改本地工作区。
3. `git pull --ff-only origin <远程分支>`：将远程指定分支快进合并到当前本地分支。

示例：

```bash
# 本地 dev 拉取远程 dev
git pull --ff-only origin dev
```

## 4. 补充说明

- 若本地有未提交改动，拉取前建议先 `git stash` 或先提交。
- `--ff-only` 可避免产生不必要的合并提交，保持提交历史更干净。

## 5. 常见问题：推送时报 Authentication failed

### 5.1 问题现象

```
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/...'
```

### 5.2 原因

GitHub 自 2021 年 8 月起**已废弃 HTTPS 密码认证**，即使密码正确也会报此错误。必须改用 Personal Access Token（PAT）或 SSH 密钥。

### 5.3 解决方案一：使用 Personal Access Token（PAT）

1. 登录 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 生成新 Token，勾选 `repo` 权限
3. 将 Token 嵌入远程 URL，避免每次手动输入：

```bash
git remote set-url origin https://<TOKEN>@github.com/<用户名>/<仓库名>.git
```

### 5.4 解决方案二：切换为 SSH 认证（推荐）

```bash
# 1. 生成 SSH 密钥（如已有可跳过）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 2. 将公钥内容添加到 GitHub → Settings → SSH and GPG keys
cat ~/.ssh/id_ed25519.pub

# 3. 将远程 URL 改为 SSH 格式
git remote set-url origin git@github.com:<用户名>/<仓库名>.git
```

配置完成后正常执行 `git push` 即可，无需输入任何凭据。

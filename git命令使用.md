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

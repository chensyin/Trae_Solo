# Windows 10 笔记本电脑配置指南

本指南用于在 Windows 10 笔记本电脑上配置 Trae 开发环境，实现与冥王峡谷主机的代码同步。

## 📋 配置步骤

### 1. 安装 Git

1. 下载 Git for Windows：[https://git-scm.com/download/win](https://git-scm.com/download/win)
2. 运行安装程序，保持默认选项即可
3. 安装完成后，打开 PowerShell 验证：

```powershell
git --version
```

### 2. 配置 Git 全局信息

```powershell
git config --global user.name "chensyin"
git config --global user.email "chensyin@outlook.com"
```

### 3. 生成 SSH Key

```powershell
# 生成 SSH Key
ssh-keygen -t ed25519 -C "chensyin@outlook.com"

# 查看公钥（复制输出内容）
Get-Content ~/.ssh/id_ed25519.pub
```

### 4. 添加 SSH Key 到 Gitee 和 GitHub

**Gitee 添加**：
1. 打开 [https://gitee.com/profile/sshkeys](https://gitee.com/profile/sshkeys)
2. 点击「添加公钥」
3. 标题填写「Windows 笔记本」
4. 粘贴公钥内容
5. 点击「确定」

**GitHub 添加**：
1. 打开 [https://github.com/settings/keys](https://github.com/settings/keys)
2. 点击「New SSH key」
3. 标题填写「Windows 笔记本」
4. Key Type 选择「Authentication Key」
5. 粘贴公钥内容
6. 点击「Add SSH key」

### 5. 验证 SSH 连接

```powershell
# 验证 Gitee 连接
ssh -T git@gitee.com

# 验证 GitHub 连接
ssh -T git@github.com
```

### 6. 克隆仓库

```powershell
# 从 Gitee 克隆（推荐，国内速度快）
git clone https://gitee.com/chensyin/trae_-solo.git Trae_Solo

# 进入仓库目录
cd Trae_Solo
```

### 7. 配置双远程推送

```powershell
# 查看当前远程配置
git remote -v

# 添加 GitHub 远程地址（如果尚未配置）
git remote set-url --add --push origin git@github.com:chensyin/Trae_Solo.git

# 确认配置
git remote -v
```

## 🚀 日常使用流程

### 拉取最新代码

```powershell
# 从 Gitee 拉取（速度快）
git pull
```

### 提交和推送

```powershell
# 暂存修改
git add .

# 提交修改
git commit -m "提交信息"

# 推送到 Gitee 和 GitHub
git push
```

### 查看状态

```powershell
git status
```

## 🔧 故障排除

### 1. SSH 连接失败

- 检查 SSH Key 是否正确添加到 Gitee/GitHub
- 检查防火墙是否阻止 SSH 连接
- 尝试重新生成 SSH Key

### 2. 推送失败

- 检查网络连接
- 检查仓库权限
- 确认 GitHub 仓库已创建

### 3. 同步冲突

```powershell
# 先拉取最新代码
git pull

# 解决冲突后重新提交
git add .
git commit -m "解决冲突"
git push
```

## 📁 目录结构

```
Trae_Solo/
├── H2Report/            # 氢能报告
├── documents/           # 文档
├── my_plans/            # 计划
├── prompts/             # 提示词
├── skills/              # 技能
├── solo_auto_plans/     # 自动计划
└── 作业指导书/          # 作业指导
```

## 📝 注意事项

1. **定期拉取**：每次开始工作前先 `git pull` 获取最新代码
2. **合理提交**：每个功能或修复单独提交，提交信息清晰
3. **备份重要文件**：虽然代码已同步到两个平台，但重要文件建议本地备份
4. **网络问题**：如果 GitHub 连接不稳定，可只推送到 Gitee，稍后再同步到 GitHub

## 🎉 完成

现在你的 Windows 10 笔记本已经配置完成，可以与冥王峡谷主机实现代码同步，开始使用 Trae 进行开发！
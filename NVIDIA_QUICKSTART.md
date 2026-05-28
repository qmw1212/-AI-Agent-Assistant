# ⚡ NVIDIA API 快速配置（3分钟）

## 🎯 快速步骤

### 1️⃣ 获取 API 密钥（1分钟）
```
访问: https://build.nvidia.com/
登录 → 选择任意模型 → 点击 "Get API Key" → 复制密钥
```

### 2️⃣ 配置密钥（1分钟）
```bash
# 打开 .env 文件
notepad .env

# 找到这一行并替换密钥：
NVIDIA_API_KEY=your_nvidia_api_key_here
# 改为：
NVIDIA_API_KEY=nvapi-你的实际密钥
```

### 3️⃣ 启动应用（1分钟）
```bash
python start.py
```

---

## 🎮 完整示例

### 你的 .env 文件应该看起来像这样：

```env
# NVIDIA API 配置
NVIDIA_API_KEY=nvapi-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
NVIDIA_MODEL=meta/llama-3.1-70b-instruct

# 其他配置保持不变
APP_TITLE=AI Agent Assistant
MAX_MEMORY_MESSAGES=10
```

---

## ✅ 验证配置

运行后应该看到：
```
✅ NVIDIA API key configured
✅ Environment configured correctly
🚀 Starting AI Agent Assistant...
```

---

## 🆘 遇到问题？

### 问题：找不到 API 密钥
**解决**: 访问 https://build.nvidia.com/ → 登录 → 点击任意模型 → "Get API Key"

### 问题：密钥无效
**解决**: 
1. 确保完整复制密钥（包括 `nvapi-` 前缀）
2. 密钥中不要有空格或换行
3. 重新生成新密钥

### 问题：应用启动失败
**解决**:
```bash
# 检查依赖
pip install -r requirements.txt

# 检查 .env 文件
cat .env  # Linux/Mac
type .env  # Windows
```

---

## 📖 详细文档

查看完整配置指南: [NVIDIA_SETUP.md](NVIDIA_SETUP.md)

---

**就这么简单！现在开始使用吧！** 🚀

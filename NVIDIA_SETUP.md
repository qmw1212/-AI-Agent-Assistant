# 🎮 NVIDIA API 配置指南

## 📋 概述

本项目现已支持使用 NVIDIA NIM API，可以访问强大的开源模型如 Llama 3.1。

---

## 🔑 获取 NVIDIA API 密钥

### 步骤 1: 注册账号
1. 访问: **https://build.nvidia.com/**
2. 点击右上角 "Sign In" 或 "Get Started"
3. 使用 NVIDIA 账号登录（或创建新账号）

### 步骤 2: 生成 API 密钥
1. 登录后，进入 **API Catalog**
2. 选择任意模型（如 Llama 3.1）
3. 点击 "Get API Key" 或 "Generate Key"
4. 复制生成的 API 密钥

---

## ⚙️ 配置项目

### 方法 1: 编辑 .env 文件

打开项目中的 `.env` 文件：

```bash
notepad .env
# 或
code .env
```

修改以下内容：

```env
# 将这一行的密钥替换为你的实际密钥
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 可选：修改模型（默认是 Llama 3.1 70B）
NVIDIA_MODEL=meta/llama-3.1-70b-instruct

# 可选：修改 API 端点（通常不需要改）
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
```

### 方法 2: 直接在命令行设置

```bash
# Windows PowerShell
$env:NVIDIA_API_KEY="your_api_key_here"

# Windows CMD
set NVIDIA_API_KEY=your_api_key_here

# Linux/Mac
export NVIDIA_API_KEY=your_api_key_here
```

---

## 🤖 可用模型

NVIDIA NIM 支持多种开源模型，你可以在 `.env` 中修改 `NVIDIA_MODEL`：

### 推荐模型

| 模型 | 模型ID | 特点 |
|------|--------|------|
| **Llama 3.1 70B** | `meta/llama-3.1-70b-instruct` | 强大、平衡（默认） |
| **Llama 3.1 405B** | `meta/llama-3.1-405b-instruct` | 最强大，速度较慢 |
| **Llama 3.1 8B** | `meta/llama-3.1-8b-instruct` | 快速、轻量 |
| **Mistral Large** | `mistralai/mistral-large` | 高性能 |
| **Mixtral 8x7B** | `mistralai/mixtral-8x7b-instruct-v0.1` | 快速、高效 |

### 修改模型示例

在 `.env` 文件中：

```env
# 使用更快的 8B 模型
NVIDIA_MODEL=meta/llama-3.1-8b-instruct

# 或使用最强大的 405B 模型
NVIDIA_MODEL=meta/llama-3.1-405b-instruct
```

---

## 🚀 启动应用

配置完成后，运行：

```bash
python start.py
```

或直接：

```bash
streamlit run app.py
```

---

## 🆚 NVIDIA vs Google Gemini

| 特性 | NVIDIA NIM | Google Gemini |
|------|------------|---------------|
| **模型选择** | 多种开源模型 | Gemini Pro |
| **免费额度** | 有限制 | 有限制 |
| **速度** | 快（取决于模型） | 快 |
| **功能** | 标准 LLM | 多模态 |
| **推荐场景** | 需要特定模型 | 通用场景 |

---

## 🔧 故障排除

### 问题 1: API 密钥无效
```
错误: Invalid API key
解决: 
1. 检查密钥是否完整复制
2. 确认密钥没有过期
3. 重新生成新密钥
```

### 问题 2: 模型不可用
```
错误: Model not found
解决:
1. 检查模型ID是否正确
2. 访问 https://build.nvidia.com/ 查看可用模型
3. 使用默认模型: meta/llama-3.1-70b-instruct
```

### 问题 3: 速率限制
```
错误: Rate limit exceeded
解决:
1. 等待几分钟后重试
2. 使用更小的模型（如 8B）
3. 减少请求频率
```

---

## 💡 优化建议

### 1. 选择合适的模型
- **日常使用**: Llama 3.1 8B（快速）
- **复杂任务**: Llama 3.1 70B（平衡）
- **最高质量**: Llama 3.1 405B（慢但强大）

### 2. 调整温度参数
在 `agent_core.py` 中修改：

```python
return ChatOpenAI(
    model=model,
    openai_api_key=nvidia_api_key,
    openai_api_base=base_url,
    temperature=0.7  # 降低到 0.3-0.5 获得更确定的输出
)
```

### 3. 监控使用量
- 访问 NVIDIA 控制台查看 API 使用情况
- 设置使用提醒

---

## 🔄 切换回 Google Gemini

如果想切换回 Google Gemini，只需在 `.env` 中：

```env
# 注释掉 NVIDIA 配置
# NVIDIA_API_KEY=...

# 启用 Google 配置
GOOGLE_API_KEY=your_google_api_key_here
```

代码会自动优先使用 NVIDIA，如果没有配置则使用 Google。

---

## 📚 更多资源

- **NVIDIA NIM 文档**: https://docs.nvidia.com/nim/
- **API 目录**: https://build.nvidia.com/explore/discover
- **模型详情**: https://catalog.ngc.nvidia.com/

---

## ✅ 配置检查清单

- [ ] 已注册 NVIDIA 账号
- [ ] 已生成 API 密钥
- [ ] 已在 .env 中配置 NVIDIA_API_KEY
- [ ] 已选择合适的模型
- [ ] 已测试运行 `python start.py`
- [ ] 应用成功启动

---

**配置完成后，享受强大的 NVIDIA AI 模型吧！** 🚀

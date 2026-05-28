# 快速参考指南 / Quick Reference

## 🚀 快速启动

```bash
# 方法1: 使用启动脚本
python start.py

# 方法2: 直接运行
streamlit run app.py
```

---

## 🎯 常用命令

### 安装
```bash
pip install -r requirements.txt
```

### 配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，添加API密钥
# GOOGLE_API_KEY=your_key_here
```

### 运行
```bash
streamlit run app.py
```

---

## 💬 使用示例

### 网络搜索
```
搜索Python 3.14新特性
搜索最新AI新闻
查找机器学习教程
```

### 数学计算
```
计算 18*25+99
(100+50)/2
2**8
```

### 文件分析
```
分析 README.md
读取 notes.txt
总结 test_document.md
```

### 记忆功能
```
我叫张三
我是数据分析师
[稍后] 我叫什么名字？
```

---

## 🛠️ 工具说明

| 工具 | 触发词 | 示例 |
|------|--------|------|
| 🔍 WebSearch | 搜索、查找、search | "搜索Python教程" |
| 🧮 Calculator | 计算、算、calculate | "计算18*25" |
| 📄 FileAnalyzer | 分析、读取、总结 | "分析README.md" |

---

## ⚙️ 侧边栏功能

### 设置
- **Enable Memory**: 开启/关闭记忆功能

### 工具状态
- 显示所有可用工具
- 实时状态指示

### 记忆状态
- 查看存储的上下文
- 用户信息预览

### 操作按钮
- **Clear Chat**: 清除聊天历史
- **Clear Memory**: 清除所有记忆

---

## 🔧 配置选项

### .env 文件
```env
# Google Gemini API
GOOGLE_API_KEY=your_key_here

# 应用设置
APP_TITLE=AI Agent Assistant
MAX_MEMORY_MESSAGES=10
```

### 获取API密钥
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **DeepSeek**: https://platform.deepseek.com/

---

## 🐛 故障排除

### 问题: API密钥错误
```
解决: 检查.env文件中的GOOGLE_API_KEY是否正确
```

### 问题: 依赖安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 重新安装
pip install -r requirements.txt
```

### 问题: 文件分析失败
```
解决: 
1. 使用绝对路径
2. 确保文件是.txt或.md格式
3. 检查文件编码为UTF-8
```

### 问题: 搜索无结果
```
解决: 使用更具体的搜索关键词
```

---

## 📊 性能提示

### 优化响应速度
1. 使用简洁的查询
2. 避免过长的对话历史
3. 定期清除聊天记录

### 节省API成本
1. 关闭不需要的记忆功能
2. 使用精确的工具触发词
3. 避免重复查询

---

## 🎨 UI快捷键

| 快捷键 | 功能 |
|--------|------|
| Enter | 发送消息 |
| Shift+Enter | 换行 |
| Ctrl+R | 刷新页面 |

---

## 📁 项目结构速查

```
AI-Agent-Assistant/
├── app.py              # 主应用
├── agent_core.py       # Agent引擎
├── memory.py           # 记忆系统
├── tools/              # 工具目录
│   ├── search_tool.py
│   ├── calculator_tool.py
│   └── file_tool.py
├── requirements.txt    # 依赖
└── .env               # 配置
```

---

## 🔗 有用链接

- **文档**: README.md
- **示例**: EXAMPLES.md
- **总览**: PROJECT_OVERVIEW.md
- **GitHub**: [项目地址]
- **问题反馈**: [Issues]

---

## 📝 开发命令

### 添加新工具
```python
# 1. 创建工具文件
# tools/my_tool.py

from langchain.tools import Tool

def my_function(input: str) -> str:
    return result

def create_my_tool() -> Tool:
    return Tool(
        name="MyTool",
        func=my_function,
        description="工具描述"
    )

# 2. 在app.py中注册
from tools.my_tool import create_my_tool
tools.append(create_my_tool())
```

### 修改LLM提供商
```python
# agent_core.py
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1"
)
```

---

## 💡 最佳实践

### DO ✅
- 使用明确的动词（搜索、计算、分析）
- 提供完整的文件路径
- 利用记忆功能存储重要信息
- 查看推理过程了解Agent思路

### DON'T ❌
- 不要使用模糊的指令
- 不要期望Agent读取不支持的文件格式
- 不要在一个查询中混合多个任务
- 不要忘记定期清理历史记录

---

## 🆘 获取帮助

1. **查看文档**: 先阅读README.md和EXAMPLES.md
2. **检查日志**: 查看终端输出的错误信息
3. **搜索问题**: 在GitHub Issues中搜索类似问题
4. **提交Issue**: 提供详细的错误信息和复现步骤

---

## 📈 版本信息

- **当前版本**: 1.0.0
- **Python要求**: 3.8+
- **主要依赖**: 
  - Streamlit 1.32.0
  - LangChain 0.1.10
  - Google Generative AI 0.4.0

---

**提示**: 将此文件加入书签，方便快速查阅！

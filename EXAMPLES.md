# 使用示例 / Usage Examples

## 基础对话 / Basic Conversation

### 示例 1: 简单问答
```
用户: 你好，你能做什么？
Agent: 你好！我是一个智能AI助手，我可以：
- 🔍 搜索网络信息
- 🧮 进行数学计算
- 📄 分析文本文件
- 💭 记住我们的对话内容

有什么我可以帮助你的吗？
```

---

## 工具使用示例 / Tool Usage Examples

### 示例 2: 网络搜索
```
用户: 搜索Python 3.14的新特性

Agent推理过程:
💭 Thought: 用户想了解Python 3.14的新特性，我需要搜索最新信息
⚡ Action: 使用 WebSearch 工具
   Input: "Python 3.14 new features"
👁️ Observation: 找到5条搜索结果...

Final Answer: 
根据搜索结果，Python 3.14的主要新特性包括：
1. 性能优化...
2. 新的语法特性...
3. 标准库更新...
```

### 示例 3: 数学计算
```
用户: 帮我算一下 18*25+99

Agent推理过程:
💭 Thought: 这是一个数学计算问题
⚡ Action: 使用 Calculator 工具
   Input: "18*25+99"
👁️ Observation: Result: 549

Final Answer: 计算结果是 549
```

### 示例 4: 文件分析
```
用户: 帮我分析一下 notes.txt 文件

Agent推理过程:
💭 Thought: 用户想要分析一个文本文件
⚡ Action: 使用 FileAnalyzer 工具
   Input: "notes.txt"
👁️ Observation: 
   File: notes.txt
   Size: 1250 characters, 180 words, 25 lines
   Content Preview: ...

Final Answer: 
这个文件包含180个单词，共25行。主要内容是关于...
```

---

## 记忆功能示例 / Memory Examples

### 示例 5: 记住用户信息
```
用户: 我叫钱毛文
Agent: 很高兴认识你，钱毛文！我会记住你的名字。

[稍后在对话中]
用户: 我叫什么名字？
Agent: 你的名字是钱毛文。
```

### 示例 6: 上下文记忆
```
用户: 搜索一下机器学习的最新进展
Agent: [搜索并返回结果]

用户: 能详细说说第一条吗？
Agent: [基于之前的搜索结果，详细解释第一条]
```

---

## 复杂任务示例 / Complex Task Examples

### 示例 7: 多步骤任务
```
用户: 帮我搜索今天的天气，然后计算如果温度是25度，转换成华氏度是多少

Agent推理过程:
💭 Thought: 这需要两个步骤：先搜索天气，再进行温度转换计算
⚡ Action: 使用 WebSearch 工具
   Input: "today weather"
👁️ Observation: [天气信息]

💭 Thought: 现在需要将25摄氏度转换为华氏度，公式是 F = C * 9/5 + 32
⚡ Action: 使用 Calculator 工具
   Input: "25 * 9/5 + 32"
👁️ Observation: Result: 77

Final Answer: 
根据搜索，今天的天气是...
25摄氏度等于77华氏度。
```

### 示例 8: 文件内容搜索
```
用户: 读取 README.md 文件，然后告诉我安装步骤

Agent推理过程:
💭 Thought: 需要先读取文件内容
⚡ Action: 使用 FileAnalyzer 工具
   Input: "README.md"
👁️ Observation: [文件内容]

Final Answer:
根据README.md文件，安装步骤如下：
1. 克隆仓库
2. 安装依赖: pip install -r requirements.txt
3. 配置API密钥
4. 运行应用: streamlit run app.py
```

---

## 实用场景 / Practical Scenarios

### 场景 1: 学习助手
```
用户: 我想学习Python装饰器，能帮我搜索一些教程吗？
Agent: [搜索并提供教程链接和简要说明]

用户: 装饰器的语法是什么样的？
Agent: [基于搜索结果解释装饰器语法]
```

### 场景 2: 数据分析助手
```
用户: 计算 (1500 + 2300 + 1800) / 3
Agent: [使用计算器] 平均值是 1866.67

用户: 如果增长20%是多少？
Agent: [计算] 1866.67 * 1.2 = 2240
```

### 场景 3: 文档助手
```
用户: 分析 project_notes.txt 并总结要点
Agent: [读取文件并总结]

用户: 文件中提到的截止日期是什么时候？
Agent: [基于文件内容回答]
```

---

## 记忆管理 / Memory Management

### 启用/禁用记忆
- 在侧边栏切换 "Enable Memory" 开关
- 禁用后，Agent不会记住对话历史

### 清除记忆
- **Clear Chat**: 清除聊天历史，但保留用户信息
- **Clear Memory**: 清除所有记忆，包括用户信息

---

## 提示技巧 / Tips

### 1. 明确的指令
✅ 好: "搜索Python 3.14新特性"
❌ 差: "Python"

### 2. 一次一个任务
✅ 好: "计算 18*25+99"
❌ 差: "算这个算那个还有那个"

### 3. 提供完整路径
✅ 好: "分析 C:/Users/Documents/notes.txt"
❌ 差: "分析那个文件"

### 4. 利用记忆功能
✅ 好: 先告诉Agent你的信息，后续对话会更个性化
❌ 差: 每次都重复相同的背景信息

---

## 故障排除 / Troubleshooting

### 问题 1: Agent没有使用工具
**原因**: 查询可能不够明确
**解决**: 使用更具体的动词，如"搜索"、"计算"、"分析"

### 问题 2: 文件分析失败
**原因**: 文件路径不正确或文件格式不支持
**解决**: 
- 使用绝对路径
- 确保文件是 .txt 或 .md 格式
- 检查文件编码是否为 UTF-8

### 问题 3: 搜索结果不准确
**原因**: 查询词不够具体
**解决**: 添加更多关键词或使用引号包围精确短语

---

## 高级用法 / Advanced Usage

### 链式任务
```
用户: 搜索"机器学习"，然后用文件工具保存结果到 ml_info.txt，最后分析这个文件

注意: 当前版本不支持文件写入，但可以：
1. 搜索信息
2. 手动保存
3. 让Agent分析
```

### 上下文对话
```
对话1: 搜索某个主题
对话2: "能详细说说第二点吗？" (Agent会记住之前的搜索结果)
对话3: "还有其他相关信息吗？" (继续基于上下文)
```

---

## 最佳实践 / Best Practices

1. **保持对话聚焦**: 一次处理一个主题
2. **使用记忆功能**: 让Agent记住重要信息
3. **明确工具需求**: 直接说"搜索"、"计算"等
4. **检查推理过程**: 展开"Agent Reasoning Process"查看思考过程
5. **定期清理**: 长对话后清除历史以提高性能

---

## 示例对话流程 / Example Conversation Flow

```
👤 用户: 你好，我叫张三，是一名数据分析师
🤖 Agent: 你好张三！很高兴认识你。作为数据分析师，我可以帮你进行计算、搜索最新的数据分析工具和技术。

👤 用户: 帮我搜索一下2024年最流行的数据可视化工具
🤖 Agent: [使用WebSearch工具搜索]
      根据搜索结果，2024年最流行的数据可视化工具包括...

👤 用户: 我叫什么名字？
🤖 Agent: 你的名字是张三。

👤 用户: 如果我有1000条数据，每条处理需要0.5秒，总共需要多少分钟？
🤖 Agent: [使用Calculator工具]
      1000 * 0.5 = 500秒，也就是约8.33分钟。

👤 用户: 分析一下 data_summary.txt
🤖 Agent: [使用FileAnalyzer工具]
      这个文件包含...
```

---

**需要更多帮助？** 查看 [README.md](README.md) 或提交 Issue！

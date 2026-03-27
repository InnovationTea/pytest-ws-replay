# pytest-ws-replay

一个基于pytest框架的WebSocket录制回放插件，用于自动化测试WebSocket交互。

## 功能概述

### 栏心功能

**录制与回放**
- 拦截WebSocket连接，自动记录交互
- 从cassette文件回放预录制的交互
- 支持多种录制模式（once、rewrite、all、none、new_episodes）

**数据存储**
- JSON格式的cassette文件存储
- 按日期自动组织：`cassette/websocket_recording/{date}/`
- 支持stable目录：`cassette/stable/`

**URL匹配**
- 精确URL匹配
- 模糊匹配：基于路径（忽略查询参数）

## 项目结构

\`\`\`
pytest-ws-replay/
├── vcr_code/              # 核心VCR实现
│   ├── vcr_proxy.py      # VCRProxy主类
│   ├── fake_websocket.py  # 模拟WebSocket
│   └── matcher.py         # URL匹配器
├── model/                 # 数据模型
│   ├── types.py          # 数据结构
│   ├── config.py         # 配置类
│   └── exceptations.py    # 异常定义
├── plugin/                # pytest集成
│   └── plugin.py         # pytest fixtures和装饰器
├── storage/               # 存储层
│   └── storage.py        # CassetteStorage
└── tests/                 # 测试
    ├── unit/             # 单元测试
    └── integration/      # 集成测试
\`\`\`

## 使用方式

### 1. 装饰器方式

\`\`\`python
import pytest
import websockets

# 基础使用
@pytest.mark.vcr
async def test_websocketry():
    async with websockets.connect("ws://example.com/chat") as ws:
        await ws.send("Hello")
        response = await ws.recv()
        assert response == "Hello back"
\`\`\`

### 2. 带参数的装饰器

\`\`\`python
import pytest
import websockets

# 强制重新录制
@pytest.mark.vcr(ws_record_mode='rewrite')
async def test_force_rerecord():
    async with websockets.connect("ws://example.com/chat") as ws:
        await ws.send("Hello")
        response = await ws.recv()
        assert response == "Hello back
\`\`\`

### 3. 使用vcr_context fixture

\`\`\`python
from pytest_ws_replay.plugin import vcr_context

def test_with_vcr_context(vcr_context):
    # vcr_context fixture自动处理录制/回放逻辑
    # 需要使用 @pytest.mark.vcr 装饰器才会激活vcr_context
    pass
\`\`\`

## 录制模式

- **once**（默认）：首次运行录制，后续运行回放
- **rewrite**：每次都录制，覆盖现有文件
- **all**：强制录制所有交互
- **none**：禁用VCR，直接连接

## 配置

### pytest.ini

\`\`\`ini
[pytest]
testpaths = tests
python_files = test_*.py
\`\`\`

### 装饰器参数

\`\`\`python
@pytest.mark.vcr(ws_record_mode='rewrite')
def test_force_rerecord():
    pass
\`\`\`

## 测试

项目包含完整的单元测试和集成测试：

\`\`\`bash
# 运行所有测试
pytest

# 只运行单元测试
pytest tests/unit/

# 只运行集成测试
pytest tests/integration/

# 详细输出
pytest -v
\`\`\`

## 数据结构

### Cassette格式

\`\`\`json
{
  "url": "ws://example.com/chat",
  "interactions": [
    {
      "type": "interaction",
      "request": "Hello",
      "response": ["Hello back"]
    }
  ]
}
\`\`\`

### Interaction结构

| 字段 | 含义 |
|-------|--------|
| \`type\` | 固定值 \`"interaction"\`，表示这是一个交互记录 |
| \`request\` | 客户端**发送**的消息（\`null\` 表示服务器主动推送） |
| \`response\` | 服务器**返回**的消息数组（可能包含多个响应） |

## 依赖

- pytest >= 6.0
- websockets >= 9.0
- Python >= 3.7

## 快速开始

1. 安装依赖：
\`\`\`bash
pip install -e .
\`\`\`

2. 编写测试并添加 \`@pytest.mark.vcr\` 装饰器

3. 首次运行测试将自动录制交互

4. 后续运行将回放预录制的交互

## 当前状态

项目已完成基础功能实现，包括：
- [x] VCRProxy核心类
- [x] 录制器（Recorder）
- [x] 回放器（Player）
- [x] FakeWebSocket模拟
- [x] URL匹配器（Matcher）
- [x] Cassette存储（CassetteStorage）
- [x] pytest fixtures集成
- [x] 完整的单元测试和集成测试



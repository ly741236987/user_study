# AI 股票看板（MVP）

这是一个最小可运行版本（MVP），用于演示你描述的目标：
- 汇总股票信息（当前先用 Mock 数据）
- 基于“AI 信号分”给出买入 / 卖出 / 观望建议
- 展示股票代码、名称、时间、建议动作、建议数量、建议原因

> ⚠️ 当前版本仅用于学习与原型验证，不构成任何投资建议。

## 1. 功能概览

- **看板展示字段**
  - 股票代码
  - 股票名称
  - 当前价格 / 涨跌幅
  - 信号分（可替换为模型输出）
  - 时间
  - 当前持仓
  - 建议动作（BUY / SELL / HOLD）
  - 建议数量
  - 建议原因

- **策略参数可调**
  - 可投入现金
  - 买入阈值
  - 卖出阈值
  - 单票最大资金占比

## 2. 项目结构

```text
.
├── app.py                         # Streamlit 看板入口
├── src/stock_dashboard/
│   ├── models.py                  # 数据模型
│   ├── engine.py                  # 建议引擎（MVP 规则版）
│   └── providers.py               # 数据源抽象 + Mock 数据源
├── tests/test_engine.py           # 引擎单元测试
└── requirements.txt
```

## 3. 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

启动后访问：`http://localhost:8501`

## 4. 运行测试

```bash
pytest -q
```

## 5. 如何接入真实数据（下一步）

在 `src/stock_dashboard/providers.py` 中新增真实 Provider（如券商 API 或合规数据服务）。

建议步骤：
1. 确认数据来源合法性与平台条款（东方财富 / 同花顺等）。
2. 将行情拉取逻辑封装为 provider，和看板解耦。
3. 将 `signal_score` 替换为 AI 模型输出（并输出理由、置信度）。
4. 增加历史回测、风险约束、交易成本模型后再尝试小资金。

## 6. 风险提示

- 请勿“完全跟单”任何自动建议。
- 至少增加：止损、仓位上限、黑天鹅保护、人工复核流程。
- 先做纸面交易和回测，再实盘。

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.stock_dashboard.engine import EngineConfig, RecommendationEngine
from src.stock_dashboard.providers import MockStockProvider

st.set_page_config(page_title="AI 股票看板", layout="wide")
st.title("📈 AI 股票看板（MVP）")
st.caption("演示版：使用 Mock 数据 + 可配置策略。仅供学习，不构成投资建议。")

with st.sidebar:
    st.header("策略参数")
    cash = st.number_input("可投入现金（元）", value=200000.0, step=10000.0, min_value=0.0)
    buy_threshold = st.slider("买入阈值", min_value=0.0, max_value=1.0, value=0.35, step=0.01)
    sell_threshold = st.slider("卖出阈值", min_value=-1.0, max_value=0.0, value=-0.35, step=0.01)
    max_position_pct = st.slider("单票最大资金占比", min_value=0.01, max_value=0.5, value=0.12, step=0.01)

provider = MockStockProvider()
engine = RecommendationEngine(
    EngineConfig(
        buy_threshold=buy_threshold,
        sell_threshold=sell_threshold,
        max_position_pct=max_position_pct,
    )
)

holdings = {
    "600519": 300,
    "000858": 500,
    "300750": 800,
    "600036": 1000,
    "601318": 600,
}

snapshots = provider.fetch_all()
rows = []
for s in snapshots:
    suggestion = engine.suggest(snapshot=s, cash=cash, holding_qty=holdings.get(s.code, 0))
    rows.append(
        {
            "股票代码": s.code,
            "股票名称": s.name,
            "当前价格": s.price,
            "涨跌幅(%)": s.change_pct,
            "信号分": round(s.signal_score, 2),
            "时间": s.timestamp.strftime("%H:%M:%S"),
            "当前持仓": holdings.get(s.code, 0),
            "建议": suggestion.action,
            "建议数量": suggestion.quantity,
            "建议原因": suggestion.reason,
        }
    )

result_df = pd.DataFrame(rows)

col1, col2 = st.columns([3, 2])
with col1:
    st.subheader("看板建议")
    st.dataframe(result_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("建议汇总")
    st.metric("买入信号数量", int((result_df["建议"] == "BUY").sum()))
    st.metric("卖出信号数量", int((result_df["建议"] == "SELL").sum()))
    st.metric("观望数量", int((result_df["建议"] == "HOLD").sum()))

st.markdown("---")
st.markdown("### 下一步接入真实数据建议")
st.markdown(
    "1. 在 `src/stock_dashboard/providers.py` 新增真实数据 Provider；\n"
    "2. 通过定时任务刷新行情并缓存；\n"
    "3. 将信号分改为 AI 模型输出（含可解释理由）；\n"
    "4. 先纸面交易回测，再小资金验证。"
)

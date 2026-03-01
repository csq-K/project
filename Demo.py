# 1导入所需的库
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# 2设置页面配置
st.set_page_config(
    page_title="XX跨境信用融资平台 - 卖家端演示",
    page_icon="💰",
    layout="wide"
)

# 3生成模拟数据的函数
# 3.1卖家基础信息
@st.cache_data
def generate_sample_sellers():
    """生成3个模拟卖家的基础信息"""
    sellers = {
        "seller_001": {
            "name": "深圳星辰科技",
            "platforms": ["亚马逊", "Shopify", "TikTok"],
            "join_date": "2023-03-15",
            "sales_history": [120000, 135000, 142000, 158000, 165000, 172000],
        },
        "seller_002": {
            "name": "杭州云动贸易",
            "platforms": ["亚马逊", "TikTok"],
            "join_date": "2023-08-22",
            "sales_history": [80000, 92000, 105000, 112000, 108000, 124000],
        },
        "seller_003": {
            "name": "广州出海电商",
            "platforms": ["Shopify", "亚马逊"],
            "join_date": "2022-11-05",
            "sales_history": [200000, 210000, 195000, 220000, 240000, 255000],
        }
    }
    return sellers

# 3.2生成信用分数据
@st.cache_data
def generate_credit_scores():
    """为每个卖家生成8个维度的信用分和最终信用分"""
    dimensions = [
        "销售稳定性", "履约能力", "客户满意度", "店铺信誉",
        "经营规模", "成长性", "多样性", "合规性"
    ]
    sellers = list(generate_sample_sellers().keys())
    scores = {}
    for seller in sellers:
        dim_scores = {dim: random.randint(65, 98) for dim in dimensions}
        avg = np.mean(list(dim_scores.values()))
        total = int(300 + (avg - 60) * (550 / 40))
        total = max(300, min(850, total))
        scores[seller] = {
            "dimensions": dim_scores,
            "total": total,
            "history": [total + random.randint(-15, 15) for _ in range(6)]
        }
    return scores

# 3.3生成预警事件
@st.cache_data
def generate_warnings():
    """生成一些预警事件"""
    warnings_data = {
        "seller_001": [
            {"date": "2024-05-10", "type": "销量骤降", "level": "红色", "detail": "连续3天销售额下降50%", "status": "待处理"},
            {"date": "2024-05-05", "type": "差评激增", "level": "橙色", "detail": "新增差评5条，超过日均200%", "status": "已处理"},
        ],
        "seller_002": [
            {"date": "2024-05-12", "type": "退货率上升", "level": "黄色", "detail": "7天退货率上升至12%", "status": "待处理"},
        ],
        "seller_003": []
    }
    return warnings_data

# 3.4 生成贷款产品列表
@st.cache_data
def generate_loan_products():
    """生成贷款产品列表（资金方提供）"""
    products = [
        {"bank": "工商银行", "name": "跨境贷", "min_score": 600, "max_amount": 50, "rate": "5.5%", "term": "12个月"},
        {"bank": "建设银行", "name": "电商贷", "min_score": 650, "max_amount": 80, "rate": "5.0%", "term": "6-18个月"},
        {"bank": "平安银行", "name": "数据贷", "min_score": 580, "max_amount": 30, "rate": "6.0%", "term": "3-12个月"},
        {"bank": "网商银行", "name": "信用贷", "min_score": 620, "max_amount": 100, "rate": "4.8%", "term": "12个月"},
    ]
    return pd.DataFrame(products)

# 4初始化数据
sellers = generate_sample_sellers()
seller_ids = list(sellers.keys())
credit_scores = generate_credit_scores()
warnings = generate_warnings()
products_df = generate_loan_products()

# 5侧边栏（卖家选择和模拟授权）
st.sidebar.header("👤 卖家登录")
selected_seller_id = st.sidebar.selectbox(
    "选择卖家账号（模拟）",
    seller_ids,
    format_func=lambda x: f"{sellers[x]['name']} ({x})"
)
seller = sellers[selected_seller_id]
seller_score = credit_scores[selected_seller_id]
seller_warnings = warnings[selected_seller_id]

st.sidebar.subheader("基本信息")
st.sidebar.write(f"**店铺名称**：{seller['name']}")
st.sidebar.write(f"**入驻平台**：{', '.join(seller['platforms'])}")
st.sidebar.write(f"**入驻日期**：{seller['join_date']}")

st.sidebar.subheader("📡 数据授权")
if st.sidebar.button("点击授权所有平台"):
    st.sidebar.success("✅ 已成功授权亚马逊、Shopify、TikTok Shop")
else:
    st.sidebar.info("⏳ 点击按钮模拟授权")

# 6主页面标签页
tab1, tab2, tab3, tab4 = st.tabs(["📊 信用分", "💰 融资产品", "⚠️ 风险预警", "📈 经营数据"])

# 6.1 标签页1：信用分
with tab1:
    st.header("📊 我的信用分")

    total_score = seller_score["total"]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h1 style='text-align: center; color: #1E88E5;'>{total_score}</h1>", unsafe_allow_html=True)
        if total_score >= 700:
            level = "优秀 (AAA)"
            color = "green"
        elif total_score >= 600:
            level = "良好 (AA)"
            color = "orange"
        else:
            level = "一般 (A)"
            color = "red"
        st.markdown(f"<h3 style='text-align: center; color: {color};'>{level}</h3>", unsafe_allow_html=True)
    with col2:
        history = seller_score["history"]
        dates = [(datetime.now() - timedelta(days=30*i)).strftime("%m-%d") for i in range(5, -1, -1)]
        fig = go.Figure(data=go.Scatter(x=dates, y=history, mode='lines+markers', line=dict(color='blue')))
        fig.update_layout(title="信用分历史趋势", xaxis_title="日期", yaxis_title="分数", height=250)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("📋 信用维度详解")
    dims = seller_score["dimensions"]
    fig_dim = go.Figure(data=[
        go.Bar(name='维度得分', x=list(dims.keys()), y=list(dims.values()), marker_color='lightblue')
    ])
    fig_dim.update_layout(yaxis_range=[0,100], height=350)
    st.plotly_chart(fig_dim, use_container_width=True)
    st.subheader("🔍 维度解读与建议")
    for dim, score in dims.items():
        if score >= 80:
            suggestion = f"优秀！{dim}表现稳定，继续保持。"
        elif score >= 65:
            suggestion = f"良好，{dim}有提升空间，可关注细节优化。"
        else:
            suggestion = f"注意：{dim}低于平均水平，建议检查原因并改进。"
        st.markdown(f"- **{dim}**：{score}分 —— {suggestion}")

# 6.2 标签页2：融资产品
with tab2:
    st.header("💰 为您推荐的融资产品")
    st.markdown("基于您的信用分和经营状况，我们为您匹配了以下产品：")
    eligible = products_df[products_df["min_score"] <= total_score].copy()
    if len(eligible) > 0:
        eligible["预估额度(万)"] = eligible["max_amount"].apply(lambda x: f"{x}万")
        eligible["利率"] = eligible["rate"]
        eligible["期限"] = eligible["term"]
        st.dataframe(eligible[["bank", "name", "预估额度(万)", "利率", "期限"]], use_container_width=True)
        st.subheader("📝 快速申请")
        col1, col2 = st.columns(2)
        with col1:
            selected_product = st.selectbox("选择产品", eligible["name"].tolist())
        with col2:
            apply_amount = st.number_input("申请金额（万元）", min_value=1, max_value=100, value=10)
        if st.button("提交申请"):
            st.success(f"您的申请已提交！产品：{selected_product}，金额：{apply_amount}万元。资金方将在24小时内联系您。")

# 6.3 标签页3：风险预警
with tab3:
    st.header("⚠️ 风险预警中心")
    if seller_warnings:
        warn_df = pd.DataFrame(seller_warnings)
        def color_level(val):
            if val == "红色":
                return "background-color: #ffcccc"
            elif val == "橙色":
                return "background-color: #ffe6b3"
            elif val == "黄色":
                return "background-color: #ffffcc"
            return ""
        st.dataframe(warn_df.style.applymap(color_level, subset=["level"]), use_container_width=True)
        st.subheader("处理预警")
        pending = warn_df[warn_df["status"]=="待处理"]
        if len(pending) > 0:
            selected_warning = st.selectbox("选择待处理预警", pending["detail"].tolist())
            if st.button("标记为已处理"):
                st.success("预警已标记为处理，感谢您的反馈！")
        else:
            st.info("当前没有待处理的预警。")
    else:
        st.success("✅ 暂无预警，经营状况良好。")

# 6.4 标签页4：经营数据
with tab4:
    st.header("📈 近期经营数据概览")
    sales = seller["sales_history"]
    months = [(datetime.now() - timedelta(days=30*i)).strftime("%Y-%m") for i in range(5, -1, -1)]
    sales_df = pd.DataFrame({"月份": months, "销售额(元)": sales})
    st.line_chart(sales_df.set_index("月份"))

    st.subheader("平台销售占比")
    if "亚马逊" in seller["platforms"]:
        amazon_share = random.randint(40, 70)
    else:
        amazon_share = 0
    if "Shopify" in seller["platforms"]:
        shopify_share = random.randint(10, 40)
    else:
        shopify_share = 0
    if "TikTok" in seller["platforms"]:
        tiktok_share = 100 - amazon_share - shopify_share
    else:
        tiktok_share = 0
    total = amazon_share + shopify_share + tiktok_share
    if total != 100:
        if amazon_share > 0:
            amazon_share += 100 - total
    pie_data = pd.DataFrame({
        "平台": ["亚马逊", "Shopify", "TikTok"],
        "占比": [amazon_share, shopify_share, tiktok_share]
    })
    fig_pie = go.Figure(data=[go.Pie(labels=pie_data["平台"], values=pie_data["占比"], hole=.3)])
    st.plotly_chart(fig_pie, use_container_width=True)

# 7页脚
st.markdown("---")
st.caption("🚀 XX跨境信用融资平台 · 卖家端演示 · 数据均为模拟，仅供参考")
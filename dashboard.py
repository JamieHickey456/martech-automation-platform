import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Customer Intelligence Dashboard",
    layout="wide"
)

st.title("📊 AI-Driven Customer Intelligence, Automation & CMS Performance Platform")
st.markdown(
    "A multi-layer platform combining customer intelligence, campaign automation, "
    "agent-based recommendations, page optimisation, and CMS KPI monitoring."
)

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    profiles = pd.read_csv("customer_profiles.csv")
    actions = pd.read_csv("campaign_actions.csv")
    pages = pd.read_csv("page_insights.csv")
    agent = pd.read_csv("agent_recommendations.csv")
    cms_perf = pd.read_csv("cms_performance.csv")
    return profiles, actions, pages, agent, cms_perf


profiles_df, actions_df, pages_df, agent_df, cms_perf_df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options=sorted(profiles_df["segment"].dropna().unique().tolist()),
    default=sorted(profiles_df["segment"].dropna().unique().tolist())
)

selected_churn = st.sidebar.multiselect(
    "Select Churn Risk",
    options=sorted(profiles_df["churn_risk"].dropna().unique().tolist()),
    default=sorted(profiles_df["churn_risk"].dropna().unique().tolist())
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(profiles_df["region"].dropna().unique().tolist()),
    default=sorted(profiles_df["region"].dropna().unique().tolist())
)

selected_cms_status = st.sidebar.multiselect(
    "Select CMS Status",
    options=sorted(cms_perf_df["status"].dropna().unique().tolist()),
    default=sorted(cms_perf_df["status"].dropna().unique().tolist())
)

filtered_profiles = profiles_df[
    (profiles_df["segment"].isin(selected_segment)) &
    (profiles_df["churn_risk"].isin(selected_churn)) &
    (profiles_df["region"].isin(selected_region))
].copy()

visible_customers = filtered_profiles["customer_id"].tolist()
filtered_actions = actions_df[actions_df["customer_id"].isin(visible_customers)].copy()
filtered_agent = agent_df[agent_df["customer_id"].isin(visible_customers)].copy()

filtered_cms = cms_perf_df[
    cms_perf_df["status"].isin(selected_cms_status)
].copy()

# -----------------------------
# OVERVIEW METRICS
# -----------------------------
st.header("📌 Overview")

total_customers = len(filtered_profiles)
total_campaign_actions = len(filtered_actions)
campaign_types = filtered_actions["campaign"].nunique() if len(filtered_actions) > 0 else 0
high_value_customers = (filtered_profiles["segment"] == "High Value").sum()
high_risk_customers = (filtered_profiles["churn_risk"] == "High").sum()
total_revenue = filtered_profiles["spend"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Campaign Actions", f"{total_campaign_actions:,}")
col3.metric("Campaign Types", campaign_types)
col4.metric("Total Revenue", f"${total_revenue:,.0f}")

col5, col6 = st.columns(2)
col5.metric("High Value Customers", f"{high_value_customers:,}")
col6.metric("High Risk Customers", f"{high_risk_customers:,}")

# -----------------------------
# CUSTOMER OVERVIEW
# -----------------------------
st.header("👥 Customer Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Segment Breakdown")
    segment_counts = filtered_profiles["segment"].value_counts()
    st.bar_chart(segment_counts)
    st.write(segment_counts)

with col2:
    st.subheader("Churn Risk Breakdown")
    churn_counts = filtered_profiles["churn_risk"].value_counts()
    st.bar_chart(churn_counts)
    st.write(churn_counts)

# -----------------------------
# CAMPAIGN PERFORMANCE
# -----------------------------
st.header("📢 Campaign Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Campaign Distribution")
    campaign_counts = filtered_actions["campaign"].value_counts()
    st.bar_chart(campaign_counts)
    st.write(campaign_counts)

with col2:
    st.subheader("Priority Distribution")
    priority_counts = filtered_actions["priority"].value_counts()
    st.bar_chart(priority_counts)
    st.write(priority_counts)

# -----------------------------
# BUSINESS IMPACT
# -----------------------------
st.header("💰 Business Impact (Simulated)")

retention_targets = filtered_profiles[
    filtered_profiles["churn_risk"] == "High"
].shape[0]

upsell_targets = filtered_profiles[
    filtered_profiles["segment"] == "High Value"
].shape[0]

st.write(f"• Customers targeted for retention campaigns: {retention_targets}")
st.write(f"• High-value upsell opportunities: {upsell_targets}")
st.write(f"• Visible customer revenue in this filtered view: ${total_revenue:,.0f}")

# -----------------------------
# AUTOMATION INSIGHTS
# -----------------------------
st.header("📈 Automation Insights")

st.write("""
- High churn customers are automatically targeted with retention campaigns
- High value customers receive upsell journeys
- Mid-value engaged users receive cross-sell campaigns
- Low engagement users enter onboarding / activation flows
""")

# -----------------------------
# AGENT RECOMMENDATIONS
# -----------------------------
st.header("🤖 Autonomous Recommendation Engine")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Recommendation Distribution")
    recommendation_counts = filtered_agent["recommendation"].value_counts()
    st.bar_chart(recommendation_counts)
    st.write(recommendation_counts)

with col2:
    st.subheader("Agent Priority Breakdown")
    agent_priority_counts = filtered_agent["priority"].value_counts()
    st.bar_chart(agent_priority_counts)
    st.write(agent_priority_counts)

st.subheader("Top High-Priority Recommendations")
top_agent = filtered_agent[
    filtered_agent["priority"] == "High"
].sort_values("score", ascending=False).head(20)

if len(top_agent) > 0:
    st.dataframe(top_agent, use_container_width=True)
else:
    st.write("No high-priority recommendations in the current filtered view.")

# -----------------------------
# SCENARIO SIMULATION
# -----------------------------
st.header("🧪 Campaign Simulation")

selected_campaign = st.selectbox(
    "Select Campaign Type",
    ["Retention_Save", "VIP_Upsell", "CrossSell", "Onboarding", "Reactivation", "Engagement_Nudge", "No_Action"]
)

simulated_users = filtered_actions[filtered_actions["campaign"] == selected_campaign].shape[0]

st.write(f"Estimated users impacted: {simulated_users}")

if selected_campaign == "Retention_Save":
    st.write("Simulated uplift: +8–15% retention (assumed benchmark)")
elif selected_campaign == "VIP_Upsell":
    st.write("Simulated uplift: +5–12% average order value (assumed benchmark)")
elif selected_campaign == "CrossSell":
    st.write("Simulated uplift: +4–10% conversion to secondary offer (assumed benchmark)")
elif selected_campaign == "Onboarding":
    st.write("Simulated uplift: +5–10% activation rate (assumed benchmark)")
elif selected_campaign == "Reactivation":
    st.write("Simulated uplift: +3–8% re-engagement (assumed benchmark)")
elif selected_campaign == "Engagement_Nudge":
    st.write("Simulated uplift: +4–9% engagement rate (assumed benchmark)")
else:
    st.write("No direct uplift simulated for this category.")

# -----------------------------
# TOP OPPORTUNITIES
# -----------------------------
st.header("🚀 Top Opportunities")

top_churn = filtered_profiles[
    filtered_profiles["churn_risk"] == "High"
].sort_values("spend", ascending=False).head(10)

if len(top_churn) > 0:
    st.write("Top high-risk customers by spend:")
    st.dataframe(
        top_churn[
            [
                "customer_id",
                "region",
                "segment",
                "churn_risk",
                "spend",
                "logins",
                "purchases"
            ]
        ],
        use_container_width=True
    )
else:
    st.write("No high-risk customers in the current filtered view.")

# -----------------------------
# OPERATIONAL DETAIL
# -----------------------------
st.header("📄 Operational View (Customer-Level Detail)")

st.subheader("Customer Profiles (Sample)")
st.dataframe(
    filtered_profiles[
        [
            "customer_id",
            "region",
            "acquisition_channel",
            "logins",
            "purchases",
            "spend",
            "avg_order_value",
            "engagement_score",
            "churn_risk",
            "segment"
        ]
    ].head(50),
    use_container_width=True
)

st.subheader("Campaign Actions (Sample)")
st.dataframe(
    filtered_actions.head(50),
    use_container_width=True
)

st.subheader("Agent Recommendations (Sample)")
st.dataframe(
    filtered_agent.head(50),
    use_container_width=True
)

# -----------------------------
# PAGE OPTIMISATION INSIGHTS
# -----------------------------
st.header("🌐 Page Optimisation Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Conversion Rate by Page")
    st.bar_chart(pages_df.set_index("page")["conversion_rate"])

with col2:
    st.subheader("Traffic by Page")
    st.bar_chart(pages_df.set_index("page")["visits"])

st.subheader("Page Recommendations")
st.dataframe(pages_df, use_container_width=True)

# -----------------------------
# CMS KPI MONITORING
# -----------------------------
st.header("📄 CMS Performance Monitoring")

average_ctr = filtered_cms["ctr"].mean() if len(filtered_cms) > 0 else 0
needs_attention_count = (filtered_cms["status"] == "Needs Attention").sum()
below_benchmark_count = (filtered_cms["status"] == "Below Benchmark").sum()

col1, col2, col3 = st.columns(3)
col1.metric("Average CTR", f"{average_ctr:.2%}")
col2.metric("Needs Attention", f"{needs_attention_count:,}")
col3.metric("Below Benchmark", f"{below_benchmark_count:,}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("CMS Status Breakdown")
    cms_status_counts = filtered_cms["status"].value_counts()
    st.bar_chart(cms_status_counts)
    st.write(cms_status_counts)

with col2:
    st.subheader("Top Performing Pages by CTR")
    top_pages = filtered_cms.sort_values("ctr", ascending=False).head(10)
    st.dataframe(
        top_pages[
            ["content_id", "content_type", "category", "page_views", "pdf_clicks", "ctr", "status"]
        ],
        use_container_width=True
    )

st.subheader("Pages Needing Attention")
attention_pages = filtered_cms[filtered_cms["status"] == "Needs Attention"].sort_values("ctr").head(20)

if len(attention_pages) > 0:
    st.dataframe(
        attention_pages[
            ["content_id", "content_type", "category", "page_views", "pdf_clicks", "ctr", "benchmark_ctr", "status"]
        ],
        use_container_width=True
    )
else:
    st.write("No pages currently flagged as needing attention.")

# -----------------------------
# SUMMARY
# -----------------------------
st.header("🧠 Summary")

st.write(
    """
    This platform demonstrates how behavioural data can be transformed into customer profiles,
    churn risk signals, campaign actions, agent-based recommendations, page optimisation insights,
    and CMS KPI monitoring. It provides a simple interface for filtering, reporting, and identifying
    opportunities for optimisation across both customer journeys and live content performance.
    """
)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Built as part of an AI + Cloud + MarTech portfolio project")
"""
IBM Employees Attrition Analysis — Streamlit Dashboard
Run: streamlit run IBM-Attrition-Dashboard.py
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IBM Employees Attrition Analysis",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# IBM COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
IBM_BLUE     = "#0F62FE"
IBM_BLACK    = "#161616"
IBM_WHITE    = "#FFFFFF"
IBM_GRAY     = "#525252"
IBM_CYAN     = "#1192E8"
IBM_PURPLE   = "#8A3FFC"
IBM_MAGENTA  = "#EE538B"
IBM_TEAL     = "#009D9A"
IBM_GREEN    = "#198038"
IBM_RED      = "#DA1E28"

# Shared attrition semantics: Red = Left, Teal/Blue = Stayed
CLR_LEFT     = IBM_RED
CLR_STAYED   = IBM_CYAN

# Per-page accent colours
PAGE1_PRIMARY = IBM_BLUE
PAGE1_SEC     = IBM_CYAN
PAGE2_PRIMARY = IBM_PURPLE
PAGE2_SEC     = IBM_MAGENTA
PAGE3_PRIMARY = IBM_TEAL
PAGE3_SEC     = IBM_GREEN
PAGE4_PRIMARY = IBM_BLUE

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — IBM Plex Sans, bold typography, Carbon-inspired UI
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

    html, body, [class*="css"], [class*="st-"] {
        font-family: 'IBM Plex Sans', 'Segoe UI', system-ui, sans-serif !important;
        font-size: 16px;
        color: #161616;
    }

    /* App background */
    .stApp {
        background: linear-gradient(160deg, #f4f6fb 0%, #eef1f8 100%);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #161616 !important;
        border-right: 3px solid #0F62FE;
    }
    section[data-testid="stSidebar"] * {
        color: #f4f4f4 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 6px 0;
        color: #c6c6c6 !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #0F62FE !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #8d8d8d !important;
        font-size: 13px !important;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-weight: 700 !important;
        color: #161616 !important;
        letter-spacing: -0.3px;
    }

    /* Dividers */
    hr {
        border-color: #dde1e7;
        margin: 20px 0;
    }

    /* ── Expanders (Business Recommendations + About page) ───────────────── */
    [data-testid="stExpander"] {
        border: none !important;
        border-radius: 8px !important;
        overflow: hidden;
        margin-bottom: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.10);
    }
    [data-testid="stExpander"] summary {
        background-color: #161616 !important;
        padding: 14px 18px !important;
        transition: background-color 0.15s ease;
    }
    [data-testid="stExpander"] summary:hover,
    [data-testid="stExpander"] summary:focus {
        background-color: #262626 !important;
    }
    [data-testid="stExpander"] details[open] > summary {
        background-color: #0F62FE !important;
    }
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary div,
    [data-testid="stExpander"] summary * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    [data-testid="stExpander"] > div:last-child {
        background: #ffffff !important;
        padding: 16px 20px !important;
    }

    /* ── Universal arrow / chevron icon fix ───────────────────────────────
       Streamlit renders these via a ligature icon font (Material Symbols).
       When that font fails to load it shows raw text like
       "keyboard_arrow_right". Replace with a plain CSS triangle that
       always inherits the surrounding text color (dark-on-light,
       light-on-dark automatically via currentColor). */
    [data-testid="stIconMaterial"] {
        font-size: 0 !important;
        width: 14px !important;
        height: 14px !important;
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        color: inherit !important;
    }
    [data-testid="stIconMaterial"]::before {
        content: "";
        display: block;
        width: 0;
        height: 0;
        border-top: 5px solid transparent;
        border-bottom: 5px solid transparent;
        border-left: 7px solid currentColor;
    }
    /* Collapsed sidebar toggle button */
    [data-testid="collapsedControl"] {
        background-color: #161616 !important;
        left: 0 !important;
        top: 0 !important;
        border-radius: 0 8px 8px 0 !important;
        color: #ffffff !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
    }
    /* Force the top header bar to stay dark regardless of light/dark mode */
    [data-testid="stHeader"] {
        background-color: #161616 !important;
    }
    [data-testid="stHeader"] svg {
        fill: #ffffff !important;
    }
    [data-testid="stHeader"] [data-testid="stIconMaterial"] {
        color: #ffffff !important;
    }
        [data-testid="stHeader"] {
        padding-left: 0 !important;
        margin-left: 0 !important;
    }
    [data-testid="collapsedControl"] {
        margin-left: 0 !important;
        margin-top: 0 !important;
    }
    html, body {
        margin: 0 !important;
        padding: 0 !important;
    }
    /* Metric / st.metric override (fallback) */
    [data-testid="stMetric"] label {
        font-weight: 700 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #525252 !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #0F62FE !important;
    }

    /* Captions */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-size: 13px !important;
        color: #6f6f6f !important;
    }

    /* DataFrame */
    [data-testid="stDataFrame"] {
        border: 1px solid #dde1e7;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & CLEANING (same steps as notebook)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("IBM-HR-Employee-Attrition.csv")
    df = df.drop_duplicates()
    constant_cols = [c for c in df.columns if df[c].nunique() == 1]
    df = df.drop(columns=constant_cols)
    df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[17, 25, 35, 45, 55, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "56+"],
        right=True,
    )
    df["TenureBand"] = pd.cut(
        df["YearsAtCompany"],
        bins=[-1, 1, 3, 5, 10, 20, 40],
        labels=["0-1 yr", "2-3 yrs", "4-5 yrs", "6-10 yrs", "11-20 yrs", "21+ yrs"],
        right=True,
    )
    return df

df_full = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg",
    width=120,
)
st.sidebar.markdown(
    "<h3 style='color:#0F62FE !important; font-weight:700; margin-top:8px;'>Navigation</h3>",
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "Go to",
    [
        "🏢 Department & Role Insights",
        "💰 Compensation & Work Conditions",
        "📈 Tenure & Career Growth",
        "📋 Business Recommendations",
        "🗂️ About the Dataset",
    ],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<p style='color:#8d8d8d !important; font-size:13px;'>Dataset: IBM HR Employee Attrition · 1,470 employees</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def page_banner(title: str, subtitle: str, accent_color: str):
    """Renders a bold colored page header banner."""
    st.markdown(
        f"""
        <div style="background:{accent_color};padding:22px 28px 18px 28px;
                    border-radius:6px;margin-bottom:24px;">
            <div style="color:#ffffff;font-size:11px;font-weight:700;
                        letter-spacing:1.5px;text-transform:uppercase;opacity:0.85;
                        margin-bottom:4px;">IBM HR ANALYTICS DASHBOARD</div>
            <div style="color:#ffffff;font-size:26px;font-weight:700;line-height:1.2;">
                {title}
            </div>
            <div style="color:rgba(255,255,255,0.82);font-size:15px;font-weight:400;
                        margin-top:6px;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(col, label: str, value: str, accent: str = IBM_BLUE,
             sub: str = "", icon: str = ""):
    """Custom styled KPI card using HTML."""
    sub_html = f"<div style='font-size:12px;color:#6f6f6f;font-weight:600;margin-top:2px;'>{sub}</div>" if sub else ""
    icon_html = f"<span style='margin-right:6px;font-size:18px;'>{icon}</span>" if icon else ""
    col.markdown(
        f"""
        <div style="background:#ffffff;border-left:4px solid {accent};
                    border-radius:6px;padding:16px 18px;height:100%;
                    box-shadow:0 1px 4px rgba(0,0,0,0.06);">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                        letter-spacing:0.8px;color:#525252;margin-bottom:6px;">{label}</div>
            <div style="font-size:26px;font-weight:700;color:{accent};line-height:1.1;">
                {icon_html}{value}
            </div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_box(text: str, accent: str = IBM_BLUE):
    """Styled callout insight box with colored left border."""
    st.markdown(
        f"""
        <div style="background:#f4f6fb;border-left:4px solid {accent};
                    border-radius:0 6px 6px 0;padding:14px 18px;margin-top:10px;
                    margin-bottom:6px;">
            <span style="font-size:13px;font-weight:700;color:{accent};
                         text-transform:uppercase;letter-spacing:0.5px;">Key Insight: </span>
            <span style="font-size:15px;font-weight:500;color:#161616;">{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def attrition_summary(df):
    total = len(df)
    left  = df["AttritionFlag"].sum()
    rate  = round(left / total * 100, 2) if total > 0 else 0.0
    return total, left, rate


def top_attrition_group(df, col):
    if df.empty:
        return "—", 0.0
    g   = df.groupby(col)["AttritionFlag"].mean()
    top = g.idxmax()
    return top, round(g.max() * 100, 1)


# Dark text used on all chart axes (charts have white/light backgrounds)
_CHART_LABEL_COLOR = "#161616"
_CHART_TICK_FONT   = dict(color=_CHART_LABEL_COLOR, size=12,
                           family="IBM Plex Sans, Segoe UI, sans-serif")
_CHART_TITLE_FONT  = dict(color=_CHART_LABEL_COLOR, size=13,
                           family="IBM Plex Sans, Segoe UI, sans-serif")

def _chart_layout(fig, accent: str):
    """Apply shared IBM chart styling with explicit high-contrast axis labels."""
    fig.update_layout(
        font=dict(family="IBM Plex Sans, Segoe UI, sans-serif", size=13,
                  color=_CHART_LABEL_COLOR),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        title_font=dict(size=15, color=_CHART_LABEL_COLOR,
                        family="IBM Plex Sans, sans-serif"),
        title_font_color=_CHART_LABEL_COLOR,
        legend=dict(
            font=dict(size=12, color=_CHART_LABEL_COLOR),
            title_font=dict(size=12, color=_CHART_LABEL_COLOR),
        ),
        xaxis=dict(
            gridcolor="#e0e0e0",
            linecolor="#c6c6c6",
            tickfont=_CHART_TICK_FONT,
            title_font=_CHART_TITLE_FONT,
            color=_CHART_LABEL_COLOR,
        ),
        yaxis=dict(
            gridcolor="#e0e0e0",
            linecolor="#c6c6c6",
            tickfont=_CHART_TICK_FONT,
            title_font=_CHART_TITLE_FONT,
            color=_CHART_LABEL_COLOR,
        ),
    )
    fig.update_layout(margin=dict(t=50, b=20))
    fig.update_xaxes(
        tickfont=_CHART_TICK_FONT,
        title_font=_CHART_TITLE_FONT,
        color=_CHART_LABEL_COLOR,
    )
    fig.update_yaxes(
        tickfont=_CHART_TICK_FONT,
        title_font=_CHART_TITLE_FONT,
        color=_CHART_LABEL_COLOR,
    )
    return fig


def bar_attrition_by(df, col, title, horizontal=False, accent=IBM_BLUE):
    grp = (
        df.groupby(col)["AttritionFlag"]
        .agg(Total="count", Attritions="sum")
        .assign(Rate=lambda x: (x["Attritions"] / x["Total"] * 100).round(2))
        .reset_index()
        .sort_values("Rate", ascending=horizontal)
    )
    max_rate = grp["Rate"].max()
    grp["Color"] = grp["Rate"].apply(
        lambda v: CLR_LEFT if v == max_rate else accent
    )
    if horizontal:
        fig = px.bar(
            grp, y=col, x="Rate", orientation="h",
            color="Color", color_discrete_map="identity",
            text=grp["Rate"].apply(lambda v: f"{v:.1f}%"),
            title=f"<b>{title}</b>",
            hover_data={"Total": True, "Attritions": True, "Color": False},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_title="Attrition Rate (%)", yaxis_title="")
    else:
        fig = px.bar(
            grp, x=col, y="Rate",
            color="Color", color_discrete_map="identity",
            text=grp["Rate"].apply(lambda v: f"{v:.1f}%"),
            title=f"<b>{title}</b>",
            hover_data={"Total": True, "Attritions": True, "Color": False},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, yaxis_title="Attrition Rate (%)", xaxis_title="")
    fig.update_layout(height=420)
    return _chart_layout(fig, accent)


def grouped_bar_attrition(df, col, title, stayed_color=IBM_CYAN, left_color=IBM_RED):
    grp = (
        df.groupby(col)["AttritionFlag"]
        .agg(Total="count", Attritions="sum")
        .assign(Retained=lambda x: x["Total"] - x["Attritions"])
        .reset_index()
    )
    fig = go.Figure()
    fig.add_bar(
        x=grp[col], y=grp["Retained"], name="Stayed",
        marker_color=stayed_color,
        text=grp["Retained"], textposition="outside",
    )
    fig.add_bar(
        x=grp[col], y=grp["Attritions"], name="Left",
        marker_color=left_color,
        text=grp["Attritions"], textposition="outside",
    )
    fig.update_layout(
        barmode="group", title=f"<b>{title}</b>",
        yaxis_title="Employees", xaxis_title="",
        legend_title="Status", height=420,
    )
    return _chart_layout(fig, stayed_color)


def boxplot_by_attrition(df, col, title, stayed_color=IBM_CYAN, left_color=IBM_RED):
    fig = px.box(
        df, x="Attrition", y=col,
        color="Attrition",
        color_discrete_map={"Yes": left_color, "No": stayed_color},
        points="outliers",
        category_orders={"Attrition": ["Yes", "No"]},
        title=f"<b>{title}</b>",
        labels={"Attrition": "Attrition (Yes=Left, No=Stayed)"},
    )
    fig.update_layout(showlegend=False, height=420)
    return _chart_layout(fig, stayed_color)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DEPARTMENT & ROLE INSIGHTS
# ═════════════════════════════════════════════════════════════════════════════
if page == "🏢 Department & Role Insights":
    page_banner(
        "🏢 Department & Role Insights",
        "Explore attrition patterns across departments, job roles, age groups, and demographics.",
        PAGE1_PRIMARY,
    )

    st.sidebar.markdown("### 🔎 Page Filters")
    dept_opts   = sorted(df_full["Department"].unique())
    role_opts   = sorted(df_full["JobRole"].unique())
    gender_opts = sorted(df_full["Gender"].unique())

    sel_dept   = st.sidebar.multiselect("Department",  dept_opts,   default=dept_opts)
    sel_role   = st.sidebar.multiselect("Job Role",    role_opts,   default=role_opts)
    sel_gender = st.sidebar.multiselect("Gender",      gender_opts, default=gender_opts)

    df = df_full[
        df_full["Department"].isin(sel_dept) &
        df_full["JobRole"].isin(sel_role) &
        df_full["Gender"].isin(sel_gender)
    ]

    total, left, rate = attrition_summary(df)
    risk_dept, risk_dept_rate = top_attrition_group(df, "Department")
    risk_role, risk_role_rate = top_attrition_group(df, "JobRole")

    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_card(k1, "Total Employees",   f"{total:,}",         accent=PAGE1_PRIMARY)
    kpi_card(k2, "Employees Left",    f"{left:,}",          accent=IBM_RED)
    kpi_card(k3, "Attrition Rate",    f"{rate}%",           accent=IBM_RED)
    kpi_card(k4, "Most At-Risk Dept", f"{risk_dept}",       accent=PAGE1_PRIMARY,
             sub=f"Rate: {risk_dept_rate}%")
    kpi_card(k5, "Most At-Risk Role", f"{risk_role}",       accent=PAGE1_PRIMARY,
             sub=f"Rate: {risk_role_rate}%")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            bar_attrition_by(df, "Department", "Attrition Rate by Department",
                             accent=PAGE1_PRIMARY),
            use_container_width=True,
        )
        insight_box(
            f"<b>{risk_dept}</b> has the highest attrition rate "
            f"(<b>{risk_dept_rate}%</b>). Sales roles face quota pressure, "
            "frequent travel, and fewer retention anchors.",
            accent=PAGE1_PRIMARY,
        )
    with c2:
        st.plotly_chart(
            bar_attrition_by(df, "JobRole", "Attrition Rate by Job Role",
                             horizontal=True, accent=PAGE1_PRIMARY),
            use_container_width=True,
        )
        insight_box(
            "<b>Sales Representatives</b>, <b>Laboratory Technicians</b>, and <b>HR roles</b> "
            "consistently top the attrition rankings — targeted retention plans are needed.",
            accent=PAGE1_SEC,
        )

    st.markdown("---")

    c3, c4 = st.columns(2)
    with c3:
        ot_grp = (
            df.groupby("OverTime")["AttritionFlag"]
            .agg(Total="count", Attritions="sum")
            .assign(
                Retained=lambda x: x["Total"] - x["Attritions"],
                Att_Rate=lambda x: (x["Attritions"] / x["Total"] * 100).round(1),
                Ret_Rate=lambda x: (x["Retained"]   / x["Total"] * 100).round(1),
            )
            .reset_index()
        )
        fig_ot = go.Figure()
        fig_ot.add_bar(
            x=ot_grp["OverTime"], y=ot_grp["Ret_Rate"],
            name="Stayed %", marker_color=PAGE1_SEC,
            text=ot_grp["Ret_Rate"].apply(lambda v: f"{v:.1f}%"),
            textposition="inside",
        )
        fig_ot.add_bar(
            x=ot_grp["OverTime"], y=ot_grp["Att_Rate"],
            name="Left %", marker_color=CLR_LEFT,
            text=ot_grp["Att_Rate"].apply(lambda v: f"{v:.1f}%"),
            textposition="inside",
        )
        fig_ot.update_layout(
            barmode="stack", title="<b>Proportional Attrition by OverTime Status</b>",
            yaxis_title="Percentage (%)", xaxis_title="OverTime",
            height=420,
            xaxis=dict(
                tickfont=_CHART_TICK_FONT,
                title_font=_CHART_TITLE_FONT,
                color=_CHART_LABEL_COLOR,
            ),
            yaxis=dict(
                tickfont=_CHART_TICK_FONT,
                title_font=_CHART_TITLE_FONT,
                color=_CHART_LABEL_COLOR,
            ),
        )
        _chart_layout(fig_ot, PAGE1_PRIMARY)
        st.plotly_chart(fig_ot, use_container_width=True)
        ot_yes = ot_grp.loc[ot_grp["OverTime"] == "Yes", "Att_Rate"].values
        ot_no  = ot_grp.loc[ot_grp["OverTime"] == "No",  "Att_Rate"].values
        ot_msg = (
            f"Overtime employees leave at <b>{ot_yes[0]}%</b> vs "
            f"<b>{ot_no[0]}%</b> for non-OT. Overtime is one of the "
            "strongest single predictors of attrition."
        ) if len(ot_yes) and len(ot_no) else "Insufficient data for this filter."
        insight_box(ot_msg, accent=PAGE1_PRIMARY)

    with c4:
        st.plotly_chart(
            bar_attrition_by(
                df.assign(AgeGroup=df["AgeGroup"].astype(str)),
                "AgeGroup", "Attrition Rate by Age Group",
                accent=PAGE1_PRIMARY,
            ),
            use_container_width=True,
        )
        insight_box(
            "The <b>18-25</b> age band has the highest attrition rate. Early-career employees "
            "are still exploring fit and have fewer financial obligations anchoring them.",
            accent=PAGE1_SEC,
        )

    st.markdown("---")

    _, c5, _ = st.columns([1, 2, 1])
    with c5:
        st.plotly_chart(
            grouped_bar_attrition(df, "MaritalStatus",
                                  "Attrition Count by Marital Status",
                                  stayed_color=PAGE1_SEC, left_color=CLR_LEFT),
            use_container_width=True,
        )
        top_ms, top_ms_rate = top_attrition_group(df, "MaritalStatus")
        insight_box(
            f"<b>{top_ms}</b> employees have the highest attrition rate "
            f"(<b>{top_ms_rate}%</b>). Fewer financial obligations and greater mobility "
            "make them more likely to change jobs.",
            accent=PAGE1_PRIMARY,
        )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2 — COMPENSATION & WORK CONDITIONS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "💰 Compensation & Work Conditions":
    page_banner(
        "💰 Compensation & Work Conditions",
        "Examine how income, commute, work-life balance, stock options, and salary hikes relate to attrition.",
        PAGE2_PRIMARY,
    )

    st.sidebar.markdown("### 🔎 Page Filters")
    dept_opts2 = sorted(df_full["Department"].unique())
    wlb_opts   = sorted(df_full["WorkLifeBalance"].unique())
    ot_opts    = sorted(df_full["OverTime"].unique())

    sel_dept2 = st.sidebar.multiselect("Department",        dept_opts2, default=dept_opts2)
    sel_wlb   = st.sidebar.multiselect("Work-Life Balance", wlb_opts,   default=wlb_opts)
    sel_ot    = st.sidebar.multiselect("OverTime",          ot_opts,    default=ot_opts)

    df2 = df_full[
        df_full["Department"].isin(sel_dept2) &
        df_full["WorkLifeBalance"].isin(sel_wlb) &
        df_full["OverTime"].isin(sel_ot)
    ]

    total2, left2, rate2 = attrition_summary(df2)
    avg_inc_left   = df2.loc[df2["Attrition"] == "Yes", "MonthlyIncome"].mean()
    avg_inc_stayed = df2.loc[df2["Attrition"] == "No",  "MonthlyIncome"].mean()
    avg_dist_left   = df2.loc[df2["Attrition"] == "Yes", "DistanceFromHome"].mean()
    avg_dist_stayed = df2.loc[df2["Attrition"] == "No",  "DistanceFromHome"].mean()

    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_card(k1, "Total Employees",      f"{total2:,}",   accent=PAGE2_PRIMARY)
    kpi_card(k2, "Employees Left",       f"{left2:,}",    accent=IBM_RED)
    kpi_card(k3, "Attrition Rate",       f"{rate2}%",     accent=IBM_RED)
    kpi_card(
        k4, "Avg Income (Left)",
        f"${avg_inc_left:,.0f}" if not np.isnan(avg_inc_left) else "—",
        accent=PAGE2_PRIMARY,
        sub=f"Stayed: ${avg_inc_stayed:,.0f}" if not np.isnan(avg_inc_stayed) else "",
    )
    kpi_card(
        k5, "Avg Dist. From Home (Left)",
        f"{avg_dist_left:.1f} km" if not np.isnan(avg_dist_left) else "—",
        accent=PAGE2_PRIMARY,
        sub=f"Stayed: {avg_dist_stayed:.1f} km" if not np.isnan(avg_dist_stayed) else "",
    )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            boxplot_by_attrition(df2, "MonthlyIncome", "Monthly Income by Attrition",
                                 stayed_color=PAGE2_PRIMARY, left_color=CLR_LEFT),
            use_container_width=True,
        )
        inc_gap = round(avg_inc_stayed - avg_inc_left, 0) if not (
            np.isnan(avg_inc_left) or np.isnan(avg_inc_stayed)
        ) else None
        gap_str = f"~<b>${inc_gap:,.0f}</b>" if inc_gap is not None else "a significant amount"
        insight_box(
            f"Employees who left earn {gap_str} less per month than those who stayed. "
            "Compensation is one of the strongest retention levers.",
            accent=PAGE2_PRIMARY,
        )
    with c2:
        st.plotly_chart(
            boxplot_by_attrition(df2, "DistanceFromHome", "Distance From Home by Attrition",
                                 stayed_color=PAGE2_PRIMARY, left_color=CLR_LEFT),
            use_container_width=True,
        )
        insight_box(
            "Employees who left commute further on average. Long commutes increase fatigue "
            "and reduce work-life balance — <b>hybrid/remote options</b> can mitigate this.",
            accent=PAGE2_SEC,
        )

    st.markdown("---")

    c3, c4 = st.columns(2)
    with c3:
        wlb_labels = {1: "1-Bad", 2: "2-Good", 3: "3-Better", 4: "4-Best"}
        df2_wlb = df2.copy()
        df2_wlb["WLB_Label"] = df2_wlb["WorkLifeBalance"].map(wlb_labels)
        st.plotly_chart(
            bar_attrition_by(df2_wlb, "WLB_Label",
                             "Attrition Rate by Work-Life Balance",
                             accent=PAGE2_PRIMARY),
            use_container_width=True,
        )
        insight_box(
            "Score <b>1 (Bad)</b> has the highest attrition rate. Flexible hours and "
            "wellness support should target scores 1 & 2 first.",
            accent=PAGE2_PRIMARY,
        )
    with c4:
        sol_labels = {0: "0-None", 1: "1-Low", 2: "2-Medium", 3: "3-High"}
        df2_sol = df2.copy()
        df2_sol["SOL_Label"] = df2_sol["StockOptionLevel"].map(sol_labels)
        st.plotly_chart(
            bar_attrition_by(df2_sol, "SOL_Label",
                             "Attrition Rate by Stock Option Level",
                             accent=PAGE2_SEC),
            use_container_width=True,
        )
        insight_box(
            "Employees with <b>no stock options (Level 0)</b> have the highest attrition. "
            "Extending Level 1 options to entry-level roles is a cost-effective retention lever.",
            accent=PAGE2_SEC,
        )

    st.markdown("---")

    _, c5, _ = st.columns([1, 2, 1])
    with c5:
        st.plotly_chart(
            boxplot_by_attrition(df2, "PercentSalaryHike",
                                 "Percent Salary Hike by Attrition",
                                 stayed_color=PAGE2_PRIMARY, left_color=CLR_LEFT),
            use_container_width=True,
        )
        insight_box(
            "The salary hike distributions are similar between groups — hike % alone is not "
            "the dominant driver, but employees receiving the <b>lowest hikes (11-13%)</b> show "
            "elevated attrition. Transparent, market-benchmarked hike policies matter.",
            accent=PAGE2_PRIMARY,
        )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 3 — TENURE & CAREER GROWTH
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📈 Tenure & Career Growth":
    page_banner(
        "📈 Tenure & Career Growth",
        "Discover how tenure, promotions, job satisfaction, training, and mobility affect attrition.",
        PAGE3_PRIMARY,
    )

    st.sidebar.markdown("### 🔎 Page Filters")
    role_opts3 = sorted(df_full["JobRole"].unique())
    sel_role3  = st.sidebar.multiselect("Job Role", role_opts3, default=role_opts3)

    yac_min, yac_max = int(df_full["YearsAtCompany"].min()), int(df_full["YearsAtCompany"].max())
    sel_yac = st.sidebar.slider("Years at Company", yac_min, yac_max, (yac_min, yac_max))

    ncw_min, ncw_max = int(df_full["NumCompaniesWorked"].min()), int(df_full["NumCompaniesWorked"].max())
    sel_ncw = st.sidebar.slider("Num Companies Worked", ncw_min, ncw_max, (ncw_min, ncw_max))

    df3 = df_full[
        df_full["JobRole"].isin(sel_role3) &
        df_full["YearsAtCompany"].between(sel_yac[0], sel_yac[1]) &
        df_full["NumCompaniesWorked"].between(sel_ncw[0], sel_ncw[1])
    ]

    total3, left3, rate3 = attrition_summary(df3)
    avg_yac_left     = df3.loc[df3["Attrition"] == "Yes", "YearsAtCompany"].mean()
    avg_yac_stayed   = df3.loc[df3["Attrition"] == "No",  "YearsAtCompany"].mean()
    avg_promo_left   = df3.loc[df3["Attrition"] == "Yes", "YearsSinceLastPromotion"].mean()
    avg_promo_stayed = df3.loc[df3["Attrition"] == "No",  "YearsSinceLastPromotion"].mean()

    k1, k2, k3, k4, k5 = st.columns(5)
    kpi_card(k1, "Total Employees",      f"{total3:,}",  accent=PAGE3_PRIMARY)
    kpi_card(k2, "Employees Left",       f"{left3:,}",   accent=IBM_RED)
    kpi_card(k3, "Attrition Rate",       f"{rate3}%",    accent=IBM_RED)
    kpi_card(
        k4, "Avg Years at Co. (Left)",
        f"{avg_yac_left:.1f} yrs" if not np.isnan(avg_yac_left) else "—",
        accent=PAGE3_PRIMARY,
        sub=f"Stayed: {avg_yac_stayed:.1f} yrs" if not np.isnan(avg_yac_stayed) else "",
    )
    kpi_card(
        k5, "Avg Yrs Since Promo (Left)",
        f"{avg_promo_left:.1f} yrs" if not np.isnan(avg_promo_left) else "—",
        accent=PAGE3_PRIMARY,
        sub=f"Stayed: {avg_promo_stayed:.1f} yrs" if not np.isnan(avg_promo_stayed) else "",
    )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.divider()

    c1, c2 = st.columns(2)
    sat_labels = {1: "1-Low", 2: "2-Med", 3: "3-High", 4: "4-Very High"}
    with c1:
        df3_js = df3.copy()
        df3_js["JS_Label"] = df3_js["JobSatisfaction"].map(sat_labels)
        st.plotly_chart(
            bar_attrition_by(df3_js, "JS_Label",
                             "Attrition Rate by Job Satisfaction",
                             accent=PAGE3_PRIMARY),
            use_container_width=True,
        )
        insight_box(
            "Employees with <b>Low (1)</b> job satisfaction leave at the highest rate. "
            "Regular engagement surveys and manager one-on-ones can flag dissatisfied employees early.",
            accent=PAGE3_PRIMARY,
        )
    with c2:
        df3_es = df3.copy()
        df3_es["ES_Label"] = df3_es["EnvironmentSatisfaction"].map(sat_labels)
        st.plotly_chart(
            bar_attrition_by(df3_es, "ES_Label",
                             "Attrition Rate by Environment Satisfaction",
                             accent=PAGE3_SEC),
            use_container_width=True,
        )
        insight_box(
            "Poor workplace environment (Score <b>1</b>) strongly correlates with attrition. "
            "Office redesign, ergonomics, and culture initiatives directly reduce this risk.",
            accent=PAGE3_SEC,
        )

    st.markdown("---")

    c3, c4 = st.columns(2)
    with c3:
        fig_hist = go.Figure()
        for label, color in [("Yes", CLR_LEFT), ("No", PAGE3_PRIMARY)]:
            subset = df3.loc[df3["Attrition"] == label, "YearsAtCompany"]
            fig_hist.add_trace(go.Histogram(
                x=subset, nbinsx=20, name=f"Left={label}",
                marker_color=color, opacity=0.65,
            ))
        fig_hist.update_layout(
            barmode="overlay",
            title="<b>YearsAtCompany Distribution by Attrition</b>",
            xaxis_title="Years at Company", yaxis_title="Count",
            height=420,
            legend=dict(title="Attrition"),
            xaxis=dict(
                tickfont=_CHART_TICK_FONT,
                title_font=_CHART_TITLE_FONT,
                color=_CHART_LABEL_COLOR,
            ),
            yaxis=dict(
                tickfont=_CHART_TICK_FONT,
                title_font=_CHART_TITLE_FONT,
                color=_CHART_LABEL_COLOR,
            ),
        )
        _chart_layout(fig_hist, PAGE3_PRIMARY)
        st.plotly_chart(fig_hist, use_container_width=True)
        insight_box(
            "Attrition peaks in the <b>0-1 year</b> band (~36%). Employees who find a role "
            "mismatch leave quickly — strong onboarding and <b>30/60/90-day check-ins</b> are critical.",
            accent=PAGE3_PRIMARY,
        )
    with c4:
        st.plotly_chart(
            bar_attrition_by(df3, "NumCompaniesWorked",
                             "Attrition Rate by Num Companies Worked",
                             accent=PAGE3_PRIMARY),
            use_container_width=True,
        )
        insight_box(
            "Employees who worked at <b>1 prior company</b> (early career) and those with "
            "<b>5+ prior companies</b> (job-hoppers) show elevated attrition — "
            "both groups warrant early engagement interventions.",
            accent=PAGE3_SEC,
        )

    st.markdown("---")

    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(
            boxplot_by_attrition(
                df3, "YearsSinceLastPromotion",
                "Years Since Last Promotion by Attrition",
                stayed_color=PAGE3_PRIMARY, left_color=CLR_LEFT,
            ),
            use_container_width=True,
        )
        insight_box(
            "Employees who left waited longer since their last promotion. "
            "<b>Bi-annual promotion reviews</b> and transparent criteria reduce "
            "the perception of stagnant career growth.",
            accent=PAGE3_PRIMARY,
        )
    with c6:
        st.plotly_chart(
            bar_attrition_by(
                df3, "TrainingTimesLastYear",
                "Attrition Rate by Training Times Last Year",
                accent=PAGE3_SEC,
            ),
            use_container_width=True,
        )
        insight_box(
            "<b>0 trainings</b> correlates with above-average attrition. A minimum of "
            "<b>2-4 training sessions</b> per year is associated with the lowest attrition rates — "
            "L&D investment signals that the company values employee growth.",
            accent=PAGE3_SEC,
        )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 4 — BUSINESS RECOMMENDATIONS
# ═════════════════════════════════════════════════════════════════════════════
elif page == "📋 Business Recommendations":
    page_banner(
        "📋 Business Recommendations",
        "Evidence-based, actionable strategies for HR leadership derived from the 15 attrition analyses.",
        PAGE4_PRIMARY,
    )

    total_f, left_f, rate_f = attrition_summary(df_full)
    ot_rate     = round(df_full.loc[df_full["OverTime"] == "Yes", "AttritionFlag"].mean() * 100, 1)
    single_rate = round(df_full.loc[df_full["MaritalStatus"] == "Single", "AttritionFlag"].mean() * 100, 1)
    income_gap  = round(
        df_full.loc[df_full["Attrition"] == "No",  "MonthlyIncome"].mean() -
        df_full.loc[df_full["Attrition"] == "Yes", "MonthlyIncome"].mean(), 0
    )

    st.markdown(
        f"""
        <div style="background:#161616;border-left:5px solid {IBM_BLUE};
                    padding:20px 26px;border-radius:6px;margin-bottom:28px;">
            <div style="color:#0F62FE;font-size:12px;font-weight:700;
                        text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">
                📊 Overall Attrition Summary
            </div>
            <p style="margin:0;line-height:1.9;color:#f4f4f4;font-size:15px;">
                Out of <strong style="color:#ffffff;">{total_f:,}</strong> employees,
                <strong style="color:{IBM_RED};">{left_f:,}</strong> left —
                an overall attrition rate of <strong style="color:{IBM_RED};">{rate_f}%</strong>.<br>
                Primary drivers across 15 analyses:
                <strong style="color:#78a9ff;">overtime</strong>
                ({ot_rate}% attrition for OT employees) ·
                <strong style="color:#78a9ff;">low monthly income</strong>
                (~${income_gap:,.0f}/mo gap) ·
                <strong style="color:#78a9ff;">poor work-life balance</strong> ·
                <strong style="color:#78a9ff;">single marital status</strong>
                ({single_rate}% rate) ·
                <strong style="color:#78a9ff;">no stock options</strong> ·
                <strong style="color:#78a9ff;">early tenure (0-1 yr)</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    recommendations = [
        {
            "icon": "🕐",
            "title": "Enforce Overtime Limits & Introduce Compensatory Mechanisms",
            "basis": "Analysis 3 — OverTime vs Attrition",
            "detail": (
                f"Overtime employees leave at <b>{ot_rate}%</b> — nearly 3× the non-OT rate. "
                "Set monthly OT caps, introduce time-off-in-lieu or OT bonuses, and train managers "
                "to redistribute workloads before approving sustained overtime."
            ),
        },
        {
            "icon": "💰",
            "title": "Conduct Targeted Compensation Reviews for Lower-Income Roles",
            "basis": "Analysis 4 — MonthlyIncome; Analysis 15 — PercentSalaryHike",
            "detail": (
                f"Employees who left earn ~<b>${income_gap:,.0f}/month less</b> than those who stayed. "
                "Benchmark salaries against market rates annually and prioritise above-average hikes "
                "for Sales Representatives, Lab Technicians, and HR roles."
            ),
        },
        {
            "icon": "📈",
            "title": "Establish Structured Career Progression & Promotion Review Cycles",
            "basis": "Analysis 13 — YearsSinceLastPromotion; Analysis 5 — Age Group",
            "detail": (
                "Employees who left waited longer since their last promotion. Implement <b>bi-annual "
                "promotion reviews</b>, create transparent advancement criteria, and fast-track "
                "high-performers stagnant for 3+ years. Communicate career ladders clearly during onboarding."
            ),
        },
        {
            "icon": "🎯",
            "title": "Launch Role-Specific Retention Programme for Sales",
            "basis": "Analysis 1 — Attrition by Department; Analysis 2 — Attrition by Job Role",
            "detail": (
                "Sales has the highest department attrition (<b>~20.6%</b>) and Sales Representatives the "
                "highest role attrition (<b>~39.8%</b>). Review quota structures, commission plans, and "
                "travel demands. Deploy mentoring, recognition, and clear Senior Sales career paths immediately."
            ),
        },
        {
            "icon": "🏠",
            "title": "Introduce Flexible Work Arrangements for High-Commute Employees",
            "basis": "Analysis 6 — DistanceFromHome vs Attrition",
            "detail": (
                "Employees who left commute ~1.7 units further on average. Identify employees "
                "beyond a commute threshold and offer <b>hybrid/remote options</b>, relocation assistance, "
                "or transport allowances — a low-cost, high-impact retention lever."
            ),
        },
        {
            "icon": "🎓",
            "title": "Invest in L&D with 2–4 Structured Training Sessions Per Year",
            "basis": "Analysis 14 — TrainingTimesLastYear vs Attrition",
            "detail": (
                "0 trainings correlates with above-average attrition. A balanced frequency of "
                "<b>2-4 sessions/year</b> shows the lowest rates. Embed development plans in performance "
                "reviews and tie training milestones to career progression."
            ),
        },
        {
            "icon": "📊",
            "title": "Expand Stock Option Coverage to Entry-Level & High-Risk Roles",
            "basis": "Analysis 12 — StockOptionLevel vs Attrition",
            "detail": (
                "Employees with no stock options (Level 0) leave at <b>24.4%</b> vs <b>9.4%</b> at Level 1. "
                "Extend Level 1 options to Sales Representatives, Lab Technicians, and single employees "
                "aged 18-35 — the demographic most likely to leave without a financial anchor."
            ),
        },
        {
            "icon": "🔍",
            "title": "Implement an Early-Warning Attrition Risk Score for New Joiners",
            "basis": "Analysis 9 — YearsAtCompany (0-1yr band ~36.4%); EDA — Correlation Heatmap",
            "detail": (
                "Attrition peaks in the first year. Build a simple risk score from key predictors "
                "(OverTime, MonthlyIncome, StockOptionLevel, JobSatisfaction, YearsAtCompany) and "
                "flag high-risk new joiners at <b>30/60/90 days</b> for proactive manager check-ins and "
                "onboarding buddy programmes."
            ),
        },
    ]

    for i, rec in enumerate(recommendations, start=1):
        with st.expander(f"**{rec['icon']} {i}. {rec['title']}**", expanded=True):
            st.markdown(
                f"<div style='font-size:12px;color:{IBM_GRAY};font-weight:600;"
                f"margin-bottom:8px;'>📎 Based on: <em>{rec['basis']}</em></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='font-size:15px;font-weight:400;line-height:1.7;"
                f"color:#161616;'>{rec['detail']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown(
        f"<p style='font-size:13px;color:{IBM_GRAY};'>⚠️ All rates and figures are computed directly "
        "from the IBM HR Employee Attrition dataset (1,470 employees). Recommendations should be "
        "validated with qualitative employee feedback (exit interviews, pulse surveys) before deployment.</p>",
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 5 — ABOUT THE DATASET
# ═════════════════════════════════════════════════════════════════════════════
elif page == "🗂️ About the Dataset":
    page_banner(
        "🗂️ About the Dataset",
        "Data source, exploration summary, EDA findings, and cleaning steps.",
        IBM_GRAY,
    )

    st.markdown(
        f"""
        <div style="background:#ffffff;border:1px solid #dde1e7;border-radius:6px;
                    padding:18px 22px;margin-bottom:20px;">
            <span style="font-size:15px;font-weight:500;color:#161616;">
                The original dataset was downloaded from
            </span>
            <a href="https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset?resource=download"
               target="_blank"
               style="color:{IBM_BLUE};font-weight:700;font-size:15px;margin-left:6px;">
                Kaggle — IBM HR Analytics Attrition Dataset
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def section_header(title, color=IBM_BLUE):
        st.markdown(
            f"<h3 style='color:{color};font-size:18px;font-weight:700;"
            f"border-bottom:2px solid {color};padding-bottom:6px;margin-top:24px;"
            f"margin-bottom:16px;'>{title}</h3>",
            unsafe_allow_html=True,
        )

    section_header("📂 Data Exploration", IBM_BLUE)

    raw_df = pd.read_csv("IBM-HR-Employee-Attrition.csv")
    n_rows, n_cols = raw_df.shape

    col_a, col_b, col_c = st.columns(3)
    kpi_card(col_a, "Total Rows",    f"{n_rows:,}",  accent=IBM_BLUE)
    kpi_card(col_b, "Total Columns", f"{n_cols}",    accent=IBM_BLUE)
    kpi_card(col_c, "Missing Values", "0",           accent=IBM_GREEN)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    with st.expander("📋 Column List & Data Types", expanded=False):
        dtype_df = pd.DataFrame({
            "Column": raw_df.columns,
            "Data Type": raw_df.dtypes.astype(str).values,
            "Unique Values": [raw_df[c].nunique() for c in raw_df.columns],
            "Sample": [str(raw_df[c].iloc[0]) for c in raw_df.columns],
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    section_header("📊 Key Summary Statistics", IBM_CYAN)
    numeric_cols = ["Age", "MonthlyIncome", "DistanceFromHome", "YearsAtCompany",
                    "TotalWorkingYears", "YearsSinceLastPromotion", "NumCompaniesWorked"]
    stats_df = raw_df[numeric_cols].describe().round(2).T.reset_index()
    stats_df.columns = ["Column", "Count", "Mean", "Std", "Min", "25%", "Median", "75%", "Max"]
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

    section_header("🔬 Exploratory Data Analysis", IBM_TEAL)

    overall_att_rate = round(raw_df["Attrition"].value_counts(normalize=True)["Yes"] * 100, 2)
    att_counts = raw_df["Attrition"].value_counts()

    st.markdown(
        f"""
        <div style="background:#f4f6fb;border-left:4px solid {IBM_TEAL};
                    border-radius:0 6px 6px 0;padding:14px 18px;margin-bottom:20px;">
            <span style="font-size:13px;font-weight:700;color:{IBM_TEAL};
                         text-transform:uppercase;letter-spacing:0.5px;">Overall Attrition Rate: </span>
            <span style="font-size:22px;font-weight:700;color:{IBM_RED};">{overall_att_rate}%</span>
            <span style="font-size:14px;color:#525252;margin-left:12px;">
                ({att_counts.get('Yes', 0):,} left out of {len(raw_df):,} employees)
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    eda_c1, eda_c2, eda_c3 = st.columns(3)

    with eda_c1:
        fig_age = px.histogram(
            raw_df, x="Age", color="Attrition",
            color_discrete_map={"Yes": CLR_LEFT, "No": IBM_TEAL},
            nbins=20, barmode="overlay", opacity=0.7,
            title="<b>Age Distribution by Attrition</b>",
        )
        fig_age.update_layout(height=360, legend_title="Attrition")
        _chart_layout(fig_age, IBM_TEAL)
        st.plotly_chart(fig_age, use_container_width=True)

    with eda_c2:
        fig_inc = px.histogram(
            raw_df, x="MonthlyIncome", color="Attrition",
            color_discrete_map={"Yes": CLR_LEFT, "No": IBM_TEAL},
            nbins=25, barmode="overlay", opacity=0.7,
            title="<b>Monthly Income Distribution</b>",
        )
        fig_inc.update_layout(height=360, legend_title="Attrition")
        _chart_layout(fig_inc, IBM_TEAL)
        st.plotly_chart(fig_inc, use_container_width=True)

    with eda_c3:
        fig_dist = px.histogram(
            raw_df, x="DistanceFromHome", color="Attrition",
            color_discrete_map={"Yes": CLR_LEFT, "No": IBM_TEAL},
            nbins=20, barmode="overlay", opacity=0.7,
            title="<b>Distance From Home Distribution</b>",
        )
        fig_dist.update_layout(height=360, legend_title="Attrition")
        _chart_layout(fig_dist, IBM_TEAL)
        st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    corr_cols = [
        "Age", "MonthlyIncome", "DistanceFromHome", "YearsAtCompany",
        "TotalWorkingYears", "YearsSinceLastPromotion", "NumCompaniesWorked",
        "JobSatisfaction", "WorkLifeBalance", "EnvironmentSatisfaction",
        "JobLevel", "StockOptionLevel", "TrainingTimesLastYear",
    ]
    corr_df_raw = raw_df.copy()
    corr_df_raw["AttritionFlag"] = corr_df_raw["Attrition"].map({"Yes": 1, "No": 0})
    corr_matrix = corr_df_raw[corr_cols + ["AttritionFlag"]].corr().round(2)

    fig_corr = px.imshow(
        corr_matrix,
        color_continuous_scale=[
            [0.0, IBM_RED], [0.5, "#ffffff"], [1.0, IBM_BLUE]
        ],
        zmin=-1, zmax=1,
        text_auto=".2f",
        title="<b>Correlation Heatmap — Key Numeric Features</b>",
        aspect="auto",
    )
    fig_corr.update_layout(
        height=520,
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            tickfont=dict(color=_CHART_LABEL_COLOR, size=11,
                          family="IBM Plex Sans, Segoe UI, sans-serif"),
            title_font=dict(color=_CHART_LABEL_COLOR, size=12,
                            family="IBM Plex Sans, Segoe UI, sans-serif"),
        ),
    )
    fig_corr.update_traces(
        textfont=dict(color="#161616", size=10,
                      family="IBM Plex Sans, Segoe UI, sans-serif"),
    )
    _chart_layout(fig_corr, IBM_TEAL)
    st.plotly_chart(fig_corr, use_container_width=True)

    insight_box(
        "Attrition is most negatively correlated with <b>JobLevel</b>, <b>TotalWorkingYears</b>, "
        "<b>MonthlyIncome</b>, and <b>YearsAtCompany</b> — senior, experienced, well-paid, "
        "long-tenured employees are significantly less likely to leave.",
        accent=IBM_TEAL,
    )

    section_header("🧹 Data Cleaning Summary", IBM_GRAY)

    raw_dupes = raw_df.duplicated().sum()
    constant_cols_found = [c for c in raw_df.columns if raw_df[c].nunique() == 1]
    missing_total = raw_df.isnull().sum().sum()

    cleaning_steps = [
        ("Duplicate Rows Checked",     f"{raw_dupes} duplicate rows found — all removed.",   IBM_GREEN  if raw_dupes == 0 else IBM_RED),
        ("Constant Columns Dropped",   f"{len(constant_cols_found)} constant column(s) removed: "
                                       f"{', '.join(constant_cols_found) if constant_cols_found else 'None'}.",  IBM_BLUE),
        ("Missing Values",             f"{missing_total} missing values — none found in this dataset.", IBM_GREEN),
        ("AttritionFlag Created",      "Binary numeric column AttritionFlag added (Yes→1, No→0) "
                                       "for numeric correlation and aggregation analysis.",             IBM_BLUE),
        ("AgeGroup Engineered",        "Age binned into 5 groups: 18-25, 26-35, 36-45, 46-55, 56+.",   IBM_CYAN),
        ("TenureBand Engineered",      "YearsAtCompany binned into 6 bands for tenure-based analysis.", IBM_CYAN),
    ]

    for step_title, step_detail, step_color in cleaning_steps:
        st.markdown(
            f"""
            <div style="background:#ffffff;border-left:4px solid {step_color};
                        border-radius:0 6px 6px 0;padding:12px 18px;margin-bottom:10px;
                        box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                <div style="font-size:13px;font-weight:700;color:{step_color};
                            text-transform:uppercase;letter-spacing:0.5px;margin-bottom:3px;">
                    {step_title}
                </div>
                <div style="font-size:14px;font-weight:400;color:#161616;">
                    {step_detail}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

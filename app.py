import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NETRA // Network Traffic Analyzer",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Live Traffic"

if "running" not in st.session_state:
    st.session_state.running = True

if "traffic_seed" not in st.session_state:
    st.session_state.traffic_seed = 42

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ----------------------------------------------------------
   GLOBAL
---------------------------------------------------------- */

:root {
    --bg: #080b0b;
    --bg-soft: #0d1110;
    --panel: #101514;
    --panel-2: #131918;
    --line: #27302d;
    --line-soft: #1b2421;

    --text: #e7eee9;
    --muted: #7e8b85;
    --muted-2: #53605b;

    --green: #a7e35d;
    --green-soft: #78a83f;

    --amber: #e8b95d;
    --red: #e46f61;
    --cyan: #71c8c3;

    --mono: 'DM Mono', monospace;
    --sans: 'Space Grotesk', sans-serif;
}

html,
body,
[class*="css"] {
    font-family: var(--sans);
}

.stApp {
    background:
        radial-gradient(
            circle at 85% 0%,
            rgba(111, 147, 80, 0.075),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 90%,
            rgba(48, 91, 80, 0.06),
            transparent 25%
        ),
        var(--bg);
    color: var(--text);
}

/* subtle technical grid */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.025;
    background-image:
        linear-gradient(#ffffff 1px, transparent 1px),
        linear-gradient(90deg, #ffffff 1px, transparent 1px);
    background-size: 48px 48px;
    z-index: 0;
}

/* ----------------------------------------------------------
   REMOVE DEFAULT STREAMLIT ELEMENTS
---------------------------------------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1500px;
}

/* ----------------------------------------------------------
   SIDEBAR
---------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: #090d0c;
    border-right: 1px solid var(--line-soft);
}

section[data-testid="stSidebar"] > div {
    padding: 1.6rem 1rem;
}

.brand {
    padding: 0.4rem 0.35rem 1.8rem 0.35rem;
}

.brand-mark {
    display: flex;
    align-items: center;
    gap: 10px;
}

.brand-symbol {
    width: 34px;
    height: 34px;
    border: 1px solid #4c5a53;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--green);
    font-family: var(--mono);
    font-size: 17px;
    background:
        linear-gradient(
            135deg,
            rgba(167,227,93,.10),
            rgba(167,227,93,.01)
        );
}

.brand-name {
    font-family: var(--mono);
    font-size: 16px;
    letter-spacing: 0.12em;
    color: var(--text);
}

.brand-sub {
    font-family: var(--mono);
    color: var(--muted);
    font-size: 9px;
    letter-spacing: 0.15em;
    margin-top: 5px;
}

.nav-label {
    font-family: var(--mono);
    color: var(--muted-2);
    font-size: 9px;
    letter-spacing: 0.18em;
    margin: 20px 5px 8px;
}

div[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    border: 1px solid transparent;
    background: transparent;
    color: #84908b;
    text-align: left;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.03em;
    padding: 0.75rem 0.8rem;
    border-radius: 2px;
    transition: all 0.15s ease;
}

div[data-testid="stSidebar"] .stButton > button:hover {
    border-color: var(--line);
    background: #101614;
    color: var(--text);
}

.sidebar-status {
    margin-top: 30px;
    border: 1px solid var(--line);
    background: #0c1110;
    padding: 13px;
}

.status-line {
    display: flex;
    justify-content: space-between;
    font-family: var(--mono);
    font-size: 9px;
    margin-bottom: 8px;
}

.status-key {
    color: var(--muted-2);
}

.status-value {
    color: var(--green);
}

.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 10px rgba(167,227,93,.7);
    margin-right: 5px;
}

/* ----------------------------------------------------------
   PAGE HEADER
---------------------------------------------------------- */

.eyebrow {
    font-family: var(--mono);
    color: var(--green);
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.page-title {
    font-family: var(--sans);
    font-size: 34px;
    line-height: 1.05;
    font-weight: 600;
    letter-spacing: -0.035em;
    color: #eef4f0;
    margin-bottom: 7px;
}

.page-description {
    color: var(--muted);
    font-family: var(--mono);
    font-size: 10px;
    line-height: 1.7;
    max-width: 760px;
}

.header-rule {
    height: 1px;
    background: linear-gradient(
        90deg,
        var(--green-soft),
        var(--line),
        transparent
    );
    margin: 23px 0 25px;
}

/* ----------------------------------------------------------
   PANELS
---------------------------------------------------------- */

.panel {
    border: 1px solid var(--line);
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.018),
            rgba(255,255,255,0)
        ),
        var(--panel);
    padding: 19px;
    position: relative;
    overflow: hidden;
}

.panel::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 70px;
    height: 1px;
    background: var(--green-soft);
    opacity: .7;
}

.panel-title {
    font-family: var(--mono);
    font-size: 10px;
    color: #a7b3ad;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.panel-meta {
    font-family: var(--mono);
    font-size: 8px;
    color: var(--muted-2);
    margin-top: 4px;
}

/* ----------------------------------------------------------
   METRIC CARDS
---------------------------------------------------------- */

.metric {
    border: 1px solid var(--line);
    background: #0d1211;
    padding: 17px;
    min-height: 116px;
    position: relative;
}

.metric-label {
    color: var(--muted-2);
    font-family: var(--mono);
    font-size: 8px;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.metric-value {
    color: #edf4ef;
    font-family: var(--mono);
    font-size: 25px;
    margin-top: 12px;
    letter-spacing: -0.04em;
}

.metric-value.green {
    color: var(--green);
}

.metric-value.amber {
    color: var(--amber);
}

.metric-value.red {
    color: var(--red);
}

.metric-foot {
    color: var(--muted-2);
    font-family: var(--mono);
    font-size: 8px;
    margin-top: 7px;
}

/* ----------------------------------------------------------
   TRAFFIC FEED
---------------------------------------------------------- */

.feed-row {
    display: grid;
    grid-template-columns:
        90px
        125px
        125px
        80px
        110px
        100px
        1fr;
    gap: 10px;
    padding: 10px 7px;
    border-bottom: 1px solid #19211f;
    font-family: var(--mono);
    font-size: 9px;
    align-items: center;
}

.feed-row:hover {
    background: rgba(167,227,93,.025);
}

.feed-header {
    color: var(--muted-2);
    font-size: 8px;
    text-transform: uppercase;
    letter-spacing: .08em;
    border-bottom: 1px solid var(--line);
}

.protocol {
    color: var(--cyan);
}

.port {
    color: #aab6b0;
}

.ip {
    color: #c7d0cb;
}

.normal {
    color: var(--green);
}

.warning {
    color: var(--amber);
}

.danger {
    color: var(--red);
}

.neutral {
    color: var(--muted);
}

.pulse {
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--green);
    margin-right: 6px;
}

/* ----------------------------------------------------------
   TAGS
---------------------------------------------------------- */

.tag {
    display: inline-block;
    padding: 3px 6px;
    border: 1px solid var(--line);
    font-family: var(--mono);
    font-size: 8px;
    letter-spacing: .05em;
}

.tag-normal {
    color: var(--green);
    border-color: rgba(167,227,93,.25);
    background: rgba(167,227,93,.04);
}

.tag-warning {
    color: var(--amber);
    border-color: rgba(232,185,93,.25);
    background: rgba(232,185,93,.04);
}

.tag-danger {
    color: var(--red);
    border-color: rgba(228,111,97,.28);
    background: rgba(228,111,97,.04);
}

/* ----------------------------------------------------------
   ALERTS
---------------------------------------------------------- */

.alert {
    border-left: 2px solid;
    background: #0c1110;
    padding: 13px 14px;
    margin-bottom: 9px;
}

.alert-danger {
    border-color: var(--red);
}

.alert-warning {
    border-color: var(--amber);
}

.alert-info {
    border-color: var(--cyan);
}

.alert-title {
    font-family: var(--mono);
    font-size: 10px;
    color: #dce5df;
}

.alert-body {
    font-family: var(--mono);
    color: var(--muted);
    font-size: 9px;
    line-height: 1.6;
    margin-top: 5px;
}

.alert-time {
    font-family: var(--mono);
    color: var(--muted-2);
    font-size: 8px;
    margin-top: 7px;
}

/* ----------------------------------------------------------
   PREDICTION
---------------------------------------------------------- */

.prediction-result {
    border: 1px solid var(--line);
    padding: 25px;
    background:
        radial-gradient(
            circle at 90% 10%,
            rgba(167,227,93,.055),
            transparent 35%
        ),
        #0b100f;
}

.prediction-label {
    color: var(--muted-2);
    font-family: var(--mono);
    font-size: 8px;
    letter-spacing: .15em;
    text-transform: uppercase;
}

.prediction-class {
    color: var(--green);
    font-family: var(--mono);
    font-size: 31px;
    margin-top: 10px;
    letter-spacing: -.04em;
}

.confidence {
    height: 5px;
    background: #1d2522;
    margin-top: 18px;
    overflow: hidden;
}

.confidence-fill {
    height: 100%;
    background: var(--green);
}

.feature-row {
    display: flex;
    justify-content: space-between;
    padding: 9px 0;
    border-bottom: 1px solid #1a211f;
    font-family: var(--mono);
    font-size: 9px;
}

.feature-name {
    color: var(--muted);
}

.feature-value {
    color: #d9e1dc;
}

/* ----------------------------------------------------------
   TABLE
---------------------------------------------------------- */

div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
}

/* ----------------------------------------------------------
   BUTTONS
---------------------------------------------------------- */

.stButton > button {
    border-radius: 2px;
    border: 1px solid #35413c;
    background: #111715;
    color: #cfd8d2;
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: .04em;
    min-height: 38px;
}

.stButton > button:hover {
    border-color: var(--green-soft);
    color: var(--green);
    background: #151c19;
}

.stButton > button[kind="primary"] {
    background: #a7e35d;
    color: #091008;
    border-color: #a7e35d;
}

.stButton > button[kind="primary"]:hover {
    background: #b8ed70;
    color: #071006;
}

/* ----------------------------------------------------------
   INPUTS
---------------------------------------------------------- */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] {
    background: #0d1211 !important;
    border-color: var(--line) !important;
    border-radius: 2px !important;
}

input,
textarea {
    color: #dfe8e2 !important;
    font-family: var(--mono) !important;
    font-size: 10px !important;
}

label {
    color: var(--muted) !important;
    font-family: var(--mono) !important;
    font-size: 9px !important;
}

/* ----------------------------------------------------------
   SLIDER
---------------------------------------------------------- */

div[data-testid="stSlider"] {
    padding-top: 5px;
}

/* ----------------------------------------------------------
   SELECTBOX TEXT
---------------------------------------------------------- */

div[data-baseweb="select"] {
    font-family: var(--mono);
}

/* ----------------------------------------------------------
   FOOTER
---------------------------------------------------------- */

.footer {
    margin-top: 50px;
    padding-top: 15px;
    border-top: 1px solid var(--line-soft);
    display: flex;
    justify-content: space-between;
    font-family: var(--mono);
    font-size: 8px;
    color: var(--muted-2);
    letter-spacing: .08em;
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DATA GENERATION
# ============================================================

random.seed(st.session_state.traffic_seed)
np.random.seed(st.session_state.traffic_seed)

PROTOCOLS = ["TCP", "UDP", "HTTP", "HTTPS", "DNS", "SSH", "ICMP"]
SERVICES = ["web", "dns", "ssh", "mail", "database", "api", "unknown"]

NORMAL_DESTINATIONS = [
    "10.0.0.21",
    "10.0.0.42",
    "10.0.0.57",
    "172.16.0.8",
    "172.16.0.19",
    "192.168.1.12",
]

SUSPICIOUS_DESTINATIONS = [
    "185.220.101.17",
    "45.155.205.23",
    "103.72.144.81",
    "91.240.118.12",
]

ATTACK_TYPES = [
    "BENIGN",
    "DOS",
    "PORT_SCAN",
    "BRUTE_FORCE",
    "BOTNET",
    "INFILTRATION",
]

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_traffic(count=25):
    rows = []

    for i in range(count):
        attack_probability = random.random()

        if attack_probability < 0.12:
            attack = random.choice(
                ["DOS", "PORT_SCAN", "BRUTE_FORCE", "BOTNET"]
            )
            dst = random.choice(SUSPICIOUS_DESTINATIONS)
            status = "ANOMALOUS"
        elif attack_probability < 0.18:
            attack = "INFILTRATION"
            dst = random.choice(SUSPICIOUS_DESTINATIONS)
            status = "ANOMALOUS"
        else:
            attack = "BENIGN"
            dst = random.choice(NORMAL_DESTINATIONS)
            status = "NORMAL"

        protocol = random.choice(PROTOCOLS)

        if attack == "DOS":
            packets = random.randint(900, 8000)
            bytes_count = random.randint(500000, 8000000)
        elif attack == "PORT_SCAN":
            packets = random.randint(100, 900)
            bytes_count = random.randint(20000, 150000)
        elif attack == "BRUTE_FORCE":
            packets = random.randint(60, 500)
            bytes_count = random.randint(10000, 200000)
        else:
            packets = random.randint(5, 250)
            bytes_count = random.randint(1000, 300000)

        duration = round(random.uniform(0.01, 8.5), 3)

        rows.append(
            {
                "Time": (
                    datetime.now()
                    - timedelta(seconds=random.randint(0, 120))
                ).strftime("%H:%M:%S"),
                "Source": random_ip(),
                "Destination": dst,
                "Protocol": protocol,
                "Port": random.choice(
                    [22, 53, 80, 443, 25, 3306, 8080]
                ),
                "Packets": packets,
                "Bytes": bytes_count,
                "Duration": duration,
                "Classification": attack,
                "Status": status,
            }
        )

    return pd.DataFrame(rows)


traffic_df = generate_traffic(30)

# ============================================================
# HELPERS
# ============================================================

def page_header(kicker, title, description):
    st.markdown(
        f"""
        <div class="eyebrow">{kicker}</div>
        <div class="page-title">{title}</div>
        <div class="page-description">{description}</div>
        <div class="header-rule"></div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, footer="", variant=""):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value {variant}">{value}</div>
            <div class="metric-foot">{footer}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def panel_open(title, meta=""):
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">{title}</div>
            <div class="panel-meta">{meta}</div>
        """,
        unsafe_allow_html=True,
    )


def panel_close():
    st.markdown("</div>", unsafe_allow_html=True)


def classification_tag(value):
    if value == "BENIGN":
        return '<span class="tag tag-normal">BENIGN</span>'

    if value in ["DOS", "INFILTRATION"]:
        return '<span class="tag tag-danger">' + value + "</span>"

    return '<span class="tag tag-warning">' + value + "</span>"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">
                <div class="brand-symbol">◈</div>
                <div>
                    <div class="brand-name">NETRA</div>
                    <div class="brand-sub">NETWORK TRAFFIC ANALYZER</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nav-label">MONITORING CONSOLE</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "01  //  LIVE TRAFFIC",
        use_container_width=True,
    ):
        st.session_state.page = "Live Traffic"

    if st.button(
        "02  //  MODEL PREDICTION",
        use_container_width=True,
    ):
        st.session_state.page = "Model Prediction"

    if st.button(
        "03  //  ALERTS & STATS",
        use_container_width=True,
    ):
        st.session_state.page = "Alerts & Stats"

    st.markdown(
        """
        <div class="sidebar-status">
            <div class="status-line">
                <span class="status-key">ENGINE</span>
                <span class="status-value">
                    <span class="status-dot"></span>ONLINE
                </span>
            </div>

            <div class="status-line">
                <span class="status-key">CAPTURE</span>
                <span class="status-value">ACTIVE</span>
            </div>

            <div class="status-line">
                <span class="status-key">MODEL</span>
                <span class="status-value">READY</span>
            </div>

            <div class="status-line">
                <span class="status-key">LATENCY</span>
                <span class="status-value">18 ms</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="
            margin-top:22px;
            color:#53605b;
            font-family:'DM Mono',monospace;
            font-size:8px;
            line-height:1.7;
        ">
        NETRA / MINI PROJECT<br>
        ML-BASED NETWORK MONITORING<br>
        v0.1.0 — DEVELOPMENT BUILD
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE 1 — LIVE / SIMULATED TRAFFIC
# ============================================================

if st.session_state.page == "Live Traffic":

    page_header(
        "01 / TELEMETRY",
        "Live traffic feed",
        "A real-time network telemetry surface for inspecting packet flows, "
        "protocol behaviour and suspicious traffic patterns.",
    )

    # Top metrics
    total_packets = int(traffic_df["Packets"].sum())
    total_bytes = int(traffic_df["Bytes"].sum())
    anomalies = int((traffic_df["Status"] == "ANOMALOUS").sum())
    active_sources = traffic_df["Source"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "PACKETS / WINDOW",
            f"{total_packets:,}",
            "rolling simulated capture",
        )

    with c2:
        metric_card(
            "THROUGHPUT",
            f"{total_bytes / 1_000_000:.2f} MB",
            "observed traffic volume",
            "green",
        )

    with c3:
        metric_card(
            "ANOMALOUS FLOWS",
            str(anomalies).zfill(2),
            "requires inspection",
            "red" if anomalies > 4 else "amber",
        )

    with c4:
        metric_card(
            "ACTIVE SOURCES",
            str(active_sources).zfill(2),
            "unique source addresses",
        )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    left, right = st.columns([2.1, 1])

    with left:

        panel_open(
            "PACKET STREAM",
            "LIVE / SIMULATED CAPTURE • LATEST 30 FLOWS",
        )

        header = """
        <div class="feed-row feed-header">
            <div>TIME</div>
            <div>SOURCE</div>
            <div>DESTINATION</div>
            <div>PROTO</div>
            <div>PORT</div>
            <div>CLASS</div>
            <div>STATUS</div>
        </div>
        """

        html = header

        for _, row in traffic_df.sort_values(
            "Time",
            ascending=False
        ).iterrows():

            status_class = (
                "danger"
                if row["Status"] == "ANOMALOUS"
                else "normal"
            )

            html += f"""
            <div class="feed-row">
                <div class="neutral">{row['Time']}</div>
                <div class="ip">{row['Source']}</div>
                <div class="ip">{row['Destination']}</div>
                <div class="protocol">{row['Protocol']}</div>
                <div class="port">{row['Port']}</div>
                <div>{classification_tag(row['Classification'])}</div>
                <div class="{status_class}">
                    <span class="pulse"></span>{row['Status']}
                </div>
            </div>
            """

        st.markdown(html, unsafe_allow_html=True)
        panel_close()

    with right:

        panel_open(
            "TRAFFIC MIX",
            "PROTOCOL DISTRIBUTION",
        )

        protocol_counts = traffic_df["Protocol"].value_counts()

        chart_data = pd.DataFrame(
            {
                "Protocol": protocol_counts.index,
                "Flows": protocol_counts.values,
            }
        )

        st.bar_chart(
            chart_data.set_index("Protocol"),
            height=240,
        )

        panel_close()

        st.markdown(
            "<div style='height:14px'></div>",
            unsafe_allow_html=True,
        )

        panel_open(
            "CAPTURE CONTROL",
            "SIMULATION PARAMETERS",
        )

        if st.button(
            "↻  REGENERATE TRAFFIC",
            use_container_width=True,
        ):
            st.session_state.traffic_seed += 1
            st.rerun()

        st.markdown(
            "<div style='height:8px'></div>",
            unsafe_allow_html=True,
        )

        refresh = st.slider(
            "SIMULATION INTENSITY",
            min_value=1,
            max_value=10,
            value=5,
        )

        st.markdown(
            f"""
            <div style="
                margin-top:10px;
                font-family:'DM Mono',monospace;
                font-size:8px;
                color:#53605b;
                line-height:1.8;
            ">
                CAPTURE MODE: SIMULATED<br>
                PACKET RATE: {refresh * 20} pkt/s<br>
                INTERFACE: eth0 / virtual<br>
                BUFFER: 64 MB
            </div>
            """,
            unsafe_allow_html=True,
        )

        panel_close()

    # Flow analysis
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    panel_open(
        "FLOW VOLUME",
        "PACKET COUNT BY TRAFFIC CLASS",
    )

    flow_chart = (
        traffic_df.groupby("Classification")["Packets"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        flow_chart,
        height=240,
    )

    panel_close()


# ============================================================
# PAGE 2 — MODEL PREDICTION
# ============================================================

elif st.session_state.page == "Model Prediction":

    page_header(
        "02 / INFERENCE",
        "Model prediction panel",
        "Inspect a network flow and estimate whether its feature profile "
        "resembles benign or anomalous traffic.",
    )

    left, right = st.columns([1.05, 1])

    with left:

        panel_open(
            "FLOW FEATURE VECTOR",
            "INPUT FEATURES / MODEL READY",
        )

        duration = st.number_input(
            "FLOW DURATION (seconds)",
            min_value=0.001,
            max_value=1000.0,
            value=2.84,
            step=0.01,
        )

        packet_count = st.number_input(
            "PACKET COUNT",
            min_value=1,
            max_value=100000,
            value=186,
            step=1,
        )

        byte_count = st.number_input(
            "BYTE COUNT",
            min_value=1,
            max_value=100000000,
            value=142500,
            step=100,
        )

        source_port = st.number_input(
            "SOURCE PORT",
            min_value=1,
            max_value=65535,
            value=49152,
        )

        destination_port = st.selectbox(
            "DESTINATION PORT",
            [22, 25, 53, 80, 443, 3306, 8080],
            index=4,
        )

        protocol = st.selectbox(
            "PROTOCOL",
            ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "DNS", "SSH"],
        )

        packet_rate = st.number_input(
            "PACKETS / SECOND",
            min_value=0.1,
            max_value=100000.0,
            value=65.5,
            step=0.1,
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        predict = st.button(
            "RUN TRAFFIC CLASSIFICATION  →",
            type="primary",
            use_container_width=True,
        )

        panel_close()

    with right:

        if predict:

            # ------------------------------------------------
            # Demo inference logic
            # Replace this block with the actual ML model.
            # ------------------------------------------------

            anomaly_score = 0.08

            if packet_rate > 500:
                anomaly_score += 0.35

            if packet_count > 1500:
                anomaly_score += 0.22

            if byte_count > 1_000_000:
                anomaly_score += 0.18

            if destination_port in [22, 23, 3389]:
                anomaly_score += 0.10

            if protocol == "ICMP" and packet_rate > 200:
                anomaly_score += 0.18

            anomaly_score = min(anomaly_score, 0.99)

            if anomaly_score >= 0.70:
                prediction = "ANOMALOUS"
                confidence = anomaly_score
                level = "HIGH"
            elif anomaly_score >= 0.40:
                prediction = "SUSPICIOUS"
                confidence = anomaly_score
                level = "MEDIUM"
            else:
                prediction = "BENIGN"
                confidence = 1 - anomaly_score
                level = "LOW"

            st.session_state.prediction_history.append(
                {
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "prediction": prediction,
                    "confidence": confidence,
                }
            )

        else:
            prediction = "WAITING"
            confidence = 0
            level = "—"

        panel_open(
            "INFERENCE RESULT",
            "ML CLASSIFICATION OUTPUT",
        )

        if prediction == "WAITING":

            st.markdown(
                """
                <div class="prediction-result">
                    <div class="prediction-label">
                        SYSTEM STATE
                    </div>

                    <div class="prediction-class"
                         style="color:#53605b;">
                        AWAITING INPUT
                    </div>

                    <div style="
                        color:#53605b;
                        font-family:'DM Mono',monospace;
                        font-size:9px;
                        line-height:1.7;
                        margin-top:12px;
                    ">
                        Provide a network flow feature vector
                        and execute classification.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            color = (
                "#a7e35d"
                if prediction == "BENIGN"
                else "#e8b95d"
                if prediction == "SUSPICIOUS"
                else "#e46f61"
            )

            st.markdown(
                f"""
                <div class="prediction-result">

                    <div class="prediction-label">
                        PREDICTED CLASS
                    </div>

                    <div class="prediction-class"
                         style="color:{color};">
                        {prediction}
                    </div>

                    <div style="
                        margin-top:8px;
                        font-family:'DM Mono',monospace;
                        font-size:9px;
                        color:#7e8b85;
                    ">
                        CONFIDENCE / {confidence * 100:.1f}%
                    </div>

                    <div class="confidence">
                        <div
                            class="confidence-fill"
                            style="
                                width:{confidence * 100:.1f}%;
                                background:{color};
                            ">
                        </div>
                    </div>

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        margin-top:12px;
                        font-family:'DM Mono',monospace;
                        font-size:8px;
                        color:#53605b;
                    ">
                        <span>RISK LEVEL</span>
                        <span style="color:{color}">
                            {level}
                        </span>
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        panel_close()

        st.markdown(
            "<div style='height:14px'></div>",
            unsafe_allow_html=True,
        )

        panel_open(
            "FEATURE SNAPSHOT",
            "VALUES PASSED TO CLASSIFIER",
        )

        feature_values = [
            ("duration", f"{duration:.3f} s"),
            ("packet_count", f"{packet_count:,}"),
            ("byte_count", f"{byte_count:,}"),
            ("src_port", str(source_port)),
            ("dst_port", str(destination_port)),
            ("protocol", protocol),
            ("packet_rate", f"{packet_rate:.2f} pkt/s"),
        ]

        feature_html = ""

        for name, value in feature_values:
            feature_html += f"""
            <div class="feature-row">
                <span class="feature-name">{name}</span>
                <span class="feature-value">{value}</span>
            </div>
            """

        st.markdown(feature_html, unsafe_allow_html=True)
        panel_close()

    # Model information
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    a, b, c = st.columns(3)

    with a:
        metric_card(
            "MODEL",
            "RF-01",
            "Random Forest / replaceable",
        )

    with b:
        metric_card(
            "FEATURES",
            "07",
            "flow-level feature vector",
        )

    with c:
        metric_card(
            "INFERENCE",
            "< 20 ms",
            "target response latency",
            "green",
        )

    # Prediction history
    if st.session_state.prediction_history:

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        panel_open(
            "RECENT INFERENCE",
            "SESSION PREDICTION HISTORY",
        )

        history_df = pd.DataFrame(
            st.session_state.prediction_history[-10:]
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        panel_close()


# ============================================================
# PAGE 3 — ALERTS & STATS
# ============================================================

elif st.session_state.page == "Alerts & Stats":

    page_header(
        "03 / INCIDENT VIEW",
        "Alerts & statistics",
        "Condensed operational view of detected anomalies, attack classes, "
        "traffic volume and network behaviour.",
    )

    anomaly_df = traffic_df[
        traffic_df["Status"] == "ANOMALOUS"
    ].copy()

    total_flows = len(traffic_df)
    anomaly_count = len(anomaly_df)
    benign_count = total_flows - anomaly_count

    anomaly_rate = (
        anomaly_count / total_flows * 100
        if total_flows
        else 0
    )

    highest_risk = (
        anomaly_df["Classification"].value_counts().idxmax()
        if not anomaly_df.empty
        else "NONE"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "TOTAL FLOWS",
            f"{total_flows:,}",
            "current observation window",
        )

    with c2:
        metric_card(
            "BENIGN",
            f"{benign_count:,}",
            f"{100 - anomaly_rate:.1f}% of observed flows",
            "green",
        )

    with c3:
        metric_card(
            "ANOMALY RATE",
            f"{anomaly_rate:.1f}%",
            "traffic requiring inspection",
            "red" if anomaly_rate > 15 else "amber",
        )

    with c4:
        metric_card(
            "TOP THREAT",
            highest_risk,
            "dominant anomaly class",
            "red",
        )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 1])

    with left:

        panel_open(
            "ACTIVE ALERTS",
            f"{len(anomaly_df)} DETECTIONS IN CURRENT WINDOW",
        )

        if anomaly_df.empty:

            st.markdown(
                """
                <div class="alert alert-info">
                    <div class="alert-title">
                        NO ACTIVE ANOMALIES
                    </div>
                    <div class="alert-body">
                        Current traffic window does not contain
                        significant deviations from the observed
                        baseline.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            for _, alert in anomaly_df.head(8).iterrows():

                if alert["Classification"] in [
                    "DOS",
                    "INFILTRATION",
                ]:
                    alert_type = "alert-danger"
                    severity = "HIGH"
                else:
                    alert_type = "alert-warning"
                    severity = "MEDIUM"

                st.markdown(
                    f"""
                    <div class="alert {alert_type}">
                        <div class="alert-title">
                            {severity}
                            &nbsp; // &nbsp;
                            {alert['Classification']}
                        </div>

                        <div class="alert-body">
                            Source {alert['Source']}
                            generated anomalous
                            {alert['Protocol']} traffic toward
                            {alert['Destination']}:{alert['Port']}.
                            Observed {alert['Packets']:,} packets.
                        </div>

                        <div class="alert-time">
                            DETECTED {alert['Time']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        panel_close()

    with right:

        panel_open(
            "ATTACK DISTRIBUTION",
            "CLASSIFICATION FREQUENCY",
        )

        attack_counts = traffic_df[
            traffic_df["Classification"] != "BENIGN"
        ]["Classification"].value_counts()

        if not attack_counts.empty:

            st.bar_chart(
                attack_counts,
                height=250,
            )

        else:

            st.markdown(
                """
                <div style="
                    padding:50px 10px;
                    text-align:center;
                    color:#53605b;
                    font-family:'DM Mono',monospace;
                    font-size:9px;
                ">
                    NO ATTACK CLASSES OBSERVED
                </div>
                """,
                unsafe_allow_html=True,
            )

        panel_close()

    # --------------------------------------------------------
    # Traffic statistics
    # --------------------------------------------------------

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:

        panel_open(
            "BYTE VOLUME",
            "TOTAL BY PROTOCOL",
        )

        bytes_protocol = (
            traffic_df
            .groupby("Protocol")["Bytes"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            bytes_protocol,
            height=250,
        )

        panel_close()

    with right:

        panel_open(
            "PACKET DISTRIBUTION",
            "TRAFFIC CLASS VS PACKET COUNT",
        )

        packet_class = (
            traffic_df
            .groupby("Classification")["Packets"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            packet_class,
            height=250,
        )

        panel_close()

    # --------------------------------------------------------
    # Source investigation
    # --------------------------------------------------------

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    panel_open(
        "SOURCE INVESTIGATION",
        "TOP SOURCES BY OBSERVED PACKETS",
    )

    source_stats = (
        traffic_df
        .groupby("Source")
        .agg(
            Flows=("Source", "count"),
            Packets=("Packets", "sum"),
            Bytes=("Bytes", "sum"),
        )
        .sort_values(
            "Packets",
            ascending=False,
        )
        .head(10)
        .reset_index()
    )

    st.dataframe(
        source_stats,
        use_container_width=True,
        hide_index=True,
    )

    panel_close()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <span>NETRA // NETWORK TRAFFIC ANALYZER</span>
        <span>ML-BASED ANOMALY DETECTION</span>
        <span>SYSTEM ONLINE</span>
    </div>
    """,
    unsafe_allow_html=True,
)
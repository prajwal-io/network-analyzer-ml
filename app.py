import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta

# ============================================================
# FLOWSENSE
# Network Traffic Intelligence & Anomaly Detection
# ============================================================

st.set_page_config(
    page_title="FlowSense",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE
# ============================================================

if "traffic_seed" not in st.session_state:
    st.session_state.traffic_seed = 100

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap'
    );

    :root {
        --bg: #080b0a;
        --panel: #0d1210;
        --panel-2: #111714;
        --border: #27312d;

        --text: #e8eee9;
        --muted: #7c8983;
        --dim: #4e5954;

        --green: #b0df63;
        --green-dark: #759c43;

        --amber: #dfb65e;
        --red: #dd6d5d;
        --cyan: #72c3bd;
    }

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    html,
    body,
    [class*="css"] {
        font-family: "Space Grotesk", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(140, 170, 100, 0.065),
                transparent 27%
            ),
            radial-gradient(
                circle at 5% 100%,
                rgba(60, 105, 95, 0.045),
                transparent 28%
            ),
            var(--bg);

        color: var(--text);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.018;

        background-image:
            linear-gradient(
                rgba(255,255,255,0.8) 1px,
                transparent 1px
            ),
            linear-gradient(
                90deg,
                rgba(255,255,255,0.8) 1px,
                transparent 1px
            );

        background-size: 48px 48px;
        z-index: 0;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: #090d0c;
        border-right: 1px solid #1b2421;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.4rem 1rem;
    }

    .brand-block {
        padding: 0.4rem 0.3rem 1.6rem;
    }

    .brand-symbol {
        color: var(--green);
        font-family: "DM Mono", monospace;
        font-size: 22px;
        line-height: 1;
        margin-bottom: 8px;
    }

    .brand-name {
        color: #eef3ef;
        font-family: "DM Mono", monospace;
        font-size: 18px;
        letter-spacing: 0.14em;
        font-weight: 500;
    }

    .brand-subtitle {
        color: var(--dim);
        font-family: "DM Mono", monospace;
        font-size: 7px;
        letter-spacing: 0.13em;
        line-height: 1.7;
        margin-top: 7px;
    }

    .sidebar-caption {
        color: #4c5752;
        font-family: "DM Mono", monospace;
        font-size: 8px;
        letter-spacing: 0.18em;
        margin: 15px 4px 8px;
    }

    /* Native Streamlit radio */
    div[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 3px;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 7px 5px;
        border-radius: 2px;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: #101613;
    }

    div[data-testid="stSidebar"] div[role="radiogroup"] p {
        font-family: "DM Mono", monospace !important;
        font-size: 10px !important;
        color: #a1aca6 !important;
    }

    .sidebar-footer {
        margin-top: 28px;
        color: #414b47;
        font-family: "DM Mono", monospace;
        font-size: 7px;
        line-height: 1.9;
        letter-spacing: 0.04em;
    }

    /* --------------------------------------------------------
       PAGE HEADER
    -------------------------------------------------------- */

    .eyebrow {
        color: var(--green);
        font-family: "DM Mono", monospace;
        font-size: 8px;
        letter-spacing: 0.22em;
        margin-bottom: 7px;
    }

    .page-title {
        color: #eef4ef;
        font-size: 35px;
        font-weight: 600;
        line-height: 1.05;
        letter-spacing: -0.045em;
        margin-bottom: 9px;
    }

    .page-description {
        color: var(--muted);
        font-family: "DM Mono", monospace;
        font-size: 9px;
        line-height: 1.75;
        max-width: 820px;
    }

    .header-line {
        height: 1px;
        margin: 23px 0 24px;

        background:
            linear-gradient(
                90deg,
                var(--green-dark),
                var(--border),
                transparent
            );
    }

    /* --------------------------------------------------------
       METRICS
    -------------------------------------------------------- */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.018),
                rgba(255,255,255,0)
            ),
            #0c1110;

        border: 1px solid var(--border);
        padding: 15px 17px;
        min-height: 110px;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--dim) !important;
        font-family: "DM Mono", monospace !important;
        font-size: 8px !important;
        letter-spacing: 0.11em;
    }

    div[data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-family: "DM Mono", monospace !important;
        font-size: 25px !important;
        letter-spacing: -0.04em;
    }

    div[data-testid="stMetricDelta"] {
        font-family: "DM Mono", monospace !important;
        font-size: 8px !important;
    }

    /* --------------------------------------------------------
       SECTION LABELS
    -------------------------------------------------------- */

    .section-title {
        color: #abb6b0;
        font-family: "DM Mono", monospace;
        font-size: 9px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: var(--dim);
        font-family: "DM Mono", monospace;
        font-size: 7px;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
    }

    /* --------------------------------------------------------
       STATUS BAR
    -------------------------------------------------------- */

    .native-status {
        border: 1px solid var(--border);
        background: #0c1110;
        padding: 12px 14px;
        margin-top: 20px;
    }

    .native-status-title {
        color: #aab5af;
        font-family: "DM Mono", monospace;
        font-size: 8px;
        letter-spacing: 0.12em;
        margin-bottom: 10px;
    }

    /* --------------------------------------------------------
       ALERT BOXES
    -------------------------------------------------------- */

    .alert-high {
        border-left: 2px solid var(--red);
        background: rgba(221,109,93,0.035);
        padding: 11px 13px;
        margin-bottom: 8px;
    }

    .alert-medium {
        border-left: 2px solid var(--amber);
        background: rgba(223,182,94,0.035);
        padding: 11px 13px;
        margin-bottom: 8px;
    }

    .alert-title {
        font-family: "DM Mono", monospace;
        font-size: 9px;
        color: #dce4de;
    }

    .alert-description {
        color: var(--muted);
        font-family: "DM Mono", monospace;
        font-size: 8px;
        line-height: 1.65;
        margin-top: 5px;
    }

    .alert-meta {
        color: var(--dim);
        font-family: "DM Mono", monospace;
        font-size: 7px;
        margin-top: 6px;
    }

    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        background: #101613;
        border: 1px solid #344039;
        border-radius: 2px;
        color: #cad4ce;
        font-family: "DM Mono", monospace;
        font-size: 9px;
        min-height: 38px;
        letter-spacing: 0.04em;
    }

    .stButton > button:hover {
        background: #151d19;
        border-color: var(--green-dark);
        color: var(--green);
    }

    /* --------------------------------------------------------
       INPUTS
    -------------------------------------------------------- */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background: #0c110f !important;
        border-color: var(--border) !important;
        border-radius: 2px !important;
    }

    input {
        color: var(--text) !important;
        font-family: "DM Mono", monospace !important;
        font-size: 10px !important;
    }

    label {
        color: var(--muted) !important;
        font-family: "DM Mono", monospace !important;
        font-size: 8px !important;
    }

    /* --------------------------------------------------------
       TABLES
    -------------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
    }

    /* --------------------------------------------------------
       INFO / SUCCESS / WARNING / ERROR
    -------------------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 2px;
        font-family: "DM Mono", monospace;
        font-size: 9px;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .app-footer {
        margin-top: 42px;
        border-top: 1px solid #1a211f;
        padding-top: 13px;

        display: flex;
        justify-content: space-between;

        color: #414b47;
        font-family: "DM Mono", monospace;
        font-size: 7px;
        letter-spacing: 0.08em;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# REALISTIC NETWORK DATA
# ============================================================

PROTOCOL_CONFIG = {
    "HTTP": {
        "ports": [80],
        "weight": 15,
    },
    "HTTPS": {
        "ports": [443],
        "weight": 30,
    },
    "DNS": {
        "ports": [53],
        "weight": 12,
    },
    "SSH": {
        "ports": [22],
        "weight": 7,
    },
    "SMTP": {
        "ports": [25],
        "weight": 4,
    },
    "MYSQL": {
        "ports": [3306],
        "weight": 3,
    },
    "TCP": {
        "ports": [8080, 8443, 9000],
        "weight": 15,
    },
    "UDP": {
        "ports": [123, 500, 4500],
        "weight": 8,
    },
    "ICMP": {
        "ports": [0],
        "weight": 6,
    },
}

INTERNAL_DESTINATIONS = [
    "10.0.0.12",
    "10.0.0.21",
    "10.0.0.42",
    "10.0.0.57",
    "10.0.0.64",
    "10.0.0.91",
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
    "DOS",
    "PORT_SCAN",
    "BRUTE_FORCE",
    "BOTNET",
    "INFILTRATION",
]


def random_ip():
    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )


def choose_protocol():
    names = list(PROTOCOL_CONFIG.keys())
    weights = [
        PROTOCOL_CONFIG[x]["weight"]
        for x in names
    ]

    return random.choices(
        names,
        weights=weights,
        k=1,
    )[0]


def generate_traffic(count=42):

    random.seed(st.session_state.traffic_seed)

    rows = []

    for _ in range(count):

        is_attack = random.random() < 0.16

        if is_attack:

            attack = random.choice(
                ATTACK_TYPES
            )

            source = random_ip()

            destination = random.choice(
                SUSPICIOUS_DESTINATIONS
            )

            if attack == "DOS":

                protocol = random.choice(
                    ["TCP", "UDP", "ICMP"]
                )

                port = random.choice(
                    [80, 443, 53, 0]
                )

                packets = random.randint(
                    2500,
                    12000,
                )

                duration = random.uniform(
                    0.1,
                    4.0,
                )

                packet_rate = (
                    packets / duration
                )

                byte_count = random.randint(
                    800_000,
                    9_000_000,
                )

            elif attack == "PORT_SCAN":

                protocol = "TCP"

                port = random.randint(
                    1,
                    65535,
                )

                packets = random.randint(
                    100,
                    900,
                )

                duration = random.uniform(
                    0.05,
                    3.0,
                )

                packet_rate = (
                    packets / duration
                )

                byte_count = random.randint(
                    10_000,
                    150_000,
                )

            elif attack == "BRUTE_FORCE":

                protocol = "SSH"

                port = 22

                packets = random.randint(
                    300,
                    1500,
                )

                duration = random.uniform(
                    2,
                    15,
                )

                packet_rate = (
                    packets / duration
                )

                byte_count = random.randint(
                    40_000,
                    450_000,
                )

            elif attack == "BOTNET":

                protocol = random.choice(
                    ["TCP", "UDP", "DNS"]
                )

                port = random.choice(
                    [53, 8080, 8443]
                )

                packets = random.randint(
                    700,
                    3000,
                )

                duration = random.uniform(
                    1,
                    10,
                )

                packet_rate = (
                    packets / duration
                )

                byte_count = random.randint(
                    100_000,
                    1_500_000,
                )

            else:

                protocol = random.choice(
                    ["TCP", "HTTPS", "DNS"]
                )

                port = (
                    443
                    if protocol == "HTTPS"
                    else 53
                    if protocol == "DNS"
                    else 8080
                )

                packets = random.randint(
                    500,
                    2200,
                )

                duration = random.uniform(
                    1,
                    12,
                )

                packet_rate = (
                    packets / duration
                )

                byte_count = random.randint(
                    150_000,
                    2_000_000,
                )

            classification = attack
            status = "ANOMALOUS"

        else:

            protocol = choose_protocol()

            port = random.choice(
                PROTOCOL_CONFIG[protocol]["ports"]
            )

            source = random_ip()

            destination = random.choice(
                INTERNAL_DESTINATIONS
            )

            packets = random.randint(
                8,
                280,
            )

            duration = random.uniform(
                0.2,
                15,
            )

            packet_rate = (
                packets / duration
            )

            byte_count = random.randint(
                2_000,
                350_000,
            )

            classification = "BENIGN"
            status = "NORMAL"

        rows.append(
            {
                "Time": (
                    datetime.now()
                    - timedelta(
                        seconds=random.randint(
                            0,
                            180,
                        )
                    )
                ).strftime("%H:%M:%S"),

                "Source": source,

                "Destination": destination,

                "Protocol": protocol,

                "Port": port,

                "Packets": packets,

                "Bytes": byte_count,

                "Duration": round(
                    duration,
                    3,
                ),

                "Packet Rate": round(
                    packet_rate,
                    2,
                ),

                "Classification": classification,

                "Status": status,
            }
        )

    return pd.DataFrame(rows)


traffic = generate_traffic()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-block">
            <div class="brand-symbol">◈</div>
            <div class="brand-name">FLOWSENSE</div>

            <div class="brand-subtitle">
                NETWORK TRAFFIC INTELLIGENCE<br>
                & ANOMALY DETECTION
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-caption">MONITORING CONSOLE</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "01  /  Live Traffic",
            "02  /  Model Prediction",
            "03  /  Alerts & Stats",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-caption">SYSTEM STATUS</div>',
        unsafe_allow_html=True,
    )

    # IMPORTANT:
    # These are native Streamlit components.
    # No HTML status block is used here.

    s1, s2 = st.columns(
        [1, 2]
    )

    with s1:
        st.caption("ENGINE")

    with s2:
        st.success(
            "ONLINE",
            icon="●",
        )

    s1, s2 = st.columns(
        [1, 2]
    )

    with s1:
        st.caption("CAPTURE")

    with s2:
        st.success(
            "ACTIVE",
            icon="●",
        )

    s1, s2 = st.columns(
        [1, 2]
    )

    with s1:
        st.caption("MODEL")

    with s2:
        st.success(
            "READY",
            icon="●",
        )

    s1, s2 = st.columns(
        [1, 2]
    )

    with s1:
        st.caption("LATENCY")

    with s2:
        st.caption("18 ms")

    st.markdown(
        """
        <div class="sidebar-footer">
            FLOWSENSE / DEVELOPMENT BUILD<br>
            ML NETWORK MONITORING<br>
            VERSION 0.2.0
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PAGE 1 — LIVE TRAFFIC
# ============================================================

if page == "01  /  Live Traffic":

    st.markdown(
        '<div class="eyebrow">01 / TELEMETRY</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Live traffic feed</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-description">
            Real-time network telemetry for observing packet flows,
            protocol behaviour, traffic volume and anomalous activity.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="header-line"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    total_packets = int(
        traffic["Packets"].sum()
    )

    total_bytes = int(
        traffic["Bytes"].sum()
    )

    anomalies = int(
        (
            traffic["Status"]
            == "ANOMALOUS"
        ).sum()
    )

    active_sources = traffic[
        "Source"
    ].nunique()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "PACKETS / WINDOW",
            f"{total_packets:,}",
            "Current capture",
        )

    with c2:
        st.metric(
            "TRAFFIC VOLUME",
            f"{total_bytes / 1_000_000:.2f} MB",
            "Observed volume",
        )

    with c3:
        st.metric(
            "ANOMALOUS FLOWS",
            f"{anomalies:02d}",
            "Requires inspection",
        )

    with c4:
        st.metric(
            "ACTIVE SOURCES",
            f"{active_sources:02d}",
            "Unique addresses",
        )

    st.write("")

    # --------------------------------------------------------
    # MAIN TELEMETRY
    # --------------------------------------------------------

    left, right = st.columns(
        [2.15, 1],
        gap="large",
    )

    with left:

        st.markdown(
            '<div class="section-title">PACKET STREAM</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">LATEST OBSERVED NETWORK FLOWS</div>',
            unsafe_allow_html=True,
        )

        table = traffic[
            [
                "Time",
                "Source",
                "Destination",
                "Protocol",
                "Port",
                "Packets",
                "Classification",
                "Status",
            ]
        ].sort_values(
            "Time",
            ascending=False,
        )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            height=560,
            column_config={
                "Time": st.column_config.TextColumn(
                    "TIME",
                    width="small",
                ),
                "Source": st.column_config.TextColumn(
                    "SOURCE",
                    width="medium",
                ),
                "Destination": st.column_config.TextColumn(
                    "DESTINATION",
                    width="medium",
                ),
                "Protocol": st.column_config.TextColumn(
                    "PROTO",
                    width="small",
                ),
                "Port": st.column_config.NumberColumn(
                    "PORT",
                    width="small",
                ),
                "Packets": st.column_config.NumberColumn(
                    "PACKETS",
                    format="%d",
                ),
                "Classification": st.column_config.TextColumn(
                    "CLASS",
                    width="medium",
                ),
                "Status": st.column_config.TextColumn(
                    "STATUS",
                    width="small",
                ),
            },
        )

    # --------------------------------------------------------
    # RIGHT PANEL
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">PROTOCOL MIX</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">FLOW DISTRIBUTION</div>',
            unsafe_allow_html=True,
        )

        protocol_counts = (
            traffic["Protocol"]
            .value_counts()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            protocol_counts,
            height=245,
        )

        st.write("")

        st.markdown(
            '<div class="section-title">CAPTURE CONTROL</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">SIMULATED TELEMETRY ENGINE</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "↻  GENERATE NEW TRAFFIC",
            use_container_width=True,
        ):

            st.session_state.traffic_seed += 1

            st.rerun()

        intensity = st.slider(
            "SIMULATION INTENSITY",
            min_value=1,
            max_value=10,
            value=5,
        )

        st.caption(
            f"PACKET RATE  /  {intensity * 20} pkt/s"
        )

        st.caption(
            "INTERFACE  /  eth0"
        )

        st.caption(
            "CAPTURE MODE  /  SIMULATED"
        )

        st.caption(
            "BUFFER  /  64 MB"
        )

    # --------------------------------------------------------
    # NETWORK ACTIVITY
    # --------------------------------------------------------

    st.write("")

    st.markdown(
        '<div class="section-title">NETWORK ACTIVITY</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">PACKETS BY TRAFFIC CLASS</div>',
        unsafe_allow_html=True,
    )

    flow_volume = (
        traffic
        .groupby("Classification")["Packets"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        flow_volume,
        height=250,
    )

    # --------------------------------------------------------
    # SECONDARY NETWORK TELEMETRY
    # --------------------------------------------------------

    st.write("")

    left2, right2 = st.columns(2)

    with left2:

        st.markdown(
            '<div class="section-title">TOP DESTINATIONS</div>',
            unsafe_allow_html=True,
        )

        destination_stats = (
            traffic
            .groupby("Destination")
            .agg(
                Flows=("Destination", "count"),
                Packets=("Packets", "sum"),
            )
            .sort_values(
                "Packets",
                ascending=False,
            )
            .head(7)
        )

        st.dataframe(
            destination_stats,
            use_container_width=True,
        )

    with right2:

        st.markdown(
            '<div class="section-title">TRAFFIC RATE</div>',
            unsafe_allow_html=True,
        )

        st.line_chart(
            traffic[
                ["Packet Rate"]
            ].reset_index(
                drop=True
            ),
            height=230,
        )

# ============================================================
# PAGE 2 — MODEL PREDICTION
# ============================================================

elif page == "02  /  Model Prediction":

    st.markdown(
        '<div class="eyebrow">02 / INFERENCE</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Model prediction</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-description">
            Submit a network-flow feature vector and estimate whether
            the observed behaviour is benign, suspicious or anomalous.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="header-line"></div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1, 1],
        gap="large",
    )

    with left:

        st.markdown(
            '<div class="section-title">FLOW FEATURE VECTOR</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">MODEL INPUT FEATURES</div>',
            unsafe_allow_html=True,
        )

        duration = st.number_input(
            "FLOW DURATION (SECONDS)",
            min_value=0.001,
            max_value=10000.0,
            value=2.84,
            step=0.01,
        )

        packet_count = st.number_input(
            "PACKET COUNT",
            min_value=1,
            max_value=1_000_000,
            value=186,
            step=1,
        )

        byte_count = st.number_input(
            "BYTE COUNT",
            min_value=1,
            max_value=100_000_000,
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
            [
                22,
                25,
                53,
                80,
                443,
                3306,
                8080,
                8443,
            ],
        )

        protocol = st.selectbox(
            "PROTOCOL",
            [
                "TCP",
                "UDP",
                "ICMP",
                "HTTP",
                "HTTPS",
                "DNS",
                "SSH",
            ],
        )

        packet_rate = st.number_input(
            "PACKETS / SECOND",
            min_value=0.1,
            max_value=100000.0,
            value=65.5,
            step=0.1,
        )

        st.write("")

        predict = st.button(
            "RUN TRAFFIC CLASSIFICATION  →",
            use_container_width=True,
        )

    with right:

        st.markdown(
            '<div class="section-title">INFERENCE RESULT</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">MODEL CLASSIFICATION OUTPUT</div>',
            unsafe_allow_html=True,
        )

        if predict:

            anomaly_score = 0.04

            # Demo scoring logic.
            # Replace this with the real trained model later.

            if packet_rate > 500:
                anomaly_score += 0.35

            if packet_count > 1500:
                anomaly_score += 0.25

            if byte_count > 1_000_000:
                anomaly_score += 0.20

            if destination_port in [
                22,
                23,
                3389,
            ]:
                anomaly_score += 0.08

            if (
                protocol == "ICMP"
                and packet_rate > 200
            ):
                anomaly_score += 0.18

            anomaly_score = min(
                anomaly_score,
                0.99,
            )

            if anomaly_score >= 0.70:

                prediction = "ANOMALOUS"
                confidence = anomaly_score
                risk = "HIGH"

            elif anomaly_score >= 0.40:

                prediction = "SUSPICIOUS"
                confidence = anomaly_score
                risk = "MEDIUM"

            else:

                prediction = "BENIGN"
                confidence = (
                    1 - anomaly_score
                )
                risk = "LOW"

            st.session_state.prediction_history.append(
                {
                    "Time": datetime.now().strftime(
                        "%H:%M:%S"
                    ),
                    "Prediction": prediction,
                    "Confidence": round(
                        confidence * 100,
                        2,
                    ),
                    "Risk": risk,
                }
            )

        else:

            prediction = "WAITING"
            confidence = 0
            risk = "—"

        if prediction == "WAITING":

            st.info(
                "Awaiting network flow feature vector."
            )

        elif prediction == "BENIGN":

            st.success(
                f"BENIGN  •  "
                f"{confidence * 100:.1f}% confidence"
            )

        elif prediction == "SUSPICIOUS":

            st.warning(
                f"SUSPICIOUS  •  "
                f"{confidence * 100:.1f}% confidence"
            )

        else:

            st.error(
                f"ANOMALOUS  •  "
                f"{confidence * 100:.1f}% confidence"
            )

        if prediction != "WAITING":

            st.progress(
                int(confidence * 100)
            )

            st.caption(
                f"RISK LEVEL  /  {risk}"
            )

        st.write("")

        st.markdown(
            '<div class="section-title">FEATURE SNAPSHOT</div>',
            unsafe_allow_html=True,
        )

        feature_table = pd.DataFrame(
            {
                "Feature": [
                    "duration",
                    "packet_count",
                    "byte_count",
                    "source_port",
                    "destination_port",
                    "protocol",
                    "packet_rate",
                ],
                "Value": [
                    f"{duration:.3f} sec",
                    f"{packet_count:,}",
                    f"{byte_count:,}",
                    str(source_port),
                    str(destination_port),
                    protocol,
                    f"{packet_rate:.2f} pkt/s",
                ],
            }
        )

        st.dataframe(
            feature_table,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # MODEL SUMMARY
    # --------------------------------------------------------

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "MODEL",
            "RF-01",
            "Random Forest",
        )

    with c2:
        st.metric(
            "FEATURES",
            "07",
            "flow-level vector",
        )

    with c3:
        st.metric(
            "CLASSES",
            "05",
            "traffic categories",
        )

    with c4:
        st.metric(
            "TARGET LATENCY",
            "<20 ms",
            "inference",
        )

    # --------------------------------------------------------
    # WHY THE MODEL FLAGGED IT
    # --------------------------------------------------------

    if predict:

        st.write("")

        st.markdown(
            '<div class="section-title">BEHAVIOUR SIGNALS</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">FEATURE CONTRIBUTION VIEW</div>',
            unsafe_allow_html=True,
        )

        feature_scores = pd.DataFrame(
            {
                "Feature": [
                    "Packet rate",
                    "Packet count",
                    "Byte volume",
                    "Destination port",
                    "Protocol",
                    "Duration",
                ],
                "Signal": [
                    min(
                        packet_rate / 1000,
                        1.0,
                    ),
                    min(
                        packet_count / 3000,
                        1.0,
                    ),
                    min(
                        byte_count / 5_000_000,
                        1.0,
                    ),
                    (
                        0.85
                        if destination_port
                        in [22, 23, 3389]
                        else 0.18
                    ),
                    (
                        0.75
                        if protocol == "ICMP"
                        else 0.25
                    ),
                    min(
                        duration / 20,
                        1.0,
                    ),
                ],
            }
        ).set_index("Feature")

        st.bar_chart(
            feature_scores,
            height=260,
        )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    if st.session_state.prediction_history:

        st.write("")

        st.markdown(
            '<div class="section-title">RECENT INFERENCE</div>',
            unsafe_allow_html=True,
        )

        history_df = pd.DataFrame(
            st.session_state.prediction_history[-10:]
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

# ============================================================
# PAGE 3 — ALERTS & STATS
# ============================================================

else:

    st.markdown(
        '<div class="eyebrow">03 / INCIDENT VIEW</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Alerts & statistics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-description">
            Operational view of detected anomalies, attack classes,
            network behaviour and high-volume sources.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="header-line"></div>',
        unsafe_allow_html=True,
    )

    anomaly_df = traffic[
        traffic["Status"]
        == "ANOMALOUS"
    ].copy()

    total_flows = len(traffic)

    anomaly_count = len(
        anomaly_df
    )

    benign_count = (
        total_flows
        - anomaly_count
    )

    anomaly_rate = (
        anomaly_count
        / total_flows
        * 100
        if total_flows
        else 0
    )

    if not anomaly_df.empty:

        top_threat = (
            anomaly_df[
                "Classification"
            ]
            .value_counts()
            .idxmax()
        )

    else:

        top_threat = "NONE"

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "TOTAL FLOWS",
            f"{total_flows:,}",
            "Current window",
        )

    with c2:
        st.metric(
            "BENIGN FLOWS",
            f"{benign_count:,}",
            "Expected behaviour",
        )

    with c3:
        st.metric(
            "ANOMALY RATE",
            f"{anomaly_rate:.1f}%",
            "Traffic requiring review",
        )

    with c4:
        st.metric(
            "TOP THREAT",
            top_threat,
            "Dominant anomaly",
        )

    st.write("")

    # --------------------------------------------------------
    # ALERTS + ATTACK DISTRIBUTION
    # --------------------------------------------------------

    left, right = st.columns(
        [1.2, 1],
        gap="large",
    )

    with left:

        st.markdown(
            '<div class="section-title">ACTIVE ALERTS</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">CURRENT NETWORK DETECTIONS</div>',
            unsafe_allow_html=True,
        )

        if anomaly_df.empty:

            st.success(
                "No active anomalies detected."
            )

        else:

            for _, row in anomaly_df.head(8).iterrows():

                if row["Classification"] in [
                    "DOS",
                    "INFILTRATION",
                ]:

                    severity = "HIGH"

                    st.markdown(
                        f"""
                        <div class="alert-high">
                            <div class="alert-title">
                                HIGH // {row['Classification']}
                            </div>

                            <div class="alert-description">
                                Source {row['Source']}
                                generated anomalous
                                {row['Protocol']} traffic toward
                                {row['Destination']}:{row['Port']}.
                            </div>

                            <div class="alert-meta">
                                {row['Time']}
                                &nbsp;•&nbsp;
                                {row['Packets']:,} packets
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                else:

                    severity = "MEDIUM"

                    st.markdown(
                        f"""
                        <div class="alert-medium">
                            <div class="alert-title">
                                MEDIUM // {row['Classification']}
                            </div>

                            <div class="alert-description">
                                Source {row['Source']}
                                generated suspicious
                                {row['Protocol']} traffic toward
                                {row['Destination']}:{row['Port']}.
                            </div>

                            <div class="alert-meta">
                                {row['Time']}
                                &nbsp;•&nbsp;
                                {row['Packets']:,} packets
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with right:

        st.markdown(
            '<div class="section-title">ATTACK DISTRIBUTION</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">ANOMALY CLASS FREQUENCY</div>',
            unsafe_allow_html=True,
        )

        attack_counts = (
            traffic[
                traffic["Classification"]
                != "BENIGN"
            ]["Classification"]
            .value_counts()
        )

        if not attack_counts.empty:

            st.bar_chart(
                attack_counts,
                height=330,
            )

        else:

            st.info(
                "No attack classes observed."
            )

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    st.write("")

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">BYTE VOLUME</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">TOTAL BY PROTOCOL</div>',
            unsafe_allow_html=True,
        )

        protocol_bytes = (
            traffic
            .groupby("Protocol")["Bytes"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            protocol_bytes,
            height=260,
        )

    with right:

        st.markdown(
            '<div class="section-title">PACKET DISTRIBUTION</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">TRAFFIC CLASS VS PACKETS</div>',
            unsafe_allow_html=True,
        )

        class_packets = (
            traffic
            .groupby("Classification")[
                "Packets"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            class_packets,
            height=260,
        )

    # --------------------------------------------------------
    # SOURCE INVESTIGATION
    # --------------------------------------------------------

    st.write("")

    st.markdown(
        '<div class="section-title">SOURCE INVESTIGATION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">TOP SOURCES BY PACKET VOLUME</div>',
        unsafe_allow_html=True,
    )

    source_stats = (
        traffic
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

    # --------------------------------------------------------
    # THREAT SOURCE VIEW
    # --------------------------------------------------------

    st.write("")

    st.markdown(
        '<div class="section-title">THREAT SOURCES</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">SOURCES ASSOCIATED WITH ANOMALOUS FLOWS</div>',
        unsafe_allow_html=True,
    )

    if not anomaly_df.empty:

        threat_sources = (
            anomaly_df
            .groupby("Source")
            .agg(
                Alerts=("Source", "count"),
                Packets=("Packets", "sum"),
                Targets=("Destination", "nunique"),
            )
            .sort_values(
                "Alerts",
                ascending=False,
            )
            .head(10)
            .reset_index()
        )

        st.dataframe(
            threat_sources,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No anomalous sources detected."
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        <span>FLOWSENSE</span>
        <span>NETWORK TRAFFIC INTELLIGENCE</span>
        <span>DEVELOPMENT BUILD 0.2.0</span>
    </div>
    """,
    unsafe_allow_html=True,
)

import streamlit as st
import pandas as pd
import numpy as np
import random
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
# THEME
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #080b0a;
        --panel: #0e1311;
        --panel2: #111815;
        --border: #26302c;
        --text: #e8eee9;
        --muted: #7d8983;
        --dim: #505b56;
        --green: #b0df63;
        --green-dark: #719d3e;
        --amber: #dfb45c;
        --red: #db6c5d;
        --cyan: #70c4c0;
    }

    * {
        font-family: "Space Grotesk", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(130, 160, 90, 0.07),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 100%,
                rgba(65, 110, 100, 0.055),
                transparent 30%
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
            linear-gradient(#ffffff 1px, transparent 1px),
            linear-gradient(90deg, #ffffff 1px, transparent 1px);
        background-size: 50px 50px;
        z-index: 0;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
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

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background: #090d0c;
        border-right: 1px solid #1b2421;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.4rem 1rem;
    }

    .sidebar-brand {
        padding: 0.4rem 0.25rem 1.7rem 0.25rem;
    }

    .brand-symbol {
        font-family: "DM Mono", monospace;
        color: var(--green);
        font-size: 24px;
        margin-bottom: 5px;
    }

    .brand-name {
        font-family: "DM Mono", monospace;
        color: var(--text);
        font-size: 19px;
        font-weight: 500;
        letter-spacing: 0.12em;
    }

    .brand-description {
        color: var(--dim);
        font-family: "DM Mono", monospace;
        font-size: 8px;
        letter-spacing: 0.13em;
        margin-top: 5px;
        line-height: 1.6;
    }

    .nav-caption {
        color: #4d5953;
        font-family: "DM Mono", monospace;
        font-size: 8px;
        letter-spacing: 0.17em;
        margin: 20px 4px 8px;
    }

    div[data-testid="stSidebar"] .stRadio label {
        color: #84908a !important;
        font-family: "DM Mono", monospace !important;
        font-size: 10px !important;
    }

    div[data-testid="stSidebar"] .stRadio > div {
        gap: 4px;
    }

    .sidebar-status {
        border: 1px solid var(--border);
        background: #0c1110;
        padding: 13px;
        margin-top: 25px;
    }

    .status-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 9px;
        font-family: "DM Mono", monospace;
        font-size: 8px;
    }

    .status-item:last-child {
        margin-bottom: 0;
    }

    .status-label {
        color: var(--dim);
    }

    .status-online {
        color: var(--green);
    }

    .sidebar-footer {
        margin-top: 25px;
        color: #414b47;
        font-family: "DM Mono", monospace;
        font-size: 8px;
        line-height: 1.8;
    }

    /* HEADERS */

    .eyebrow {
        color: var(--green);
        font-family: "DM Mono", monospace;
        font-size: 8px;
        letter-spacing: 0.2em;
        margin-bottom: 8px;
    }

    .main-title {
        color: #eef3ef;
        font-size: 35px;
        font-weight: 600;
        letter-spacing: -0.045em;
        line-height: 1.05;
        margin-bottom: 9px;
    }

    .main-description {
        color: var(--muted);
        font-family: "DM Mono", monospace;
        font-size: 9px;
        line-height: 1.8;
        max-width: 800px;
    }

    .rule {
        height: 1px;
        margin: 23px 0 25px;
        background: linear-gradient(
            90deg,
            var(--green-dark),
            var(--border),
            transparent
        );
    }

    /* METRIC CARDS */

    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            rgba(255,255,255,0.018),
            rgba(255,255,255,0)
        );
        border: 1px solid var(--border);
        padding: 15px 17px;
        min-height: 105px;
    }

    div[data-testid="stMetricLabel"] {
        color: var(--dim) !important;
        font-family: "DM Mono", monospace !important;
        font-size: 8px !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-family: "DM Mono", monospace !important;
        font-size: 25px !important;
        margin-top: 8px;
    }

    div[data-testid="stMetricDelta"] {
        font-family: "DM Mono", monospace !important;
        font-size: 8px !important;
    }

    /* PANELS */

    .section-title {
        color: #aab5af;
        font-family: "DM Mono", monospace;
        font-size: 9px;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: var(--dim);
        font-family: "DM Mono", monospace;
        font-size: 7px;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }

    /* BUTTONS */

    .stButton > button {
        background: #101613;
        border: 1px solid #344039;
        border-radius: 2px;
        color: #cbd4ce;
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

    /* INPUTS */

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

    /* DATAFRAME */

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
    }

    /* EXPANDER */

    div[data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 2px;
        background: #0d1210;
    }

    /* FOOTER */

    .app-footer {
        border-top: 1px solid #1a211f;
        margin-top: 45px;
        padding-top: 14px;
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
# DATA
# ============================================================

random.seed(42)
np.random.seed(42)

PROTOCOLS = [
    "TCP",
    "UDP",
    "HTTP",
    "HTTPS",
    "DNS",
    "SSH",
    "ICMP",
]

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

ATTACKS = [
    "BENIGN",
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


def generate_traffic(n=35):

    records = []

    for _ in range(n):

        roll = random.random()

        if roll < 0.10:
            classification = random.choice(
                ["DOS", "PORT_SCAN", "BRUTE_FORCE", "BOTNET"]
            )
            destination = random.choice(
                SUSPICIOUS_DESTINATIONS
            )
            status = "ANOMALOUS"

        elif roll < 0.14:
            classification = "INFILTRATION"
            destination = random.choice(
                SUSPICIOUS_DESTINATIONS
            )
            status = "ANOMALOUS"

        else:
            classification = "BENIGN"
            destination = random.choice(
                NORMAL_DESTINATIONS
            )
            status = "NORMAL"

        if classification == "DOS":
            packets = random.randint(1200, 9000)
            bytes_count = random.randint(
                500_000,
                8_000_000,
            )

        elif classification == "PORT_SCAN":
            packets = random.randint(100, 900)
            bytes_count = random.randint(
                20_000,
                150_000,
            )

        elif classification == "BRUTE_FORCE":
            packets = random.randint(60, 500)
            bytes_count = random.randint(
                10_000,
                200_000,
            )

        else:
            packets = random.randint(5, 280)
            bytes_count = random.randint(
                1_000,
                300_000,
            )

        records.append(
            {
                "Time": (
                    datetime.now()
                    - timedelta(
                        seconds=random.randint(0, 180)
                    )
                ).strftime("%H:%M:%S"),

                "Source": random_ip(),

                "Destination": destination,

                "Protocol": random.choice(PROTOCOLS),

                "Port": random.choice(
                    [
                        22,
                        53,
                        80,
                        443,
                        25,
                        3306,
                        8080,
                    ]
                ),

                "Packets": packets,

                "Bytes": bytes_count,

                "Duration": round(
                    random.uniform(
                        0.01,
                        8.5,
                    ),
                    3,
                ),

                "Classification": classification,

                "Status": status,
            }
        )

    return pd.DataFrame(records)


traffic = generate_traffic()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-symbol">◈</div>
            <div class="brand-name">FLOWSENSE</div>
            <div class="brand-description">
                NETWORK TRAFFIC INTELLIGENCE<br>
                & ANOMALY DETECTION
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="nav-caption">MONITORING CONSOLE</div>',
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
        """
        <div class="sidebar-status">
            <div class="status-item">
                <span class="status-label">ENGINE</span>
                <span class="status-online">● ONLINE</span>
            </div>

            <div class="status-item">
                <span class="status-label">CAPTURE</span>
                <span class="status-online">ACTIVE</span>
            </div>

            <div class="status-item">
                <span class="status-label">MODEL</span>
                <span class="status-online">READY</span>
            </div>

            <div class="status-item">
                <span class="status-label">LATENCY</span>
                <span class="status-online">18 ms</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            FLOWSENSE / DEVELOPMENT BUILD<br>
            ML NETWORK MONITORING<br>
            VERSION 0.1.0
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
        '<div class="main-title">Live traffic feed</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-description">
            Real-time network telemetry for observing packet flows,
            protocols, traffic volume and anomalous behaviour.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="rule"></div>',
        unsafe_allow_html=True,
    )

    total_packets = int(traffic["Packets"].sum())
    total_bytes = int(traffic["Bytes"].sum())
    anomalies = int(
        (traffic["Status"] == "ANOMALOUS").sum()
    )
    sources = traffic["Source"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "PACKETS / WINDOW",
            f"{total_packets:,}",
            "rolling capture",
        )

    with c2:
        st.metric(
            "TRAFFIC VOLUME",
            f"{total_bytes / 1_000_000:.2f} MB",
            "observed",
        )

    with c3:
        st.metric(
            "ANOMALOUS FLOWS",
            str(anomalies).zfill(2),
            "requires inspection",
        )

    with c4:
        st.metric(
            "ACTIVE SOURCES",
            str(sources).zfill(2),
            "unique addresses",
        )

    st.write("")

    left, right = st.columns(
        [2.1, 1],
        gap="large",
    )

    # --------------------------------------------------------
    # TRAFFIC TABLE
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">PACKET STREAM</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">LIVE / SIMULATED CAPTURE</div>',
            unsafe_allow_html=True,
        )

        display_df = traffic[
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
            display_df,
            use_container_width=True,
            hide_index=True,
            height=610,
        )

    # --------------------------------------------------------
    # PROTOCOL PANEL
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">TRAFFIC MIX</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">PROTOCOL DISTRIBUTION</div>',
            unsafe_allow_html=True,
        )

        protocol_counts = (
            traffic["Protocol"]
            .value_counts()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            protocol_counts,
            height=270,
        )

        st.write("")

        st.markdown(
            '<div class="section-title">CAPTURE CONTROL</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">SIMULATION PARAMETERS</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "↻  REGENERATE TRAFFIC",
            use_container_width=True,
        ):
            traffic = generate_traffic()
            st.rerun()

        intensity = st.slider(
            "SIMULATION INTENSITY",
            1,
            10,
            5,
        )

        st.caption(
            f"PACKET RATE  /  {intensity * 20} pkt/s"
        )

        st.caption("INTERFACE  /  eth0 / virtual")
        st.caption("BUFFER  /  64 MB")

    st.write("")

    st.markdown(
        '<div class="section-title">FLOW VOLUME</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">PACKETS BY TRAFFIC CLASS</div>',
        unsafe_allow_html=True,
    )

    flow_volume = (
        traffic.groupby("Classification")["Packets"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        flow_volume,
        height=260,
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
        '<div class="main-title">Model prediction</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-description">
            Submit a network-flow feature vector and estimate whether
            the observed behaviour is benign, suspicious or anomalous.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="rule"></div>',
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
            '<div class="section-subtitle">MODEL INPUT</div>',
            unsafe_allow_html=True,
        )

        duration = st.number_input(
            "FLOW DURATION",
            min_value=0.001,
            value=2.84,
            step=0.01,
        )

        packet_count = st.number_input(
            "PACKET COUNT",
            min_value=1,
            value=186,
            step=1,
        )

        byte_count = st.number_input(
            "BYTE COUNT",
            min_value=1,
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
            value=65.5,
            step=0.1,
        )

        predict = st.button(
            "RUN CLASSIFICATION  →",
            use_container_width=True,
        )

    with right:

        st.markdown(
            '<div class="section-title">INFERENCE RESULT</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">CLASSIFIER OUTPUT</div>',
            unsafe_allow_html=True,
        )

        if predict:

            anomaly_score = 0.06

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
                anomaly_score += 0.10

            if protocol == "ICMP" and packet_rate > 200:
                anomaly_score += 0.20

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
                confidence = 1 - anomaly_score
                risk = "LOW"

        else:

            prediction = "WAITING"
            confidence = 0
            risk = "—"

        if prediction == "WAITING":

            st.info(
                "Submit a flow feature vector to run the classifier."
            )

        else:

            if prediction == "BENIGN":

                st.success(
                    f"BENIGN  •  {confidence * 100:.1f}% confidence"
                )

            elif prediction == "SUSPICIOUS":

                st.warning(
                    f"SUSPICIOUS  •  {confidence * 100:.1f}% confidence"
                )

            else:

                st.error(
                    f"ANOMALOUS  •  {confidence * 100:.1f}% confidence"
                )

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

        features = pd.DataFrame(
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
                    source_port,
                    destination_port,
                    protocol,
                    f"{packet_rate:.2f} pkt/s",
                ],
            }
        )

        st.dataframe(
            features,
            use_container_width=True,
            hide_index=True,
        )

    st.write("")

    c1, c2, c3 = st.columns(3)

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
            "TARGET LATENCY",
            "<20 ms",
            "inference",
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
        '<div class="main-title">Alerts & statistics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-description">
            Operational summary of detected anomalies, attack classes,
            network behaviour and high-volume traffic sources.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="rule"></div>',
        unsafe_allow_html=True,
    )

    anomaly_df = traffic[
        traffic["Status"] == "ANOMALOUS"
    ].copy()

    total_flows = len(traffic)
    anomaly_count = len(anomaly_df)
    benign_count = total_flows - anomaly_count

    anomaly_rate = (
        anomaly_count / total_flows * 100
        if total_flows
        else 0
    )

    top_threat = (
        anomaly_df["Classification"]
        .value_counts()
        .idxmax()
        if not anomaly_df.empty
        else "NONE"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "TOTAL FLOWS",
            total_flows,
            "observation window",
        )

    with c2:
        st.metric(
            "BENIGN FLOWS",
            benign_count,
            f"{100 - anomaly_rate:.1f}% of traffic",
        )

    with c3:
        st.metric(
            "ANOMALY RATE",
            f"{anomaly_rate:.1f}%",
            "requires review",
        )

    with c4:
        st.metric(
            "TOP THREAT",
            top_threat,
            "dominant class",
        )

    st.write("")

    left, right = st.columns(
        [1.2, 1],
        gap="large",
    )

    # --------------------------------------------------------
    # ALERTS
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">ACTIVE ALERTS</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">CURRENT DETECTIONS</div>',
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

                else:

                    severity = "MEDIUM"

                with st.expander(
                    f"{severity}  •  {row['Classification']}  •  {row['Time']}"
                ):

                    st.write(
                        f"Source: `{row['Source']}`"
                    )

                    st.write(
                        f"Destination: `{row['Destination']}:{row['Port']}`"
                    )

                    st.write(
                        f"Protocol: `{row['Protocol']}`"
                    )

                    st.write(
                        f"Packets observed: `{row['Packets']:,}`"
                    )

    # --------------------------------------------------------
    # ATTACK DISTRIBUTION
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">ATTACK DISTRIBUTION</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">DETECTED CLASSES</div>',
            unsafe_allow_html=True,
        )

        attacks = (
            traffic[
                traffic["Classification"] != "BENIGN"
            ]["Classification"]
            .value_counts()
        )

        if not attacks.empty:

            st.bar_chart(
                attacks,
                height=300,
            )

        else:

            st.info(
                "No attack classes observed."
            )

    st.write("")

    # --------------------------------------------------------
    # BYTE VOLUME
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">BYTE VOLUME</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">BY PROTOCOL</div>',
            unsafe_allow_html=True,
        )

        protocol_bytes = (
            traffic.groupby("Protocol")["Bytes"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            protocol_bytes,
            height=270,
        )

    with right:

        st.markdown(
            '<div class="section-title">PACKET DISTRIBUTION</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-subtitle">BY CLASSIFICATION</div>',
            unsafe_allow_html=True,
        )

        class_packets = (
            traffic.groupby("Classification")["Packets"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            class_packets,
            height=270,
        )

    st.write("")

    # --------------------------------------------------------
    # SOURCE INVESTIGATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">SOURCE INVESTIGATION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">TOP SOURCES BY PACKET VOLUME</div>',
        unsafe_allow_html=True,
    )

    source_stats = (
        traffic.groupby("Source")
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

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="app-footer">
        <span>FLOWSENSE</span>
        <span>NETWORK TRAFFIC INTELLIGENCE</span>
        <span>SYSTEM ONLINE</span>
    </div>
    """,
    unsafe_allow_html=True,
)

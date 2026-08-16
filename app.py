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
# SESSION STATE
# ============================================================

if "seed" not in st.session_state:
    st.session_state.seed = 42

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []

# ============================================================
# NATIVE STREAMLIT THEME
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #080b0a;
    }

    section[data-testid="stSidebar"] {
        background-color: #090d0c;
    }

    div[data-testid="stMetric"] {
        background-color: #0d1210;
        border: 1px solid #27312d;
        padding: 15px;
    }

    div[data-testid="stMetricLabel"] {
        color: #7d8983 !important;
        font-family: monospace;
        font-size: 11px;
    }

    div[data-testid="stMetricValue"] {
        color: #e8eee9 !important;
        font-family: monospace;
    }

    .stButton > button {
        border-radius: 3px;
        background-color: #101613;
        border: 1px solid #344039;
        color: #cbd4ce;
        font-family: monospace;
    }

    .stButton > button:hover {
        border-color: #8eaf51;
        color: #b0df63;
    }

    h1, h2, h3 {
        color: #e8eee9;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #27312d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# NETWORK CONFIGURATION
# ============================================================

PROTOCOLS = {
    "HTTP": [80],
    "HTTPS": [443],
    "DNS": [53],
    "SSH": [22],
    "SMTP": [25],
    "MYSQL": [3306],
    "TCP": [8080, 8443],
    "UDP": [123, 500, 4500],
    "ICMP": [0],
}

NORMAL_DESTINATIONS = [
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

ATTACKS = [
    "DOS",
    "PORT_SCAN",
    "BRUTE_FORCE",
    "BOTNET",
    "INFILTRATION",
]

# ============================================================
# HELPERS
# ============================================================

def random_ip():
    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )


def generate_traffic(count=40):

    random.seed(st.session_state.seed)

    rows = []

    for _ in range(count):

        attack = random.random() < 0.16

        if attack:

            classification = random.choice(ATTACKS)

            source = random_ip()

            destination = random.choice(
                SUSPICIOUS_DESTINATIONS
            )

            if classification == "DOS":

                protocol = random.choice(
                    ["TCP", "UDP", "ICMP"]
                )

                port = random.choice(
                    [53, 80, 443, 0]
                )

                packets = random.randint(
                    2500,
                    12000,
                )

                duration = random.uniform(
                    0.1,
                    4.0,
                )

                bytes_count = random.randint(
                    800_000,
                    9_000_000,
                )

            elif classification == "PORT_SCAN":

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

                bytes_count = random.randint(
                    10_000,
                    150_000,
                )

            elif classification == "BRUTE_FORCE":

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

                bytes_count = random.randint(
                    40_000,
                    450_000,
                )

            elif classification == "BOTNET":

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

                bytes_count = random.randint(
                    100_000,
                    1_500_000,
                )

            else:

                protocol = random.choice(
                    ["TCP", "HTTPS", "DNS"]
                )

                if protocol == "HTTPS":
                    port = 443
                elif protocol == "DNS":
                    port = 53
                else:
                    port = 8080

                packets = random.randint(
                    500,
                    2200,
                )

                duration = random.uniform(
                    1,
                    12,
                )

                bytes_count = random.randint(
                    150_000,
                    2_000_000,
                )

            status = "ANOMALOUS"

        else:

            protocol = random.choice(
                list(PROTOCOLS.keys())
            )

            port = random.choice(
                PROTOCOLS[protocol]
            )

            source = random_ip()

            destination = random.choice(
                NORMAL_DESTINATIONS
            )

            packets = random.randint(
                8,
                280,
            )

            duration = random.uniform(
                0.2,
                15,
            )

            bytes_count = random.randint(
                2_000,
                350_000,
            )

            classification = "BENIGN"
            status = "NORMAL"

        packet_rate = packets / duration

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

                "Bytes": bytes_count,

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

    st.title("◈ FLOWSENSE")

    st.caption(
        "NETWORK TRAFFIC INTELLIGENCE\n"
        "& ANOMALY DETECTION"
    )

    st.divider()

    st.caption("MONITORING CONSOLE")

    page = st.radio(
        "Navigation",
        [
            "01 / Live Traffic",
            "02 / Model Prediction",
            "03 / Alerts & Stats",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("SYSTEM STATUS")

    col1, col2 = st.columns(
        [1, 1.5]
    )

    with col1:
        st.write("ENGINE")

    with col2:
        st.success("ONLINE")

    col1, col2 = st.columns(
        [1, 1.5]
    )

    with col1:
        st.write("CAPTURE")

    with col2:
        st.success("ACTIVE")

    col1, col2 = st.columns(
        [1, 1.5]
    )

    with col1:
        st.write("MODEL")

    with col2:
        st.success("READY")

    col1, col2 = st.columns(
        [1, 1.5]
    )

    with col1:
        st.write("LATENCY")

    with col2:
        st.write("18 ms")

    st.divider()

    st.caption(
        "FLOWSENSE DEVELOPMENT BUILD\n"
        "ML NETWORK MONITORING\n"
        "VERSION 0.3.0"
    )

# ============================================================
# PAGE 1 — LIVE TRAFFIC
# ============================================================

if page == "01 / Live Traffic":

    st.caption("01 / TELEMETRY")

    st.title("Live traffic feed")

    st.write(
        "Real-time network telemetry for observing packet flows, "
        "protocol behaviour, traffic volume and anomalous activity."
    )

    st.divider()

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

    left, right = st.columns(
        [2.1, 1]
    )

    # --------------------------------------------------------
    # TRAFFIC TABLE
    # --------------------------------------------------------

    with left:

        st.subheader("Packet stream")

        st.caption(
            "LATEST OBSERVED NETWORK FLOWS"
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
        )

    # --------------------------------------------------------
    # PROTOCOL MIX
    # --------------------------------------------------------

    with right:

        st.subheader("Protocol mix")

        st.caption(
            "FLOW DISTRIBUTION"
        )

        protocol_counts = (
            traffic["Protocol"]
            .value_counts()
        )

        st.bar_chart(
            protocol_counts,
            height=250,
        )

        st.write("")

        st.subheader("Capture control")

        st.caption(
            "SIMULATED TELEMETRY ENGINE"
        )

        if st.button(
            "REGENERATE TRAFFIC",
            use_container_width=True,
        ):

            st.session_state.seed += 1

            st.rerun()

        intensity = st.slider(
            "SIMULATION INTENSITY",
            1,
            10,
            5,
        )

        st.write(
            f"Packet rate: {intensity * 20} pkt/s"
        )

        st.write("Interface: eth0")
        st.write("Mode: simulated")
        st.write("Buffer: 64 MB")

    # --------------------------------------------------------
    # NETWORK ACTIVITY
    # --------------------------------------------------------

    st.divider()

    st.subheader("Network activity")

    st.caption(
        "PACKETS BY TRAFFIC CLASS"
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
    # EXTRA TELEMETRY
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("Top destinations")

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
            .head(8)
        )

        st.dataframe(
            destination_stats,
            use_container_width=True,
        )

    with right:

        st.subheader("Traffic rate")

        st.line_chart(
            traffic[
                ["Packet Rate"]
            ].reset_index(
                drop=True
            ),
            height=250,
        )

# ============================================================
# PAGE 2 — MODEL PREDICTION
# ============================================================

elif page == "02 / Model Prediction":

    st.caption("02 / INFERENCE")

    st.title("Model prediction")

    st.write(
        "Submit a network-flow feature vector and estimate whether "
        "the observed behaviour is benign, suspicious or anomalous."
    )

    st.divider()

    left, right = st.columns(2)

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    with left:

        st.subheader("Flow feature vector")

        st.caption(
            "MODEL INPUT FEATURES"
        )

        duration = st.number_input(
            "FLOW DURATION (SECONDS)",
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
            value=65.5,
            step=0.1,
        )

        predict = st.button(
            "RUN TRAFFIC CLASSIFICATION",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    with right:

        st.subheader("Inference result")

        st.caption(
            "MODEL CLASSIFICATION OUTPUT"
        )

        if predict:

            score = 0.04

            if packet_rate > 500:
                score += 0.35

            if packet_count > 1500:
                score += 0.25

            if byte_count > 1_000_000:
                score += 0.20

            if destination_port in [
                22,
                23,
                3389,
            ]:
                score += 0.08

            if (
                protocol == "ICMP"
                and packet_rate > 200
            ):
                score += 0.18

            score = min(
                score,
                0.99,
            )

            if score >= 0.70:

                prediction = "ANOMALOUS"
                confidence = score
                risk = "HIGH"

            elif score >= 0.40:

                prediction = "SUSPICIOUS"
                confidence = score
                risk = "MEDIUM"

            else:

                prediction = "BENIGN"
                confidence = 1 - score
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

            if prediction == "BENIGN":

                st.success(
                    f"BENIGN — "
                    f"{confidence * 100:.1f}% confidence"
                )

            elif prediction == "SUSPICIOUS":

                st.warning(
                    f"SUSPICIOUS — "
                    f"{confidence * 100:.1f}% confidence"
                )

            else:

                st.error(
                    f"ANOMALOUS — "
                    f"{confidence * 100:.1f}% confidence"
                )

            st.progress(
                int(confidence * 100)
            )

            st.write(
                f"Risk level: **{risk}**"
            )

        else:

            st.info(
                "Awaiting network flow feature vector."
            )

        st.write("")

        st.subheader("Feature snapshot")

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

    # --------------------------------------------------------
    # MODEL INFO
    # --------------------------------------------------------

    st.divider()

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
            "Flow-level vector",
        )

    with c3:
        st.metric(
            "CLASSES",
            "05",
            "Traffic categories",
        )

    with c4:
        st.metric(
            "TARGET LATENCY",
            "<20 ms",
            "Inference",
        )

    # --------------------------------------------------------
    # SIGNAL ANALYSIS
    # --------------------------------------------------------

    if predict:

        st.divider()

        st.subheader("Behaviour signals")

        st.caption(
            "FEATURE SIGNAL STRENGTH"
        )

        signal_data = pd.DataFrame(
            {
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
                ]
            },
            index=[
                "Packet rate",
                "Packet count",
                "Byte volume",
                "Destination port",
                "Protocol",
                "Duration",
            ],
        )

        st.bar_chart(
            signal_data,
            height=260,
        )

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    if st.session_state.prediction_history:

        st.divider()

        st.subheader("Recent inference")

        history = pd.DataFrame(
            st.session_state.prediction_history[-10:]
        )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True,
        )

# ============================================================
# PAGE 3 — ALERTS & STATS
# ============================================================

else:

    st.caption("03 / INCIDENT VIEW")

    st.title("Alerts & statistics")

    st.write(
        "Operational view of detected anomalies, attack classes, "
        "network behaviour and high-volume traffic sources."
    )

    st.divider()

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
            "Requires review",
        )

    with c4:
        st.metric(
            "TOP THREAT",
            top_threat,
            "Dominant anomaly",
        )

    st.write("")

    # --------------------------------------------------------
    # ALERTS
    # --------------------------------------------------------

    left, right = st.columns(
        [1.2, 1]
    )

    with left:

        st.subheader("Active alerts")

        st.caption(
            "CURRENT NETWORK DETECTIONS"
        )

        if anomaly_df.empty:

            st.success(
                "No active anomalies detected."
            )

        else:

            for _, row in anomaly_df.head(8).iterrows():

                severity = (
                    "HIGH"
                    if row["Classification"]
                    in [
                        "DOS",
                        "INFILTRATION",
                    ]
                    else "MEDIUM"
                )

                with st.expander(
                    f"{severity} — "
                    f"{row['Classification']} — "
                    f"{row['Time']}"
                ):

                    st.write(
                        f"Source: {row['Source']}"
                    )

                    st.write(
                        f"Destination: "
                        f"{row['Destination']}:{row['Port']}"
                    )

                    st.write(
                        f"Protocol: "
                        f"{row['Protocol']}"
                    )

                    st.write(
                        f"Packets: "
                        f"{row['Packets']:,}"
                    )

                    st.write(
                        f"Packet rate: "
                        f"{row['Packet Rate']:.2f} pkt/s"
                    )

    # --------------------------------------------------------
    # ATTACK DISTRIBUTION
    # --------------------------------------------------------

    with right:

        st.subheader(
            "Attack distribution"
        )

        st.caption(
            "ANOMALY CLASS FREQUENCY"
        )

        attacks = (
            traffic[
                traffic["Classification"]
                != "BENIGN"
            ]["Classification"]
            .value_counts()
        )

        if not attacks.empty:

            st.bar_chart(
                attacks,
                height=330,
            )

        else:

            st.info(
                "No attack classes observed."
            )

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader(
            "Byte volume"
        )

        st.caption(
            "TOTAL BY PROTOCOL"
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

        st.subheader(
            "Packet distribution"
        )

        st.caption(
            "TRAFFIC CLASS VS PACKETS"
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

    st.divider()

    st.subheader(
        "Source investigation"
    )

    st.caption(
        "TOP SOURCES BY PACKET VOLUME"
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
    # THREAT SOURCES
    # --------------------------------------------------------

    st.write("")

    st.subheader(
        "Threat sources"
    )

    st.caption(
        "SOURCES ASSOCIATED WITH ANOMALOUS FLOWS"
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

st.divider()

st.caption(
    "FLOWSENSE  •  NETWORK TRAFFIC INTELLIGENCE  •  "
    "DEVELOPMENT BUILD 0.3.0"
)

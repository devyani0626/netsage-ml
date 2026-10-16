
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NetSage ML | NOC",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "network_model.pkl"

# ---------------- THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #050d1a;
    color: #e6f2ff;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background: #071426;
    border-right: 1px solid #19334d;
}
[data-testid="stSidebar"] * { color: #dcecff; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
h1, h2, h3 { color: #f0f7ff !important; }
small { color: #8da9c5; }

.metric-card {
    background: linear-gradient(145deg,#0c1d31,#091525);
    border: 1px solid #203b56;
    border-radius: 14px;
    padding: 18px;
    min-height: 118px;
}
.metric-label {
    color: #9bb3cb;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}
.metric-value {
    font-size: 30px;
    font-weight: 800;
    margin-top: 12px;
}
.panel {
    background: #081729;
    border: 1px solid #1b3651;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 12px;
}
.muted { color: #8da9c5; font-size: 13px; }
.cyan { color: #17c8f5; }
.green { color: #16e0a0; }
.yellow { color: #ffca43; }
.red { color: #ff5470; }
.device {
    background: #0a1b2e;
    border: 1px solid #1c3650;
    border-radius: 10px;
    padding: 12px;
    margin: 5px 0;
}
div.stButton > button {
    background: linear-gradient(90deg,#04a8e8,#0875f9);
    color: white;
    border: 0;
    border-radius: 9px;
    font-weight: 700;
    min-height: 42px;
    width: 100%;
}
div.stButton > button:hover {
    border: 1px solid #49d8ff;
    color: white;
}
[data-testid="stMetric"] {
    background: #0a1b2e;
    padding: 12px;
    border: 1px solid #203b56;
    border-radius: 10px;
}
hr { border-color: #1c3650; }
</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None

model = load_model()

# ---------------- NAVIGATION ----------------
with st.sidebar:
    st.markdown("## 🌐 NetSage **ML**")
    st.caption("INTELLIGENT NETWORK OPERATIONS")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "NOC Overview",
            "AI Assistant",
            "Topology",
            "Device Inventory",
            "About Project"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("🟢 **MODEL STATUS**")
    st.caption("Model loaded" if model is not None else "Model file not found")
    st.caption("NetSage ML • Student Prototype")
    st.caption("Network diagnostics dashboard")

# ---------------- HEADER ----------------
st.markdown(
    '<div class="muted cyan">━━ OPERATIONAL INTELLIGENCE ENGINE</div>',
    unsafe_allow_html=True
)
st.title(page.upper())
st.caption(
    f"Network Fault Prediction Platform  •  "
    f"Dashboard session: {datetime.now().strftime('%d %b %Y, %H:%M')}"
)

# ---------------- SAMPLE INVENTORY ----------------
devices = [
    ("access-sw-01", "10.0.0.11", "SWITCH", "ONLINE"),
    ("access-sw-02", "10.0.0.12", "SWITCH", "ONLINE"),
    ("app-srv-01", "10.0.1.20", "SERVER", "ONLINE"),
    ("app-srv-02", "10.0.1.21", "SERVER", "ONLINE"),
    ("db-srv-01", "10.0.2.10", "DATABASE", "ONLINE"),
    ("dns-srv-01", "10.0.2.53", "DNS SERVER", "ONLINE"),
]

# ---------------- PREDICTION FUNCTION ----------------
def predict_fault(ip, gateway, server, dns):
    if model is None:
        return None, None
    features = pd.DataFrame([{
        "ip_configured": int(ip),
        "gateway_ping": int(gateway),
        "server_ping": int(server),
        "dns_working": int(dns)
    }])
    prediction = model.predict(features)[0]
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(max(model.predict_proba(features)[0])) * 100
    return prediction, confidence

fault_advice = {
    "IP_CONFIGURATION": [
        "Inspect the host IP address and subnet mask.",
        "Check DHCP availability or static IP settings.",
        "Verify that the host has a valid network configuration."
    ],
    "GATEWAY_CONNECTIVITY": [
        "Verify the default gateway address.",
        "Check local switch ports, VLAN and cabling.",
        "Inspect gateway interface status and ARP resolution."
    ],
    "SERVER_CONNECTIVITY": [
        "Check server availability and its IP configuration.",
        "Inspect routing, ACL and firewall rules.",
        "Test the server service and path from the client."
    ],
    "DNS": [
        "Check the configured DNS server address.",
        "Test name resolution using nslookup.",
        "Verify DNS service status and relevant records."
    ],
    "NO_FAULT": [
        "The entered checks passed.",
        "If an application still fails, test its port and service.",
        "Confirm the result with additional network diagnostics."
    ]
}

# ---------------- NOC OVERVIEW ----------------
if page == "NOC Overview":
    st.info(
        "Demo mode: inventory and health indicators below are sample data, "
        "not live network telemetry."
    )

    cols = st.columns(6)
    metrics = [
        ("REGISTERED DEVICES", "06", "#17c8f5"),
        ("ONLINE (DEMO)", "06", "#16e0a0"),
        ("OFFLINE (DEMO)", "00", "#ff5470"),
        ("DEGRADED", "00", "#ffca43"),
        ("AI MODEL", "READY" if model is not None else "MISSING", "#17c8f5"),
        ("FAULT CLASSES", "05", "#b38cff")
    ]

    for col, (label, value, color) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-value" style="color:{color};">'
                f'{value}</div></div>',
                unsafe_allow_html=True
            )

    st.write("")
    left, right = st.columns([1.55, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("◉ Network Health Monitor")
        st.caption("Illustrative indicators — not measured from real devices")
        health_cols = st.columns(3)
        for col, label, value in [
            (health_cols[0], "Network checks", "100%"),
            (health_cols[1], "CPU utilization", "66%"),
            (health_cols[2], "Memory usage", "55%")
        ]:
            with col:
                st.metric(label, value)
        st.progress(1.0, text="Demo network health")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("▤ Infrastructure Inventory")
        for i in range(0, len(devices), 2):
            row = st.columns(2)
            for col, device in zip(row, devices[i:i + 2]):
                name, ip, kind, status = device
                with col:
                    st.markdown(
                        f'<div class="device">'
                        f'<span class="green">●</span> <b>{name}</b><br>'
                        f'<span class="muted">{ip} · {kind}</span><br>'
                        f'<span class="green">● {status} (DEMO)</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("✧ AI Fault Assistant")
        st.write(
            "Analyze four network observations to receive a predicted "
            "fault category and troubleshooting guidance."
        )
        st.caption("Predictions depend on your trained model and its dataset.")
        if st.button("OPEN AI PREDICTIONS", key="overview_ai"):
            st.session_state["open_ai"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Network Topology")
        st.markdown("""
        ```text
              [ Router ]
                  |
              [ Switch ]
             /    |    \\
          [PC] [Server] [DNS]
        ```
        """)
        st.caption("Illustrative topology — edit to match your actual lab.")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.pop("open_ai", False):
        st.session_state["nav_to_ai"] = True
        st.info("Choose AI Assistant in the sidebar to run a prediction.")

# ---------------- AI ASSISTANT ----------------
elif page == "AI Assistant":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Network Observation Input")
    st.write(
        "Enter the results you observed in your lab. "
        "A value of 1 means the check passed; 0 means it failed."
    )

    with st.form("prediction_form"):
        c1, c2 = st.columns(2)
        with c1:
            ip = st.selectbox("IP address configured?", [1, 0], format_func=lambda x: "Yes" if x else "No")
            gateway = st.selectbox("Can the host ping its gateway?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        with c2:
            server = st.selectbox("Can the host ping the server?", [1, 0], format_func=lambda x: "Yes" if x else "No")
            dns = st.selectbox("Is DNS resolution working?", [1, 0], format_func=lambda x: "Yes" if x else "No")
        submitted = st.form_submit_button("ANALYZE NETWORK")

    if submitted:
        prediction, confidence = predict_fault(ip, gateway, server, dns)
        if prediction is None:
            st.error("Model not found. Place network_model.pkl in the project folder.")
        else:
            st.session_state["last_prediction"] = prediction
            st.session_state["last_inputs"] = (ip, gateway, server, dns)
            st.markdown("---")
            st.subheader("AI Analysis Result")
            st.markdown(f"### 🔎 {prediction.replace('_', ' ')}")
            if confidence is not None:
                st.metric("Model confidence (not validated)", f"{confidence:.1f}%")
                st.caption(
                    "This is the model's probability estimate, not a guarantee "
                    "of real-world correctness."
                )
            st.subheader("Recommended troubleshooting")
            for item in fault_advice.get(prediction, [
                "Validate the diagnosis using additional network tests."
            ]):
                st.markdown(f"- {item}")
            st.warning(
                "Confirm the suggested diagnosis using real commands and "
                "your network topology before changing any configuration."
            )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TOPOLOGY ----------------
elif page == "Topology":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Illustrative Network Topology")
    st.graphviz_chart("""
    graph network {
        bgcolor="#081729"
        node [style=filled, fontcolor="white", color="#17c8f5",
              fillcolor="#102d46", fontname="Helvetica"]
        edge [color="#17c8f5"]
        Router -- Switch
        Switch -- "PC-01"
        Switch -- "PC-02"
        Switch -- "App Server"
        Switch -- "DNS Server"
        "App Server" -- "Database"
    }
    """)
    st.caption("Example only. This graph is not discovered from live network devices.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DEVICE INVENTORY ----------------
elif page == "Device Inventory":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Registered Demo Devices")
    inventory = pd.DataFrame(
        devices,
        columns=["Device Name", "IP Address", "Device Type", "Demo Status"]
    )
    st.dataframe(inventory, use_container_width=True, hide_index=True)
    st.caption("Sample inventory; no devices are automatically scanned.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ABOUT ----------------
elif page == "About Project":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("About NetSage ML")
    st.write(
        "NetSage ML is an educational network fault classification project. "
        "It predicts one of five categories from four manually entered "
        "network observations."
    )
    st.markdown("""
    **Machine-learning inputs**
    - IP configuration status
    - Gateway ping status
    - Server ping status
    - DNS status

    **Current limitations**
    - Uses a small, synthetic dataset.
    - Does not connect to routers, switches or servers.
    - Dashboard device data is illustrative.
    - Model performance needs careful evaluation on independent cases.

    **Future improvements**
    - Collect more varied, verified lab cases.
    - Evaluate with a confusion matrix and per-class metrics.
    - Import sanitized network command outputs.
    - Add human-reviewed diagnosis history.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("NetSage ML • Educational prototype • No live monitoring enabled")

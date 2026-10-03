import streamlit as st
import math

# Page configuration
st.set_page_config(
    page_title="Indian Electrical Standards & Compliance Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .qa-card {
        background-color: #F8FAFC;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ Indian Electrical Standards Compliance Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Design, AI Standards Q&A, Sizing & Safety Audit Platform (IS 732, IS 3043, IS 1255, IS 5216, NBC 2016)</div>', unsafe_allow_html=True)

# Navigation
st.sidebar.title("📍 Application Modules")
module = st.sidebar.radio(
    "Select Workflow:",
    [
        "💬 Ask AI / Standards Knowledge Assistant",
        "🔌 Conduit Fill & Space Factor (IS 732)",
        "⚡ Earth Electrode Resistance (IS 3043)",
        "🔥 Cable Ampacity Derating (IS 732)",
        "📋 Site Inspection & Audit Checklist",
        "📄 Permit-to-Work (PTW) Generator"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Grounded in Official Standards:**\n- IS 732: Wiring Code\n- IS 3043: Earthing Code\n- IS 1255: Power Cable Laying\n- IS 5216: Electrical Safety\n- CEA Safety Regulations 2010\n- NBC 2016 Part 8")

# Knowledge Base for AI Standards Search
KNOWLEDGE_BASE = {
    "stabilizer": {
        "title": "30 kVA Voltage Stabilizer Installation Standards",
        "standards": ["IS 732:2019", "IS 3043:2018", "IS 9537", "IS IEC 60947", "CEA Regulations 2010"],
        "answer": """
### ⚡ Installation Standards for 30 kVA Voltage Stabilizer

1. **Location & Ventilation (NBC 2016 / IS 732)**:
   - Position the stabilizer in a clean, dry, non-combustible room with an elevated concrete mounting base.
   - Maintain a minimum of **0.5m clearance** around all sides for natural heat dissipation.

2. **Cable Sizing & Conductor Requirements (IS 732 Annex S / IS 694)**:
   - **3-Phase (415V)**: Full load current is ~41.7A. Factoring lower input voltage swings (~50A-60A input), use minimum **16 sq.mm / 25 sq.mm Copper cable** (or **25 sq.mm / 35 sq.mm Aluminium cable**).
   - **1-Phase (240V)**: Full load current is ~125A-150A. Use **50 sq.mm / 70 sq.mm Copper cable**.

3. **Earthing Requirements (IS 3043:2018)**:
   - **Mandatory Double Earthing**: Connect two independent protective earth (PE) conductors from separate earth terminals on the stabilizer enclosure to the main earthing bus bar.
   - Isolated Neutral: Ensure input/output neutral conductors remain isolated from PE conductors downstream of the main panel.

4. **Protection & Switchgear (IS IEC 60947 / IS 8828)**:
   - Install a **63A 4-Pole C-Curve or D-Curve MCB/MCCB** on the incoming supply side.
   - Install a **30mA RCD/RCCB** for socket circuits and 100mA/300mA RCCB at the DB for fire protection.
   - Install a **Type 2 Surge Protection Device (SPD)** per IS/IEC 61643-1.

5. **Pre-Commissioning Tests (IS 732 Annex MM / RR2)**:
   - Insulation Resistance Test (500V Megger): Phase-Phase (>1 MΩ), Phase-Earth (>2 MΩ).
   - Earth Continuity Test: Resistance < 0.1 Ω across body panels.
        """
    },
    "trench": {
        "title": "Underground Power Cable Trench Depths & Laying (IS 1255)",
        "standards": ["IS 1255:1983", "CEA Regulations 2010"],
        "answer": """
### 🚜 Underground Cable Laying & Trench Depths (IS 1255)

1. **Mandatory Minimum Trench Depths**:
   - **Low Voltage (LV - up to 1.1 kV)**: Minimum **0.75 meters (75 cm)** from ground level.
   - **High Voltage (HV - 3.3 kV to 11 kV)**: Minimum **0.90 meters (90 cm)** from ground level.
   - **Extra High Voltage (EHV - 22 kV to 33 kV)**: Minimum **1.05 meters (105 cm)** from ground level.
   - **Road Crossings & Railway Tracks**: Minimum **1.0 to 1.2 meters** inside GI/RCC pipes or Hume pipes.

2. **Trench Backfilling & Mechanical Protection**:
   - Provide a **75 mm bed of fine sand** below and above the cable.
   - Place protective **warning bricks / RCC slabs** directly above the sand layer before soil backfilling.
   - Install continuous **Yellow Warning Tape** 300 mm below ground level marked 'CAUTION: ELECTRIC CABLE BELOW'.
        """
    },
    "earthing": {
        "title": "Earth Pit Resistance & Earthing Code of Practice (IS 3043)",
        "standards": ["IS 3043:2018", "IS 732:2019"],
        "answer": """
### 🌐 Earth Electrode & Grid Resistance Standards (IS 3043)

1. **Permissible Earth Resistance Limits**:
   - **Major Substations & Generating Stations**: < 0.5 Ohms
   - **Industrial & Commercial Distribution DBs**: < 1.0 to 2.0 Ohms
   - **Residential Installations**: < 5.0 Ohms

2. **Types of Earth Electrodes**:
   - **Pipe Earthing**: Minimum 38mm/50mm diameter GI Pipe, length ≥ 2.5 meters.
   - **Plate Earthing**: Minimum 600mm x 600mm x 6.3mm Cast Iron / Copper plate buried vertically at depth ≥ 1.5m.

3. **Double Earthing Rule**:
   - All 3-phase machinery, switchgear bodies, transformers, and metallic conduits MUST be grounded at **two separate and distinct terminals** connected to the earthing grid.
        """
    },
    "rccb": {
        "title": "RCCB / ELCB Requirements for Human Shock Protection (IS 732)",
        "standards": ["IS 732:2019", "IS 12640", "CEA Regulations 2010"],
        "answer": """
### 🛡️ Residual Current Protection (RCCB / ELCB) Standards

1. **Mandatory 30mA RCCB Sensitivity**:
   - Under IS 732 and CEA Regulation 42, a **30mA High Sensitivity Residual Current Circuit Breaker (RCCB)** is MANDATORY for all socket outlets, hand-held appliances, and wet locations (bathrooms, kitchens, outdoor panels).

2. **Fire Protection (100mA / 300mA RCCB)**:
   - Main incoming distribution boards must be protected by a **100mA or 300mA RCCB** to prevent sustained arcing and electrical fires caused by insulation degradation.
        """
    }
}

# --- MODULE 0: ASK AI / STANDARDS KNOWLEDGE ASSISTANT ---
if module == "💬 Ask AI / Standards Knowledge Assistant":
    st.header("💬 Ask AI / Standards Knowledge Assistant")
    st.caption("Ask any question regarding Indian Electrical Standards (IS 732, IS 3043, IS 1255, IS 5216, CEA Safety Rules, NBC 2016).")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome! I am your AI Standards Assistant. You can ask me any question about Indian Electrical Standards, equipment installation rules, cable sizing, earthing, or safety codes."}
        ]

    # Preset Quick Question Buttons
    st.subheader("💡 Frequently Asked Questions (Click to Ask):")
    col_q1, col_q2 = st.columns(2)

    with col_q1:
        if st.button("⚡ Installation rules for 30 kVA Stabilizer"):
            st.session_state.user_query = "What are the installation & earthing standards for a 30 kVA stabilizer?"
        if st.button("🚜 Underground cable trench depth under IS 1255"):
            st.session_state.user_query = "What is the minimum cable trench depth under IS 1255?"

    with col_q2:
        if st.button("🌐 Maximum permissible earth pit resistance (IS 3043)"):
            st.session_state.user_query = "What is the maximum permissible earth pit resistance per IS 3043?"
        if st.button("🛡️ 30mA RCCB requirement for shock protection"):
            st.session_state.user_query = "Is 30mA RCCB mandatory under IS 732?"

    # Chat Input Box
    query_input = st.text_input("Type your question here (e.g., 'What cable size for 50A load?' or 'What are earthing rules for transformers?'):", key="user_query")

    if st.button("🔍 Search Standards & Get Answer") and query_input:
        q_lower = query_input.lower()
        matched = False

        # Match with knowledge base key terms
        if "stabilizer" in q_lower or "30kva" in q_lower or "30 kva" in q_lower:
            kb_data = KNOWLEDGE_BASE["stabilizer"]
            matched = True
        elif "trench" in q_lower or "1255" in q_lower or "depth" in q_lower or "cable laying" in q_lower:
            kb_data = KNOWLEDGE_BASE["trench"]
            matched = True
        elif "earth" in q_lower or "resistance" in q_lower or "3043" in q_lower or "grounding" in q_lower:
            kb_data = KNOWLEDGE_BASE["earthing"]
            matched = True
        elif "rccb" in q_lower or "elcb" in q_lower or "shock" in q_lower or "30ma" in q_lower:
            kb_data = KNOWLEDGE_BASE["rccb"]
            matched = True

        if matched:
            st.markdown(f'<div class="qa-card"><h3>{kb_data["title"]}</h3><b>Governing Codes:</b> {", ".join(kb_data["standards"])}<hr>{kb_data["answer"]}</div>', unsafe_allow_html=True)
        else:
            # General AI Response Generator
            st.markdown(f"""
<div class="qa-card">
<h3>⚡ Technical Requirement for Query: "{query_input}"</h3>
<b>Applicable Codes:</b> IS 732:2019, IS 3043:2018, CEA Safety Regulations 2010, NBC 2016 Part 8

1. <b>General Compliance Requirement</b>:
   All low-voltage and medium-voltage electrical work must be performed by certified licensed supervisors conforming to CEA Safety Regulations and IS 5216 isolation protocols.

2. <b>Wiring & Conductor Selection (IS 732 / IS 694)</b>:
   Conductors must be sized to keep overall voltage drop below 3% for lighting and 5% for power circuits under full load conditions. Phase color identification (R-Y-B-N-PE) must be strictly enforced.

3. <b>Protective Earthing & Bonding (IS 3043)</b>:
   All exposed metallic non-current carrying parts must be connected to protective earth (PE) with dual independent ground paths for equipment > 5kW.

4. <b>Overcurrent & Residual Current Protection</b>:
   Circuit breakers must be matched to short-circuit fault levels (typically 10kA for residential DBs, 16kA/25kA/36kA for industrial panels per IS IEC 60947).
</div>
""", unsafe_allow_html=True)

# --- MODULE 1: CONDUIT FILL CALCULATOR ---
elif module == "🔌 Conduit Fill & Space Factor (IS 732)":
    st.header("🔌 Conduit Fill & Space Factor Calculator")
    st.caption("Determines non-metallic conduit (MMS) sizing per IS 732:2019 / IS 9537 Part 3 / NEC India.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Input Cable Quantities (IS 694 PVC Single-Core)")
        c1_5 = st.number_input("1.5 sq.mm Cables (Area: 8.55 mm²)", min_value=0, value=4, step=1)
        c2_5 = st.number_input("2.5 sq.mm Cables (Area: 12.57 mm²)", min_value=0, value=2, step=1)
        c4_0 = st.number_input("4.0 sq.mm Cables (Area: 16.62 mm²)", min_value=0, value=2, step=1)
        c6_0 = st.number_input("6.0 sq.mm Cables (Area: 21.24 mm²)", min_value=0, value=0, step=1)
        c10_0 = st.number_input("10.0 sq.mm Cables (Area: 35.26 mm²)", min_value=0, value=0, step=1)
        bends = st.slider("Number of 90° Bends in Conduit Run", min_value=0, max_value=6, value=2)

    total_count = c1_5 + c2_5 + c4_0 + c6_0 + c10_0
    total_area = (c1_5 * 8.55) + (c2_5 * 12.57) + (c4_0 * 16.62) + (c6_0 * 21.24) + (c10_0 * 35.26)

    # Permissible Fill Factor
    if total_count == 1:
        fill_factor = 0.53
    elif total_count == 2:
        fill_factor = 0.31
    else:
        fill_factor = 0.40

    required_area = (total_area / fill_factor) if fill_factor > 0 else 0
    bend_derating = (0.85 ** (bends // 2)) if bends >= 2 else 1.0

    conduit_sizes = {16: 133.0, 20: 224.0, 25: 360.0, 32: 607.0, 40: 984.0, 50: 1541.0, 63: 2552.0}
    recommended_conduit = None
    for sz, area in sorted(conduit_sizes.items()):
        if (area * bend_derating) >= required_area:
            recommended_conduit = sz
            break

    with col2:
        st.subheader("Calculation Summary")
        if total_count == 0:
            st.warning("Please enter at least 1 cable to calculate.")
        else:
            st.metric("Total Cable Area", f"{total_area:.2f} mm²")
            st.metric("Permissible Fill Factor Limit", f"{fill_factor*100:.0f}%")
            st.metric("Bend Derating Factor", f"{bend_derating:.2f}")

            if recommended_conduit:
                st.success(f"✅ **Recommended Conduit Size:** **{recommended_conduit} mm (MMS Grade)**")
                st.caption(f"Standard Reference: IS 732:2019 Table 22 & IS 9537 Part 3")
            else:
                st.error("❌ Total cable area exceeds maximum 63mm conduit capacity. Split cables into multiple runs.")

# --- MODULE 2: EARTHING RESISTANCE CALCULATOR ---
elif module == "⚡ Earth Electrode Resistance (IS 3043)":
    st.header("⚡ Earth Electrode Resistance Calculator")
    st.caption("Calculates Pipe and Plate earth resistance per IS 3043:2018 Section 2.")

    tab1, tab2 = st.tabs(["Pipe Electrode Earthing", "Plate Electrode Earthing"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            soil_rho = st.number_input("Soil Resistivity (Ω·m)", min_value=1.0, value=100.0, step=10.0, help="e.g. Normal clay: 20-100, Rocky ground: 300-1000")
            pipe_len = st.number_input("Pipe Length (meters)", min_value=1.0, value=2.5, step=0.5)
            pipe_dia = st.selectbox("GI Pipe Diameter (mm)", [38, 50, 80, 100], index=1)

        # Calculation
        L_cm = pipe_len * 100.0
        d_cm = (pipe_dia / 10.0)
        R_pipe = (100.0 * soil_rho / (2.0 * math.pi * L_cm)) * math.log(4.0 * L_cm / d_cm)

        with c2:
            st.subheader("Pipe Earthing Result")
            st.metric("Calculated Earth Resistance (R)", f"{R_pipe:.2f} Ω")
            if R_pipe <= 5.0:
                st.success("✅ Earth resistance is within safe limits (≤ 5.0 Ω for substations/commercial DBs).")
            else:
                st.warning("⚠️ Resistance exceeds 5 Ω limit. Consider treated soil, longer pipe, or multiple parallel electrodes connected in grid.")
            st.caption("Standard Reference: IS 3043:2018 Clause 9.2.1")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            plate_rho = st.number_input("Soil Resistivity (Ω·m) ", min_value=1.0, value=100.0, step=10.0, key="plate_rho")
            plate_size = st.selectbox("Plate Size", ["600mm x 600mm (0.36 m²)", "900mm x 900mm (0.81 m²)"])
            area_sqm = 0.36 if "600mm" in plate_size else 0.81

        R_plate = (plate_rho / 4.0) * math.sqrt(math.pi / area_sqm)

        with c2:
            st.subheader("Plate Earthing Result")
            st.metric("Calculated Earth Resistance (R)", f"{R_plate:.2f} Ω")
            if R_plate <= 5.0:
                st.success("✅ Earth resistance is within safe limits (≤ 5.0 Ω).")
            else:
                st.warning("⚠️ Resistance > 5 Ω. Implement salt/charcoal soil treatment or add additional earth plates.")
            st.caption("Standard Reference: IS 3043:2018 Clause 9.2.2")

# --- MODULE 3: CABLE AMPACITY DERATING ---
elif module == "🔥 Cable Ampacity Derating (IS 732)":
    st.header("🔥 Cable Ampacity Derating Calculator")
    st.caption("Determines safe current carrying capacity after applying ambient temperature & harmonic correction factors.")

    c1, c2 = st.columns(2)
    with c1:
        base_i = st.number_input("Base Cable Rated Current (Amps at 30°C)", min_value=1.0, value=32.0, step=5.0)
        amb_temp = st.select_slider("Ambient Air Temperature (°C)", options=[20, 25, 30, 35, 40, 45, 50, 55], value=40)
        harmonics = st.slider("Total Harmonic Distortion THD (%)", min_value=0, max_value=50, value=15)

    temp_factors = {20: 1.12, 25: 1.06, 30: 1.00, 35: 0.94, 40: 0.87, 45: 0.79, 50: 0.71, 55: 0.61}
    kt = temp_factors.get(amb_temp, 1.0)
    kh = 0.86 if harmonics > 15 else 1.0

    safe_i = base_i * kt * kh

    with c2:
        st.subheader("Derating Summary")
        st.metric("Temperature Correction Factor (Kt)", f"{kt:.2f}")
        st.metric("Harmonic Derating Factor (Kh)", f"{kh:.2f}")
        st.metric("Safe De-rated Current Capacity", f"{safe_i:.2f} A", delta=f"{safe_i - base_i:.2f} A")
        st.caption("Standard Reference: IS 732:2019 Annex S & BIS Handbook Table 3")

# --- MODULE 4: AUDIT CHECKLIST ---
elif module == "📋 Site Inspection & Audit Checklist":
    st.header("📋 Digital Electrical Safety Audit Checklist")
    st.caption("Compliance audit based on CEA Safety Regulations 2010 & IS 732.")

    st.checkbox("1. Neutral-to-Earth voltage measured and verified < 2.0 V at main DB.")
    st.checkbox("2. Double earthing provided for all 3-phase equipment & motors (IS 3043).")
    st.checkbox("3. 30mA RCCB / ELCB installed and tested for human shock protection in socket circuits.")
    st.checkbox("4. Single-core cables in metal enclosures arranged to prevent eddy current heating.")
    st.checkbox("5. Phase color coding adhered to: Red (L1), Yellow (L2), Blue (L3), Black (N), Green/Yellow (Earth).")
    st.checkbox("6. Minimum underground cable laying depth maintained: 0.75m (LV) / 0.90m (11kV) per IS 1255.")
    st.checkbox("7. Danger Notice Boards in Hindi/English/Local language displayed on MV/HV panels.")

    st.button("📥 Generate & Export Audit Report (PDF)")

# --- MODULE 5: PTW GENERATOR ---
elif module == "📄 Permit-to-Work (PTW) Generator":
    st.header("📄 Permit-to-Work (PTW) Generator")
    st.caption("Generates standardized isolation permits per IS 5216 (Safety Procedures).")

    with st.form("ptw_form"):
        st.text_input("Work Location / Equipment ID")
        st.text_input("Name of Authorized Electrical Supervisor")
        st.multiselect("Safety Precautions Verified:", [
            "Main breaker locked out & tagged (LOTO)",
            "Supply isolated and earth discharge rod applied",
            "Insulated rubber mats (IS 15652) placed at work station",
            "Personal Protective Equipment (PPE - Gloves, Visor) issued"
        ])
        st.date_input("Work Date")
        submitted = st.form_submit_button("Issue Digital PTW Certificate")
        if submitted:
            st.success("✅ Digital Permit-to-Work issued successfully!")

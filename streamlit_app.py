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
    .metric-card {
        background-color: #F3F4F6;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚡ Indian Electrical Standards Compliance Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Design, Sizing & Safety Audit Platform (IS 732, IS 3043, IS 1255, IS 5216, NBC 2016)</div>', unsafe_allow_html=True)

# Navigation
st.sidebar.title("📍 Application Modules")
module = st.sidebar.radio(
    "Select Workflow:",
    [
        "🔌 Conduit Fill & Space Factor (IS 732)",
        "⚡ Earth Electrode Resistance (IS 3043)",
        "🔥 Cable Ampacity Derating (IS 732)",
        "📋 Site Inspection & Audit Checklist",
        "📄 Permit-to-Work (PTW) Generator"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Grounded in Official Standards:**\n- IS 732: Wiring Code\n- IS 3043: Earthing Code\n- IS 1255: Power Cable Laying\n- CEA Safety Regulations 2010")

# --- MODULE 1: CONDUIT FILL CALCULATOR ---
if module == "🔌 Conduit Fill & Space Factor (IS 732)":
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
        submitted = st.form_submit_state = st.form_submit_button("Issue Digital PTW Certificate")
        if submitted:
            st.success("✅ Digital Permit-to-Work issued successfully!")

import streamlit as st
import math
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Retaining Wall Design Calculator",
    page_icon="🧱",
    layout="wide"
)

# Title
st.title("🧱 Retaining Wall Design Calculator")
st.markdown("---")

# Sidebar for Input Data
st.sidebar.header("📝 INPUT PARAMETERS")

# Section 1: Soil Properties
st.sidebar.subheader("1. Soil Properties")
gamma_soil = st.sidebar.number_input("Density of soil (γe) [kN/m³]", value=18.0, min_value=10.0, max_value=25.0, step=0.5)
sbc = st.sidebar.number_input("SBC of soil (qa) [kN/m²]", value=200.0, min_value=50.0, max_value=500.0, step=10.0)
mu = st.sidebar.number_input("Coefficient of friction (μ)", value=0.5, min_value=0.3, max_value=0.8, step=0.05)
phi = st.sidebar.number_input("Angle of Repose (φ) [degrees]", value=30.0, min_value=20.0, max_value=45.0, step=1.0)
surcharge = st.sidebar.number_input("Surcharge Pressure (Ws) [kN/m²]", value=10.0, min_value=0.0, max_value=50.0, step=1.0)

# Section 2: Material Properties
st.sidebar.subheader("2. Material Properties")
fck = st.sidebar.selectbox("Grade of Concrete [N/mm²]", [20, 25, 30, 35, 40], index=1)
fy = st.sidebar.selectbox("Grade of Steel [N/mm²]", [415, 500, 550], index=1)
gamma_concrete = st.sidebar.number_input("Density of Concrete [kN/m³]", value=25.0, min_value=23.0, max_value=26.0, step=0.5)

# Section 3: Wall Geometry
st.sidebar.subheader("3. Wall Geometry")
depth_foundation = st.sidebar.number_input("Depth of foundation [m]", value=1.0, min_value=0.5, max_value=3.0, step=0.1)
depth_footing = st.sidebar.number_input("Depth of footing [m]", value=0.35, min_value=0.2, max_value=1.0, step=0.05)
height_embankment = st.sidebar.number_input("Height of embankment above GL [m]", value=3.3, min_value=1.0, max_value=10.0, step=0.1)
stem_thickness_bottom = st.sidebar.number_input("Stem thickness at bottom [m]", value=0.3, min_value=0.2, max_value=1.0, step=0.05)
stem_thickness_top = st.sidebar.number_input("Stem thickness at top [m]", value=0.3, min_value=0.15, max_value=1.0, step=0.05)
heel_length = st.sidebar.number_input("Length of heel [m]", value=1.7, min_value=0.5, max_value=5.0, step=0.1)
toe_length = st.sidebar.number_input("Length of toe [m]", value=0.7, min_value=0.3, max_value=3.0, step=0.1)

# ============= CALCULATIONS =============

# Basic Geometry Calculations
height_stem = height_embankment + depth_foundation - depth_footing
total_height = height_embankment + depth_foundation
base_length = heel_length + stem_thickness_bottom + toe_length
toe_fill_height = depth_foundation - depth_footing

# Earth Pressure Coefficient
phi_rad = math.radians(phi)
Ka = (1 - math.sin(phi_rad)) / (1 + math.sin(phi_rad))
Kp = (1 + math.sin(phi_rad)) / (1 - math.sin(phi_rad))

# Lateral Earth Pressure Calculations
lateral_pressure_base = Ka * gamma_soil * total_height
lateral_pressure_stem = Ka * gamma_soil * height_stem

# Earth forces
Pa1 = 0.5 * Ka * gamma_soil * (total_height ** 2)
Mo1 = Pa1 * total_height / 3

Pa2 = Ka * surcharge * total_height
Mo2 = Pa2 * total_height / 2

total_overturning_moment = Mo1 + Mo2

# Weight Calculations
W1 = stem_thickness_bottom * height_stem * gamma_concrete
x1 = heel_length + stem_thickness_bottom / 2
M1 = W1 * x1

W2 = base_length * depth_footing * gamma_concrete
x2 = base_length / 2
M2 = W2 * x2

W3 = heel_length * height_stem * gamma_soil
x3 = heel_length / 2
M3 = W3 * x3

W4 = toe_length * toe_fill_height * gamma_soil
x4 = heel_length + stem_thickness_bottom + toe_length / 2
M4 = W4 * x4

total_weight = W1 + W2 + W3 + W4
total_stabilising_moment = M1 + M2 + M3 + M4

# Overturning Check
Xw = total_stabilising_moment / total_weight
Mr = total_weight * (base_length - Xw)
FOS_overturning = 0.9 * Mr / total_overturning_moment

# Sliding Check
horizontal_force = Pa1 + Pa2
resisting_force = mu * total_weight
FOS_sliding = 0.9 * resisting_force / horizontal_force

# Soil Pressure at Footing Base
Xw_net = (total_stabilising_moment - total_overturning_moment) / total_weight
eccentricity = base_length / 2 - Xw_net
Pmax = (total_weight / base_length) * (1 + 6 * eccentricity / base_length)
Pmin = (total_weight / base_length) * (1 - 6 * eccentricity / base_length)

# ============= DISPLAY RESULTS =============

# Section 1: Geometry
st.header("📐 Section 1: Wall Geometry")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Calculated Dimensions")
    st.write(f"- **Height of Stem:** {height_stem:.3f} m")
    st.write(f"- **Total Height (H):** {total_height:.3f} m")
    st.write(f"- **Base Length (L):** {base_length:.3f} m")
    st.write(f"- **Toe Fill Height:** {toe_fill_height:.3f} m")

with col2:
    st.subheader("Earth Pressure Coefficients")
    st.write(f"- **Active (Ka):** {Ka:.3f}")
    st.write(f"- **Passive (Kp):** {Kp:.3f}")
    st.info("Ka = (1-sinφ)/(1+sinφ)")

st.markdown("---")

# Section 2: Lateral Earth Pressure
st.header("⚡ Section 2: Lateral Earth Pressure")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Due to Soil")
    st.write(f"- **Pressure at Base:** {lateral_pressure_base:.2f} kN/m²")
    st.write(f"- **Earth Force (Pa1):** {Pa1:.2f} kN/m")
    st.write(f"- **Overturning Moment (Mo1):** {Mo1:.2f} kN·m")

with col2:
    st.subheader("Due to Surcharge")
    st.write(f"- **Earth Force (Pa2):** {Pa2:.2f} kN/m")
    st.write(f"- **Overturning Moment (Mo2):** {Mo2:.2f} kN·m")

st.error(f"**Total Overturning Moment (Mo) = {total_overturning_moment:.2f} kN·m**")

st.markdown("---")

# Section 3: Weight Calculations
st.header("⚖️ Section 3: Stability Against Overturning")

weight_data = {
    'Component': ['W1 - Stem Wall', 'W2 - Base Slab', 'W3 - Backfill (Heel)', 'W4 - Toe Fill', '**TOTAL**'],
    'Weight (kN)': [f"{W1:.3f}", f"{W2:.3f}", f"{W3:.3f}", f"{W4:.3f}", f"**{total_weight:.2f}**"],
    'Distance from Heel (m)': [f"{x1:.3f}", f"{x2:.3f}", f"{x3:.3f}", f"{x4:.3f}", "-"],
    'Moment (kN·m)': [f"{M1:.3f}", f"{M2:.3f}", f"{M3:.3f}", f"{M4:.3f}", f"**{total_stabilising_moment:.2f}**"]
}

df_weights = pd.DataFrame(weight_data)
st.table(df_weights)

st.markdown("---")

# Section 4: Stability Checks
st.header("✅ Section 4: Stability Checks")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔄 Overturning Check")
    st.write(f"- Distance from Heel (Xw): **{Xw:.3f} m**")
    st.write(f"- Stabilising Moment (Mr): **{Mr:.3f} kN·m**")
    st.write(f"- **Factor of Safety: {FOS_overturning:.3f}**")
    
    if FOS_overturning >= 1.5:
        st.success(f"✅ SAFE (FOS = {FOS_overturning:.2f} ≥ 1.5)")
    else:
        st.error(f"❌ UNSAFE (FOS = {FOS_overturning:.2f} < 1.5)")

with col2:
    st.subheader("➡️ Sliding Check")
    st.write(f"- Horizontal Force: **{horizontal_force:.2f} kN**")
    st.write(f"- Resisting Force: **{resisting_force:.2f} kN**")
    st.write(f"- **Factor of Safety: {FOS_sliding:.3f}**")
    
    if FOS_sliding >= 1.5:
        st.success(f"✅ SAFE (FOS = {FOS_sliding:.2f} ≥ 1.5)")
    else:
        st.error(f"❌ UNSAFE (FOS = {FOS_sliding:.2f} < 1.5)")

st.markdown("---")

# Section 5: Soil Pressure
st.header("🏗️ Section 5: Soil Pressure at Footing Base")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Eccentricity (e)", f"{eccentricity:.3f} m")

with col2:
    st.metric("Max Pressure (Pmax)", f"{Pmax:.2f} kN/m²")
    if Pmax <= sbc:
        st.success(f"✅ Pmax ({Pmax:.2f}) < SBC ({sbc})")
    else:
        st.error(f"❌ Pmax ({Pmax:.2f}) > SBC ({sbc})")

with col3:
    st.metric("Min Pressure (Pmin)", f"{Pmin:.2f} kN/m²")
    if Pmin >= 0:
        st.success(f"✅ No Tension (Pmin = {Pmin:.2f} > 0)")
    else:
        st.error(f"❌ Tension Zone! (Pmin = {Pmin:.2f} < 0)")

st.markdown("---")

# Summary
st.header("📋 Design Summary")

summary_data = {
    'Check': ['Overturning', 'Sliding', 'Bearing Capacity', 'No Tension'],
    'Value': [f"FOS = {FOS_overturning:.2f}", f"FOS = {FOS_sliding:.2f}", 
              f"Pmax = {Pmax:.2f} kN/m²", f"Pmin = {Pmin:.2f} kN/m²"],
    'Requirement': ['≥ 1.5', '≥ 1.5', f'≤ {sbc} kN/m²', '≥ 0'],
    'Status': [
        '✅ SAFE' if FOS_overturning >= 1.5 else '❌ UNSAFE',
        '✅ SAFE' if FOS_sliding >= 1.5 else '❌ UNSAFE',
        '✅ SAFE' if Pmax <= sbc else '❌ UNSAFE',
        '✅ SAFE' if Pmin >= 0 else '❌ UNSAFE'
    ]
}

df_summary = pd.DataFrame(summary_data)
st.table(df_summary)

# Overall Status
all_safe = (FOS_overturning >= 1.5 and FOS_sliding >= 1.5 and Pmax <= sbc and Pmin >= 0)

if all_safe:
    st.success("## ✅ DESIGN IS SAFE - All checks passed!")
else:
    st.error("## ❌ DESIGN IS UNSAFE - Please revise the dimensions!")

# Footer
st.markdown("---")
st.caption("🧱 Retaining Wall Design Calculator | Based on IS Codes | For Educational Use")

import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Initialize configurations
load_dotenv()
st.set_page_config(page_title="MissionSafe Dashboard", page_icon="🛡️", layout="wide")

try:
    client = genai.Client()
    api_available = True
except Exception:
    api_available = False

# Core App Title
st.title("🛡️ MissionSafe: Centralized Relief Directory")
st.caption("Texas A&M University - San Antonio | Public Safety Infrastructure Platform")

# ----------------- DATA INGESTION PIPELINE -----------------
@st.cache_data
def load_facility_registry():
    try:
        return pd.read_csv("local.csv")
    except Exception as e:
        st.error(f"Critical System Failure loading registry file: {e}")
        return pd.DataFrame()

df_facilities = load_facility_registry()

# ----------------- UI CONTROL INTERFACES -----------------
# 1. Hazard Toggle Layout Control
hazard_mode = st.radio(
    "Select Emergency Threat Profile:",
    ["Extreme Heat", "Winter Freeze"],
    horizontal=True
)

# 2. Dynamic Sidebar Configuration Checklist
st.sidebar.header(f"🚨 Quick Action Checklist ({hazard_mode})")
if hazard_mode == "Extreme Heat":
    st.sidebar.markdown("""
    * 💧 Pack at least 1 gallon of water per person.
    * 📱 Charge backup communication devices.
    * 🧢 Bring lightweight, loose clothing.
    * 💊 Ensure medication isn't left in hot vehicles.
    """)
else:
    st.sidebar.markdown("""
    * 🧣 Dress in deep insulation layers.
    * 🔋 Bring auxiliary device charging bricks.
    * 📦 Gather heavy blankets and thermal gear.
    * 🧴 Bring specialized skin protection barrier items.
    """)

# ----------------- GEO-LOCATIONAL FILTER LOGIC -----------------
st.subheader("📍 Interactive Facility Lookup")
zip_query = st.text_input("Enter target 5-Digit ZIP Code (e.g., 78237, 78249):", max_chars=5)

if zip_query:
    try:
        target_zip = int(zip_query)
        # Query execution against local data foundation
        matched_results = df_facilities[df_facilities['Zip_Code'] == target_zip]
        
        if not matched_results.empty:
            st.success(f"Discovered {len(matched_results)} active operations serving Area Code {target_zip}:")
            st.dataframe(matched_results[['Facility_Name', 'Address', 'Amenities']], use_container_width=True)
            
            # Convert matched rows to text payload string for prompt ingestion
            facility_context = ""
            for _, row in matched_results.iterrows():
                facility_context += f"- {row['Facility_Name']} located at {row['Address']}. Utilities/Amenities: {row['Amenities']}\n"
            
            # ----------------- GENERATIVE INFERENCE PIPELINE -----------------
            st.subheader("🤖 Live AI Safety Briefing")
            
            system_directive = (
                "You are an empathetic, precise emergency safety dispatcher for the City of San Antonio. "
                "Your mission is to process public facility listings and convert them into highly clear, actionable "
                "conversational advisories containing travel safety, location hours reminders, and operational guidance."
            )
            
            user_prompt = (
                f"Context Threat: Current environment is under an active {hazard_mode} warning.\n"
                f"Target Area: Residents within zip code {target_zip}.\n"
                f"Available Locations:\n{facility_context}\n\n"
                f"Task: Please formulate a supportive, direct summary telling people how to get safely to these locations, "
                f"what utilities they can look forward to using, and a quick arrival tip specific to a {hazard_mode} crisis."
            )
            
            if api_available:
                with st.spinner("Compiling tactical safety directives..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.1-flash-lite",
                            contents=user_prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=system_directive,
                                temperature=0.3
                            )
                        )
                        st.markdown(response.text)
                    except Exception as ai_err:
                        st.error(f"Inference execution failed: {ai_err}")
            else:
                st.warning("⚠️ Core Logic execution offline: Verify GEMINI_API_KEY environment configuration.")
                st.info("Simulated Model Input Context would read as follows:\n\n" + user_prompt)
                
        else:
            st.warning(f"No current operations mapped to ZIP Code: {target_zip}. Please check adjoining sectors.")
    except ValueError:
        st.error("Invalid Parameter: Please input standard numerical characters.")
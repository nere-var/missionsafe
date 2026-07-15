# MissionSafe - Heating and Cooling Centers
## Emma Whitehead - CSCI4313 - Summer 2026

## 📌 Project Overview
**MissionSafe** is a centralized public safety directory designed to protect vulnerable populations from San Antonio's extreme climate challenges, specifically severe summer heat and winter freezes.

When the City of San Antonio opens dynamic emergency shelters, finding accurate, centralized information can be difficult. This application bridges that gap by allowing users to instantly look up verified local relief centers by zip code and receive an empathetic, dynamic, AI-generated safety advisory.

### Key Features
*   **Hazard Toggle UI:** Dynamically switch the layout and preparedness focus between Extreme Heat and Winter Freeze modes.
*   **Interactive Zip Code Lookup:** Filter localized facility data quickly from a structured offline dataset (`local.csv`).
*   **AI Safety Summary:** Leverage Google’s lightweight `gemini-3.1-flash-lite` model to turn tabular facility lists into highly clear, actionable arrival briefs and travel advice.
*   **Dynamic Emergency Sidebar:** A contextual sidebar providing immediate, threat-specific emergency checklists.

---

## 🛠️ Technical Architecture
*   **Frontend UI:** Streamlit (Python)
*   **Data Processing:** Pandas (programmatic offline filtering)
*   **Generative AI Layer:** Modern `google-genai` SDK using the `gemini-3.1-flash-lite` engine
*   **Data Registry:** Localized, static CSV database (`local.csv`)

---

## Streamlit App Preview
<img width="1296" height="1122" alt="image" src="https://github.com/user-attachments/assets/6329949f-7ecc-4c4b-8d89-8c2bdbf97731" />

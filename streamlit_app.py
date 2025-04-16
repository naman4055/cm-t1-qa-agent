import streamlit as st
import pandas as pd

st.set_page_config(page_title="CM vs T1 QA Agent", layout="wide")

st.title("🧠 CM vs T1 QA Agent")
st.markdown("Upload your **CM Legacy Spreadsheet** and **T1 Trafficking Sheet** to begin QA.")

legacy_file = st.file_uploader("Upload CM Legacy Sheet", type=["xlsx"])
t1_file = st.file_uploader("Upload T1 Trafficking Sheet", type=["xlsx", "xlsm"])

field_mapping = {
    "Site Name": "SITE NAME",
    "Placement Name": "PLACEMENT NAME",
    "Placement Compatibility": "PLACEMENT TYPE",
    "Dimensions": "DISPLAY DIMENSION",
    "Placement Duration": "VIDEO DURATION",
    "Start Date": "PLACEMENT START DATE",
    "End Date": "PLACEMENT END DATE",
    "Creative Name": "CREATIVE NAME",
    "Creative Start Date": "CREATIVE START DATE",
    "Creative End Date": "CREATIVE END DATE",
    "Creative Type": "CREATIVE TYPE",
    "Rotation Value": "ROTATION",
    "Creative Click-Through URL": "FINAL CLICK-THROUGH URL",
}

if legacy_file and t1_file:
    legacy_df = pd.read_excel(legacy_file)
    t1_df = pd.read_excel(t1_file)

    st.subheader("🔍 QA Results")
    mismatches = []

    for cm_col, t1_col in field_mapping.items():
        if cm_col in legacy_df.columns and t1_col in t1_df.columns:
            merged = legacy_df[[cm_col]].copy()
            merged["T1"] = t1_df[t1_col]
            merged["Field"] = cm_col
            merged["Match"] = merged[cm_col].astype(str).str.strip() == merged["T1"].astype(str).str.strip()
            mismatches.extend(merged[~merged["Match"]].to_dict("records"))

    if mismatches:
        mismatch_df = pd.DataFrame(mismatches)[["Field", cm_col, "T1"]]
        st.error("❌ Mismatches Found")
        st.dataframe(mismatch_df, use_container_width=True)
        csv = mismatch_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Mismatch Report", csv, "qa_mismatches.csv", "text/csv")
    else:
        st.success("✅ All fields matched successfully!")

else:
    st.info("Please upload both files to begin comparison.")

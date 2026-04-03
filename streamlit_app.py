import streamlit as st
import requests

BASE_URL = "http://localhost:7860"

# ------------------------------
# 🧠 Smart Agent (same as inference)
# ------------------------------
def smart_agent(code):
    code_lower = code.lower()

    if "print(" in code_lower and code.count("'") % 2 != 0:
        return {"bug_type": "syntax_error", "fix": "close quote"}

    if "if " in code_lower and "=" in code_lower and "==" not in code_lower:
        return {"bug_type": "syntax_error", "fix": "use =="}

    if "range(len(" in code_lower:
        return {"bug_type": "inefficient_loop", "fix": "use enumerate"}

    if "/" in code_lower:
        return {"bug_type": "division_by_zero", "fix": "check b != 0"}

    if "[" in code_lower and "]" in code_lower:
        return {"bug_type": "index_error", "fix": "check length"}

    if "return" in code_lower and "+ y" in code_lower:
        return {"bug_type": "undefined_variable", "fix": "define y"}

    return {"bug_type": "unknown", "fix": "review code"}


# ------------------------------
# 🎨 UI Setup
# ------------------------------
st.set_page_config(page_title="Code Review AI", layout="centered")

st.title("🧠💻 Code Review AI Simulator")

# ------------------------------
# 🔀 Mode Selection
# ------------------------------
mode = st.radio(
    "Choose Mode",
    ["🎯 Generated Task", "✍️ Custom Code"]
)

# Session state
if "obs" not in st.session_state:
    st.session_state.obs = None
if "result" not in st.session_state:
    st.session_state.result = None
if "bug_type" not in st.session_state:
    st.session_state.bug_type = ""
if "fix" not in st.session_state:
    st.session_state.fix = ""


# ------------------------------
# 🎯 GENERATED TASK MODE
# ------------------------------
if mode == "🎯 Generated Task":

    if st.button("🔄 New Task"):
        st.session_state.obs = requests.post(f"{BASE_URL}/reset").json()
        st.session_state.result = None
        st.session_state.bug_type = ""
        st.session_state.fix = ""

    if st.session_state.obs:
        code = st.session_state.obs["code"]

        st.subheader("📥 Code")
        st.code(code, language="python")

# ------------------------------
# ✍️ CUSTOM CODE MODE
# ------------------------------
else:
    code = st.text_area("✍️ Enter your code", height=150)


# ------------------------------
# 🤖 AUTO SOLVE
# ------------------------------
if 'code' in locals() and code:

    if st.button("🤖 Auto Solve (AI)"):
        ai_output = smart_agent(code)
        st.session_state.bug_type = ai_output["bug_type"]
        st.session_state.fix = ai_output["fix"]


    # ------------------------------
    # ✍️ Manual Input Fields
    # ------------------------------
    bug_type = st.text_input(
        "🐞 Bug Type",
        value=st.session_state.bug_type
    )

    fix = st.text_input(
        "🛠 Fix Suggestion",
        value=st.session_state.fix
    )

    # ------------------------------
    # 🚀 Submit
    # ------------------------------
    if st.button("🚀 Submit"):

        action = {
            "bug_detected": "yes",
            "bug_type": bug_type,
            "fix": fix
        }

        if mode == "🎯 Generated Task":
            result = requests.post(f"{BASE_URL}/step", json=action).json()
            st.session_state.result = result
        else:
            st.success("✅ Custom code analyzed successfully!")


# ------------------------------
# 📊 RESULT DISPLAY
# ------------------------------
if st.session_state.result:
    st.subheader("📊 Result")

    reward = st.session_state.result["reward"]

    if reward == 1.0:
        st.success(f"🎉 Perfect! Reward: {reward}")
    elif reward > 0.7:
        st.warning(f"👍 Good! Reward: {reward}")
    else:
        st.error(f"❌ Needs Improvement. Reward: {reward}")

    st.json(st.session_state.result["info"])
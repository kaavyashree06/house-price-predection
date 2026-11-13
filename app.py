
st.markdown("""
<style>

/* ===== GLOBAL THEME ===== */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255,255,255,0.9), transparent 35%),
        linear-gradient(135deg, #eee0ce, #d9c1a5, #f4e9dc);
    color: #493629;
    font-family: 'Segoe UI', sans-serif;
}

/* ===== MAIN CONTENT ===== */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* ===== HEADINGS ===== */
h1, h2, h3, h4 {
    color: #493629 !important;
    font-weight: 700 !important;
}

p, label, span, div {
    font-family: 'Segoe UI', sans-serif;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: rgba(255, 248, 239, 0.65);
    backdrop-filter: blur(25px);
    border-right: 1px solid rgba(255,255,255,0.7);
}

section[data-testid="stSidebar"] * {
    color: #513d2e;
}

/* ===== GLASS CONTAINERS ===== */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 250, 244, 0.48);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255,255,255,0.75);
    border-radius: 22px;
    box-shadow: 0 8px 30px rgba(91, 61, 36, 0.10);
    padding: 15px;
    transition: all 0.3s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 12px 35px rgba(91, 61, 36, 0.16);
    transform: translateY(-2px);
}

/* ===== METRIC CARDS ===== */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.52);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(80,50,25,0.08);
}

div[data-testid="stMetricLabel"] {
    color: #82674f !important;
}

div[data-testid="stMetricValue"] {
    color: #493629 !important;
    font-weight: 700;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, #9c7654, #694a32);
    color: white !important;
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 14px;
    padding: 0.65rem 1.4rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(80,50,25,0.15);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #765338, #4e3524);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(80,50,25,0.2);
}

/* ===== INPUT FIELDS ===== */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"],
.stDateInput input,
.stTextArea textarea {
    background: rgba(255,255,255,0.65) !important;
    color: #493629 !important;
    border: 1px solid rgba(130,100,70,0.25) !important;
    border-radius: 12px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border: 1px solid #9c7654 !important;
    box-shadow: 0 0 0 2px rgba(156,118,84,0.15) !important;
}

/* ===== SELECT BOX ===== */
.stSelectbox {
    border-radius: 12px;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(255,255,255,0.35);
    padding: 8px;
    border-radius: 14px;
}

.stTabs [data-baseweb="tab"] {
    color: #694a32;
    border-radius: 10px;
}

.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.8);
    color: #493629 !important;
}

/* ===== DATAFRAMES ===== */
div[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* ===== ALERTS ===== */
div[data-testid="stAlert"] {
    background: rgba(255,255,255,0.65);
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.8);
}

/* ===== DIVIDERS ===== */
hr {
    border-color: rgba(105,74,50,0.18);
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #eee0ce;
}

::-webkit-scrollbar-thumb {
    background: #ad8b6b;
    border-radius: 10px;
}

/* ===== SMOOTH ANIMATIONS ===== */
.stMarkdown, .stButton, .stMetric {
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

</style>
""", unsafe_allow_html=True)

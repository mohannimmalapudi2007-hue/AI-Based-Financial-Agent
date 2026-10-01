import os
import sys
import subprocess

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

OUTPUT_FILE = os.path.join(
    ROOT,
    "output.csv"
)

st.set_page_config(
    page_title="Buy or Wait AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# STYLE
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .status-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 10px;
    }

    .small-label {
        color: #6b7280;
        font-size: 13px;
    }

    .big-value {
        font-size: 26px;
        font-weight: 700;
    }

    /* Floating AI assistant */
    div[data-testid="stPopover"] {
        position: fixed !important;
        right: 28px !important;
        bottom: 28px !important;
        z-index: 999999 !important;
        width: 60px !important;
        min-width: 60px !important;
        max-width: 60px !important;
    }

    div[data-testid="stPopover"] > button {
        width: 58px !important;
        min-width: 58px !important;
        max-width: 58px !important;
        height: 58px !important;
        min-height: 58px !important;
        max-height: 58px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 50% !important;
        font-size: 24px !important;
        line-height: 1 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.18) !important;
        border: 1px solid #e5e7eb !important;
        background: white !important;
    }

    div[data-testid="stPopover"] > button p {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 24px !important;
    }

    .chat-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .chat-subtitle {
        color: #6b7280;
        font-size: 13px;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_output():

    if not os.path.exists(OUTPUT_FILE):
        return pd.DataFrame()

    return pd.read_csv(OUTPUT_FILE)


df = load_output()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="dashboard-title">💰 Buy or Wait AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'AI-powered financial affordability and payment recommendation system'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Controls")

    if st.button(
        "🔄 Refresh Predictions",
        use_container_width=True
    ):

        result = subprocess.run(
            [
                sys.executable,
                os.path.join(
                    ROOT,
                    "code",
                    "main.py"
                ),
                "--requests-file",
                os.path.join(
                    ROOT,
                    "dataset",
                    "requests.csv"
                ),
                "--output",
                OUTPUT_FILE
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            st.cache_data.clear()

            st.success(
                "Predictions refreshed successfully."
            )

            st.rerun()

        else:

            st.error(
                result.stderr
            )

    st.divider()

    st.subheader("Filter")

    if not df.empty:

        statuses = sorted(
            df["affordability_status"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_status = st.multiselect(
            "Affordability",
            statuses,
            default=statuses
        )

        methods = sorted(
            df["recommended_payment_method"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_method = st.multiselect(
            "Payment Method",
            methods,
            default=methods
        )

    else:

        selected_status = []
        selected_method = []


# ---------------------------------------------------------
# EMPTY DATA
# ---------------------------------------------------------

if df.empty:

    st.error(
        "output.csv was not found. "
        "Run the financial agent first."
    )

    st.stop()


# ---------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------

filtered = df[
    df["affordability_status"].isin(
        selected_status
    )
    &
    df["recommended_payment_method"].isin(
        selected_method
    )
].copy()


# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

total = len(filtered)

affordable_now = len(
    filtered[
        filtered["affordability_status"]
        == "affordable_now"
    ]
)

with_plan = len(
    filtered[
        filtered["affordability_status"]
        == "affordable_with_plan"
    ]
)

later = len(
    filtered[
        filtered["affordability_status"]
        == "affordable_later"
    ]
)

not_affordable = len(
    filtered[
        filtered["affordability_status"]
        == "not_affordable"
    ]
)


st.subheader("📊 Financial Overview")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.metric(
        "Total Requests",
        total
    )

with c2:

    st.metric(
        "Affordable Now",
        affordable_now
    )

with c3:

    st.metric(
        "With Plan",
        with_plan
    )

with c4:

    st.metric(
        "Later",
        later
    )

with c5:

    st.metric(
        "Not Affordable",
        not_affordable
    )


st.divider()


# ---------------------------------------------------------
# CHARTS
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader(
        "Affordability Distribution"
    )

    status_data = (
        filtered[
            "affordability_status"
        ]
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status_data,
        names="Status",
        values="Count",
        hole=0.55
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        ),
        legend_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right:

    st.subheader(
        "Recommended Payment Methods"
    )

    method_data = (
        filtered[
            "recommended_payment_method"
        ]
        .value_counts()
        .reset_index()
    )

    method_data.columns = [
        "Method",
        "Count"
    ]

    fig = px.bar(
        method_data,
        x="Method",
        y="Count",
        text="Count"
    )

    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        ),
        xaxis_title="",
        yaxis_title="Requests"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# TOP RECOMMENDED ACTIONS
# ---------------------------------------------------------

st.subheader("💡 Recommended Actions")

action_counts = (
    filtered["recommended_payment_method"]
    .value_counts()
    .reset_index()
)

action_counts.columns = [
    "Action",
    "Requests"
]

if not action_counts.empty:

    action_cols = st.columns(
        len(action_counts)
    )

    for col, (_, action) in zip(
        action_cols,
        action_counts.iterrows()
    ):

        method = str(
            action["Action"]
        ).replace(
            "_",
            " "
        ).title()

        count = int(
            action["Requests"]
        )

        with col:

            st.metric(
                method,
                count
            )
# ---------------------------------------------------------
# REQUEST SEARCH
# ---------------------------------------------------------

st.divider()

st.subheader("🔎 Request Analysis")

search = st.text_input(
    "Search Request ID",
    placeholder="Example: request_125"
)


if search:

    search_result = filtered[
        filtered["request_id"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

else:

    search_result = filtered


# ---------------------------------------------------------
# REQUEST TABLE
# ---------------------------------------------------------

display_columns = [
    "request_id",
    "amount_safe_to_pay",
    "affordability_status",
    "recommended_payment_method",
    "earliest_date_for_full_payment",
    "spending_changes_needed"
]

st.dataframe(
    search_result[display_columns],
    use_container_width=True,
    hide_index=True
)


# ---------------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------------

st.download_button(
    label="⬇️ Download Filtered Report",
    data=search_result.to_csv(
        index=False
    ).encode("utf-8"),
    file_name="buy_or_wait_report.csv",
    mime="text/csv",
    use_container_width=True
)


# ---------------------------------------------------------
# REQUEST DETAILS
# ---------------------------------------------------------

if not search_result.empty:

    st.divider()

    st.subheader("📋 Request Details")

    selected_request = st.selectbox(
        "Select a request",
        search_result["request_id"].tolist()
    )

    row = search_result[
        search_result["request_id"]
        == selected_request
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            '<div class="metric-card">'
            '<div class="small-label">Request ID</div>'
            f'<div class="big-value">'
            f'{row["request_id"]}'
            f'</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            '<div class="metric-card">'
            '<div class="small-label">Safe Amount</div>'
            f'<div class="big-value">'
            f'{row["amount_safe_to_pay"]:,.2f}'
            f'</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            '<div class="metric-card">'
            '<div class="small-label">Payment Method</div>'
            f'<div class="big-value">'
            f'{row["recommended_payment_method"]}'
            f'</div>'
            '</div>',
            unsafe_allow_html=True
        )


    st.write("")

    d1, d2 = st.columns(2)

    with d1:

        st.markdown(
            "### Affordability"
        )

        st.info(
            str(
                row[
                    "affordability_status"
                ]
            ).replace(
                "_",
                " "
            ).title()
        )

        st.markdown(
            "**Earliest Full Payment Date:** "
            + str(
                row[
                    "earliest_date_for_full_payment"
                ]
            )
        )


    with d2:

        st.markdown(
            "### Spending Changes"
        )

        st.info(
            str(
                row[
                    "spending_changes_needed"
                ]
            )
        )


    st.markdown(
        "### 💳 Payment Plan"
    )

    st.code(
        str(
            row[
                "payment_plan"
            ]
        ),
        language="text"
    )
    # ---------------------------------------------------------
# AI CONFIDENCE
# ---------------------------------------------------------

status = str(
    row["affordability_status"]
)

method = str(
    row["recommended_payment_method"]
)

safe_amount = float(
    row["amount_safe_to_pay"]
)

confidence = "Medium"

if status == "affordable_now" and safe_amount > 0:
    confidence = "High"

elif status == "affordable_with_plan" and safe_amount > 0:
    confidence = "High"

elif status == "affordable_later":
    confidence = "Medium"

elif status == "not_affordable":
    confidence = "Medium"


st.markdown(
    "### 🎯 AI Confidence"
)

if confidence == "High":

    st.success(
        "High Confidence — strong affordability evidence."
    )

elif confidence == "Medium":

    st.info(
        "Medium Confidence — decision depends on future financial conditions."
    )

else:

    st.warning(
        "Low Confidence — limited evidence available."
    )


    st.markdown(
        "### 🤖 AI Decision Explanation"
    )

    st.success(
        str(
            row[
                "decision_explanation"
            ]
        )
    )



# ---------------------------------------------------------
# AI CHATBOT
# ---------------------------------------------------------

with st.popover("🤖", use_container_width=False):

    st.markdown(
        '<div class="chat-title">?? Buy or Wait AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="chat-subtitle">'
        'Ask me about affordability, payments, spending, or your requests.'
        '</div>',
        unsafe_allow_html=True
    )

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask your financial question..."
    )

    if question:

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        q = question.lower().strip()

        answer = None

        # Request ID lookup
        request_matches = df[
            df["request_id"]
            .astype(str)
            .str.lower()
            .str.contains(q.replace("request ", ""), na=False)
        ]

        if not request_matches.empty:

            r = request_matches.iloc[0]

            answer = (
                f"### Request {r['request_id']}\n\n"
                f"**Safe amount:** {r['amount_safe_to_pay']:,.2f}\n\n"
                f"**Affordability:** "
                f"{str(r['affordability_status']).replace('_', ' ').title()}\n\n"
                f"**Recommended method:** "
                f"{str(r['recommended_payment_method']).replace('_', ' ').title()}\n\n"
                f"**Payment plan:** {r['payment_plan']}\n\n"
                f"**Earliest full payment:** "
                f"{r['earliest_date_for_full_payment']}\n\n"
                f"**Why:** {r['decision_explanation']}"
            )

        elif any(
            word in q
            for word in [
                "how many requests",
                "total requests",
                "number of requests"
            ]
        ):

            answer = (
                f"There are **{len(df)} financial requests** "
                f"in the current dataset."
            )

        elif any(
            word in q
            for word in [
                "affordable now",
                "can afford now",
                "affordable today"
            ]
        ):

            count = len(
                df[
                    df["affordability_status"]
                    == "affordable_now"
                ]
            )

            answer = (
                f"**{count} requests** are currently classified "
                f"as affordable now."
            )

        elif any(
            word in q
            for word in [
                "installment",
                "installments"
            ]
        ):

            count = len(
                df[
                    df["recommended_payment_method"]
                    == "installments"
                ]
            )

            answer = (
                f"**{count} requests** currently have "
                f"installments as the recommended payment method."
            )

        elif any(
            word in q
            for word in [
                "not affordable",
                "cannot afford",
                "can't afford"
            ]
        ):

            count = len(
                df[
                    df["affordability_status"]
                    == "not_affordable"
                ]
            )

            answer = (
                f"**{count} requests** are currently classified "
                f"as not affordable."
            )

        elif any(
            word in q
            for word in [
                "wait",
                "later",
                "when can i pay"
            ]
        ):

            count = len(
                df[
                    df["recommended_payment_method"]
                    == "wait"
                ]
            )

            answer = (
                f"**{count} requests** currently recommend waiting "
                f"for a safer full-payment date."
            )

        elif any(
            word in q
            for word in [
                "payment method",
                "recommended method"
            ]
        ):

            counts = (
                df["recommended_payment_method"]
                .value_counts()
            )

            answer = "### Recommended Payment Methods\n\n"

            for method, count in counts.items():
                answer += (
                    f"- **{str(method).replace('_', ' ').title()}**: "
                    f"{count}\n"
                )

        elif any(
            word in q
            for word in [
                "hello",
                "hi",
                "hey"
            ]
        ):

            answer = (
                "Hi! ?? I can help you understand the financial "
                "decisions in this dashboard. Try asking:\n\n"
                "- `Can I afford request_125?`\n"
                "- `How many requests are affordable now?`\n"
                "- `Which requests recommend installments?`\n"
                "- `How many requests should wait?`"
            )

        else:

            # Natural-language request matching
            requests_file = os.path.join(
                ROOT,
                "dataset",
                "requests.csv"
            )

            try:
                requests_data = pd.read_csv(requests_file)

                # Score requests against words in the user's question.
                question_words = {
                    word.strip(".,!?")
                    for word in q.split()
                    if len(word.strip(".,!?")) >= 4
                }

                best_match = None
                best_score = 0

                for _, request in requests_data.iterrows():

                    request_text = str(
                        request.get("request_text", "")
                    ).lower()

                    request_words = {
                        word.strip(".,!?")
                        for word in request_text.split()
                        if len(word.strip(".,!?")) >= 4
                    }

                    score = len(
                        question_words.intersection(request_words)
                    )

                    if score > best_score:
                        best_score = score
                        best_match = request

                if best_match is not None and best_score >= 2:

                    matched_id = str(
                        best_match["request_id"]
                    )

                    matched = df[
                        df["request_id"].astype(str)
                        == matched_id
                    ]

                    if not matched.empty:

                        r = matched.iloc[0]

                        status = str(
                            r["affordability_status"]
                        ).replace(
                            "_",
                            " "
                        ).title()

                        method = str(
                            r["recommended_payment_method"]
                        ).replace(
                            "_",
                            " "
                        ).title()

                        answer = (
                            f"### ?? Financial Assessment\n\n"
                            f"**Request:** {matched_id}\n\n"
                            f"**Safe amount:** "
                            f"{float(r['amount_safe_to_pay']):,.2f}\n\n"
                            f"**Affordability:** {status}\n\n"
                            f"**Recommended action:** {method}\n\n"
                            f"**Payment plan:** "
                            f"{r['payment_plan']}\n\n"
                            f"**Earliest full payment:** "
                            f"{r['earliest_date_for_full_payment']}\n\n"
                            f"**Explanation:** "
                            f"{r['decision_explanation']}"
                        )

            except Exception:
                answer = None

            if answer is None:
                answer = (
                    "I couldn't identify a specific request from "
                    "your question. Try including the item and amount, "
                    "for example:\n\n"
                    "**Can I afford a laptop for 80000?**\n\n"
                    "or use a request ID such as **request_125**."
                )

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()
st.divider()

# ---------------------------------------------------------
# STATUS SUMMARY
# ---------------------------------------------------------

st.subheader("📈 Affordability Summary")

if total > 0:

    summary_data = pd.DataFrame(
        {
            "Status": [
                "Affordable Now",
                "With Plan",
                "Later",
                "Not Affordable"
            ],
            "Requests": [
                affordable_now,
                with_plan,
                later,
                not_affordable
            ]
        }
    )

    summary_data["Percentage"] = (
        summary_data["Requests"]
        / total
        * 100
    ).round(1)

    st.dataframe(
        summary_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Percentage": st.column_config.ProgressColumn(
                "Percentage",
                format="%.1f%%",
                min_value=0,
                max_value=100
            )
        }
    )
st.caption(
    "Buy or Wait AI • Financial Decision Support Agent"
)
# 💰 AI-Based Financial Agent

> **An intelligent financial decision-support system that helps users determine whether they can safely afford an expense.**

The **AI-Based Financial Agent** goes beyond checking a user's current balance. It analyzes income, recurring expenses, pending payments, essential spending, minimum balance requirements, payment preferences, available payment options, and relevant financial information to provide a personalized recommendation.

For example:

> 💬 **"Can I afford this laptop?"**

The agent evaluates the user's financial situation and determines whether they should **pay in full, pay partially, use installments, wait, or not proceed**.

---

## 🚀 Key Features

### 💳 Smart Affordability Analysis

The agent calculates the maximum amount a user can safely spend while maintaining their required minimum balance and covering upcoming financial commitments.

### 📊 Financial Forecasting

The system forecasts the user's financial timeline by considering:

* 💰 Current available balance
* 💵 Confirmed income
* 🔄 Recurring expenses
* 🧾 Pending payments
* ⭐ Essential expenses
* 🏦 Minimum balance requirements
* 📅 Future financial events

### 🧠 Personalized Recommendations

Recommendations are based on each user's individual financial profile, commitments, priorities, payment preferences, and flexibility.

Possible recommendations include:

| Recommendation         | Meaning                                                                |
| ---------------------- | ---------------------------------------------------------------------- |
| 💵 **Full Payment**    | The expense can safely be paid in full                                 |
| 💳 **Partial Payment** | A safe portion can be paid now and the remaining amount later          |
| 📆 **Installments**    | The expense can be completed using an available installment plan       |
| ⏳ **Wait**             | The expense becomes affordable at a later date                         |
| 🚫 **Not Recommended** | The expense cannot be completed safely under the available constraints |

### 🔍 Financial Evidence

The system can work with supporting financial information from:

* 💬 User messages
* 🖼️ Financial images
* 📄 Statements
* 🧾 Bills and receipts
* 💼 Payment options

### 🤖 AI Financial Chatbot

The dashboard includes an interactive chatbot that allows users to ask natural-language questions about their financial requests.

Examples:

```text
Can I afford this laptop?

How much can I safely spend?

Should I wait or use installments?

How many requests are affordable now?

What payment method is recommended?
```

### 📈 Interactive Dashboard

The Streamlit dashboard provides:

* 📊 Financial overview
* 💰 Affordability statistics
* 💳 Payment-method analysis
* 🔎 Request search
* 📋 Detailed request analysis
* 🤖 AI chatbot
* 📥 Filtered report download

---

# 🏗️ System Architecture

```text
                       👤 USER
                           │
                           │ Financial Question
                           ▼
                 🤖 AI FINANCIAL AGENT
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   👤 Financial       💳 Payment       💬 Messages
      Profile            Options          & Images
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  🧠 Financial Analysis
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        💰 Balance     📅 Forecast    🛡️ Safety
          Analysis       Timeline        Checks
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                  📊 Decision Engine
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       Pay Now         Pay Later      Payment Plan
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  🤖 Recommendation
                           │
                           ▼
                 📊 Streamlit Dashboard
                           │
                           ▼
                     💬 AI Chatbot
```

---

# 🔄 How It Works

### 1️⃣ User Request

The system receives a financial request such as:

> **"Can I afford this laptop?"**

Each request contains information such as the requested amount, request date, desired completion date, and partial-payment preference.

### 2️⃣ User Financial Profile

The agent retrieves the user's financial profile, including:

* Current balance
* Minimum balance to maintain
* Home currency
* Financial priorities
* Spending preferences
* Accepted payment methods

### 3️⃣ Financial Events

The system analyzes historical and future financial events.

It distinguishes between:

* Income
* Expenses
* Recurring transactions
* Pending transactions
* Confirmed payments
* Other financial events

### 4️⃣ Forecast

The agent builds a financial timeline and forecasts the user's balance over the required period.

The system checks whether the balance remains above the user's preferred minimum balance.

### 5️⃣ Payment Options

Available payment options are evaluated, including installment schedules and payment terms.

The system selects an appropriate plan while respecting the user's accepted payment methods.

### 6️⃣ Safety Check

A recommendation is considered safe only when the user can:

* Complete the required payment plan
* Cover essential expenses
* Maintain the required minimum balance
* Complete the purchase within the required deadline

### 7️⃣ Final Recommendation

The agent generates:

* 💰 Maximum safe amount
* 📊 Affordability status
* 💳 Recommended payment method
* 📆 Payment plan
* 📅 Earliest safe full-payment date
* 🔄 Required spending changes
* 🧠 Decision explanation

---

# 📊 Dashboard

The project includes an interactive Streamlit dashboard that provides a high-level view of all financial requests.

It displays:

* Total requests
* Affordable-now requests
* Requests affordable with a plan
* Requests that should be delayed
* Requests that are not affordable
* Affordability distribution
* Recommended payment methods
* Recommended actions

The dashboard gives users a quick visual understanding of the overall financial decision results.

---

# 🔎 Request Analysis

The **Request Analysis** section allows users to search and inspect individual financial requests.

Users can:

* 🔍 Search by Request ID
* 📋 View the generated prediction
* 💰 Check the safe amount
* 📊 View affordability status
* 💳 View the recommended payment method
* 📅 Check the earliest full-payment date
* 🔄 View required spending changes
* 📥 Download the filtered report

This section makes it easier to move from the overall dashboard statistics to a specific financial request.

---

# 📋 Request Details

The **Request Details** section provides a deeper view of an individual request.

For the selected request, the dashboard displays:

* 🆔 Request ID
* 💰 Safe amount
* 💳 Recommended payment method
* 📊 Affordability status
* 📅 Earliest full-payment date
* 🔄 Spending changes
* 💵 Payment plan
* 🎯 AI confidence
* 🧠 Decision information

This provides a detailed explanation of how the financial decision applies to a specific request.

---

# 🧮 Decision Outputs

For every financial request, the system produces:

```text
amount_safe_to_pay
affordability_status
recommended_payment_method
payment_plan
earliest_date_for_full_payment
spending_changes_needed
decision_explanation
```

The affordability status can be:

```text
affordable_now
affordable_with_plan
affordable_later
not_affordable
```

The recommended payment method can be:

```text
full_payment
partial_payment
installments
wait
not_recommended
```

---

# 🛠️ Technology Stack

## 🐍 Backend & Financial Decision Logic

* Python
* Pandas
* Financial forecasting and decision logic
* Currency conversion
* Pytest

## 📊 Dashboard

* Streamlit
* Plotly

## 📁 Data

* CSV-based financial datasets
* Financial profiles
* Financial events
* Payment options
* Exchange rates
* Messages
* Supporting images

## 🧰 Development Tools

* Git
* GitHub
* VS Code
* Python Virtual Environment

---

# 📁 Project Structure

```text
AI-Based-Financial-Agent/
│
├── 📂 code/
│   ├── balance_calculator.py
│   ├── currency_converter.py
│   ├── data_loader.py
│   ├── event_classifier.py
│   ├── event_date_handler.py
│   ├── event_lookup.py
│   ├── financial_timeline.py
│   ├── forecast_window.py
│   ├── inspect_dataset.py
│   ├── main.py
│   ├── minimum_balance_checker.py
│   ├── profile_lookup.py
│   ├── ui.py
│   │
│   └── 🧪 test_*.py
│
├── 📂 dataset/
│   ├── requests.csv
│   ├── sample_requests.csv
│   ├── financial_profiles.csv
│   ├── financial_events.csv
│   ├── request_payment_options.csv
│   ├── exchange_rates.csv
│   ├── messages.csv
│   ├── images.csv
│   └── 📂 media/
│
├── 📂 docs/
│   └── 📂 screenshots/
│       ├── dashboard-overview.png
│       ├── request-analysis.png
│       └── request-details.png
│
├── 📄 problem_statement.md
├── 📄 requirements.txt
├── 📄 output.csv
├── 📄 .gitignore
└── 📄 README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```powershell
git clone <your-repository>
cd AI-Based-Financial-Agent
```

## 2️⃣ Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

## 3️⃣ Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# ▶️ Run the Financial Agent

Generate predictions for the complete dataset:

```powershell
python code\main.py --requests-file dataset\requests.csv --output output.csv
```

The system generates predictions for all requests and saves them to:

```text
output.csv
```

---

# 📊 Run the Dashboard

Start the interactive Streamlit dashboard:

```powershell
streamlit run code\ui.py
```

The dashboard will open in the browser and provide an interactive interface for exploring the financial predictions.

---

# 🤖 Using the AI Chatbot

Click the **💬 chatbot button** in the dashboard.

You can ask questions such as:

```text
Can I afford this laptop?

How much can I safely spend?

Should I wait?

Should I use installments?

How many requests are affordable now?

What payment method is recommended?
```

The chatbot uses the financial prediction data to provide relevant answers about the available requests and recommendations.

---

# 🧪 Testing

The project includes automated tests for the major financial components.

Run:

```powershell
python -m pytest -q
```

Current test status:

```text
30 passed
```

The tests cover important components such as:

* Balance calculations
* Currency conversion
* Event classification
* Event date handling
* Event lookup
* Financial timeline
* Forecast window
* Minimum balance checking
* Profile lookup
* Main financial decision logic

---

# 📈 Current Dataset

The project processes:

```text
250 financial requests
```

The generated output contains one prediction for each request.

The system evaluates:

* Affordability
* Safe spending amount
* Payment methods
* Payment plans
* Future affordability
* Spending adjustments
* Decision explanations

### Current Affordability Results

| Status                  | Requests |
| ----------------------- | -------: |
| 💰 Affordable Now       |       70 |
| 💳 Affordable With Plan |       65 |
| ⏳ Affordable Later      |       38 |
| 🚫 Not Affordable       |       77 |
| **Total**               |  **250** |

### Recommended Payment Methods

| Payment Method     | Requests |
| ------------------ | -------: |
| 🚫 Not Recommended |       77 |
| 💵 Full Payment    |       70 |
| 💳 Installments    |       61 |
| ⏳ Wait             |       38 |
| 💰 Partial Payment |        4 |

---

# 🔐 Financial Safety Principles

The agent is designed around financial safety rather than simply checking whether the current balance is large enough.

A recommendation must consider the user's:

```text
Current Balance
      +
Confirmed Income
      -
Recurring Expenses
      -
Pending Payments
      -
Essential Spending
      -
Required Minimum Balance
      ↓
Safe Financial Capacity
```

The system therefore avoids making a recommendation solely from the user's current balance.

---

# 🧠 Decision-Making Process

The financial decision engine follows a structured process:

```text
1. Read User Request
          ↓
2. Load Financial Profile
          ↓
3. Analyze Financial Events
          ↓
4. Identify Income & Expenses
          ↓
5. Build Financial Timeline
          ↓
6. Apply Minimum Balance Protection
          ↓
7. Calculate Safe Spending Amount
          ↓
8. Evaluate Payment Options
          ↓
9. Determine Affordability Status
          ↓
10. Generate Recommendation
          ↓
11. Explain the Decision
```

This approach allows the system to produce an explainable financial recommendation rather than relying only on a single balance value.

---

# 🎯 Example

### 👤 User

> 💬 **Can I afford this laptop?**

### 🧠 Agent Analysis

```text
Requested Amount:        ₹80,000
Safe Amount Today:       ₹35,000
Affordability:           Affordable With Plan
Recommended Method:      Installments
```

### 🤖 Recommendation

```text
💳 Use an available installment plan.

The full amount cannot be safely paid immediately
while maintaining the required minimum balance and
covering upcoming financial commitments.
```

---

# 📥 Output File

The financial agent generates an `output.csv` file containing the prediction for each request.

The output includes:

```text
request_id
amount_safe_to_pay
affordability_status
recommended_payment_method
payment_plan
earliest_date_for_full_payment
spending_changes_needed
decision_explanation
```

This output can be used for:

* 📊 Dashboard visualization
* 🔎 Request-level analysis
* 📥 Report generation
* 🤖 Chatbot responses
* 🧪 Evaluation and testing

---

# 🌟 Project Highlights

* ✅ Personalized financial affordability analysis
* ✅ Financial forecasting
* ✅ Recurring expense handling
* ✅ Pending and confirmed transaction analysis
* ✅ Minimum-balance protection
* ✅ Payment-plan evaluation
* ✅ Currency conversion
* ✅ Interactive Streamlit dashboard
* ✅ Request-level financial analysis
* ✅ Natural-language chatbot
* ✅ Filtered report download
* ✅ Automated testing
* ✅ CSV prediction generation
* ✅ Explainable financial decision logic

---

# 🔮 Future Enhancements

Potential future improvements include:

* 🧠 LLM-powered financial conversations
* 📸 Automated OCR for financial documents and receipts
* 🔊 Voice-based financial queries
* 📱 Mobile application
* 🔔 Smart payment reminders
* 📉 Advanced spending trend analysis
* 🔐 Stronger authentication and data privacy
* 📊 Personalized financial insights
* 💡 Budget recommendations
* ☁️ Cloud deployment
* 🤖 More advanced agentic financial workflows

---

# 👨‍💻 Author

## Mohan Nimmalapudi

**AI & Machine Learning Enthusiast | Developer**

GitHub:

```text
mohannimmalapudi2007-hue
```

---

# 🎯 Project Goal

The goal of the **AI-Based Financial Agent** is to make financial decisions more understandable and personalized by transforming complex financial information into a clear and explainable recommendation.

Instead of simply asking:

> **"Do I have enough money?"**

the system asks:

> **"Can I safely afford this expense while protecting my future financial commitments?"**

---

# ⭐ Final Summary

The **AI-Based Financial Agent** combines financial data analysis, forecasting, affordability checks, payment-plan evaluation, and an interactive dashboard into a single decision-support system.

It helps users understand:

```text
💰 How much can I safely spend?
          ↓
📊 Can I afford the requested expense?
          ↓
💳 Which payment method is suitable?
          ↓
📅 If not now, when can I afford it?
          ↓
🧠 Why did the system make this recommendation?
```

> **Don't just ask "Can I afford it?" — understand whether you can afford it safely.** 💰🤖

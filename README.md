# IBM HR Employee Attrition Analysis Dashboard

An interactive Streamlit dashboard analysing employee attrition patterns using the IBM HR Analytics Employee Attrition & Performance dataset. Built as the final capstone project for the **IBM SkillsBuild Data Analytics with AI Internship**, in collaboration with **Bharat Cares**.

## 🔗 Live Demo

**Try the dashboard here:** [ibm-employee-attrition-dashboard.streamlit.app](https://ibm-employee-attrition-dashboard.streamlit.app/)

No installation needed — the live app lets you explore all five pages, apply filters, and view the business recommendations directly in your browser.

## Project Description

Employee attrition is costly and disruptive for any organisation. This project explores the IBM HR Employee Attrition dataset (1,470 employee records) to identify the strongest drivers of voluntary attrition — including overtime, compensation, department/job role, tenure, promotion recency, work-life balance, and training investment — and presents the findings through a five-page, filterable dashboard aimed at HR decision-makers.

The dashboard code was generated with the assistance of an AI coding agent (IBM Bob), guided by detailed requirements from the author, and was reviewed and validated against the project's functional requirements before being finalised.

**Dashboard pages:**
1. 🏢 Department & Role Insights
2. 💰 Compensation & Work Conditions
3. 📈 Tenure & Career Growth
4. 📋 Business Recommendations
5. 🗂️ About the Dataset

## Dataset

**Source:** [IBM HR Analytics Employee Attrition Dataset — Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

- 1,470 employee records, 35 attributes
- No missing values
- Target variable: `Attrition` (Yes / No)

> Download `IBM-HR-Employee-Attrition.csv` from the Kaggle link above and place it in the project's root directory before running the app (see Setup below).

## Technologies Used

| Category | Tool / Library |
|---|---|
| Language | Python 3 |
| Data Handling | Pandas, NumPy |
| Visualisation | Plotly Express, Plotly Graph Objects |
| App Framework | Streamlit |
| AI-assisted Development | IBM Bob (AI coding agent) |

## Setup & Run Instructions

1. **Clone or download this repository** and navigate into the project folder.

2. **Add the dataset.** Download `IBM-HR-Employee-Attrition.csv` from the [Kaggle link](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) above and place it in the same directory as `IBM-Attrition-Dashboard.py`.

3. **Install dependencies:**
   ```bash
   pip install streamlit pandas numpy plotly
   ```
   or
   ```bash
   python -m pip install streamlit pandas numpy plotly
   ```

4. **Run the app:**
   ```bash
   streamlit run IBM-Attrition-Dashboard.py
   ```
   or
   ```bash
   python -m streamlit run IBM-Attrition-Dashboard.py
   ```

5. Streamlit will open the dashboard automatically in your browser (typically at `http://localhost:8501`). Use the sidebar to navigate between pages and apply filters.

## Key Information

- **Overall attrition rate:** ~16% of employees in the dataset left the company.
- **Deliverable includes:** 15 underlying analyses, a correlation heatmap, and 8 evidence-based business recommendations for HR leadership.
- **Full write-up:** see `Pranay_ProjectReport.docx` for the complete project report, methodology, and findings.

### Key Insights

- **Overtime** is one of the strongest single predictors — employees working overtime leave at nearly 3× the rate of those who don't.
- **Compensation gap** — employees who left earn noticeably less on average per month than those who stayed.
- **Department & role risk** — the Sales department has the highest attrition rate, with Sales Representatives, Laboratory Technicians, and HR roles topping the individual role rankings.
- **Early tenure is the danger zone** — attrition peaks sharply in an employee's first year (0–1 year band, ~36%), then declines steadily with tenure.
- **No stock options, higher risk** — employees at Stock Option Level 0 attrite at a much higher rate than those with any stock option level.
- **Promotion stagnation** — employees who left had, on average, waited longer since their last promotion than those who stayed.
- **Work-life balance matters** — the lowest self-reported work-life balance score (1 – Bad) shows the highest attrition rate.
- **Training investment pays off** — zero training sessions in the past year correlates with above-average attrition; 2–4 sessions/year is associated with the lowest rates.
- **Commute distance** — employees who left commute further from home on average than those who stayed.
- **Marital status** — single employees show higher attrition than married or divorced employees, likely reflecting fewer financial/family anchors and greater job mobility.

### Business Recommendations

1. **Enforce overtime limits & compensatory mechanisms** — monthly OT caps, time-off-in-lieu, or OT bonuses.
2. **Targeted compensation reviews** for lower-paid, high-attrition roles (Sales Reps, Lab Technicians, HR).
3. **Structured promotion review cycles** — bi-annual reviews with transparent advancement criteria.
4. **Role-specific retention programme for Sales** — revisit quotas, commissions, travel demands, and career paths.
5. **Flexible/hybrid work arrangements** for employees with long commutes.
6. **Increase L&D investment** to 2–4 structured training sessions per employee per year.
7. **Expand stock option coverage** to entry-level and high-risk roles (Sales Reps, Lab Techs, single employees aged 18–35).
8. **Early-warning attrition risk score** for new joiners, flagging high-risk cases at the 30/60/90-day marks for proactive manager check-ins.

## Author

**Pranay Jha** — IBM SkillsBuild Data Analytics with AI Internship (Bharat Cares), September 2026.

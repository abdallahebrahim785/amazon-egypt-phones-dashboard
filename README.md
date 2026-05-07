# 📱 Amazon Smartphones Analysis

🌐 **Live App:** [Click here to open the dashboard](https://amazon-egypt-phones-dashboard.streamlit.app/)

A full end-to-end data science project that scrapes, cleans, analyzes, and visualizes smartphone listings from **Amazon Egypt** — presented through an interactive Streamlit dashboard.

---

## 🗂️ Project Structure

```
Amazon Project/
│
├── Amazon_smartphones_web_scrapping.ipynb   # Web scraping notebook
├── Amazon_eda.ipynb                         # Data cleaning & EDA notebook
├── Amazon_smartphones_cleaned_data.csv      # Final cleaned dataset
├── app.py                                   # Streamlit dashboard
├── amazon.jpg                               # Logo used in sidebar
└── requirements.txt                         # Project dependencies
```

---

## 🎯 Objective

Collect real smartphone data from Amazon Egypt, clean and analyze it, then build an interactive dashboard to uncover:
- Market share and brand dominance
- Price distribution and segmentation
- Customer ratings and review trends
- Discount patterns across brands

---

## 🔄 Project Pipeline

### 1. 🕷️ Web Scraping
**File:** `Amazon_smartphones_web_scrapping.ipynb`

Scraped Amazon Egypt's smartphone category using `requests` and `BeautifulSoup`, extracting:
| Field | Description |
|---|---|
| `Name` | Product title |
| `Brand` | Extracted from product name |
| `Price` | Current price in EGP |
| `Rate` | Customer star rating |
| `number_of_reviews` | Total review count |
| `Discount(%)` | Calculated from original vs current price |
| `Description` | Product subtitle/specs |
| `URL` | Direct Amazon product link |

---

### 2. 🧹 Data Cleaning & EDA
**File:** `Amazon_eda.ipynb`

**Cleaning steps:**
- Dropped irrelevant/constant columns (`Storage`, `category`, `Unnamed: 0`)
- Fixed price formatting (removed commas, cast to numeric)
- Handled missing values (dropped nulls on critical fields, filled missing ratings with 0)
- Removed outliers using IQR method on `Rate`, `Price`, `Discount(%)`, and `number_of_reviews`
- Filtered out non-smartphone items (`Price >= 700 EGP`)
- Standardized brand casing (fixed `XIAOMI` vs `Xiaomi` inconsistencies)
- Removed zero-rated products (null-filled artifacts)

**Engineered Features:**
- `Price_Category` — 4 price tiers: Budget / Mid-Range / Premium / Flagship
- `Rating_Category` — 4 rating tiers: Excellent / Good / Average / Poor

**EDA Coverage:**
- Uni-variate, bi-variate, and multi-variate analysis
- Brand distribution and market share
- Price positioning per brand
- Rating and review patterns
- Discount analysis

---

### 3. 📊 Streamlit Dashboard
**File:** `app.py`

An Amazon-themed interactive dashboard with 4 tabs:

#### 🏆 Brand Analysis
- Top 10 brands by product count
- Market share pie chart
- Most expensive brands
- Brand positioning map (Price vs Rating)
- Best rated & most discounted brands

#### 💰 Price Analysis
- Price distribution histogram
- Market share by price segment
- Average price per brand
- Price distribution box plots
- Discount analysis (% of products with discounts)
- Price segments summary table

#### ⭐ Ratings & Reviews
- Rating distribution histogram
- Products by rating category
- Top rated & most reviewed products
- Price vs Rating correlation scatter
- Customer engagement vs Rating
- Top brands by average rating

#### 🔍 Product Explorer
- Keyword search across Name, Brand & Description
- Live results count with unique products & brands
- Sortable, filterable data table
- Clickable Amazon links per product

---

## 📦 Dataset

| Property | Value |
|---|---|
| Source | Amazon Egypt — Smartphones category |
| Records | ~5,823 listings |
| Features | 11 columns |
| Price Currency | EGP (Egyptian Pound) |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `Python` | Core language |
| `requests` + `BeautifulSoup` | Web scraping |
| `Pandas` + `NumPy` | Data manipulation |
| `Matplotlib` + `Seaborn` | EDA visualizations |
| `Plotly` | Interactive dashboard charts |
| `Streamlit` | Dashboard framework |

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/your-username/amazon-smartphones-analysis.git
cd amazon-smartphones-analysis
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the dashboard**
```bash
streamlit run app.py
```

**4. Open in browser**
```
http://localhost:8501
```

---

## 👤 Author

**Abdallah Ibrahim**
Data Science & AI Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/abdallah-ibrahim-mohamed-4556792a5)

---

> *Data scraped from Amazon Egypt for educational and analytical purposes only.*

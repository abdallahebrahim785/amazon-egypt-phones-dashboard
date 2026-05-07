import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
import base64
warnings.filterwarnings("ignore")


# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Amazon Smartphones Analysis",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Load image as base64 ───────────────────────────────────────────────────
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return data
    except Exception:
        return None

LOGO_B64 = get_image_base64("amazon.jpg")

# ─── Custom CSS (Amazon Theme - Orange/Black) ───────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 1.2rem 2rem 2rem; }

/* Amazon-themed header */
.app-header {
    background: linear-gradient(135deg, #232F3E 0%, #37475A 70%, #FF9900 100%);
    border-radius: 16px;
    padding: 20px 32px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.app-header h1 { color: #fff; font-size: 24px; font-weight: 700; margin: 0; }
.app-header h1 span { color: #FF9900; }
.app-header p { color: rgba(255,255,255,0.75); font-size: 12px; margin: 6px 0 0; }
.header-badge {
    background: #FF9900;
    color: #232F3E;
    font-size: 11px;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 30px;
    white-space: nowrap;
}

/* KPI Cards */
.kpi-wrap { display: flex; gap: 12px; margin-bottom: 1.5rem; flex-wrap: wrap; }
.kpi-card {
    flex: 1;
    min-width: 140px;
    background: linear-gradient(135deg, #FFF8F0 0%, #FFF3E6 100%);
    border: 1px solid #FFD699;
    border-radius: 16px;
    padding: 16px 20px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.12);
    background: linear-gradient(135deg, #FFF3E6 0%, #FFE6CC 100%);
    border-color: #FF9900;
}
.kpi-card .val { font-size: 28px; font-weight: 800; color: #232F3E; line-height: 1.2; letter-spacing: -0.5px; }
.kpi-card .lbl { font-size: 11px; color: #666; margin-top: 8px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }

/* Section Header */
.sec-hdr {
    font-size: 13px;
    font-weight: 700;
    color: #232F3E;
    border-left: 4px solid #FF9900;
    padding-left: 12px;
    margin: 1.5rem 0 0.8rem;
}

/* Insight Box */
.insight {
    background: #FFF8F0;
    border-left: 4px solid #FF9900;
    border-radius: 0 10px 10px 0;
    padding: 12px 18px;
    font-size: 13px;
    color: #232F3E;
    margin-top: 0.8rem;
}

/* Sidebar */
[data-testid="stSidebar"] { background: #F7F7F7; border-right: 1px solid #E0E0E0; }
.sb-logo-box {
    background: linear-gradient(135deg, #232F3E, #37475A);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
    margin-bottom: 16px;
}
.sb-logo-box .title { color: #fff; font-size: 18px; font-weight: 700; margin: 10px 0 4px; }
.sb-logo-box .title span { color: #FF9900; }
.sb-logo-box .sub { color: rgba(255,255,255,0.7); font-size: 11px; }
.sb-section { font-size: 10px; font-weight: 700; color: #FF9900; text-transform: uppercase; margin: 16px 0 8px; }
.sb-divider { border-top: 1px solid #E0E0E0; margin: 12px 0; }
.sb-stat { display: flex; justify-content: space-between; padding: 6px 0; font-size: 12px; }
.sb-stat .sk { color: #666; }
.sb-stat .sv { color: #232F3E; font-weight: 500; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #E2E8F0; }
.stTabs [data-baseweb="tab"] { font-size: 14px; font-weight: 500; padding: 8px 20px; color: #666; }
.stTabs [aria-selected="true"] { color: #FF9900 !important; border-bottom: 2px solid #FF9900 !important; }

/* Footer */
.footer-credit { text-align: center; padding: 20px 0 8px; border-top: 1px solid #E0E0E0; margin-top: 20px; }
.credit-name { font-size: 18px; font-weight: 700; color: #FF9900; text-decoration: none; }
.credit-name:hover { color: #232F3E; }
.credit-title { font-size: 11px; color: #666; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def kpi_card(val, lbl):
    return f'<div class="kpi-card"><div class="val">{val}</div><div class="lbl">{lbl}</div></div>'

def section_header(title):
    st.markdown(f'<div class="sec-hdr">{title}</div>', unsafe_allow_html=True)

def insight_box(text):
    st.markdown(f'<div class="insight">💡 {text}</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_data
def load_data():
    """Load cleaned Amazon smartphones data"""
    df = pd.read_csv('Amazon_smartphones_cleaned_data.csv')
    return df

df = load_data()
df = df[df['Rate'] > 0]

# Sidebar KPIs
total_products = len(df)
avg_price = df['Price'].mean()
avg_rating = df['Rate'].mean()
total_reviews = df['number_of_reviews'].sum()
unique_brands = df['Brand'].nunique()


# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    if LOGO_B64:
        st.markdown(f"""
        <div class="sb-logo-box">
            <img src="data:image/jpeg;base64,{LOGO_B64}"
                 style="width:100%; max-width:180px; border-radius:12px;
                        margin-bottom:12px; background:#fff; padding:8px;" />
            <div class="title">Amazon <span>Smartphones</span></div>
            <div class="sub">Data Analysis Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sb-logo-box">
            <div style="font-size:48px">📱</div>
            <div class="title">Amazon <span>Smartphones</span></div>
            <div class="sub">Data Analysis Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sb-section">📋 Project Brief</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#fff;border-radius:10px;padding:14px 16px;border:1px solid #E0E0E0;font-size:12px;color:#444;line-height:1.7;">
        <b style="color:#232F3E;">🎯 Objective</b><br>
        Analyze Amazon Egypt smartphone listings to uncover market trends, pricing patterns, and customer insights.<br><br>
        <b style="color:#232F3E;">📦 Data Source</b><br>
        Web scraped from Amazon Egypt — smartphones category.<br><br>
        <b style="color:#232F3E;">📊 Analysis Covers</b><br>
        Brand performance · Price segmentation · Ratings & reviews · Discount trends
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sb-section">🔎 Filters</div>', unsafe_allow_html=True)
    
    # Brand filter
    all_brands = sorted(df['Brand'].dropna().unique())
    selected_brands = st.multiselect("Select Brands", options=all_brands, default=[])
    
    # Price range filter
    min_price = int(df['Price'].min())
    max_price = int(df['Price'].max())
    price_range = st.slider("Price Range (EGP)", min_price, max_price, (min_price, max_price))
    
    # Rating filter
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1)
    
    st.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
    
    # LinkedIn Profile
    st.markdown("""
    <div class="footer-credit">
        <a href="https://www.linkedin.com/in/abdallah-ibrahim-mohamed-4556792a5" 
           target="_blank" class="credit-name">
            Abdallah Ibrahim
        </a>
        <div class="credit-title">Data Science & AI Engineer</div>
    </div>
    """, unsafe_allow_html=True)


# Apply filters
filtered_df = df.copy()
if selected_brands:
    filtered_df = filtered_df[filtered_df['Brand'].isin(selected_brands)]
filtered_df = filtered_df[(filtered_df['Price'] >= price_range[0]) & (filtered_df['Price'] <= price_range[1])]
filtered_df = filtered_df[filtered_df['Rate'] >= min_rating]


# ═══════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="app-header">
    <div>
        <h1>📱 Amazon <span>Smartphones Analysis</span></h1>
        <p>Comprehensive market analysis · Price trends · Brand performance · Customer insights</p>
    </div>
    <span class="header-badge">Data-Driven Insights</span>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Brand Analysis",
    "💰 Price Analysis",
    "⭐ Ratings & Reviews",
    "🔍 Product Explorer"
])


# ────────────────────────────────────────────────────────────────────────────
# TAB 1 – BRAND ANALYSIS
# ────────────────────────────────────────────────────────────────────────────

with tab1:
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
    else:
        # KPIs
        top_brand = filtered_df['Brand'].value_counts().index[0]
        top_brand_count = filtered_df['Brand'].value_counts().iloc[0]
        brand_count = filtered_df['Brand'].nunique()
        avg_price_by_brand = filtered_df.groupby('Brand')['Price'].mean()
        most_expensive_brand = avg_price_by_brand.idxmax()
        most_expensive_price = avg_price_by_brand.max()
        
        st.markdown(
            '<div class="kpi-wrap">'
            + kpi_card(f"{top_brand}", " Top Brand")
            + kpi_card(f"{top_brand_count}", " Products")
            + kpi_card(f"{brand_count}", " Total Brands")
            + kpi_card(f"{most_expensive_brand}", "💎 Most Expensive")
            + kpi_card(f"EGP {most_expensive_price:,.0f}", " Avg Price")
            + '</div>', unsafe_allow_html=True)
        
        section_header("Market Share & Brand Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            brand_counts = filtered_df['Brand'].value_counts().head(10)
            fig1 = px.bar(x=brand_counts.values, y=brand_counts.index, orientation='h',
                          title='Top 10 Brands by Product Count',
                          labels={'x': 'Number of Products', 'y': 'Brand'},
                          color=brand_counts.values, color_continuous_scale='Oranges')
            fig1.update_layout(height=450)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.pie(values=brand_counts.values[:8], names=brand_counts.index[:8],
                          title='Market Share by Brand (Top 8)',
                          color_discrete_sequence=px.colors.sequential.Oranges_r,
                          hole=0.4)
            fig2.update_layout(height=450)
            st.plotly_chart(fig2, use_container_width=True)
        
        section_header("Price Positioning by Brand")
        
        col3, col4 = st.columns(2)
        
        with col3:
            avg_price_df = filtered_df.groupby('Brand')['Price'].mean().sort_values(ascending=False).head(10)
            fig3 = px.bar(x=avg_price_df.values, y=avg_price_df.index, orientation='h',
                          title='Top 10 Most Expensive Brands',
                          labels={'x': 'Average Price (EGP)', 'y': 'Brand'},
                          color=avg_price_df.values, color_continuous_scale='Oranges')
            fig3.update_layout(height=450)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            brand_performance = filtered_df.groupby('Brand').agg({
                'Price': 'mean',
                'Rate': 'mean',
                'Brand': 'count'
            }).rename(columns={'Brand': 'Count'}).round(2)
            brand_performance = brand_performance[brand_performance['Count'] >= 10].sort_values('Price', ascending=False).head(10)
            
            if len(brand_performance) > 0:
                fig4 = px.scatter(brand_performance, x='Price', y='Rate', 
                                  text=brand_performance.index, size='Count',
                                  title='Brand Positioning Map (Price vs Rating)',
                                  labels={'Price': 'Average Price (EGP)', 'Rate': 'Average Rating'},
                                  color='Rate', color_continuous_scale='Oranges')
                fig4.update_traces(textposition='top center')
                fig4.update_layout(height=450)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("Not enough data to show brand positioning. Try broadening your filters.")
        
        section_header("Brand Performance Metrics")
        
        col5, col6 = st.columns(2)
        
        with col5:
            top_rated = filtered_df.groupby('Brand')['Rate'].mean().sort_values(ascending=False).head(10)
            fig5 = px.bar(x=top_rated.values, y=top_rated.index, orientation='h',
                          title='Top 10 Best Rated Brands',
                          labels={'x': 'Average Rating (out of 5)', 'y': 'Brand'},
                          color=top_rated.values, color_continuous_scale='Oranges')
            fig5.update_layout(height=450)
            st.plotly_chart(fig5, use_container_width=True)
        
        with col6:
            best_discount = filtered_df.groupby('Brand')['Discount(%)'].mean().sort_values(ascending=False).head(10)
            fig6 = px.bar(x=best_discount.values, y=best_discount.index, orientation='h',
                          title='Top 10 Brands with Best Discounts',
                          labels={'x': 'Average Discount (%)', 'y': 'Brand'},
                          color=best_discount.values, color_continuous_scale='Oranges')
            fig6.update_layout(height=450)
            st.plotly_chart(fig6, use_container_width=True)
        
        insight_box(f"""
        **📊 Brand Analysis Key Insights:**  
        • **{top_brand}** is the market leader with **{top_brand_count}** products  
        • **{most_expensive_brand}** is the most expensive brand (avg. EGP {most_expensive_price:,.0f})  
        • Average price of smartphones is **EGP {filtered_df['Price'].mean():,.0f}**  
        """)


# ────────────────────────────────────────────────────────────────────────────
# TAB 2 – PRICE ANALYSIS
# ────────────────────────────────────────────────────────────────────────────

with tab2:
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
    else:
        # KPIs
        avg_price = filtered_df['Price'].mean()
        median_price = filtered_df['Price'].median()
        min_price = filtered_df['Price'].min()
        max_price = filtered_df['Price'].max()
        avg_discount = filtered_df['Discount(%)'].mean()
        
        st.markdown(
            '<div class="kpi-wrap">'
            + kpi_card(f"EGP {avg_price:,.0f}", " Average Price")
            + kpi_card(f"EGP {median_price:,.0f}", " Median Price")
            + kpi_card(f"EGP {min_price:,.0f}", " Min Price")
            + kpi_card(f"EGP {max_price:,.0f}", " Max Price")
            + kpi_card(f"{avg_discount:.1f}%", " Avg Discount")
            + '</div>', unsafe_allow_html=True)
        
        section_header("Price Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(filtered_df, x='Price', nbins=50, 
                                title='Smartphone Price Distribution',
                                labels={'Price': 'Price (EGP)', 'count': 'Number of Products'},
                                color_discrete_sequence=['#FF9900'])
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            segment_counts = filtered_df['Price_Category'].value_counts()
            fig2 = px.pie(values=segment_counts.values, names=segment_counts.index,
                          title='Market Share by Price Segment',
                          color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        section_header("Price by Brand")
        
        col3, col4 = st.columns(2)
        
        with col3:
            top_brands_price = filtered_df.groupby('Brand')['Price'].mean().sort_values(ascending=False).head(10)
            fig3 = px.bar(x=top_brands_price.values, y=top_brands_price.index, orientation='h',
                          title='Average Price by Brand (Top 10)',
                          labels={'x': 'Average Price (EGP)', 'y': 'Brand'},
                          color=top_brands_price.values, color_continuous_scale='Oranges')
            fig3.update_layout(height=450)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            top_brands_list = filtered_df['Brand'].value_counts().head(8).index
            fig4 = px.box(filtered_df[filtered_df['Brand'].isin(top_brands_list)], 
                          x='Brand', y='Price', title='Price Distribution by Top Brands',
                          color='Brand', color_discrete_sequence=px.colors.qualitative.Set2)
            fig4.update_layout(height=450, xaxis_tickangle=-45)
            st.plotly_chart(fig4, use_container_width=True)
        
        section_header("Discount Analysis")
        
        col5, col6 = st.columns(2)
        
        with col5:
            discount_products = filtered_df[filtered_df['Discount(%)'] > 0]
            fig5 = px.pie(values=[len(discount_products), len(filtered_df) - len(discount_products)],
                          names=['With Discount', 'No Discount'],
                          title=f'Products with Discount ({len(discount_products)} of {len(filtered_df)})',
                          color_discrete_sequence=['#FF9900', '#E0E0E0'])
            fig5.update_layout(height=400)
            st.plotly_chart(fig5, use_container_width=True)
        
        with col6:
            fig6 = px.histogram(filtered_df[filtered_df['Discount(%)'] > 0], 
                                x='Discount(%)', nbins=30,
                                title='Discount Percentage Distribution',
                                labels={'Discount(%)': 'Discount (%)', 'count': 'Number of Products'},
                                color_discrete_sequence=['#FF9900'])
            fig6.update_layout(height=400)
            st.plotly_chart(fig6, use_container_width=True)
        
        section_header("Price Segments Summary")
        
        segment_summary = filtered_df.groupby('Price_Category').agg({
            'Price': ['count', 'mean', 'min', 'max'],
            'Rate': 'mean',
            'Discount(%)': 'mean'
        }).round(2)
        
        segment_summary.columns = ['Count', 'Avg Price', 'Min Price', 'Max Price', 'Avg Rating', 'Avg Discount']
        st.dataframe(segment_summary, use_container_width=True)
        
        insight_box(f"""
        **💰 Price Analysis Key Insights:**  
        • Most smartphones are in the **Mid-Range (5K-15K EGP)** segment  
        • The average discount across all products is **{avg_discount:.1f}%**  
        • **{len(discount_products)}** products ({len(discount_products)/len(filtered_df)*100:.1f}%) currently have discounts  
        """)


# ────────────────────────────────────────────────────────────────────────────
# TAB 3 – RATINGS & REVIEWS
# ────────────────────────────────────────────────────────────────────────────

with tab3:
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
    else:
        # KPIs
        avg_rating = filtered_df['Rate'].mean()
        median_rating = filtered_df['Rate'].median()
        total_reviews_filtered = filtered_df['number_of_reviews'].sum()
        avg_reviews = filtered_df['number_of_reviews'].mean()
        excellent_products = len(filtered_df[filtered_df['Rate'] >= 4.5])
        
        st.markdown(
            '<div class="kpi-wrap">'
            + kpi_card(f"{avg_rating:.2f}", " Average Rating")
            + kpi_card(f"{median_rating:.1f}", " Median Rating")
            + kpi_card(f"{total_reviews_filtered:,.0f}", " Total Reviews")
            + kpi_card(f"{avg_reviews:.0f}", " Avg Reviews/Product")
            + kpi_card(f"{excellent_products}", " Excellent (4.5+)")
            + '</div>', unsafe_allow_html=True)
        
        section_header("Rating Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(filtered_df, x='Rate', nbins=20,
                                title='Product Rating Distribution',
                                labels={'Rate': 'Rating (out of 5)', 'count': 'Number of Products'},
                                color_discrete_sequence=['#FF9900'])
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            rating_category_counts = filtered_df['Rating_Category'].value_counts()
            fig2 = px.bar(x=rating_category_counts.values, y=rating_category_counts.index, orientation='h',
                          title='Products by Rating Category',
                          labels={'x': 'Number of Products', 'y': 'Rating Category'},
                          color=rating_category_counts.values, color_continuous_scale='Oranges')
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        section_header("Top Rated & Most Reviewed Products")
        
        col3, col4 = st.columns(2)
        
        with col3:
            top_rated = filtered_df.nlargest(10, 'Rate')[['Brand', 'Rate', 'Price', 'number_of_reviews']]
            top_rated['Product'] = top_rated['Brand'] + ' Smartphone'
            fig3 = px.bar(top_rated, x='Rate', y='Product', orientation='h',
                          title='Top 10 Highest Rated Products',
                          labels={'Rate': 'Rating (out of 5)', 'Product': ''},
                          color='Rate', color_continuous_scale='Oranges')
            fig3.update_layout(height=450)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            most_reviewed = filtered_df.nlargest(10, 'number_of_reviews')[['Brand', 'number_of_reviews', 'Rate', 'Price']]
            most_reviewed['Product'] = most_reviewed['Brand'] + ' Smartphone'
            fig4 = px.bar(most_reviewed, x='number_of_reviews', y='Product', orientation='h',
                          title='Top 10 Most Reviewed Products',
                          labels={'number_of_reviews': 'Number of Reviews', 'Product': ''},
                          color='number_of_reviews', color_continuous_scale='Oranges')
            fig4.update_layout(height=450)
            st.plotly_chart(fig4, use_container_width=True)
        
        section_header("Price vs Rating Correlation")
        
        col5, col6 = st.columns(2)
        
        with col5:
            fig5 = px.scatter(filtered_df, x='Price', y='Rate', 
                             title='Price vs Rating Correlation',
                             labels={'Price': 'Price (EGP)', 'Rate': 'Rating (out of 5)'},
                             color='Brand', opacity=0.6,
                             color_discrete_sequence=px.colors.qualitative.Set2)
            fig5.update_layout(height=450)
            st.plotly_chart(fig5, use_container_width=True)
            
            correlation = filtered_df['Price'].corr(filtered_df['Rate'])
            st.metric("Correlation Coefficient", f"{correlation:.3f}")
        
        with col6:
            fig6 = px.scatter(filtered_df, x='number_of_reviews', y='Rate', 
                             title='Customer Engagement vs Rating',
                             labels={'number_of_reviews': 'Number of Reviews', 'Rate': 'Rating (out of 5)'},
                             color='Brand', opacity=0.6,
                             log_x=True,
                             color_discrete_sequence=px.colors.qualitative.Set2)
            fig6.update_layout(height=450)
            st.plotly_chart(fig6, use_container_width=True)
            
            reviews_rating_corr = filtered_df['number_of_reviews'].corr(filtered_df['Rate'])
            st.metric("Correlation Coefficient", f"{reviews_rating_corr:.3f}")
        
        section_header("Rating by Brand")
        
        brand_rating = filtered_df.groupby('Brand').agg({
            'Rate': 'mean',
            'number_of_reviews': 'sum',
            'Brand': 'count'
        }).rename(columns={'Brand': 'Count'}).round(2)
        
        brand_rating_filtered = brand_rating[brand_rating['Count'] >= 10].sort_values('Rate', ascending=False).head(10)
        
        if len(brand_rating_filtered) > 0:
            fig7 = px.bar(x=brand_rating_filtered['Rate'], y=brand_rating_filtered.index, orientation='h',
                          title='Top 10 Brands by Average Rating (Min 10 products)',
                          labels={'x': 'Average Rating (out of 5)', 'y': 'Brand'},
                          color=brand_rating_filtered['Rate'], color_continuous_scale='Oranges')
            fig7.update_layout(height=450)
            st.plotly_chart(fig7, use_container_width=True)
        
        insight_box(f"""
        **⭐ Ratings & Reviews Key Insights:**  
        • Average rating across all products is **{avg_rating:.2f}⭐**  
        • **{excellent_products}** products ({excellent_products/len(filtered_df)*100:.1f}%) have excellent ratings (4.5+)  
        • There is a **{correlation:.3f}** correlation between price and rating  
        """)
# ────────────────────────────────────────────────────────────────────────────
# TAB 4 – PRODUCT EXPLORER
# ────────────────────────────────────────────────────────────────────────────

with tab4:
    if len(filtered_df) == 0:
        st.warning("No data matches the selected filters.")
    else:
        section_header("Browse & Search Products")

        search_query = st.text_input("🔎 Search by keyword (e.g. Samsung, Oppo, Xiaomi, Infinix...)", "")

        explorer_df = filtered_df[['Brand', 'Name', 'Description', 'Price', 'Rate', 'Discount(%)', 'number_of_reviews', 'Price_Category', 'URL']].copy()

        # Apply keyword search across Name, Brand, Description
        if search_query:
            keywords = search_query.strip().split()
            mask = pd.Series([True] * len(explorer_df), index=explorer_df.index)
            for keyword in keywords:
                keyword_mask = (
                    explorer_df['Name'].str.contains(keyword, case=False, na=False) |
                    explorer_df['Brand'].str.contains(keyword, case=False, na=False) |
                    explorer_df['Description'].str.contains(keyword, case=False, na=False)
                )
                mask = mask & keyword_mask
            explorer_df = explorer_df[mask]

        # Deduplicate by Name + Price — keep listing with most reviews
        explorer_df = (
            explorer_df
            .sort_values('number_of_reviews', ascending=False)
            .drop_duplicates(subset=['Name', 'Price'], keep='first')
            .sort_values(['Rate', 'number_of_reviews'], ascending=[False, False])
            .reset_index(drop=True)
        )

        explorer_df = explorer_df.drop(columns=['Description'])

        # Summary stats
        total = len(explorer_df)
        unique_brands = explorer_df['Brand'].nunique()
        unique_products = explorer_df['Name'].nunique()

        st.markdown(f"""
        <div style="background:#FFF8F0;border:1px solid #FFD699;border-radius:10px;
                    padding:10px 18px;margin-bottom:12px;font-size:13px;color:#232F3E;">
            🔍 <b>{total:,}</b> results &nbsp;|&nbsp;
            📱 <b>{unique_products:,}</b> unique products &nbsp;|&nbsp;
            🏷️ <b>{unique_brands}</b> brands
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            explorer_df,
            use_container_width=True,
            column_config={
                "URL": st.column_config.LinkColumn("Product Link", display_text="🔗 View on Amazon"),
                "Rate": st.column_config.ProgressColumn("Rating ⭐", format="%.1f", min_value=0, max_value=5),
                "Price": st.column_config.NumberColumn("Price (EGP)", format="EGP %,.0f"),
                "Discount(%)": st.column_config.NumberColumn("Discount", format="%.1f%%"),
                "number_of_reviews": st.column_config.NumberColumn("Reviews", format="%,d"),
            },
            height=520,
        )

        insight_box(f"Showing <b>{total:,}</b> products · sorted by highest rating · click any link to open on Amazon Egypt")
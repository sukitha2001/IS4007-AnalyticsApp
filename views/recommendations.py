import streamlit as st
from utils.theme import apply_theme, page_header, recommendation_card

def render_recommendations():
    
    
    
    
    page_header(
        "Business Recommendations",
        "Data-backed action plans derived from the revenue analysis notebook.",
        badge="Strategic Actions",
    )
    
    st.write("")
    
    # Custom HTML Card Template
    def custom_rec_card(title, summary, detail, color_hex):
        html_string = f"""
        <div style='background-color: rgba(255,255,255,0.03); padding: 1.5rem; border-left: 4px solid {color_hex}; border-radius: 4px; margin-bottom: 1.5rem;'>
            <h3 style='color: #e2e8f0; font-size: 18px; margin-top: 0;'>{title}</h3>
            <p style='color: {color_hex}; font-size: 14px; font-weight: 600; margin-bottom: 0.5rem;'>{summary}</p>
            <p style='color: #94a3b8; font-size: 14px; line-height: 1.6; margin-bottom: 0;'>{detail}</p>
        </div>
        """
        st.html(html_string)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Growth & Retention Strategy")
        custom_rec_card(
            "Target 'Second Purchase' Incentives",
            "Priority: High | Focus: Frequency Growth",
            "Implement aggressive 'second purchase' incentives (e.g., immediate discount on next order). The standardized CLV regression model proves that driving repeat visits (Frequency) matters more than optimizing the discount strategy for increasing total lifetime value.",
            "#3b82f6" # Blue
        )
        custom_rec_card(
            "Win-Back 'At Risk' Customers",
            "Priority: High | Focus: Churn Prevention",
            "Implement win-back emails with aggressive targeted discounts specifically for the 'At Risk' segment. Simultaneously, nurture 'Recent Customers' to transition them into the 'Loyal' segment before they lapse.",
            "#10b981" # Green
        )
        custom_rec_card(
            "Investigate Branch Outperformance",
            "Priority: Medium | Focus: Retail Optimization",
            "ANOVA testing shows a statistically significant difference in revenue generation between branches. Management must investigate the top-performing branch's practices (staffing, inventory, local marketing) to apply these best practices across the underperforming branches.",
            "#8b5cf6" # Purple
        )
        
    with col2:
        st.markdown("#### Pricing & Risk Management")
        custom_rec_card(
            "Tighten SME Credit Policies",
            "Priority: Critical | Focus: Revenue Leakage",
            "Chi-Square testing reveals a statistically significant dependency between customer type and payment status. If SME accounts show a higher observed 'Overdue' count than expected, credit policies for SMEs need immediate tightening.",
            "#ef4444" # Red
        )
        custom_rec_card(
            "Eliminate Margin-Eroding Discounts",
            "Priority: High | Focus: Pricing Controls",
            "Regression analysis shows some channels generate high volume but low-quality, low-CLV customers due to excessive discounting. Immediately review categories sitting in the 'High Discount, Low Margin' danger zone and pull back on promotional campaigns for those products.",
            "#f59e0b" # Orange
        )
        custom_rec_card(
            "Cross-Sell in Low AOV Channels",
            "Priority: Medium | Focus: Cart Size Expansion",
            "Implement volume discounts, minimum-spend free shipping thresholds, or targeted cross-sells in low-AOV (Average Order Value) channels to artificially bump up the transaction size without eroding base margins.",
            "#0ea5e9" # Light Blue
        )
    
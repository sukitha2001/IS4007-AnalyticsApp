import streamlit as st
import plotly.io as pio

def apply_theme():
    """Configures the aesthetic theme for the Streamlit app and Plotly charts to mimic Shadcn UI."""
    pio.templates.default = "plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white"

    # Custom CSS for Shadcn UI dashboard look - BOLDER and BIGGER
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;500;600;700;800;900&display=swap');

        /* Global Font Override */
        html, body, [class*="css"] {
            font-family: 'Work Sans', sans-serif !important;
        }

        /* Hide Streamlit default headers, footers, and native sidebar */
        header[data-testid="stHeader"] {display: none;}
        footer {display: none;}
        [data-testid="stSidebar"] {display: none;}

        /* Tighter block container to maximize screen real estate */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1600px; /* Wider max width */
        }

        /* Text Gradients for eye-catching headers */
        .text-gradient {
            background-image: linear-gradient(90deg, #60a5fa, #c084fc); /* Blue to Purple */
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
        }

        /* MASSIVE Metric Cards for eye-catching impact */
        div[data-testid="stMetricValue"] {
            font-size: 3rem !important;
            font-weight: 900 !important;
            line-height: 1.1;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* General Typography - Bolder headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Work Sans', sans-serif !important;
            font-weight: 800; /* Extra bold headings */
            letter-spacing: -0.025em;
        }

        /* Custom avatar list styling for Recent Sales */
        .recent-sales-list {list-style: none; padding: 0; margin: 0;}
        .recent-sales-item {
            display: flex; align-items: center; padding: 16px 0; /* More padding */
            border-bottom: 1px solid rgba(255,255,255,0.1); /* Lighter border for dark mode */
        }
        .recent-sales-item:last-child {border-bottom: none;}
        .rs-avatar {
            width: 48px; height: 48px; border-radius: 50%; /* Bigger avatar */
            background-color: #334155; color: #f1f5f9; /* Slate 700 / Slate 100 */
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 16px; margin-right: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5); /* subtle glow */
        }
        .rs-details {flex-grow: 1;}
        .rs-name {font-size: 16px; font-weight: 700; margin: 0; line-height: 1.2; color: #f1f5f9;} /* Slate 100 */
        .rs-email {font-size: 14px; color: #94a3b8; margin: 0; margin-top: 4px;} /* Slate 400 */
        .rs-amount {font-weight: 800; font-size: 16px; color: #10b981;} /* Emerald green for positive amount */

        /* Dark mode overrides for custom HTML */
        @media (prefers-color-scheme: dark) {
            .rs-avatar {background-color: #374151; color: #f3f4f6;}
            .rs-email {color: #9ca3af;}
        }
        </style>
    """, unsafe_allow_html=True)



def clean_plotly_layout(fig, height=390, showlegend=False):
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="gray", size=14)),
        yaxis=dict(showgrid=True, gridcolor="rgba(128,128,128,0.2)", tickfont=dict(color="gray", size=14)),
        height=height,
        showlegend=showlegend
    )
    return fig

def metric_card(title, value, description, prefix="", trend="neutral"):
    if trend == "positive":
        color = "#10b981"
        icon = "📈"
    elif trend == "negative":
        color = "#ef4444"
        icon = "📉"
    else:
        color = "#3b82f6"
        icon = "📊"
        
    # Some usages pass an icon symbol as prefix
    if prefix in ["▣", "▦", "◎", "!", "💰", "👥", "🛒", "⚡", "%"]:
        if prefix != "%":
            icon = prefix
            prefix = ""
    
    st.html(f"""
    <div style="
        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-top: 2px solid {color};
        border-radius: 12px;
        padding: 1.4rem 1.5rem 1.2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    ">
        <div style="
            position: absolute; top: -20px; right: -10px;
            font-size: 5rem; opacity: 0.06; user-select: none;
        ">{icon}</div>
        <p style="margin:0 0 0.5rem; font-size:0.75rem; font-weight:600;
                  text-transform:uppercase; letter-spacing:0.08em;
                  color:{color};">{title}</p>
        <p style="margin:0 0 0.4rem; font-size:2rem; font-weight:800;
                  color:#f1f5f9; line-height:1.1;">{prefix}{value}</p>
        <p style="margin:0; font-size:0.78rem; color:#64748b;">{description}</p>
    </div>
    """)

def page_header(title, description, badge=""):
    st.markdown(f"<h2>{title} <span style='font-size: 0.5em; color: gray;'>{badge}</span></h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: gray; margin-bottom: 24px;'>{description}</p>", unsafe_allow_html=True)

def tabs(label, options, key, default_value):
    return st.segmented_control(
        label=label,
        options=options,
        default=default_value,
        key=key,
        label_visibility="collapsed",
    )

def escape(text):
    import html
    return html.escape(str(text))

def recommendation_card(title, content, description, variant="high"):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(content)
        st.caption(description)

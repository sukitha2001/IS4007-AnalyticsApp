import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_data
from utils.theme import apply_theme, clean_plotly_layout, metric_card, page_header
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def render_revenue_forecasting():
    
    
    page_header(
        "Revenue Forecasting",
        "Project net revenue from historical monthly trends and adjust the forward-looking horizon.",
        badge="Scenario view",
    )
    
    sales, customers, products, campaigns = load_data()
    
    if sales.empty:
        st.warning("Data could not be loaded.")
    else:
        # Prepare monthly time series
        sales['month'] = sales['transaction_date'].dt.to_period('M')
        ts_data = sales.groupby('month')['net_revenue'].sum().reset_index()
        ts_data['month'] = ts_data['month'].dt.to_timestamp()
        ts_data.set_index('month', inplace=True)
        
        # Forecast horizon slider
        with st.container(border=True):
            st.markdown("#### Settings")
            months_to_forecast = st.slider("Months to forecast", min_value=3, max_value=12, value=6)
        
        try:
            # Fit Holt-Winters model (Exponential Smoothing)
            model = ExponentialSmoothing(ts_data['net_revenue'], trend='add', seasonal=None, initialization_method="estimated")
            fit_model = model.fit()
            forecast = fit_model.forecast(months_to_forecast)
            
            # Create forecast dataframe
            future_dates = [ts_data.index[-1] + pd.DateOffset(months=i) for i in range(1, months_to_forecast + 1)]
            forecast_df = pd.DataFrame({'month': future_dates, 'forecast': forecast.values})
            forecast_df.set_index('month', inplace=True)
    
            next_month = forecast_df["forecast"].iloc[0]
            forecast_total = forecast_df["forecast"].sum()
            latest_actual = ts_data["net_revenue"].iloc[-1]
            forecast_change = ((next_month - latest_actual) / latest_actual) * 100 if latest_actual else 0
    
            cols = st.columns(3)
            with cols[0]:
                metric_card("Latest Actual", f"{latest_actual:,.0f}", "Most recent transaction month", "$")
            with cols[1]:
                metric_card("Next Forecast", f"{next_month:,.0f}", f"{forecast_change:+.1f}% vs latest actual", "$", "positive" if forecast_change >= 0 else "negative")
            with cols[2]:
                metric_card("Forecast Total", f"${forecast_total:,.0f}", f"Next {months_to_forecast} months", "positive")
            
            # Plotting
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ts_data.index, y=ts_data['net_revenue'], mode='lines+markers', name='Historical', line=dict(color='#2563eb', width=3)))
            fig.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['forecast'], mode='lines+markers', name='Forecast', line=dict(color='#16a34a', width=3, dash='dash')))
            
            fig.update_layout(title="Revenue Forecast", xaxis_title="Date", yaxis_title="Net Revenue")
            clean_plotly_layout(fig, height=440, showlegend=True)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
            st.markdown("#### Forecast Details")
            st.dataframe(forecast_df.reset_index().style.format({'forecast': '${:,.2f}', 'month': '{:%Y-%m}'}), use_container_width=True)
            
        except Exception as e:
            st.error(f"Not enough data or error in forecasting model: {e}")
    
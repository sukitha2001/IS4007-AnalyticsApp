import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.data_loader import load_data
from utils.theme import apply_theme, clean_plotly_layout, metric_card, page_header
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

def render_revenue_forecasting():
    
    
    page_header(
        "Revenue Forecasting",
        "Project net revenue from historical monthly trends and adjust the forward-looking horizon.",
        badge="Forecast & Scenario Analysis",
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
        ts_data = ts_data.asfreq('MS') 
        
        # Settings panel
        with st.container(border=True):
            st.markdown("#### Settings")
            settings_cols = st.columns(2)
            with settings_cols[0]:
                months_to_forecast = st.slider("Months to forecast", min_value=3, max_value=12, value=6)
            with settings_cols[1]:
                scenario_spread = st.slider("Scenario spread (%)", min_value=5, max_value=25, value=10,
                                            help="Percentage above/below the base forecast for best and low case scenarios.")
        
        try:
            # ── Fit Holt-Winters model with additive seasonality ──
            n_obs = len(ts_data)
            seasonal_periods = 12

            if n_obs >= 2 * seasonal_periods:
                model = ExponentialSmoothing(
                    ts_data['net_revenue'],
                    trend='add',
                    seasonal='add',
                    seasonal_periods=seasonal_periods,
                    initialization_method="estimated"
                )
            else:
                model = ExponentialSmoothing(
                    ts_data['net_revenue'],
                    trend='add',
                    seasonal=None,
                    initialization_method="estimated"
                )

            fit_model = model.fit(optimized=True)
            forecast = fit_model.forecast(months_to_forecast)
            
            # Create forecast dataframe
            future_dates = [ts_data.index[-1] + pd.DateOffset(months=i) for i in range(1, months_to_forecast + 1)]
            forecast_df = pd.DataFrame({'forecast': forecast.values}, index=future_dates)
            forecast_df.index.name = 'month'

            # ── Scenario Analysis (best / base / low) ──
            spread = scenario_spread / 100.0
            forecast_df['best_case'] = forecast_df['forecast'] * (1 + spread)
            forecast_df['low_case']  = forecast_df['forecast'] * (1 - spread)
            
            # ── Forecast Error Metrics──
            fitted = fit_model.fittedvalues
            actual = ts_data['net_revenue']
            # Drop NaN fitted values (first few observations where model can't compute)
            valid = fitted.dropna()
            actual_aligned = actual.loc[valid.index]

            mae  = np.mean(np.abs(actual_aligned - valid))
            rmse = np.sqrt(np.mean((actual_aligned - valid) ** 2))
            mape = np.mean(np.abs((actual_aligned - valid) / actual_aligned)) * 100

            # ── KPI Metric Cards ──
            next_month = forecast_df["forecast"].iloc[0]
            forecast_total = forecast_df["forecast"].sum()
            latest_actual = ts_data["net_revenue"].iloc[-1]
            forecast_change = ((next_month - latest_actual) / latest_actual) * 100 if latest_actual else 0

            cols = st.columns(3)
            with cols[0]:
                metric_card("Latest Actual", f"${latest_actual:,.0f}", "Most recent transaction month")
            with cols[1]:
                metric_card("Next Forecast", f"${next_month:,.0f}", f"{forecast_change:+.1f}% vs latest actual")
            with cols[2]:
                metric_card("Forecast Total", f"${forecast_total:,.0f}", f"Next {months_to_forecast} months")

            # ── Forecast Accuracy Metrics ──
            st.markdown("#### Model accuracy (in-sample)")
            err_cols = st.columns(3)
            with err_cols[0]:
                metric_card("MAE", f"${mae:,.0f}", "Mean Absolute Error")
            with err_cols[1]:
                metric_card("RMSE", f"${rmse:,.0f}", "Root Mean Squared Error")
            with err_cols[2]:
                metric_card("MAPE", f"{mape:.1f}%", "Mean Absolute Percentage Error")
            
            # ── Main Forecast Chart with Scenario Bands ──
            # Bridge: prepend last historical point so the lines connect
            bridge = pd.DataFrame({
                'forecast':  [ts_data['net_revenue'].iloc[-1]],
                'best_case': [ts_data['net_revenue'].iloc[-1]],
                'low_case':  [ts_data['net_revenue'].iloc[-1]],
            }, index=[ts_data.index[-1]])
            plot_forecast = pd.concat([bridge, forecast_df])

            fig = go.Figure()

            # Scenario band (filled area between best and low case)
            fig.add_trace(go.Scatter(
                x=list(plot_forecast.index) + list(plot_forecast.index[::-1]),
                y=list(plot_forecast['best_case']) + list(plot_forecast['low_case'][::-1]),
                fill='toself',
                fillcolor='rgba(22, 163, 74, 0.12)',
                line=dict(color='rgba(0,0,0,0)'),
                name='Scenario Range',
                hoverinfo='skip',
                showlegend=True,
            ))

            # Historical line
            fig.add_trace(go.Scatter(
                x=ts_data.index, y=ts_data['net_revenue'],
                mode='lines+markers', name='Historical',
                line=dict(color='#2563eb', width=3),
                marker=dict(size=5),
            ))

            # Base forecast line
            fig.add_trace(go.Scatter(
                x=plot_forecast.index, y=plot_forecast['forecast'],
                mode='lines+markers', name='Base Forecast',
                line=dict(color='#16a34a', width=3, dash='dash'),
                marker=dict(size=6),
            ))

            # Best case line
            fig.add_trace(go.Scatter(
                x=plot_forecast.index, y=plot_forecast['best_case'],
                mode='lines', name=f'Best Case (+{scenario_spread}%)',
                line=dict(color='#22d3ee', width=2, dash='dot'),
            ))

            # Low case line
            fig.add_trace(go.Scatter(
                x=plot_forecast.index, y=plot_forecast['low_case'],
                mode='lines', name=f'Low Case (−{scenario_spread}%)',
                line=dict(color='#f97316', width=2, dash='dot'),
            ))
            
            fig.update_layout(title="Revenue Forecast — Scenario View", xaxis_title="Date", yaxis_title="Net Revenue ($)")
            clean_plotly_layout(fig, height=480, showlegend=True)
            # Override legend position for this chart
            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # ── Scenario Summary Table ──
            st.markdown("#### Scenario comparison")
            scenario_summary = forecast_df.copy()
            scenario_summary = scenario_summary.reset_index()
            scenario_summary.columns = ['Month', 'Base Case', 'Best Case', 'Low Case']
            
            st.dataframe(
                scenario_summary.style.format({
                    'Base Case': '${:,.2f}',
                    'Best Case': '${:,.2f}',
                    'Low Case':  '${:,.2f}',
                    'Month':     '{:%Y-%m}',
                }),
                use_container_width=True,
            )

            # ── Scenario Totals ──
            total_cols = st.columns(3)
            with total_cols[0]:
                metric_card("Best Case Total", f"${forecast_df['best_case'].sum():,.0f}", f"+{scenario_spread}% scenario")
            with total_cols[1]:
                metric_card("Base Case Total", f"${forecast_total:,.0f}", "Base forecast")
            with total_cols[2]:
                metric_card("Low Case Total", f"${forecast_df['low_case'].sum():,.0f}", f"−{scenario_spread}% scenario")

            # ── Seasonal Decomposition ──
            st.markdown("#### Seasonal decomposition")
            st.markdown("<p style='color: gray;'>Decomposing historical revenue into trend, seasonal, and residual components.</p>", unsafe_allow_html=True)

            if n_obs >= 2 * seasonal_periods:
                decomposition = seasonal_decompose(ts_data['net_revenue'], model='additive', period=seasonal_periods)

                from plotly.subplots import make_subplots
                fig_decomp = make_subplots(
                    rows=4, cols=1, shared_xaxes=True,
                    subplot_titles=('Observed', 'Trend', 'Seasonal', 'Residual'),
                    vertical_spacing=0.06,
                )

                fig_decomp.add_trace(go.Scatter(x=ts_data.index, y=decomposition.observed, mode='lines', name='Observed',
                                                line=dict(color='#3b82f6', width=2)), row=1, col=1)
                fig_decomp.add_trace(go.Scatter(x=ts_data.index, y=decomposition.trend, mode='lines', name='Trend',
                                                line=dict(color='#f59e0b', width=2)), row=2, col=1)
                fig_decomp.add_trace(go.Scatter(x=ts_data.index, y=decomposition.seasonal, mode='lines', name='Seasonal',
                                                line=dict(color='#10b981', width=2)), row=3, col=1)
                fig_decomp.add_trace(go.Scatter(x=ts_data.index, y=decomposition.resid, mode='markers', name='Residual',
                                                marker=dict(color='#ec4899', size=5)), row=4, col=1)

                fig_decomp.update_layout(
                    height=700,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=30, b=0),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                # Style all axes
                for i in range(1, 5):
                    fig_decomp.update_xaxes(showgrid=False, tickfont=dict(color="gray", size=12), row=i, col=1)
                    fig_decomp.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)", tickfont=dict(color="gray", size=12), row=i, col=1)
                # Style subplot titles
                for ann in fig_decomp['layout']['annotations']:
                    ann['font'] = dict(size=14, color='gray')

                st.plotly_chart(fig_decomp, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info(f"Seasonal decomposition requires at least {2 * seasonal_periods} months of data. Current data has {n_obs} months.")
            
        except Exception as e:
            st.error(f"Not enough data or error in forecasting model: {e}")
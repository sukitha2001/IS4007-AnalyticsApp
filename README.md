# Revenue Analytics Command Center

An interactive, data-driven Revenue Analytics Dashboard built with Python, Streamlit, and Plotly. This application is designed to act as a command center for business users, providing actionable insights into revenue performance, customer behavior, pricing impact, and future trends.

## 🚀 Features

The application is structured into the following key modules:

1. **Executive Revenue Analytics**
   - High-level overview of total revenue, transactions, and active customers.
   - Revenue trends (Moving Average), category share, and quarterly growth.
   - Product profitability matrix (Star Products, Cash Cows, etc.).

2. **Customer Analytics**
   - Customer segmentation (e.g., Champions, At-Risk, Lost) using K-means and RFM analysis.
   - Insights into customer lifetime value and purchase behavior.

3. **Product & Channel**
   - Analysis of top-performing products and categories.
   - Channel comparison and performance metrics.

4. **Pricing & Discount**
   - Assessment of discount strategies and their impact on gross margins.
   - Analysis of revenue by discount band to identify over-discounted areas.

5. **Revenue Forecasting**
   - Future revenue projections based on historical data.
   - Trend analysis to anticipate seasonal changes and business cycles.

6. **Leakage & Underperformance**
   - Identification of revenue gaps, overdue payments, and low-margin sales.
   - Highlighting inactive customers and underperforming branches/channels.

7. **Recommendations**
   - Data-backed business recommendations to improve pricing, retention, and collection strategies.

## 🛠️ Technology Stack

- **Python**: Core programming language.
- **Streamlit**: Web framework for building the interactive dashboard.
- **Plotly**: For creating rich, interactive data visualizations.
- **Pandas**: For data manipulation and analysis.
- **Streamlit Shadcn UI**: For enhanced, clean UI components.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sukitha2001/IS4007-AnalyticsApp.git
   cd IS4007-AnalyticsApp
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the dashboard:**
   Open your browser and navigate to `http://localhost:8501`.

## 📁 Project Structure

- `app.py`: The main entry point for the Streamlit application.
- `views/`: Contains the logic and UI for each individual module/tab.
- `utils/`: Utility functions, including data loading (`data_loader.py`) and theming (`theme.py`).
- `generated_data/`: Directory for storing the dummy/anonymized dataset used by the application.
- `analysis/`: Exploratory analysis scripts or notebooks (if applicable).

## 📝 License

This project is created for educational purposes (IS4007 Module) and uses dummy business data.

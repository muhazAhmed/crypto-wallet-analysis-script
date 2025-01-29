# 📌 Cryptocurrency Wallet Analysis Project

## 📖 Project Overview

This project focuses on **analyzing cryptocurrency wallets** by collecting transaction histories and portfolio data, then leveraging **machine learning** to rank wallets based on performance indicators such as:

- **Return on Investment (ROI)**
- **Trading Frequency**
- **Activity Level**
- **Portfolio Volatility**
- **Sharpe Ratio** (Risk-adjusted return)
- **Historical Loss Ratios**

The goal is to **build a ranking model** that helps users track high-performing wallets and analyze their activity for better investment decisions.

---

## 📂 Project Structure

```
crypto-wallet-analysis-script/
│── data/
│   ├── portfolio_data.csv           # Processed portfolio data
│   ├── wallet_data.csv              # Processed transaction data
│   ├── wallet_features.csv          # Engineered features dataset
│   ├── wallet_features_clean.csv    # Normalized features dataset
│   ├── top_traders_account_numbers.csv # Input wallet addresses
│
│── scripts/
│   ├── fetch_data.py                # Fetches transaction & portfolio data
│   ├── feature_engineering.py       # Computes financial features
│   ├── preprocess_data.py           # Cleans & normalizes data
│   ├── train_model.py               # ML model for ranking wallets
│
│── requirements.txt                 # Python dependencies
│── README.md                        # Project documentation
```

---

## 🔧 Setup & Installation

### 📌 Prerequisites

- **Python 3.8+**
- **Virtual Environment** (Recommended: `venv` or `conda`)
- Required Libraries:
  ```sh
  pip install -r requirements.txt
  ```

### 🚀 How to Run the Project

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/crypto-wallet-analysis.git
   cd crypto-wallet-analysis
   ```

2. **Activate Virtual Environment**

   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Fetch Transaction & Portfolio Data**

   ```sh
   python scripts/fetch_data.py
   ```

4. **Perform Feature Engineering**

   ```sh
   python scripts/feature_engineering.py
   ```

5. **Preprocess Data for ML**

   ```sh
   python scripts/preprocess_data.py
   ```

6. **Train Machine Learning Model**

   ```sh
   python scripts/train_model.py
   ```

7. **View Final Wallet Rankings** The final ranking will be available in:

   ```sh
   data/wallet_rankings.csv
   ```

---

## 🔍 Data Collection

### **1️⃣ Fetching Transaction & Portfolio Data**

- Uses **Helius API** to collect:
  - **Transaction History** (timestamps, amounts, counterparties, fees)
  - **Portfolio Data** (token balances, NFT holdings)
- Stores data in `wallet_data.csv` and `portfolio_data.csv`

### **2️⃣ Data Cleaning & Processing**

- **Handles missing values** (fills NaN with median values)
- **Normalizes numeric features** using MinMaxScaler

---

## 🧑‍💻 Feature Engineering

### **Key Features Computed**

| Feature                  | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| **ROI**                  | Return on Investment (Final portfolio vs. initial investment) |
| **Trading Frequency**    | Number of transactions per day                                |
| **Activity Score**       | Measures how active the wallet is over time                   |
| **Portfolio Volatility** | Standard deviation of portfolio value fluctuations            |
| **Sharpe Ratio**         | Risk-adjusted return based on volatility                      |
| **Loss Ratio**           | Percentage of transactions that resulted in a loss            |

### **Feature Engineering Pipeline**

1. Compute **financial metrics** (ROI, trading frequency, activity score)
2. Compute **risk-based metrics** (volatility, Sharpe ratio, loss ratio)
3. **Normalize data** before model training

---

## 🤖 Machine Learning Model

### **Approach**

- **Supervised Learning** model trained to predict wallet rankings
- Features used: ROI, trading frequency, volatility, etc.
- **Model Evaluation**:
  - Used **RandomForestRegressor** for ranking wallets
  - **Performance Metric**: Mean Squared Error (MSE)

### **Training Pipeline**

1. Split dataset into **training & test sets**
2. Train **Random Forest Regressor**
3. Evaluate model performance
4. Generate final rankings in `wallet_rankings.csv`

---

## ⚠️ Challenges Faced

### **1️⃣ API Rate Limits & Data Fetching Issues**

- **Issue:** Helius API rate limits caused timeouts
- **Solution:** Added `time.sleep(1)` to avoid exceeding limits

### **2️⃣ Missing & Inconsistent Data**

- **Issue:** Some wallets had missing transaction data
- **Solution:** Filled missing values with median & removed empty wallets

### **3️⃣ Feature Scaling Impact on Model Performance**

- **Issue:** Large numeric differences affected model predictions
- **Solution:** Applied **MinMaxScaler** to normalize feature values

### **4️⃣ Wallet Ranking Logic**

- **Issue:** Initial ranking was incorrect due to weighting errors
- **Solution:** Adjusted ranking formula to prioritize ROI & activity score

---

## 📌 Submission Guidelines Checklist

✅ **Code & Data Pushed to GitHub** 🔗 ✅ **README File with Project Details** 📄 ✅ **Scripts Run Without Errors** ⚙️ ✅ **Feature Engineering & ML Model Completed** 🚀 ✅ **Challenges & Optimizations Documented** ✍️

---

## 📢 Future Improvements

- **Hyperparameter tuning** for better model accuracy
- **Deploy ML model via Flask API** for real-time wallet analysis
- **Mobile App Development** for user-friendly access to rankings

---

## 📬 Contact

For any queries, feel free to reach out:

- 📧 **Email:** [muhazvla313@gmail.com](mailto\:muhazvla313@gmail.com)
- 🌐 **Portfolio** [Muhaz Ahmed](https://muhazahmed.com)


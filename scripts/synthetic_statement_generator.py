import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_financial_inputs(start_year, end_year, filename="FMVA_raw_data.csv"):
    years = [str(y) for y in range(start_year, end_year + 1)]
    
    metrics = [
        # --- P&L: REVENUE & OPERATING LAYERS ---
        "Revenue: Passenger", "Revenue: Cargo & Other",
        "Salaries, Wages & Benefits", "Fuel Expense (Net of Hedges)",
        "Fuel Hedging Ineffectiveness (P&L Hit)", 
        "Aircraft Maintenance, Materials & Repairs",
        "Depreciation: Owned Assets", "Depreciation: ROU Assets (Leases)",
        "Amortization of Intangibles", "Impairment of Assets/Goodwill",
        
        # --- P&L: NON-OPERATING & TAX ---
        "Interest Income", "Interest Expense: Financial Debt",
        "Interest Expense: Lease Liabilities",
        "Gain/(Loss) on Disposal of Assets", "Foreign Exchange Gain/(Loss)",
        "Income/(Loss) from Equity Accounted Investees",
        "Statutory Tax Rate", "Deferred Tax Movement (Provision)",
        "Net Income Attributable to Non-Controlling Interest",

        # --- OCI: COMPREHENSIVE INCOME ---
        "OCI: Cash Flow Hedges (Unrealized)", "OCI: Available-for-Sale Securities",
        
        # --- WORKING CAPITAL DRIVERS (DAYS) ---
        "DSO", "DIO", "DPO", "Current Portion of Lease Liab. (Trigger)",
        
        # --- BS: OPENING BALANCES (YEAR 0) ---
        "Op. Cash & Short-Term Investments", "Op. Restricted Cash",
        "Op. Net Accounts Receivable", "Op. Inventories",
        "Op. PP&E (Net)", "Op. ROU Assets (Net)", "Op. Goodwill & Intangibles",
        "Op. Accounts Payable", "Op. Accrued Expenses",
        "Op. Short-Term Debt", "Op. Long-Term Debt", 
        "Op. Lease Liabilities (Current & Non-Current)",
        "Op. Net Deferred Tax Liability", "Op. Pension Liabilities",
        "Op. Common Stock", "Op. Retained Earnings", "Op. Accum. OCI",
        "Op. Non-Controlling Interest (Equity)",

        # --- CASH FLOW / EQUITY ACTIONS ---
        "CapEx: Flight Equipment", "CapEx: Ground & Tech",
        "Proceeds from Asset Sales", "Repayment of Lease Principal",
        "New Debt Issuance", "Debt Repayment",
        "Share-Based Comp (Equity Credit)", "Dividends to Shareholders"
    ]

    data = {"Metric": metrics}

    seeds = [
        120000.0, 25000.0, 55000.0, 30000.0,     # Current Assets
        650000.0, 210000.0, 45000.0,             # Long-Term Assets
        48000.0, 32000.0,                        # Current Liab
        15000.0, 185000.0, 205000.0,             # Debt & Leases
        28000.0, 12000.0,                        # Other Liab
        85000.0, 155000.0, -8000.0, 12000.0      # Equity (inc. NCI)
    ]

    prev_rev = 350000.00 # Starting base for Revenue

    for year in years:
        # Volatile Growth
        growth = 1 + np.random.normal(0.04, 0.18)
        curr_rev = prev_rev * growth

        hedge_fail = -2500.00 if np.random.random() > 0.8 else 0.0
        impairment = -12000.00 if growth < 0.9 else 0.0

        data[year] = [
            round(curr_rev * 0.75, 2), round(curr_rev * 0.25, 2), # Revenue
            round(-(curr_rev * 0.18), 2), round(-(curr_rev * 0.32), 2), # Ops
            hedge_fail, round(-(curr_rev * 0.09), 2),            # Maint
            -18000.0, -12000.0, -1500.0, impairment,            # D, A & I
            
            1200.0, -8500.0, -11500.0,                          # Interest
            800.0, round(np.random.normal(0, 2000), 2),         # G/L & FX
            1500.0, 0.28, -2500.0, -800.0,                      # Tax & NCI
            
            round(np.random.normal(0, 4000), 2), -500.0,        # OCI Items
            
            52, 35, 60, 0.15,                                   # WC Days
            
            *seeds,                                             # Opening Balances
            
            25000.0, 4500.0, 2200.0,                            # Investing
            -14000.0, 10000.0, -15000.0,                        # Financing
            3500.0, -2000.0                                     # Equity Actions
        ]
        prev_rev = curr_rev

    return pd.DataFrame(data)

df_final = generate_financial_inputs(2021, 2025)
print(f"✅ Data exported to {df_final}.")
df_final.to_csv('../data/FMVA_raw_data.csv')
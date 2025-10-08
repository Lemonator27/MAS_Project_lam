import yfinance as yf
import pandas as pd
from tqdm import tqdm
import time
def get_sp500_tickers():
    """Returns a hardcoded list of S&P 500 tickers."""
    print("Using a reliable, hardcoded list of S&P 500 tickers.")
    # List updated as of late 2023/early 2024.
    tickers = [
        'A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK', 'AEE', 'AEP',
        'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME',
        'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APTV', 'ARE', 'AVB', 'AVGO',
        'AVY', 'AWK', 'AXON', 'AXP', 'AZO', 'BA', 'BAC', 'BALL', 'BAX', 'BBWI', 'BBY', 'BDX', 'BEN', 'BF-B', 'BIIB',
        'BIO', 'BK', 'BKNG', 'BKR', 'BLK', 'BMY', 'BR', 'BRK-B', 'BRO', 'BSX', 'BWA', 'BX', 'BXP', 'C', 'CAG', 'CAH',
        'CAT', 'CB', 'CBOE', 'CBRE', 'CCI', 'CCL', 'CDNS', 'CDW', 'CE', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI',
        'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'COP', 'COR', 'COST',
        'CPB', 'CPRT', 'CPT', 'CRL', 'CRM', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH', 'CVS', 'CVX', 'D',
        'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRI', 'DTE',
        'DUK', 'DVA', 'DVN', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'ELV', 'EMN', 'EMR', 'ENPH', 'EOG',
        'EPAM', 'EQIX', 'EQR', 'EQT', 'ERJ', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE',
        'EXR', 'F', 'FANG', 'FAST', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FI', 'FICO', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC',
        'FOX', 'FOXA', 'FRT', 'FSLR', 'FTNT', 'FTV', 'GD', 'GE', 'GEHC', 'GEN', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC',
        'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT',
        'HOLX', 'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUM', 'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN',
        'INCY', 'INTC', 'INTU', 'INVH', 'IP', 'IPG', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'J', 'JBL', 'JCI',
        'JEF', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'K', 'KDP', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO',
        'KR', 'KVUE', 'L', 'LDOS', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNT', 'LOW', 'LULU', 'LUV', 'LVS',
        'LW', 'LYB', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'META', 'MGM',
        'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS', 'MSCI',
        'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NI', 'NKE', 'NOC', 'NOW', 'NRG',
        'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL', 'OKE', 'OMC', 'ON', 'ORCL',
        'ORLY', 'OTIS', 'OXY', 'PANW', 'PARA', 'PAYC', 'PAYX', 'PCAR', 'PCG', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG',
        'PGR', 'PH', 'PHM', 'PKG', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PODD', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX',
        'PTC', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL',
        'ROP', 'ROST', 'RSG', 'RTX', 'RVTY', 'SBAC', 'SBUX', 'SCHW', 'SJM', 'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI',
        'SRE', 'STE', 'STLD', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH',
        'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 'TMO', 'TMUS', 'TPR', 'TRGP', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA',
        'TSN', 'TT', 'TTWO', 'TXN', 'TXT', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VFC',
        'VICI', 'VLO', 'VMC', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBD', 'WCN', 'WDC', 'WEC',
        'WELL', 'WFC', 'WHR', 'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XOM', 'XRAY', 'XYL',
        'YUM', 'ZBH', 'ZBRA', 'ZTS'
    ]
    return tickers

NECESSARY_COLUMNS = [
    'Total Cash From Operating Activities', # Our Target Variable
    'Net Income',
    'Depreciation And Amortization',
    'Change In Working Capital',
    'Total Revenue',
    'Gross Profit',
    'Operating Income',
    'Total Assets',
    'Accounts Receivable',
    'Inventory',
    'Accounts Payable'
]

def get_company_financials(ticker_symbol):
    """Fetches, merges, and cleans financial data for a single ticker."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        cash_flow = ticker.quarterly_cashflow.T
        income_stmt = ticker.quarterly_financials.T
        balance_sheet = ticker.quarterly_balance_sheet.T
        
        if cash_flow.empty or income_stmt.empty or balance_sheet.empty:
            return None

        df = pd.concat([cash_flow, income_stmt, balance_sheet], axis=1)
        df = df.loc[:,~df.columns.duplicated()].copy()
        market_cap = ticker.info.get('marketCap', 0)

        df['ticker'] = ticker_symbol
        df['marketCap'] = market_cap
        return df

    except Exception as e:
        return None

if __name__ == "__main__":
    all_tickers = get_sp500_tickers()
    all_company_data = []
    print(f"\nFetching financial data for {len(all_tickers)} companies... (This may take 15-20 minutes)")

    for ticker_symbol in tqdm(all_tickers):
        company_df = get_company_financials(ticker_symbol)
        if company_df is not None:
            all_company_data.append(company_df)
        time.sleep(0.5)

    print("\nCombining all data into a single DataFrame...")
    final_df = pd.concat(all_company_data)
    LARGE_CAP_THRESHOLD = 10_000_000_000
    MID_CAP_THRESHOLD = 2_000_000_000

    def categorize_size(market_cap):
        if market_cap >= LARGE_CAP_THRESHOLD:
            return 'Large-Cap'
        elif market_cap >= MID_CAP_THRESHOLD:
            return 'Mid-Cap'
        else:
            return 'Small-Cap'

    final_df['size_category'] = final_df['marketCap'].apply(categorize_size)
    final_columns = ['ticker', 'marketCap', 'size_category'] + NECESSARY_COLUMNS
    final_df = final_df.reindex(columns=final_columns)
    final_df.reset_index(inplace=True)
    final_df.rename(columns={'index': 'date'}, inplace=True)
    final_df.sort_values(by=['ticker', 'date'], inplace=True)

    # --- 6. Save the Dataset to a File ---
    output_filename = 'financial_data_sp500.csv'
    print(f"\nSaving the final dataset to '{output_filename}'...")
    final_df.to_csv(output_filename, index=False)
    print("Save complete!")

    # --- 7. Display Final Results ---
    print("\n--- Final Cleaned Dataset (First 5 Rows) ---")
    print(final_df.head())
    print("\n--- Dataset Info ---")
    final_df.info()
    print("\n--- Company Size Distribution ---")
    print(final_df.drop_duplicates(subset=['ticker'])['size_category'].value_counts())
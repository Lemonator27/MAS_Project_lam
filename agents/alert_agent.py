import pandas as pd
import os
from datetime import datetime, timedelta

# LangChain and OpenAI imports
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# --- 1. CONSTANTS AND CONFIGURATION ---

# Path for the data file
DATA_PATH = "data/transactions_extended.csv"

# Define budgets for different spending categories
BUDGETS = {
    "Marketing": 1000.00,
    "Software": 2500.00,
    "Office Supplies": 500.00,
    "Utilities": 200.00,
    "Travel": 100.00
}


# --- 2. DATA SETUP FUNCTION ---

def create_sample_data():
    """
    Creates and saves a sample CSV file with extended transaction data.
    This function makes the script self-contained and runnable.
    """
    # Create a sample dataframe
    data = {
        'transaction_id': [f'T00{i}' for i in range(1, 11)],
        'timestamp': [
            '2025-10-07 10:00:00', '2025-10-07 14:15:00', '2025-10-07 23:30:00', # Unusual hour transaction
            '2025-10-08 09:00:00', '2025-10-08 11:00:00', '2025-10-06 15:00:00',
            '2025-10-05 18:00:00', '2025-09-10 12:00:00', '2025-10-08 13:00:00',
            '2025-10-08 08:45:00'
        ],
        'amount': [
            150.00, 2000.00, 350.00,
            99999.00, # High Z-score transaction
            800.00, 120.00, 450.00, 50.00, 75.00, 1500.00
        ],
        'category': [
            'Marketing', 'Software', 'Office Supplies', 'Software', 'Marketing',
            'Utilities', 'Office Supplies', 'Utilities', 'Travel', 'Software'
        ],
        'vendor': [
            'Facebook Ads', 'Adobe Inc.', 'Office Depot', 'Microsoft', 'Google Ads',
            'EVN HCMC', 'Office Depot', 'VNPT', 'Grab', 'Figma'
        ],
        'due_date': [
            None, None, None, None, None, None, None,
            (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'), # Late payment
            None, (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d') # Late payment
        ],
        'status': [
            'paid', 'paid', 'paid', 'paid', 'paid',
            'paid', 'paid', 'pending', 'paid', 'pending'
        ]
    }
    df = pd.DataFrame(data)

    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save to CSV
    df.to_csv(DATA_PATH, index=False)
    print(f"Sample data created at {DATA_PATH}")


# --- 3. SPECIALIZED ANALYSIS TOOLS ---

@tool
def detect_high_value_transactions(z_threshold: float = 3.0) -> str:
    """
    Detects unusually high-value transactions based on Z-score.
    Use this tool to find financial outliers.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        amounts = df["amount"].dropna()
        mean = amounts.mean()
        std = amounts.std(ddof=0)
        if std == 0: return "No variance in transaction amounts."
        
        df['zscore'] = ((df['amount'] - mean) / std).abs()
        anomalies = df[df['zscore'] >= z_threshold]
        
        if anomalies.empty:
            return "No unusually high-value transactions found."
        return f"Detected high-value transactions:\n{anomalies[['transaction_id', 'amount', 'zscore']].to_string(index=False)}"
    except Exception as e:
        return f"Error during processing: {e}"

@tool
def detect_unusual_hours_transactions(start_hour: int = 7, end_hour: int = 22) -> str:
    """
    Detects transactions occurring outside of normal business hours (before 7 AM or after 10 PM).
    """
    try:
        df = pd.read_csv(DATA_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        anomalies = df[(df['timestamp'].dt.hour < start_hour) | (df['timestamp'].dt.hour >= end_hour)]
        
        if anomalies.empty:
            return "No transactions found outside of business hours."
        return f"Detected transactions outside business hours:\n{anomalies[['transaction_id', 'timestamp', 'amount']].to_string(index=False)}"
    except Exception as e:
        return f"Error during processing: {e}"

@tool
def detect_over_budget_spending() -> str:
    """
    Checks for and reports on spending categories that have exceeded their defined budget.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        spending_by_category = df.groupby('category')['amount'].sum()
        
        report = []
        for category, spent in spending_by_category.items():
            budget = BUDGETS.get(category, 0)
            if budget > 0 and spent > budget:
                report.append(
                    f"- Category '{category}': Spent {spent:,.2f} USD, exceeding budget by {spent - budget:,.2f} USD (Budget: {budget:,.2f} USD)."
                )
        
        if not report:
            return "All spending categories are within budget."
        return "Detected over-budget spending:\n" + "\n".join(report)
    except Exception as e:
        return f"Error during processing: {e}"

@tool
def detect_late_supplier_payments() -> str:
    """
    Checks for supplier invoices that are past their due date for payment.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        df['due_date'] = pd.to_datetime(df['due_date'], errors='coerce')
        df_pending = df[(df['status'] == 'pending') & (df['due_date'].notna())].copy()
        
        today = datetime.now()
        anomalies = df_pending[df_pending['due_date'] < today]
        
        if anomalies.empty:
            return "No supplier payments are overdue."
        
        anomalies['days_overdue'] = (today - anomalies['due_date']).dt.days
        return f"Detected late supplier payments:\n{anomalies[['vendor', 'amount', 'due_date', 'days_overdue']].to_string(index=False)}"
    except Exception as e:
        return f"Error during processing: {e}"


# --- 4. AGENT SETUP AND EXECUTION ---

def main():
    """
    Main function to set up and run the financial analysis agent.
    """
    # Load environment variables from .env file
    load_dotenv()

    # 1. Initialize the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=os.getenv("OPENAI_API_KEY"))

    # 2. Assemble the tools
    tools = [
        detect_high_value_transactions,
        detect_unusual_hours_transactions,
        detect_over_budget_spending,
        detect_late_supplier_payments
    ]

    # 3. Create the Prompt Template
    prompt_template = """
    You are an expert Vietnamese financial analyst. Your task is to detect anomalies and generate a clear, concise report.

    You have access to the following tools:
    {tools}

    Use the tools to check for all possible financial alerts based on the user's request.
    After gathering all information from the tools, synthesize it into a comprehensive final report in Vietnamese.
    The report should explain WHAT the alert is, WHY it is an alert, and provide specific details (like transaction IDs, amounts, dates).

    Use the following format:

    Question: The user's request.
    Thought: You should always think about what to do. I need to check for all types of anomalies. I will start by checking for high-value transactions.
    Action: The action to take, should be one of [{tool_names}].
    Action Input: The input to the action.
    Observation: The result of the action.
    Thought: Now I will check for the next type of anomaly.
    Action: ...
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I have gathered all necessary information. I will now compile the final report in Vietnamese.
    Final Answer: [Your final, comprehensive report in Vietnamese]

    Begin!

    Question: {input}
    {agent_scratchpad}
    """
    prompt = PromptTemplate.from_template(prompt_template)

    # 4. Create the Agent
    agent = create_react_agent(llm, tools, prompt)

    # 5. Create the Agent Executor
    financial_agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # 6. Run the Agent
    response = financial_agent_executor.invoke({
        "input": "Hãy kiểm tra toàn bộ dữ liệu và lập báo cáo về các cảnh báo tài chính tiềm ẩn."
    })
    
    # 7. Print the final, formatted report
    print("\n" + "="*50)
    print("BÁO CÁO TÀI CHÍNH TỔNG HỢP")
    print("="*50)
    print(response['output'])


if __name__ == "__main__":
    # Ensure sample data exists before running the agent
    create_sample_data()
    # Run the main agent function
    main()
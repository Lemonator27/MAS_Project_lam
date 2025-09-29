import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI  # For OpenAI models
from langchain_community.llms import Ollama  # For local Ollama models
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
_ = load_dotenv()
def load_cashflow_data(path: str = "data/cashflow_data.csv") -> pd.DataFrame:
    """Load cash flow data"""
    try:
        df = pd.read_csv(path)
        # Ensure numeric columns are float
        numeric_cols = ['revenue', 'operating_expenses', 'capital_expenditures', 'net_cashflow', 'cash_balance']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    except Exception:
        # Fallback data if file doesn't exist
        return pd.DataFrame({
            "date": pd.date_range(start="2024-01-01", periods=3),
            "quarter": ["Q1", "Q1", "Q1"],
            "revenue": [100000.0, 120000.0, 95000.0],
            "operating_expenses": [80000.0, 85000.0, 75000.0],
            "capital_expenditures": [10000.0, 5000.0, 15000.0],
            "net_cashflow": [10000.0, 30000.0, 5000.0],
            "cash_balance": [500000.0, 530000.0, 535000.0]
        })

class CashFlowPredictor:
    """ML model for predicting future cash flows"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self._is_trained = False

    def _prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract and prepare features for prediction"""
        df = df.copy()
        if 'date' not in df.columns:
            df['date'] = pd.date_range(end=datetime.now(), periods=len(df))
            
        # Convert date column to datetime if it's not already
        df['date'] = pd.to_datetime(df['date'])
            
        # Create temporal features
        df['month'] = df['date'].dt.month
        df['day_of_week'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        df['day_of_month'] = df['date'].dt.day
        
        # Ensure numeric columns are float
        numeric_cols = ['revenue', 'operating_expenses', 'capital_expenditures', 'net_cashflow']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calculate rolling means for numeric columns only
        for col in numeric_cols:
            if col in df.columns:
                df[f'{col}_7d_mean'] = df[col].rolling(window=7, min_periods=1).mean()
                df[f'{col}_30d_mean'] = df[col].rolling(window=30, min_periods=1).mean()
        
        # Start with numeric features
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        base_features = [col for col in numeric_cols if col not in ['cash_balance']]
        
        if not base_features:
            raise ValueError("No numeric features found in the data")
            
        # Create initial feature DataFrame
        X = df[base_features].fillna(method='ffill').fillna(0)
        
        # Add temporal features
        if 'month' in df.columns:
            X['month'] = df['month'].astype(float)
        if 'day_of_week' in df.columns:
            X['day_of_week'] = df['day_of_week'].astype(float)
        if 'day_of_month' in df.columns:
            X['day_of_month'] = df['day_of_month'].astype(float)
            
        # Handle quarter with one-hot encoding
        if 'quarter' in df.columns:
            quarter_dummies = pd.get_dummies(df['quarter'], prefix='quarter')
            X = pd.concat([X, quarter_dummies], axis=1)
            
        return self.scaler.fit_transform(X.astype(float))

    def train(self, df: pd.DataFrame, prediction_days: int = 30) -> None:
        """Train the model on historical data"""
        if df.empty:
            raise ValueError("No data provided for training")
            
        X = self._prepare_features(df)
        y = df['net_cashflow'].shift(-prediction_days).fillna(method='ffill')
        
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self._is_trained = True

    def predict(self, df: pd.DataFrame, days_ahead: int = 30) -> pd.DataFrame:
        """Generate predictions for future cash flows"""
        if not self._is_trained:
            self.train(df)
            
        # Generate future dates
        last_date = pd.to_datetime(df['date'].max())
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=days_ahead)
        
        # Create feature dataframe for prediction
        # Use last 30 days as base for rolling features
        future_df = df.tail(30).copy()
        
        # Create future data with all necessary columns
        future_data = pd.DataFrame({
            'date': future_dates,
            'quarter': [f'Q{(d.month-1)//3 + 1}' for d in future_dates],
            'revenue': [0] * days_ahead,  # Placeholder values
            'operating_expenses': [0] * days_ahead,
            'capital_expenditures': [0] * days_ahead,
            'net_cashflow': [0] * days_ahead
        })
        
        # Combine historical and future data
        future_df = pd.concat([future_df, future_data]).reset_index(drop=True)
        
        # Prepare features and make predictions
        X_future = self._prepare_features(future_df)
        predictions = self.model.predict(X_future[-days_ahead:])
        
        return pd.DataFrame({
            'date': future_dates,
            'predicted_cashflow': predictions
        })


def analyze_cashflow_trends(df: pd.DataFrame) -> str:
    """Analyze cash flow trends"""
    if df.empty:
        return "Không có dữ liệu cash flow để phân tích."
    
    # Calculate trends
    recent_periods = df.tail(30)  # Last 30 days
    avg_revenue = recent_periods['revenue'].mean()
    avg_expenses = recent_periods['operating_expenses'].mean()
    avg_cashflow = recent_periods['net_cashflow'].mean()
    
    current_balance = df['cash_balance'].iloc[-1]
    
    # Calculate growth rates
    if len(df) > 1:
        revenue_growth = ((recent_periods['revenue'].iloc[-1] - recent_periods['revenue'].iloc[0]) / 
                         recent_periods['revenue'].iloc[0] * 100) if recent_periods['revenue'].iloc[0] > 0 else 0
        expense_growth = ((recent_periods['operating_expenses'].iloc[-1] - recent_periods['operating_expenses'].iloc[0]) / 
                         recent_periods['operating_expenses'].iloc[0] * 100) if recent_periods['operating_expenses'].iloc[0] > 0 else 0
    else:
        revenue_growth = 0
        expense_growth = 0
    
    # Predict future cash flow (simple linear projection)
    if len(df) >= 7:  # Need at least a week of data
        recent_cashflow = df['net_cashflow'].tail(7).mean()
        projected_30_days = recent_cashflow * 30
        projected_balance = current_balance + projected_30_days
    else:
        projected_30_days = avg_cashflow * 30
        projected_balance = current_balance + projected_30_days
    
    # Generate insights
    insights = []
    
    if avg_cashflow > 0:
        insights.append(f"✅ Dòng tiền dương trung bình: ${avg_cashflow:,.2f}/ngày")
    else:
        insights.append(f"⚠️ Dòng tiền âm trung bình: ${avg_cashflow:,.2f}/ngày")
    
    if revenue_growth > 5:
        insights.append(f"📈 Doanh thu tăng trưởng tốt: +{revenue_growth:.1f}%")
    elif revenue_growth < -5:
        insights.append(f"📉 Doanh thu giảm: {revenue_growth:.1f}%")
    else:
        insights.append(f"📊 Doanh thu ổn định: {revenue_growth:+.1f}%")
    
    if projected_balance < current_balance * 0.8:
        insights.append("🚨 Cảnh báo: Dự báo dòng tiền giảm trong 30 ngày tới")
    elif projected_balance > current_balance * 1.2:
        insights.append("💚 Tích cực: Dự báo dòng tiền tăng trong 30 ngày tới")
    
    return f"""
**Phân tích dòng tiền:**
- Số dư hiện tại: ${current_balance:,.2f}
- Doanh thu trung bình: ${avg_revenue:,.2f}/ngày
- Chi phí trung bình: ${avg_expenses:,.2f}/ngày
- Dòng tiền ròng trung bình: ${avg_cashflow:,.2f}/ngày

**Dự báo 30 ngày tới:**
- Dòng tiền dự kiến: ${projected_30_days:,.2f}
- Số dư dự kiến: ${projected_balance:,.2f}

**Insights:**
{chr(10).join(insights)}
"""

def cashflow_tool(query: str) -> str:
    """Main cash flow analysis tool"""
    df = load_cashflow_data()
    return analyze_cashflow_trends(df)

# LangChain Tools and Agent Setup
class PredictionRequest(BaseModel):
    days: int = Field(default=30, description="Number of days to predict ahead")

class CashFlowTools:
    def __init__(self):
        self.predictor = CashFlowPredictor()
        self.df = load_cashflow_data()
        if not self.df.empty:
            self.predictor.train(self.df)

    def analyze_current_cashflow(self) -> str:
        """Analyze current cash flow situation and trends"""
        return analyze_cashflow_trends(self.df)

    def predict_cashflow(self, days: int = 30) -> str:
        """Predict future cash flows using ML model"""
        predictions = self.predictor.predict(self.df, days_ahead=days)
        
        total_predicted = predictions['predicted_cashflow'].sum()
        avg_daily = predictions['predicted_cashflow'].mean()
        trend = "tăng" if predictions['predicted_cashflow'].iloc[-1] > predictions['predicted_cashflow'].iloc[0] else "giảm"
        
        return f"""
**Dự báo dòng tiền {days} ngày tới:**

- Tổng dòng tiền dự kiến: ${total_predicted:,.2f}
- Trung bình mỗi ngày: ${avg_daily:,.2f}
- Xu hướng: {trend}

*Dự báo dựa trên mô hình ML được huấn luyện từ dữ liệu lịch sử*
"""


class CashFlowAgentExecutor:
    """Enhanced Cash Flow Agent Executor with AI and ML capabilities"""
    
    def __init__(self, model_name: str = "gpt-5-nano", use_local: bool = False):
        self.tools = CashFlowTools()
        
        # Set up the language model
        if use_local:
            # Use local Ollama model
            self.llm = Ollama(model="llama2")  # or another model you have in Ollama
        else:
            # Use OpenAI model
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=0.7,
                streaming=True
            )
        
        # Define LangChain tools
        self.langchain_tools = [
            Tool(
                name="analyze_cashflow",
                func=self.tools.analyze_current_cashflow,
                description="Analyze current cash flow patterns and trends"
            ),
            Tool(
                name="predict_cashflow",
                func=lambda x: self.tools.predict_cashflow(days=x.get('days', 30)),
                description="Predict future cash flows using ML model"
            )
        ]
        
        # Create agent with tools
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a finance AI expert specializing in cash flow analysis. "
                      "Use the available tools to provide detailed insights and predictions."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        self.agent = create_openai_functions_agent(prompt = prompt, tools = self.langchain_tools, llm=self.llm)
        self.agent_executor = AgentExecutor(
            agent=self.agent, 
            tools=self.langchain_tools,
            verbose=True  # Set to True to see the agent's thought process
        )

    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        query = inputs.get("input", "")
        
        try:
            # Run query through AI agent
            result = self.agent_executor.invoke({
                "input": query,
                "chat_history": []
            })
            return {"output": result["output"]}
            
        except Exception as e:
            # Fallback to traditional analysis if AI fails
            result = cashflow_tool(query)
            return {"output": result}


# Initialize with default OpenAI model
cashflow_agent_executor = CashFlowAgentExecutor(
    model_name="gpt-5-nano",  # You can change to "gpt-4" or other models
    use_local=False  # Set to True to use local Ollama model
)

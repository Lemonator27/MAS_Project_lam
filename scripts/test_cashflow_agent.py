import os
import sys
from datetime import datetime

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from agents.cashflow_agent import CashFlowAgentExecutor

def test_cashflow_agent():
    """Test the enhanced cash flow agent with various queries"""
    
    # Initialize agent with GPT-3.5-turbo
    agent = CashFlowAgentExecutor(
        model_name="gpt-3.5-turbo",
        use_local=False  # Set to True to use Ollama's local model
    )
    
    # Test queries to demonstrate different capabilities
    test_queries = [
        # Basic cash flow analysis
        "Phân tích dòng tiền hiện tại",
        
        # Future predictions with different timeframes
        "Dự báo dòng tiền 30 ngày tới",
        "Dự đoán cash flow 60 ngày tới",
        
        # Specific analysis requests
        "So sánh doanh thu và chi phí 3 tháng gần đây",
        "Phân tích xu hướng dòng tiền và đưa ra cảnh báo nếu có",
        
        # Combined analysis
        "Đánh giá tình hình hiện tại và dự báo 90 ngày tới",
        
        # Risk assessment
        "Có dấu hiệu rủi ro về dòng tiền không?",
        
        # Trend analysis
        "Xu hướng dòng tiền đang tăng hay giảm?",
    ]
    
    print("🔄 Testing Enhanced Cash Flow Agent")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 30)
        
        try:
            # Run query through agent
            result = agent.invoke({"input": query})
            
            # Print response
            print("\nResponse:")
            print(result.get("output", "No output"))
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("-" * 50)
    
    print("\n✅ Testing completed!")

def compare_models():
    """Compare responses between OpenAI and local models"""
    
    # Test query for comparison
    test_query = "Phân tích dòng tiền hiện tại và dự báo 30 ngày tới"
    
    print("🔄 Comparing Model Responses")
    print("=" * 50)
    
    # Test with OpenAI model
    print("\n1. Testing with gpt-5-nano:")
    try:
        openai_agent = CashFlowAgentExecutor(model_name="gpt-5-nano", use_local=False)
        result = openai_agent.invoke({"input": test_query})
        print(result.get("output", "No output"))
    except Exception as e:
        print(f"❌ Error with OpenAI model: {str(e)}")
    
    print("\n2. Testing with Local Llama2:")
    try:
        local_agent = CashFlowAgentExecutor(use_local=True)
        result = local_agent.invoke({"input": test_query})
        print(result.get("output", "No output"))
    except Exception as e:
        print(f"❌ Error with local model: {str(e)}")
    
    print("\n✅ Comparison completed!")

if __name__ == "__main__":
    # Run basic tests
    test_cashflow_agent()
    
    # Uncomment to run model comparison
    # compare_models()
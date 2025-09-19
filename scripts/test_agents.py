import os
import sys

# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from orchestration.mas_graph import app as mas_app

def test_agents():
    """Test all agents with sample queries"""
    
    test_queries = [
        # Budget Agent
        "So sánh budget marketing tháng này?",
        "Ngân sách phòng R&D như thế nào?",
        
        # Spending Agent  
        "Chi tiêu subscription theo vendor?",
        "Vendor nào tốn nhiều nhất?",
        
        # Alert Agent
        "Phát hiện giao dịch bất thường",
        "Có giao dịch nào vượt ngưỡng bất thường không?",
        
        # Cash Flow Agent
        "Phân tích dòng tiền hiện tại",
        "Dự báo cash flow 30 ngày tới",
        
        # Invoice Agent
        "Hóa đơn nào đang quá hạn?",
        "Tình trạng thanh toán hóa đơn",
        
        # RAG queries
        "Chính sách chi tiêu > 5000 USD cần ai duyệt?",
        "Quy định travel policy như thế nào?"
    ]
    
    print("🧪 Testing Multi-Agent Finance System")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 30)
        
        try:
            result = mas_app.invoke({"messages": [{"role": "user", "content": query}]})
            output = result.get("result", {})
            
            agent_type = output.get("type", "unknown")
            print(f"Agent: {agent_type}")
            
            if isinstance(output.get("output"), list):
                print(f"Records: {len(output['output'])}")
                if output["output"]:
                    print(f"Sample: {output['output'][0]}")
            else:
                print(f"Output: {output.get('output', 'No output')[:200]}...")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_agents()

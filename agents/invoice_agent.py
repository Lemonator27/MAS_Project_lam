import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta

def load_invoice_data(path: str = "data/invoices_data.csv") -> pd.DataFrame:
    """Load invoice data"""
    try:
        df = pd.read_csv(path)
        df['invoice_date'] = pd.to_datetime(df['invoice_date'])
        df['due_date'] = pd.to_datetime(df['due_date'])
        return df
    except Exception:
        # Fallback data
        return pd.DataFrame({
            "invoice_id": ["INV_001", "INV_002"],
            "vendor": ["Vendor A", "Vendor B"],
            "amount": [1000, 2000],
            "status": ["pending", "paid"],
            "is_overdue": [False, False]
        })

def analyze_invoice_status(df: pd.DataFrame) -> str:
    """Analyze invoice status and overdue payments"""
    if df.empty:
        return "Không có dữ liệu hóa đơn để phân tích."
    
    # Calculate statistics
    total_invoices = len(df)
    pending_invoices = len(df[df['status'] == 'pending'])
    paid_invoices = len(df[df['status'] == 'paid'])
    overdue_invoices = len(df[df['is_overdue'] == True])
    
    total_amount = df['amount'].sum()
    pending_amount = df[df['status'] == 'pending']['amount'].sum()
    overdue_amount = df[df['is_overdue'] == True]['amount'].sum()
    
    # Vendor analysis
    vendor_summary = df.groupby('vendor').agg({
        'amount': ['sum', 'count'],
        'status': lambda x: (x == 'pending').sum()
    }).round(2)
    
    vendor_summary.columns = ['total_amount', 'invoice_count', 'pending_count']
    top_vendors = vendor_summary.sort_values('total_amount', ascending=False).head(5)
    
    # Payment terms analysis
    payment_terms_analysis = df['payment_terms'].value_counts()
    
    # Generate insights
    insights = []
    
    if overdue_invoices > 0:
        insights.append(f"🚨 {overdue_invoices} hóa đơn quá hạn (${overdue_amount:,.2f})")
    
    if pending_amount > total_amount * 0.3:
        insights.append(f"⚠️ {pending_amount/total_amount*100:.1f}% tổng giá trị hóa đơn chưa thanh toán")
    
    avg_invoice_amount = total_amount / total_invoices if total_invoices > 0 else 0
    if avg_invoice_amount > 10000:
        insights.append("💰 Hóa đơn trung bình cao - cần theo dõi cash flow")
    
    return f"""
**Tổng quan hóa đơn:**
- Tổng số hóa đơn: {total_invoices}
- Đã thanh toán: {paid_invoices} (${total_amount - pending_amount:,.2f})
- Chưa thanh toán: {pending_invoices} (${pending_amount:,.2f})
- Quá hạn: {overdue_invoices} (${overdue_amount:,.2f})

**Top 5 vendors theo giá trị:**
{vendor_summary.head().to_string()}

**Phân tích điều khoản thanh toán:**
{payment_terms_analysis.to_string()}

**Insights:**
{chr(10).join(insights) if insights else "✅ Tất cả hóa đơn đều trong tình trạng tốt"}
"""

def invoice_tool(query: str) -> str:
    """Main invoice analysis tool"""
    df = load_invoice_data()
    return analyze_invoice_status(df)

class InvoiceAgentExecutor:
    """Invoice Management Agent Executor"""
    
    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        query = inputs.get("input", "")
        result = invoice_tool(query)
        
        return {"output": result}

invoice_agent_executor = InvoiceAgentExecutor()

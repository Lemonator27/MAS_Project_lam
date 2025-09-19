import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
from typing import List, Dict

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_budget_data(n=100) -> pd.DataFrame:
    """Generate synthetic budget data for Budget Agent"""
    departments = [
        "Marketing", "Sales", "R&D", "Engineering", "HR", "Finance", 
        "Operations", "Customer Success", "Product", "Legal", "IT", "Admin"
    ]
    
    projects = [f"Project_{i:03d}" for i in range(1, 51)]
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    
    data = []
    for i in range(n):
        dept = random.choice(departments)
        project = random.choice(projects)
        quarter = random.choice(quarters)
        year = random.choice([2023, 2024])
        
        # Generate realistic budget amounts
        base_amount = np.random.lognormal(10, 1)  # Log-normal distribution
        approved = round(base_amount, 2)
        
        # Actual spent varies around approved (80-120% typically)
        variance_factor = np.random.normal(0.95, 0.15)
        variance_factor = max(0.5, min(1.5, variance_factor))  # Clamp between 50-150%
        actual = round(approved * variance_factor, 2)
        
        data.append({
            "dept": dept,
            "project_id": project,
            "quarter": quarter,
            "year": year,
            "approved_amount": approved,
            "actual_spent": actual,
            "category": random.choice(["Capital", "Operating", "R&D", "Marketing", "Travel"])
        })
    
    return pd.DataFrame(data)

def generate_transaction_data(n=100) -> pd.DataFrame:
    """Generate synthetic transaction data for Spending/Alert Agent"""
    merchants = [
        "Amazon Web Services", "Microsoft Azure", "Google Cloud", "Slack", "Zoom", "Notion",
        "Adobe Creative Suite", "Salesforce", "HubSpot", "Stripe", "PayPal", "Shopify",
        "LinkedIn Ads", "Google Ads", "Facebook Ads", "Twitter Ads", "TikTok Ads",
        "Uber", "Lyft", "Delta Airlines", "United Airlines", "American Airlines",
        "Marriott", "Hilton", "Airbnb", "Expedia", "Booking.com",
        "Starbucks", "McDonald's", "Subway", "Chipotle", "Pizza Hut",
        "Office Depot", "Staples", "Best Buy", "Apple Store", "Microsoft Store",
        "GitHub", "Atlassian", "Trello", "Asana", "Monday.com", "Basecamp"
    ]
    
    categories = [
        "subscription", "travel", "marketing", "payroll", "office_supplies",
        "software", "hardware", "consulting", "legal", "insurance", "utilities",
        "meals", "entertainment", "training", "conference", "advertising"
    ]
    
    employees = [f"EMP_{i:03d}" for i in range(1, 101)]
    
    data = []
    for i in range(n):
        # Generate transaction date in last 12 months
        days_ago = random.randint(1, 365)
        date = datetime.now() - timedelta(days=days_ago)
        
        merchant = random.choice(merchants)
        category = random.choice(categories)
        employee = random.choice(employees)
        
        # Generate amount based on category (different distributions)
        if category == "subscription":
            amount = np.random.lognormal(6, 1)  # $100-2000 typically
        elif category == "travel":
            amount = np.random.lognormal(7, 1)  # $500-5000 typically
        elif category == "marketing":
            amount = np.random.lognormal(8, 1)  # $1000-10000 typically
        elif category == "payroll":
            amount = np.random.lognormal(9, 1)  # $5000-50000 typically
        else:
            amount = np.random.lognormal(6.5, 1)  # $200-3000 typically
        
        amount = round(amount, 2)
        
        # Generate fraud flag (5% chance of fraud)
        fraud_flag = 1 if random.random() < 0.05 else 0
        
        # Make some transactions anomalous (high amounts)
        if random.random() < 0.1:  # 10% chance of high amount
            amount = round(amount * np.random.uniform(3, 10), 2)
        
        data.append({
            "transaction_id": f"TXN_{i+1:06d}",
            "amount": amount,
            "date": date.strftime("%Y-%m-%d"),
            "category": category,
            "merchant": merchant,
            "employee_id": employee,
            "fraud_flag": fraud_flag,
            "description": f"Payment to {merchant} for {category}",
            "payment_method": random.choice(["credit_card", "bank_transfer", "check", "cash"]),
            "currency": "USD",
            "status": random.choice(["completed", "pending", "failed"]),
            "approval_required": 1 if amount > 5000 else 0
        })
    
    return pd.DataFrame(data)

def generate_cashflow_data(n=100) -> pd.DataFrame:
    """Generate synthetic cash flow data for Cash Flow Agent"""
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(n):
        date = base_date + timedelta(days=i)
        month = date.month
        quarter = f"Q{(month-1)//3 + 1}"
        
        # Generate realistic cash flow patterns
        # Revenue (positive)
        revenue = np.random.lognormal(12, 0.5)  # $50k-500k typically
        
        # Operating expenses (negative)
        operating_exp = np.random.lognormal(11.5, 0.4)  # $30k-300k typically
        
        # Capital expenditures (negative, less frequent)
        capex = np.random.lognormal(10, 1) if random.random() < 0.3 else 0
        
        # Net cash flow
        net_cashflow = revenue - operating_exp - capex
        
        # Cash balance (cumulative)
        if i == 0:
            cash_balance = np.random.lognormal(13, 0.5)  # $100k-1M starting
        else:
            prev_balance = data[-1]["cash_balance"]
            cash_balance = prev_balance + net_cashflow
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "quarter": quarter,
            "revenue": round(revenue, 2),
            "operating_expenses": round(operating_exp, 2),
            "capital_expenditures": round(capex, 2),
            "net_cashflow": round(net_cashflow, 2),
            "cash_balance": round(cash_balance, 2),
            "cash_flow_category": random.choice(["operating", "investing", "financing"]),
            "forecast_accuracy": round(np.random.uniform(0.85, 0.98), 3)
        })
    
    return pd.DataFrame(data)

def generate_invoice_data(n=100) -> pd.DataFrame:
    """Generate synthetic invoice data for Invoice Management Agent"""
    vendors = [
        "TechCorp Solutions", "Global Services Inc", "Premier Consulting", "Elite Systems",
        "Advanced Technologies", "Professional Services Co", "Innovation Labs", "Digital Partners",
        "Strategic Solutions", "Excellence Corp", "Prime Services", "Superior Systems",
        "Enterprise Solutions", "Premium Technologies", "Master Services", "Ultimate Systems"
    ]
    
    invoice_types = ["services", "products", "consulting", "software", "hardware", "maintenance"]
    payment_terms = ["Net 30", "Net 15", "Net 45", "Due on Receipt", "Net 60"]
    statuses = ["pending", "approved", "paid", "overdue", "disputed", "cancelled"]
    
    data = []
    for i in range(n):
        # Generate invoice date
        days_ago = random.randint(1, 180)
        invoice_date = datetime.now() - timedelta(days=days_ago)
        
        vendor = random.choice(vendors)
        invoice_type = random.choice(invoice_types)
        payment_term = random.choice(payment_terms)
        status = random.choice(statuses)
        
        # Generate amount
        amount = np.random.lognormal(8, 1)  # $1000-50000 typically
        amount = round(amount, 2)
        
        # Calculate due date based on payment terms
        if payment_term == "Due on Receipt":
            due_date = invoice_date
        elif payment_term == "Net 15":
            due_date = invoice_date + timedelta(days=15)
        elif payment_term == "Net 30":
            due_date = invoice_date + timedelta(days=30)
        elif payment_term == "Net 45":
            due_date = invoice_date + timedelta(days=45)
        else:  # Net 60
            due_date = invoice_date + timedelta(days=60)
        
        # Determine if overdue
        is_overdue = datetime.now() > due_date and status not in ["paid", "cancelled"]
        
        data.append({
            "invoice_id": f"INV_{i+1:06d}",
            "vendor": vendor,
            "invoice_date": invoice_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "amount": amount,
            "invoice_type": invoice_type,
            "payment_terms": payment_term,
            "status": status,
            "is_overdue": is_overdue,
            "description": f"Services provided by {vendor}",
            "po_number": f"PO_{random.randint(1000, 9999)}",
            "approval_required": 1 if amount > 10000 else 0,
            "approved_by": f"Manager_{random.randint(1, 20)}" if status in ["approved", "paid"] else None
        })
    
    return pd.DataFrame(data)

def generate_rag_documents() -> List[Dict]:
    """Generate synthetic documents for RAG system"""
    documents = [
        {
            "text": "Policy: Chi tiêu trên $5,000 cần được phê duyệt bởi CFO. Chi tiêu trên $10,000 cần được phê duyệt bởi CEO.",
            "category": "spending_policy",
            "tags": ["approval", "spending_limit", "cfo", "ceo"]
        },
        {
            "text": "GAAP: Tất cả báo cáo tài chính phải tuân thủ nguyên tắc dồn tích (accrual basis). Doanh thu được ghi nhận khi dịch vụ được cung cấp.",
            "category": "accounting_standards",
            "tags": ["gaap", "accrual", "revenue_recognition"]
        },
        {
            "text": "Travel Policy: Giới hạn $2,000 mỗi nhân viên mỗi tháng cho chi phí đi lại. Ngoại lệ cần phê duyệt trước 48 giờ.",
            "category": "travel_policy",
            "tags": ["travel", "limit", "approval", "expense"]
        },
        {
            "text": "Subscription Management: Tất cả subscription SaaS phải được đánh giá hàng quý. Subscription không sử dụng trong 6 tháng sẽ bị cắt giảm.",
            "category": "subscription_policy",
            "tags": ["saas", "subscription", "review", "optimization"]
        },
        {
            "text": "Cash Flow Management: Duy trì tỷ lệ thanh khoản tối thiểu 2:1. Cảnh báo khi dự báo dòng tiền âm trong 30 ngày tới.",
            "category": "cash_flow_policy",
            "tags": ["cash_flow", "liquidity", "forecast", "alert"]
        },
        {
            "text": "Vendor Management: Đánh giá vendor hàng năm. Ưu tiên vendor có giá cả cạnh tranh và dịch vụ tốt.",
            "category": "vendor_policy",
            "tags": ["vendor", "evaluation", "cost_optimization"]
        },
        {
            "text": "Fraud Detection: Giao dịch trên $1,000 từ vendor mới cần xác minh. Giao dịch bất thường sẽ được flag tự động.",
            "category": "fraud_prevention",
            "tags": ["fraud", "detection", "verification", "anomaly"]
        },
        {
            "text": "Budget Planning: Ngân sách được lập hàng quý. Variance trên 10% cần giải thích và điều chỉnh.",
            "category": "budget_policy",
            "tags": ["budget", "planning", "variance", "quarterly"]
        },
        {
            "text": "Invoice Processing: Hóa đơn phải được xử lý trong 5 ngày làm việc. Hóa đơn quá hạn sẽ bị phạt 1.5% mỗi tháng.",
            "category": "invoice_policy",
            "tags": ["invoice", "processing", "deadline", "penalty"]
        },
        {
            "text": "Cost Optimization: Mục tiêu giảm 5% chi phí operating mỗi năm. Tập trung vào subscription và vendor optimization.",
            "category": "cost_optimization",
            "tags": ["cost_reduction", "optimization", "subscription", "vendor"]
        }
    ]
    
    # Generate more variations
    for i in range(90):
        categories = ["spending_policy", "travel_policy", "budget_policy", "vendor_policy", "fraud_prevention"]
        category = random.choice(categories)
        
        if category == "spending_policy":
            amount = random.choice([1000, 2500, 5000, 7500, 10000])
            approver = random.choice(["Manager", "Director", "CFO", "CEO"])
            text = f"Policy: Chi tiêu trên ${amount:,} cần được phê duyệt bởi {approver}. Chi tiêu này bao gồm {random.choice(['travel', 'marketing', 'software', 'consulting'])}."
            
        elif category == "travel_policy":
            limit = random.choice([1500, 2000, 2500, 3000])
            text = f"Travel Policy: Giới hạn ${limit:,} mỗi {random.choice(['nhân viên', 'phòng ban'])} mỗi {random.choice(['tháng', 'quý'])} cho chi phí đi lại."
            
        elif category == "budget_policy":
            variance = random.choice([5, 10, 15, 20])
            text = f"Budget Policy: Variance trên {variance}% cần {random.choice(['giải thích', 'phê duyệt', 'điều chỉnh'])}. Ngân sách được {random.choice(['lập', 'review'])} {random.choice(['hàng tháng', 'hàng quý', 'hàng năm'])}."
            
        elif category == "vendor_policy":
            text = f"Vendor Policy: Đánh giá vendor {random.choice(['hàng quý', 'hàng năm', '6 tháng'])}. Ưu tiên {random.choice(['giá cả', 'dịch vụ', 'chất lượng'])} cạnh tranh."
            
        else:  # fraud_prevention
            amount = random.choice([500, 1000, 1500, 2000])
            text = f"Fraud Prevention: Giao dịch trên ${amount:,} từ {random.choice(['vendor mới', 'địa điểm mới', 'thời gian bất thường'])} cần xác minh."
        
        documents.append({
            "text": text,
            "category": category,
            "tags": [category.split("_")[0], "policy", "management"]
        })
    
    return documents

def main():
    """Generate all synthetic datasets"""
    print("Generating synthetic datasets...")
    
    # Generate datasets
    budget_df = generate_budget_data(100)
    transaction_df = generate_transaction_data(100)
    cashflow_df = generate_cashflow_data(100)
    invoice_df = generate_invoice_data(100)
    rag_docs = generate_rag_documents()
    
    # Save to files
    budget_df.to_csv("data/budgets_extended.csv", index=False)
    transaction_df.to_csv("data/transactions_extended.csv", index=False)
    cashflow_df.to_csv("data/cashflow_data.csv", index=False)
    invoice_df.to_csv("data/invoices_data.csv", index=False)
    
    # Save RAG documents
    with open("data/rag_documents.json", "w", encoding="utf-8") as f:
        json.dump(rag_docs, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(budget_df)} budget records")
    print(f"Generated {len(transaction_df)} transaction records")
    print(f"Generated {len(cashflow_df)} cashflow records")
    print(f"Generated {len(invoice_df)} invoice records")
    print(f"Generated {len(rag_docs)} RAG documents")
    print("\nFiles saved:")
    print("- data/budgets_extended.csv")
    print("- data/transactions_extended.csv")
    print("- data/cashflow_data.csv")
    print("- data/invoices_data.csv")
    print("- data/rag_documents.json")

if __name__ == "__main__":
    main()

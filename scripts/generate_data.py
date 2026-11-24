"""Synthetic business finance dataset (fictional company: FinPulse). Seeded -> reproducible."""
import os
import numpy as np, pandas as pd
rng = np.random.default_rng(7)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data"); os.makedirs(out, exist_ok=True)

# ---- products: (name, category, department, avg price INR, margin)
P = [("Office Chair","Furniture","Operations",9500,.30),("Standing Desk","Furniture","Operations",24000,.28),("Filing Cabinet","Furniture","Operations",7800,.33),
     ("Laptop","Technology","Technology",68000,.22),("Tablet","Technology","Technology",32000,.24),("External SSD","Technology","Technology",7500,.35),
     ("Business Laptop","Technology","Technology",85000,.21),("Cloud Subscription","Software","Technology",18000,.55),("Accounting Software","Software","Finance",26000,.52),
     ("Backup Service","Software","Technology",14000,.50),("Security Suite","Software","Finance",21000,.48),("Printer","Office Equipment","Operations",16000,.27),
     ("Document Scanner","Office Equipment","Operations",12500,.30),("Projector","Office Equipment","Marketing",28000,.26),("Shredder","Office Equipment","Operations",6500,.32),
     ("Keyboard & Mouse","Accessories","Marketing",2200,.40),("Webcam","Accessories","Marketing",3800,.38),("Headset","Accessories","Marketing",4500,.37),
     ("Monitor Stand","Accessories","Operations",2800,.42),("Ad Banner Pack","Accessories","Marketing",5200,.45)]
prod = pd.DataFrame([(f"P{i+1:03d}",*p[:4]) for i,p in enumerate(P)],columns=["product_id","product_name","category","department","list_price"])
margin = {f"P{i+1:03d}":p[4] for i,p in enumerate(P)}

# ---- customers
first=["Aarav","Vivaan","Arjun","Karthik","Rahul","Rohit","Suresh","Vijay","Manoj","Dinesh","Priya","Ananya","Divya","Kavya","Meena","Lakshmi","Sneha","Pooja","Deepa","Anjali"]
last=["Kumar","Sharma","Reddy","Nair","Iyer","Patel","Singh","Gowda","Rao","Pillai","Das","Mehta"]
N_C=150
cust = pd.DataFrame({"customer_id":[f"C{i+1:03d}" for i in range(N_C)],
  "customer_name":[f"{rng.choice(first)} {rng.choice(last)}" for _ in range(N_C)],
  "region":rng.choice(["North","South","East","West"],N_C,p=[.22,.34,.18,.26]),
  "segment":rng.choice(["Enterprise","SMB","Startup"],N_C,p=[.25,.5,.25])})

# ---- add state/city/country consistent with region (separate RNG so other data stays identical)
_r2 = np.random.default_rng(99)
_geo = {"North":{"Delhi":["New Delhi"],"Punjab":["Ludhiana","Amritsar"],"Haryana":["Gurugram","Faridabad"],"Uttar Pradesh":["Lucknow","Noida"],"Rajasthan":["Jaipur","Jodhpur"]},
        "South":{"Karnataka":["Bengaluru","Mysuru"],"Tamil Nadu":["Chennai","Coimbatore"],"Kerala":["Kochi","Thiruvananthapuram"],"Telangana":["Hyderabad","Warangal"],"Andhra Pradesh":["Visakhapatnam","Vijayawada"]},
        "East":{"West Bengal":["Kolkata","Siliguri"],"Odisha":["Bhubaneswar","Cuttack"],"Bihar":["Patna","Gaya"],"Jharkhand":["Ranchi","Jamshedpur"]},
        "West":{"Maharashtra":["Mumbai","Pune"],"Gujarat":["Ahmedabad","Surat"],"Goa":["Panaji"],"Madhya Pradesh":["Bhopal","Indore"]}}
_st, _ct = [], []
for rg in cust.region:
    s_ = _r2.choice(list(_geo[rg])); _st.append(s_); _ct.append(_r2.choice(_geo[rg][s_]))
cust["state"] = _st; cust["city"] = _ct; cust["country"] = "India"

# ---- transactions 2022-2025 (growth, seasonality, weekday skew)
yg={2022:1.0,2023:1.12,2024:1.25,2025:1.38}; seas=np.array([.88,.85,.95,.98,1.0,1.0,1.02,1.03,1.05,1.12,1.14,1.12])
rows=[]
for y,g in yg.items():
    days=pd.date_range(f"{y}-01-01",f"{y}-12-31")
    w=seas[days.month-1]*np.where(days.dayofweek<5,1.2,.7); w=w/w.sum()
    n=int(5200*g); rows.append((y,n,rng.choice(days,n,p=w)))
tx=[]
pw=np.array([.05,.04,.04,.06,.06,.07,.04,.07,.05,.05,.04,.05,.04,.04,.03,.07,.05,.05,.04,.05]); pw/=pw.sum()
for y,n,d in rows:
    pid=rng.choice(prod.product_id,n,p=pw)
    price=prod.set_index("product_id").list_price[pid].values
    qty=rng.choice([1,2,3,4,5],n,p=[.5,.25,.12,.08,.05])
    rev=(price*qty*rng.normal(1,.06,n)*(1+(y-2022)*.02)).round(2)
    m=np.array([margin[p] for p in pid])+rng.normal(0,.025,n)+(y-2022)*.004
    exp=(rev*(1-m)).round(2)
    tx.append(pd.DataFrame({"transaction_date":d,"customer_id":rng.choice(cust.customer_id,n),"product_id":pid,"quantity":qty,
      "sales_channel":rng.choice(["Direct Sales","Online","Partner","Retail"],n,p=[.2,.38,.25,.17]),
      "payment_method":rng.choice(["Bank Transfer","Credit Card","Debit Card","Cash"],n,p=[.4,.3,.2,.1]),
      "transaction_status":rng.choice(["Completed","Pending","Cancelled"],n,p=[.9,.06,.04]),
      "revenue":rev,"expenses":exp}))
f=pd.concat(tx).sort_values("transaction_date").reset_index(drop=True)
f.insert(0,"transaction_id",[f"FP-{i+1:05d}" for i in range(len(f))])
f["transaction_date"]=pd.to_datetime(f.transaction_date).dt.date

# ---- monthly budget per department (completed revenue/expenses x noise)
c=f[f.transaction_status=="Completed"].merge(prod[["product_id","department"]],on="product_id")
c["year"]=pd.to_datetime(c.transaction_date).dt.year; c["month"]=pd.to_datetime(c.transaction_date).dt.month
b=c.groupby(["year","month","department"])[["revenue","expenses"]].sum().reset_index()
b["budget_revenue"]=(b.revenue*rng.normal(1.03,.05,len(b))).round(2); b["budget_expenses"]=(b.expenses*rng.normal(0.99,.05,len(b))).round(2)
b=b[["year","month","department","budget_revenue","budget_expenses"]]

f.to_csv(os.path.join(out,"fact_transactions.csv"),index=False); cust.to_csv(os.path.join(out,"dim_customers.csv"),index=False)
prod.to_csv(os.path.join(out,"dim_products.csv"),index=False); b.to_csv(os.path.join(out,"budget.csv"),index=False)
print(f.shape,cust.shape,prod.shape,b.shape)

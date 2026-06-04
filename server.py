# path: cd project_coll/simulated_bank
# D:/appcode/miniconda3/envs/python312/python.exe -m uvicorn server:app --reload

import pymysql
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates # template path finder 
from fastapi.responses import HTMLResponse, RedirectResponse #a response class for html,a fastapi response type to redirect to a new site
from datetime import datetime
from typing import Optional #for main page has more than one form, the marked action string need to be optional
from openai import OpenAI

#get server object
app=FastAPI()
#get html path use parameter'directory'
templates= Jinja2Templates(directory='templates') 

#get api,enter password
client_ai = OpenAI(api_key="",
    base_url="https://api.groq.com/openai/v1")

#copy the prompt from the groq website and make it a function to use below
def get_financial_tip(balance, income, expense, type_summary):
    prompt = f"""你是一个为这个展板准备的ai理财助理，请使用一下数据给出一段简短的实用理财建议：
    用户信息: Balance: {balance}, Income: {income}, Expense: {expense}, 
    Expense on different type: {type_summary} 请用中文回答，控制在5句话以内."""
    response = client_ai.chat.completions.create(
       model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

#data was stored in mysql
def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",

        #enter password
        password="",
        database="simulated_bank",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def fetch_one(sql, params=()):
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    finally:
        conn.close()

def fetch_all(sql, params=()):
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        conn.close()

@app.get('/')
def root(request:Request):
    return templates.TemplateResponse('page0.html',{'request':request})

@app.get('/customer0',response_class=HTMLResponse)
def customer0(request:Request):
    return templates.TemplateResponse('customer0.html',{'request':request})

#login page
@app.post('/customer0',response_class=HTMLResponse)
def customer_login(request:Request,input_id:str=Form(...),input_password:str=Form(...)):

    #clean the two form inputs
    input_id = input_id.strip()
    input_password = input_password.strip()

    #retrieve customer
    cus = fetch_one("SELECT * FROM cus_info WHERE account_id=%s",(input_id,))

    #login condition if-else
    if not cus:
        return templates.TemplateResponse('customer0.html',{'request':request,'error1':'ID不存在'})
    if cus["password"] == input_password:
        return RedirectResponse(url=f'/customer1/{input_id}',status_code=303) 
    else:  
        return templates.TemplateResponse('customer0.html',{'request':request,'error2':'密码错误'})

#main page
@app.get('/customer1/{input_id}', response_class=HTMLResponse)
def customer_page(request: Request, input_id: str):
    now = datetime.now()
    now_str = now.strftime("%Y-%m")

    month_start = datetime(now.year, now.month, 1)
    if now.month == 12:
        month_end = datetime(now.year + 1, 1, 1)
    else:
        month_end = datetime(now.year, now.month + 1, 1)

    trans_now = fetch_all("""
        SELECT * FROM transactions
        WHERE account_id=%s AND time >= %s AND time < %s
        ORDER BY time ASC""", (input_id, month_start, month_end))

    balance = sum(t["amount"] for t in trans_now)
    income = sum(t["amount"] for t in trans_now if t["amount"] > 0)
    expense = sum(t["amount"] for t in trans_now if t["amount"] < 0)

    type_summary = fetch_all("""
        SELECT type, SUM(amount) AS total
        FROM transactions
        WHERE account_id=%s AND time >= %s AND time < %s
        GROUP BY type""", (input_id, month_start, month_end))

    ai_tip = get_financial_tip(balance, income, expense, type_summary)

    recent = fetch_all("""
        SELECT * FROM transactions
        WHERE account_id=%s AND time >= %s AND time < %s
        ORDER BY time DESC
        LIMIT 5""", (input_id, month_start, month_end))

    return templates.TemplateResponse('customer1.html', {'request': request,'input_id': input_id,
        'balance': balance,'income': income,'expense': expense,
        'type_summary': type_summary,'recent': recent,
        'now_str': now_str,'ai_tip': ai_tip
    })

@app.post('/customer1/{input_id}', response_class=HTMLResponse)
def search(request: Request, input_id: str, selected_month: Optional[str] = Form(None), action: Optional[str] = Form(None)):
    if action == "logout":
        return RedirectResponse(url="/", status_code=303)

    if action == "search":
        if not selected_month:
            selected_month = datetime.now().strftime("%Y-%m")

        month_start = datetime.strptime(selected_month, "%Y-%m")
        if month_start.month == 12:
            month_end = datetime(month_start.year + 1, 1, 1)
        else:
            month_end = datetime(month_start.year, month_start.month + 1, 1)

        trans_now = fetch_all("""
            SELECT * FROM transactions
            WHERE account_id=%s AND time >= %s AND time < %s
            ORDER BY time ASC""", (input_id, month_start, month_end))

        balance = sum(t["amount"] for t in trans_now)
        income = sum(t["amount"] for t in trans_now if t["amount"] > 0)
        expense = sum(t["amount"] for t in trans_now if t["amount"] < 0)

        type_summary = fetch_all("""
            SELECT type, SUM(amount) AS total
            FROM transactions
            WHERE account_id=%s AND time >= %s AND time < %s
            GROUP BY type""", (input_id, month_start, month_end))

        ai_tip = get_financial_tip(balance, income, expense, type_summary)

        recent = fetch_all("""
            SELECT * FROM transactions
            WHERE account_id=%s AND time >= %s AND time < %s
            ORDER BY time DESC
            LIMIT 5""", (input_id, month_start, month_end))

        return templates.TemplateResponse('customer1.html', {'request': request,'input_id': input_id,
            'balance': balance,'income': income,'expense': expense,'type_summary': type_summary,'recent': recent,
            'now_str': selected_month,'ai_tip': ai_tip
        })
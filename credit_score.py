import pandas as pd
import joblib
from flask import Flask,request,jsonify,render_template
import penalty
from penalty import apply_penalties,total_debt


app=Flask(__name__)
model1=joblib.load('Randomforest.pkl')
model2=joblib.load('lr_baggingmodel.pkl')

@app.route('/')
def home():
    return render_template('predict.html')

@app.route ('/predict',methods=['POST'])

def predict():
    
    Annual_income=int(request.form.get("Annual_Income"))
    numofcreditcard=int(request.form.get('Num_Credit_Card'))
    numofloan=int(request.form.get('Num_of_Loan'))
    delayfromduedate=int(request.form.get('Delay_from_due_date'))
    changecreditlimit=int(request.form.get('Changed_Credit_Limit'))
    outstandingdebt=int(request.form.get('Outstanding_Debt'))
    credithistory=int(request.form.get('Credit_History_Age'))
    investedamount=int(request.form.get('Amount_invested_monthly'))
    monthlybalance=int(request.form.get('Monthly_Balance'))
    monthlyinhandsalary=int(request.form.get('Monthly_Inhand_Salary'))
    interestrate=int(request.form.get('Interest_Rate'))
    Totalemi=int(request.form.get('Total_EMI_per_month'))
    numofdelayedpayments=int(request.form.get('Num_of_Delayed_Payment'))
    numofcreditinquiry=int(request.form.get("Num_Credit_Inquiries"))

    features=[[Annual_income,numofcreditcard,interestrate,numofloan,delayfromduedate,
               numofdelayedpayments,changecreditlimit,numofcreditinquiry,outstandingdebt,credithistory,investedamount,
                monthlybalance,monthlyinhandsalary,Totalemi]]
    prediction1=model1.predict(features)
    prediction2=model2.predict(features)
    if prediction1==prediction2:
        pd=prediction2 
    else: 
        pd=prediction1
    try:
        if pd==0:
            score =600
            score=apply_penalties(score,numofdelayedpayments,numofcreditinquiry,delayfromduedate,numofcreditcard,outstandingdebt)
            score=max(score,300)
            
            
        elif pd==1:
            score=750
            score=apply_penalties(score,numofdelayedpayments,numofcreditinquiry,delayfromduedate,numofcreditcard,outstandingdebt)
            score= max(score,500)
            
        if score<=580:
            category="POOR"
        elif score>580: 
            category="GOOD"       
        return jsonify({'scoreValue':score,'scoreCategory':category})
    except Exception as e:
        score="N/A"
        category="Error"
        print(f"Error calculating score {e}")
        return jsonify({'scoreValue':"N/A",'scoreCategory':"Error"})

        
if __name__ == "__main__":
    app.run(debug=True)



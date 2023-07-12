import plotly.graph_objs as go
from flask import Flask,render_template,request,url_for
import pandas as pd
import numpy as np
import plotly_express as px
import utilis
from utilis import prediction
server = Flask(__name__)
df=pd.read_csv('C:\datascience\IBM Attrition Data.csv')
# print(data)
@server.route('/')
def index():
    return render_template('att.html')
@server.route('/predict')
def predict():
    return render_template('predict.html')
@server.route('/display/',methods=['POST','GET'])
def display():
    input=[] #input to the model
    given=[]
    if request.method=='POST':
        age=request.form['age']
        given.append(age)
        department=request.form['Department']
        given.append(department)
        distance=request.form['distance']
        given.append(distance)
        education=request.form['ed']
        given.append(education)
        education_feild=request.form['education']
        given.append(education_feild)
        job_satisfaction=request.form['job_satisfaction']
        given.append(job_satisfaction)
        environment=request.form['environment']
        given.append(environment)
        maritial_status=request.form['maritial_status']
        given.append(maritial_status)
        monthlyincome=request.form['monthly_income']
        given.append(monthlyincome)
        companies_worked=request.form['companies_worked']
        given.append(companies_worked)
        work_life=request.form['work_life']
        given.append(work_life)
        years_at_company=request.form['years_at_company']
        given.append(years_at_company)
        print(len(given))
        print(given)
        input.append(int(age))
        input.append(int(distance))
        if education=='High school':
            input.append(1)
        elif education=='Degree':
            input.append(2)
        elif education=='Bachlers':
            input.append(3)
        elif education=='Masters':
            input.append(4)
        elif education=='Phd':
            input.append(5)
        t=[]
        t.append(environment)
        t.append(job_satisfaction)
        for i in range(2):
            if t[i]=='Bad':
                input.append(1)
            elif t[i]=='Good':
                input.append(2)
            elif t[i]=='Very Good':
                input.append(3)
            else:
                input.append(4)
        x=int(monthlyincome)
        input.append(np.log1p(x))
        input.append(int(companies_worked))
        if work_life=='Bad':
                input.append(1)
        if work_life=='Good':
            input.append(2)
        if work_life=='Very Good':
            input.append(3)
        if work_life=='Excellent':
            input.append(4)
        input.append(int(years_at_company))
        if department=='Sales':
            input.extend([0,1,0])
        if department=='Research & Development':
            input.extend([1,0,0])
        if department=='Human Resources':
            input.extend([0,0,1])
        if education_feild=='Human Resources':
            input.extend([1,0,0,0,0,0])
        if education_feild=='LifeSciences':
            input.extend([0,1,0,0,0,0])
        if education_feild=='Marketing':
            input.extend([0,0,1,0,0,0])
        if education_feild=='Medical':
            input.extend([0,0,0,1,0,0])
        if education_feild=='Other':
            input.extend([0,0,0,0,1,0])
        if education_feild=='Technical Degree':
            input.extend([0,0,0,0,0,1])
        if maritial_status=='Divorced':
            input.extend([1,0,0])
        if maritial_status=='Single':
            input.extend([0,1,0])
        if maritial_status=='Married':
            input.extend([0,0,1])
        print(len(input),input)
        # pred=0
        pred=prediction(input)
        return render_template('display.html',pred=pred)
@server.route('/dashboard/')
def dashboard():
    colors = [ '#17202A','#1ABC9C', '#0000FF']
    fig = px.scatter(df, y="Age", x="EducationField", color="Attrition",height=500,width=700,color_discrete_sequence=colors)
    graph=fig.to_html(full_html=False)
    # all.append(graph)
    fig2=px.histogram(df, x="MaritalStatus", y="MonthlyIncome", color="Attrition", barmode="group",height=500,width=700,color_discrete_sequence=['#F2A2E8','#967BB6'])
    graph2=fig2.to_html(full_html=False)
    # all.append(graph2)
    fig3 = px.bar(df, x="Department", y="MonthlyIncome", color="Attrition",animation_frame="Age", animation_group="Department", range_y=[0,70000],height=500,width=700,color_discrete_sequence=['#50C878','#E2F516'])
    graph3=fig3.to_html(full_html=False)
    # all.append(graph3)
    fig4= px.scatter(df, x="JobSatisfaction", y="YearsAtCompany", color="Attrition", marginal_y="violin",
    marginal_x="box", trendline="ols", template="simple_white",height=500,width=700)
    graph4=fig4.to_html(full_html=False)
    # all.append(graph4)
    fig5=px.scatter(df, y="EnvironmentSatisfaction", x="NumCompaniesWorked", size='Education', color="Attrition",
           hover_name="Attrition", log_x=True, size_max=60,color_discrete_sequence=['#DEB887','#3EB489'],height=500,width=700)
    graph5=fig5.to_html(full_html=False)
    fig6= px.ecdf(df, x="Age",y='JobSatisfaction', color="Attrition",color_discrete_sequence=['#800000','#2916F5'],height=500,width=700)
    graph6=fig6.to_html(full_html=False)
    return render_template('dash.html', graph1=graph,graph2=graph2,graph3=graph3,graph4=graph4,graph5=graph5,graph6=graph6)

if __name__ == '__main__':
    server.run(debug=True)

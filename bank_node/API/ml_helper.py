import os
import pickle, json
import pandas as pd, numpy as np

# Resolve path relative to this file's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(BASE_DIR, 'Deep Learning Model', 'finalized_model.sav')
mapper_path = os.path.join(BASE_DIR, 'Deep Learning Model', 'mapper.pkl')

loaded_model = pickle.load(open(model_path, 'rb'))
loaded_mapper = pickle.load(open(mapper_path, 'rb'))

def preProcess(a, mapper,parameter_cols):
    data=list(a.values())
    colz=list(a.keys())
    dfx=pd.DataFrame(data=[data], columns=colz)
    dfx

    XX1=mapper.transform(dfx)
    XX2=dfx[parameter_cols]
    XX = np.hstack((XX1,XX2))
    return XX

def calculate_score(applicant_data):
    parameter_cols=['sub_grade_num', 'short_emp', 'emp_length_num','dti', 'payment_inc_ratio', 'delinq_2yrs',
                'delinq_2yrs_zero', 'inq_last_6mths', 'last_delinq_none', 'last_major_derog_none', 'open_acc',
                'pub_rec', 'pub_rec_zero','revol_util']
    required_fields = ['dti', 'inq_last_6mths', 'open_acc', 'emp_length_num', 'revol_util', 'grade', 'payment_inc_ratio', 'purpose', 'delinq_2yrs_zero', 'pub_rec_zero', 'pub_rec', 'short_emp', 'home_ownership', 'sub_grade_num', 'last_major_derog_none', 'last_delinq_none', 'delinq_2yrs']
    a = {}
    for field in required_fields:
        a[field] = applicant_data[field]

    XX=preProcess(a, loaded_mapper,parameter_cols)

    score = loaded_model.predict_proba(XX)[:,1][0]

    score = score * 10
    score = round(10 - score,2)

    return score

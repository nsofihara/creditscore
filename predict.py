import pickle
import pandas as pd
import numpy as np
from collections import defaultdict
from flask import abort

raw_input = {'person_age': 25,
 'person_income': 50000,
 'person_emp_length': 3,
 'loan_amnt': 5000,
 'loan_int_rate': 10,
 'loan_percent_income': 0.15,
 'cb_person_cred_hist_length': 4,
 'person_home_ownership': 'RENT',
 'loan_intent': 'PERSONAL',
 'loan_grade': 'B',
 'cb_person_default_on_file': 'N'}


test_input = {'person_age': 23,
 'person_income': 95000,
 'person_emp_length': 7,
 'loan_amnt': 35000,
 'loan_int_rate': 7.9,
 'loan_percent_income': 0.37,
 'cb_person_cred_hist_length': 4,
 'person_home_ownership': 'MORTGAGE',
 'loan_intent': 'EDUCATION',
 'loan_grade': 'A',
 'cb_person_default_on_file': 'N',
'cb_person_default_on_file_Y': 0,
 'cb_person_default_on_file_N': 1,
 'loan_grade_A': 1,
 'loan_grade_B': 0,
 'loan_grade_C': 0,
 'loan_grade_D': 0,
 'loan_grade_E': 0,
 'loan_grade_F': 0,
 'loan_grade_G': 0,
 'loan_intent_EDUCATION': 1,
 'loan_intent_HOMEIMPROVEMENT': 0,
 'loan_intent_MEDICAL': 0,
 'loan_intent_PERSONAL': 0,
 'loan_intent_VENTURE': 0,
 'loan_intent_DEBTCONSOLIDATION': 0,
 'person_home_ownership_OTHER': 0,
 'person_home_ownership_OWN': 0,
 'person_home_ownership_RENT': 0,
 'person_home_ownership_MORTGAGE': 1,
 'person_age_WOE': -0.0006,
 'person_income_WOE': -0.814,
 'person_emp_length_WOE': 0.196,
 'loan_amnt_WOE': 1.599,
 'loan_int_rate_WOE': 0.131,
 'loan_percent_income_WOE': 2.114,
 'cb_person_cred_hist_length_WOE': 0.042}


with open("WOE-1.0.0.pkl", "rb") as f:
	woe_dict = pickle.load(f)

with open("OHE-1.0.0.pkl", "rb") as f:
	encoder = pickle.load(f)

with open("COL-NAME1.0.0.pkl", "rb") as f:
	cat_columns = pickle.load(f)

with open("LR-ALL-WOE-1.0.0.pkl", "rb") as f:
	lr_model = pickle.load(f)


def formatting_data(raw_input):
	required_columns = ['person_age', 'person_income', 'person_emp_length', 'loan_amnt', 'loan_int_rate', 'loan_percent_income', 'cb_person_cred_hist_length', 'person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']

	for col in required_columns:
		try:
			raw_input[col]
		except KeyError as err:
			if(col == 'person_home_ownership' or col == 'loan_intent' or col == 'loan_grade' or col == 'cb_person_default_on_file'):
				abort(400, {'message': 'categorical column is missing'})
			else:
				raw_input[col] = np.nan


	mapper_replace = {
		"null": np.nan,
		"" : np.nan,
		None: np.nan
}

	data = pd.DataFrame([raw_input]).replace(mapper_replace)

	return data

def preprocess(data):
	for feature, woe_info in woe_dict.items():
		data[f'{feature}_WOE'] = pd.cut(data[feature], bins=woe_info['binning'], labels=woe_info['labels'])
		data[f'{feature}_WOE'] = data[f'{feature}_WOE'].values.add_categories('Nan').fillna('Nan') 
		data[f'{feature}_WOE'] = data[f'{feature}_WOE'].replace('Nan', woe_info['nan'])
		data[f'{feature}_WOE'] = data[f'{feature}_WOE'].astype(float)

	data_transformed = encoder.transform(data[cat_columns]).toarray()

	column_name = encoder.get_feature_names(cat_columns)

	data_one_hot_encoded = pd.DataFrame(data_transformed, columns=column_name, index=data[cat_columns].index).astype(int)

	data = pd.concat([data, data_one_hot_encoded], axis=1).reset_index(drop=True)

	return data

def pred(data):
	model = lr_model
	all_features = ['person_age_WOE', 'person_income_WOE', 'person_emp_length_WOE','loan_amnt_WOE','loan_int_rate_WOE', 'loan_percent_income_WOE', 'cb_person_cred_hist_length_WOE', 'cb_person_default_on_file_Y', 'cb_person_default_on_file_N','loan_grade_A','loan_grade_B', 'loan_grade_C', 'loan_grade_D', 'loan_grade_E', 'loan_grade_F', 'loan_grade_G', 'loan_intent_EDUCATION', 'loan_intent_HOMEIMPROVEMENT', 'loan_intent_MEDICAL', 'loan_intent_PERSONAL', 'loan_intent_VENTURE', 'loan_intent_DEBTCONSOLIDATION', 'person_home_ownership_OTHER', 'person_home_ownership_OWN', 'person_home_ownership_RENT', 'person_home_ownership_MORTGAGE']

	pred_proba = model.predict_proba(data[all_features])[:, 1]
	threshold = 0.5
	prediction = (pred_proba > threshold).astype(int)
	return { "data": [ { "pred_proba": float(pred_proba[0]), "prediction": int(prediction[0])} ] }

def make_prediction(raw_input):
	data = formatting_data(raw_input)
	data = preprocess(data)
	prediction = pred(data)
	return prediction

if __name__ == "__main__":
	result = make_prediction(raw_input)
	print(result)

if __name__ == "__main__":
	result = pred(pd.DataFrame([test_input]))
	print(result)









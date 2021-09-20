## Access Credit Score Calculator via Heroku :
https://nadiasofihara-creditscore.herokuapp.com

## Access Rest API via POSTMAN :
[POST] - https://nadiasofihara-creditscore.herokuapp.com/predict-api

### Input
<img width="856" alt="Screen Shot 2021-09-20 at 12 10 35 PM" src="https://user-images.githubusercontent.com/90818060/133959180-c21b9d0b-cac5-4b3f-b497-fc3d787becf2.png">

Steps for Calculate Credit Score using REST API :
- From Postman, select POST method.
- Input https://nadiasofihara-creditscore.herokuapp.com/predict-api to REST API link column.
- Choose Content-Type: application/json as Request Header
- Input Body Parameter

Feature | Description | Value 
------|-------------|-------
person_age | Age. | Integer 
person_income | Annual Income. | Integer 
person_home_ownership | Home ownership. | 'RENT', 'MORTGAGE', 'OWN', or 'OTHER'
person_emp_length | Employment length (in years) | Integer 
loan_amnt | Loan amount. | Integer 
loan_int_rate | Interest rate. | Float 
loan_percent_income | Percent income. | Float (Between 0 and 1)
cb_person_cred_hist_length | Credit history length. | Integer 
loan_intent | Loan intent. | 'PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', or 'DEBTCONSOLIDATION' 
loan_grade | Loan grade. | 'A', 'B', 'C, 'D', 'E', 'F', or 'G' 
cb_person_default_on_file | Historical default. | 'Y', or 'N' 

```
{
    "person_age": 25,
    "person_income": 50000,
    "person_emp_length": 3,
    "person_home_ownership": "RENT",
    "loan_amnt": 5000,
    "loan_int_rate": 10,
    "loan_percent_income": 0.15,
    "cb_person_cred_hist_length": 4,
    "loan_intent": "PERSONAL",
    "loan_grade": "B",
    "cb_person_default_on_file": "N"
}
```
- Click Send


### Output
<img width="538" alt="Screen Shot 2021-09-20 at 12 13 36 PM" src="https://user-images.githubusercontent.com/90818060/133960175-2274ec84-d259-4eeb-bcd8-9202e2fc8ed9.png">

Field | Description
------|------------
model | Machine learning model used for Credit Scoring Prediction.
version | Model version.
score_proba | Probability estimates.
prediction | Predict class labels (0 is non default 1 is default).

```
{
    "model": "LR-ALL-WOE",
    "prediction": 0,
    "score_proba": 0.007841520883857913,
    "version": "1.0.0"
}
```

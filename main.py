from fastapi import FastAPI,Path,HTTPException,Query
import json

app=FastAPI()

def load_data():
    try:
        with open('patients.json','r') as f:
            data=json.load(f)
            return data
    except FileNotFoundError:
        return {}

@app.get('/')
def started():
    return {'message': 'Patient management system project'}

@app.get('/about')
def root():
    return {'message':'a fully functional api to manage patient records '}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_key}')
def get_patient_data(patient_key: str = Path(..., title="Patient ID", examples=["P001", "P002"])):
    # load the data
    data = load_data()
    # check if the patient_id exists in the data
    if patient_key in data:
        return data[patient_key]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


@app.get('/sort')
def sort_patient_data(sort_by:str=Query(...,description="sort by name,age,city"),order:str=Query(...,description="asc or desc")):

    valid_sorts=['weight','height','bmi','age']

    valid_order=['asc','desc']

    if sort_by not in valid_sorts:
        raise HTTPException(status_code=400,detail="Invalid sort key please enter valid sort key")

    if order not in valid_order:
        raise HTTPException(status_code=400,detail="Invalid order please enter valid order")

    data=load_data()

    reverse_order=True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x : x.get(sort_by),reverse=reverse_order)

    return sorted_data
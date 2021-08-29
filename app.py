from flask import Flask, abort, request
from flask.globals import request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assessment.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Model
class Employees(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    monthly_salary = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return "User: {} Montly Salary: {}".format(self.name, self.monthly_salary)

# View
@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employees.query.all()
    response = app.response_class(
        response=json.dumps([employee.to_dict() for employee in employees], indent=3),
        mimetype='application/json'
    )
    return response

@app.route('/calculate_salary/<employee>', methods=['POST', 'GET'])
def calculate_salary(employee):
        employee_detail = {
            'name': request.json['name'],
            'salary': request.json['salary']
        }

        employee = Employees.query.filter_by(name = employee_detail['name']).first()

        if not employee:
            abort(404)

        if 'name' in request.json == '':
            abort(404)
        
        
        tax = None
        gross_income =  employee_detail['salary'] * 12
        
        if gross_income <= 5000:
            tax = 0
        elif gross_income <= 20000:
            tax = (gross_income - 5000) * 1 
        elif gross_income <= 35000:
            tax = (gross_income - 20000) * 0.3 + 150
        elif gross_income <= 50000:
            tax = (gross_income - 35000) * 0.8 + 600
        elif gross_income <= 70000:
            tax = (gross_income - 50000) * 0.14 + 1800
        elif gross_income <= 100000:
            tax = (gross_income - 700000) * 0.21 + 4600
        elif gross_income <= 250000:
            tax = (gross_income - 100000) * 0.24 + 10900
        elif gross_income <= 400000:
            tax =(gross_income - 250000) * 0.245 + 46900
        elif gross_income <= 600000:
            tax = (gross_income - 400000) * 0.25 + 83650

        tax_payable = tax * 100
        salary = gross_income * 100

        return json.dumps({
            'name': employee_detail['name'],
            'salary': salary,
            'tax_payable': tax_payable
            })

@app.route('/update_salary/<employee>', methods=['PUT'])
def update_salary(employee):
    employee_detail = {
        'name': request.json['name'],
        'salary': request.json['salary']
        }

    employee = Employees.query.filter_by(name = employee_detail['name']).first()

    if 'name' in request.json == '':
        abort(404) 

    employee.monthly_salary = employee_detail['salary']

    db.session.commit()

    return "Update Salary to {}".format(employee_detail['salary'])

if __name__ == "__main__":
    app.run(debug=True)
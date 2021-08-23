from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DecimalField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret Key'


def gross_income(annual_salary):
    return round(annual_salary / 12)


def income_tax(income):
    tax = None

    if income <= 18200:
        tax = 0
    elif income <= 37000:
        tax = (income - 18200) * 0.19
    elif income <= 87000:
        tax = (income - 37000) * 0.325 + (37000 - 18200) * 0.19
    elif income <= 1800000:
        tax = (income - 87000) * 0.37 + (87000 - 37000) * 0.19
    elif income >= 1800001:
        tax = (income - 1800000) * 0.45 + (1800000 - 87000) * 0.37 + (87000 - 37000) * 0.325 + (37000 - 18200) * 0.19

    return round(tax)


def net_income(gross_income, income_tax):
    return round(gross_income - income_tax)


def super_rate(gross_income, super_rate):
    return round(gross_income * super_rate)


class Employee(FlaskForm):
    first_name = StringField('first_name')
    last_name = StringField('last_name')
    annual_salary = FloatField('annual_salary')
    super_rate = DecimalField('super_rate')
    payment_start_date = StringField('payment_start_date')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Employee()
    if form.validate_on_submit():
        form_annual_salary = form.annual_salary.data
        form_super = form.super_rate.data

        gross_income_value = gross_income(form_annual_salary)
        income_tax_value = income_tax(form_annual_salary)
        net_income_value = net_income(gross_income_value, income_tax_value)
        super_rate_value = super_rate(gross_income_value, int(form_super))

        return render_template('success.html', form=form, gross_income_value=gross_income_value, income_tax_value=income_tax_value, net_income_value=net_income_value, super_rate_value=super_rate_value)
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)

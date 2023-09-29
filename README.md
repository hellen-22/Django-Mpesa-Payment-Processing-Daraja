# Django-Mpesa-Payment-Processing-Daraja
Simple Mpesa Express Project that enables sending stk push and generating callback data, processing payment of a specific order and checking if transactions where complete or not.

Available endpoints:

```sql
/stk/
 ```
This endpoint allows sending stk push to the provided phone number. The required data for this POST request is phone number and amount.

```sql
/callback/order_id/
 ```
This endpoint allows viewing of callback data sent from Safaricom.

## To install, follow these steps:

- Clone the repository
 
- Create a virtual environment and activate it:
```sql
python -m venv env
env/Scripts/activate
```
- Install the required packages:
```sql
pip install -r requirements.txt 
```
- Set up the database:
```sql
python manage.py migrate
```
- Run the server:
```sql
python manage.py runserver

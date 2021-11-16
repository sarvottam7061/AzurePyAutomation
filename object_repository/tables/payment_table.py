from sqlalchemy.sql import text

# have all the queries specific to a table here
# if your query involves multiple table, use common_table.py

# queries can be string
query_total_amount = "select Sum(amount) From payment"

# you can use sqlalchemy text function, to pass params to string n here
query_amount_greater_8 = text("select count(amount) from payment Where amount > :n").bindparams(n=8)

query_amount_average = "select AVG(amount) from payment"

query_amount_between = text("select amount from payment Where amount BETWEEN :x AND :y").\
                        bindparams(x=5, y=10)

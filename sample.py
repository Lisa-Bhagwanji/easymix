import datetime

scheduled_date = "12/06/2022"
converted_time = datetime.datetime.strptime(scheduled_date, '%d/%m/%Y')

print((converted_time - datetime.datetime.today()).days)

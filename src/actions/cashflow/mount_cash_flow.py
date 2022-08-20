from datetime import date, timedelta

def mount_cash_flow(investments, installments, cash_flows):
  for investment in investments:
    cash_flows.append({
      'date': investment['created_at'],
      'amount': float(investment['amount']) * -1
    })

  for installment in installments:
    cash_flows.append({
      'date': installment['due_date'],
      'amount': float(installment['amount'])
    })

  cash_flows.sort(key=sort_by_date)

  include_dates_in_cash_flows(cash_flows)
  
  cash_flows.sort(key=sort_by_date)

def include_dates_in_cash_flows(cash_flows):
    startDate = date.fromisoformat(cash_flows[0]['date'])
    endDate = date.fromisoformat(cash_flows[-1]['date'])
    dates = getDatesRange(startDate, endDate)
    for singleDate in dates:
      teste = list(filter(lambda x: x['date'] == singleDate.isoformat(), cash_flows))
      if len(teste) < 1:
        cash_flows.append({
          'date': singleDate.isoformat(),
          'amount': 0.00
        })

def sort_by_date(e):
    return e['date']

def getDatesRange(startDate, endDate):
    dates = []
    while startDate <= endDate:
        dates.append(startDate)
        startDate += timedelta(days=1)
    return dates
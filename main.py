import sys
sys.path.insert(0, './src/')

from datetime import date, timedelta
from src.installments import installments
from src.investments import investments
import numpy_financial as npf


def getDatesRange(startDate, endDate):
    dates = []
    while startDate <= endDate:
        dates.append(startDate)
        startDate += timedelta(days=1)
    return dates

def sort_by_date(e):
    return e['date']

def sum_duplicates(original_list, destination_list, key):
    index = 0
    date_key = 'created_at' if key == 'investments' else 'due_date'
    for item in original_list:
        previousItem = original_list[index - 1] if index - 1 < len(original_list) else None
        nextItem = original_list[index + 1] if index + 1 < len(original_list) else None
        if previousItem and item[date_key] == previousItem[date_key]:
            continue
        elif nextItem and item[date_key] == nextItem[date_key]:
            if key == 'installments':
              newItem = {
                  'investment_id': item['investment_id'],
                  'due_date': item['due_date'],
                  'amount': str(float(item['amount']) + float(nextItem['amount']))
              }
            else:
              newItem = {
                  'id': item['id'],
                  'created_at': item['created_at'],
                  'amount': str(float(item['amount']) + float(nextItem['amount']))
              }
            destination_list.append(newItem)
            index += 1
        else:
            destination_list.append(item)
        index += 1

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

def calc_irr():
    data = []
    computedInstallments = []
    computedInvestments = []
    cashflows = []

    investmentsTransactions = sorted(investments.investments, key=lambda k: k['created_at'], reverse=False)
    installmentsTransactions = sorted(installments.installments, key=lambda k: k['due_date'], reverse=False)

    sum_duplicates(investmentsTransactions, computedInvestments, 'investments')
    sum_duplicates(installmentsTransactions, computedInstallments, 'installments')

    mount_cash_flow(computedInvestments, computedInstallments, cashflows)

    for transaction in cashflows:
      data.append(transaction['amount'])
    
    irr = round(npf.irr(data), 2)
    print("TIR:", irr)


if __name__ == "__main__":
    calc_irr()
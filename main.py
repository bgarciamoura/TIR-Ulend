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

def calc_irr():
    data = []
    computedInstallments = []
    computedInvestments = []
    cashflows = []
    index = 0 

    investmentsTransactions = sorted(investments.investments, key=lambda k: k['created_at'], reverse=False)
    installmentsTransactions = sorted(installments.installments, key=lambda k: k['due_date'], reverse=False)

    sum_duplicates(investmentsTransactions, computedInvestments, 'investments')
    sum_duplicates(installmentsTransactions, computedInstallments, 'installments')


    # for investment in computedInvestments:
    #   cashflows.append({
    #     'date': investment['created_at'],
    #     'amount': float(investment['amount']) * -1
    #   })

    # for installment in computedInstallments:
    #   cashflows.append({
    #     'date': installment['due_date'],
    #     'amount': float(installment['amount'])
    #   })

    # cashflows.sort(key=sort_by_date)
    # startDate = date.fromisoformat(cashflows[0]['date'])
    # endDate = date.fromisoformat(cashflows[-1]['date'])
    # dates = getDatesRange(startDate, endDate)
    
    # for singleDate in dates:
    #   teste = list(filter(lambda x: x['date'] == singleDate.isoformat(), cashflows))
    #   if len(teste) < 1:
    #     cashflows.append({
    #       'date': singleDate.isoformat(),
    #       'amount': 0.00
    #     })
    
    # cashflows.sort(key=sort_by_date)

    # some = 0
    # for transaction in cashflows:
    #   data.append(transaction['amount'])
    #   some += transaction['amount']
    
    # irr = round(npf.irr(data), 2)
    # print("TIR:", irr)


if __name__ == "__main__":
    calc_irr()
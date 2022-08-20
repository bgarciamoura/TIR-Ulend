import sys
sys.path.insert(0, './src/')

from datetime import date, timedelta
from src.installments import installments
from src.investments import investments
import numpy_financial as npf


cashflows = []

def sortByCreatedAt(e):
    return e['created_at']

def sortByDue(e):
    return e['due_date']

def sortByDate(e):
    return e['date']

def getDatesRange(startDate, endDate):
    dates = []
    while startDate <= endDate:
        dates.append(startDate)
        startDate += timedelta(days=1)
    return dates



def calc_irr():
    data = []
    computedInstallments = []
    computedInvestments = []

    investments.investments.sort(key=sortByCreatedAt('created_at'))
    installments.installments.sort(key=sortByDue)

    index = 0 
    for installment in installments.installments:
        previousInstallment = installments.installments[index - 1] if index - 1 < len(installments.installments) else None
        nextInstallment = installments.installments[index + 1] if index + 1 < len(installments.installments) else None
        if previousInstallment and installment['due_date'] == previousInstallment['due_date']:
            continue
        elif nextInstallment and installment['due_date'] == nextInstallment['due_date']:
            newInstallment = {
                'investment_id': installment['investment_id'],
                'due_date': installment['due_date'],
                'amount': str(float(installment['amount']) + float(nextInstallment['amount']))
            }
            computedInstallments.append(newInstallment)
            index += 1
        else:
            computedInstallments.append(installment)
        index += 1


    index = 0
    for investment in investments.investments:
        previousInvestment = investments.investments[index - 1] if index - 1 < len(investments.investments) else None
        nextInvestment = investments.investments[index + 1] if index + 1 < len(investments.investments) else None
        if previousInvestment and investment['created_at'] == previousInvestment['created_at']:
            continue
        elif nextInvestment and investment['created_at'] == nextInvestment['created_at']:
            newInvestment = {
                'id': investment['id'],
                'created_at': investment['created_at'],
                'amount': str(float(investment['amount']) + float(nextInvestment['amount']))
            }
            computedInvestments.append(newInvestment)
            index += 1
        else:
            computedInvestments.append(investment)
        index += 1


    for investment in computedInvestments:
      cashflows.append({
        'date': investment['created_at'],
        'amount': float(investment['amount']) * -1
      })

    for installment in computedInstallments:
      cashflows.append({
        'date': installment['due_date'],
        'amount': float(installment['amount'])
      })

    cashflows.sort(key=sortByDate)
    startDate = date.fromisoformat(cashflows[0]['date'])
    endDate = date.fromisoformat(cashflows[-1]['date'])
    dates = getDatesRange(startDate, endDate)
    
    for singleDate in dates:
      teste = list(filter(lambda x: x['date'] == singleDate.isoformat(), cashflows))
      if len(teste) < 1:
        cashflows.append({
          'date': singleDate.isoformat(),
          'amount': 0.00
        })
    
    cashflows.sort(key=sortByDate)

    some = 0
    for transaction in cashflows:
      data.append(transaction['amount'])
      some += transaction['amount']
    
    irr = round(npf.irr(data), 2)
    print("TIR:", irr)


if __name__ == "__main__":
    calc_irr()
import sys
sys.path.insert(0, './src/')
sys.path.insert(1, './src/actions/cashflow')
sys.path.insert(2, './src/actions/duplicates')

from src.actions.cashflow import mount_cash_flow
from src.actions.duplicates import duplicates
from src.installments import installments
from src.investments import investments
import numpy_financial as npf

def calc_irr():
    data = []
    computedInstallments = []
    computedInvestments = []
    cashflows = []

    investmentsTransactions = sorted(investments.investments, key=lambda k: k['created_at'], reverse=False)
    installmentsTransactions = sorted(installments.installments, key=lambda k: k['due_date'], reverse=False)

    duplicates.sum_duplicates(investmentsTransactions, computedInvestments, 'investments')
    duplicates.sum_duplicates(installmentsTransactions, computedInstallments, 'installments')

    mount_cash_flow.mount_cash_flow(computedInvestments, computedInstallments, cashflows)

    for transaction in cashflows:
      data.append(transaction['amount'])
    
    irr = round(npf.irr(data), 2)
    print("TIR:", irr)


if __name__ == "__main__":
    calc_irr()
import os
from dotenv import load_dotenv

load_dotenv()

def get_non_processed(rows):
    non_processed = []
    for row in rows[1:-1]:  # Skip header row
        if row[31] == "": # this is the column that gets the date in Expense Report
            non_processed.append(row)
    return non_processed

subaccounts = {
    "Executive": os.getenv('EXECUTIVE_SUBACCOUNT'),
    "Development": os.getenv('DEVELOPMENT_SUBACCOUNT'),
    "External": os.getenv('EXTERNAL_SUBACCOUNT'),
    "Internal": os.getenv('INTERNAL_SUBACCOUNT'),
    "Operations": os.getenv('OPERATIONS_SUBACCOUNT')
}

def get_relevant_values(row, payment_type):
    if payment_type == "Reimbursement":
        parts = row[11].split(", ", 1)
        line1 = parts[0] # address line 1
        line2 = parts[1] if len(parts) > 1 else "" # address line 2
        # for the below array, row[1] is the second column in the Expense Report, for example
        return [row[1], f'{"This paid for " + row[2]}.', row[3], subaccounts[row[4]], line1, line2, row[12], row[13]]
    elif payment_type == "Invoice":
        parts = row[18].split(", ", 1)
        line1 = parts[0] # address line 1
        line2 = parts[1] if len(parts) > 1 else "" # address line 2
        return [f'{"This will pay for " + row[2]}.', row[3], subaccounts[row[4]], row[16], row[17], line1, line2]
    elif payment_type == "SOFC Credit Card Payment (must be submitted 3-4 weeks in advance)":
        return [row[1], f'{"This will pay for " + row[2]}.', row[3], subaccounts[row[4]], row[20], row[21], "314-858-0848", row[22]]
    else:
        return []
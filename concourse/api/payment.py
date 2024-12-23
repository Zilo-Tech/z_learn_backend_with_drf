from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator
from datetime import datetime
from pymesomb.operations import PaymentOperation


access_key = "15a980c6-82e6-4d1e-a759-0afbfde8daef"
secret_key = "85f7f5bb-1ef3-471a-b9ec-16a75a86a076"
application_key = "81c6eb7ab02fa9e81bf7e07beb77c949129bcfab"

# operation = PaymentOperation(application_key, access_key, secret_key)
# response = operation.make_collect({
#     'amount': 11,
#     'service': 'MTN',
#     'payer': '672384579',
#     'date': datetime.now(),
#     'nonce': RandomGenerator.nonce(),
#     'trxID': '1'
# })
# print(response.is_operation_success())
# print(response.is_transaction_success())



def make_payment(application_key, access_key, secret_key, amount, service, payer, trxID):
    # Initialize the PaymentOperation
    operation = PaymentOperation(application_key, access_key, secret_key)

    # Making a collect operation
    response = operation.make_collect({
        'amount': amount,
        'service': service,
        'payer': payer,
        'date': datetime.now(),
        'nonce': RandomGenerator.nonce(),
        'trxID': trxID
    })

    # Check if operation and transaction were successful
    operation_success = response.is_operation_success()
    transaction_success = response.is_transaction_success()

    results = {
        "Operation Success": operation_success,
        "Transaction Success": transaction_success
    }

    # Print results
    print(f"The results are {results}")
    return results

    return operation_success, transaction_success


# make_payment(application_key, access_key, secret_key, amount=11, service='MTN', payer='672384579', trxID='1')

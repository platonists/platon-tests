

def test_transactionCount(normal_aide):
    result = normal_aide.graphql.execute('{pending {transactionCount}}')
    transaction_count = result.get('pending').get('transactionCount')
    pending_transaction_count = int(normal_aide.txpool.status()['pending'][2:], 16)
    assert transaction_count == pending_transaction_count == 0


def test_transactions(normal_aide):
    result = normal_aide.graphql.execute('{pending {transactions {index status gasUsed cumulativeGasUsed}}}')
    transactions = result.get('pending').get('transactions')
    assert transactions == []


def test_account(normal_aide):
    result = normal_aide.graphql.execute('{pending {account(address: atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0) {address balance transactionCount code storage(slot: "0xa98e6baea6233965a0740e20e626c5500ecf16121547e8255ee5a28a4f08fc57")}}}')
    account_address = result.get('pending').get('account').get('address')
    assert account_address == 'atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0'


def test_call(normal_aide):
    result = normal_aide.graphql.execute('{pending {call(data: {from:atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0 to:atp1x3r5qyx6mzn98h6kvp0r9r4zkq89c9qedjmxew gas:21000 gasPrice:1000000000 value:0 data: "0x"}){data gasUsed status}}}')
    status = int(result.get('pending').get('call').get('status')[2:])
    assert status == 1


def test_estimateGas(normal_aide):
    result = normal_aide.graphql.execute('{pending {estimateGas(data: {from:atp1zkrxx6rf358jcvr7nruhyvr9hxpwv9uncjmns0 to:atp1x3r5qyx6mzn98h6kvp0r9r4zkq89c9qedjmxew gas:21000 gasPrice:1000000000 value:0 data: "0x"})}}')
    estimate_gas = int(result.get('pending').get('estimateGas')[2:], 16)
    assert estimate_gas == 21000
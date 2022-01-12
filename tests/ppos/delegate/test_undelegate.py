import pytest

from lib.funcs import wait_settlement
from tests.conftest import generate_account
from loguru import logger


@pytest.mark.P0
@pytest.mark.compatibility
def test_ROE_001_007_015(normal_aide):
    """
    和用例test_DI_031一致，需要合并吗？
    :param normal_aide_obj:
    :return:
    """
    value = normal_aide.delegate._economic.staking_limit
    address, prikey = generate_account(normal_aide, value * 3)
    normal_aide.staking.create_staking(amount=value, benifit_address=address, private_key=prikey)

    delegate_address, delegate_prikey = generate_account(normal_aide, normal_aide.delegate._economic.delegate_limit * 3)
    delegate_result = normal_aide.delegate.delegate(private_key=delegate_prikey)
    assert delegate_result['status'] == 1
    logger.info(delegate_result)

    msg = normal_aide.staking.staking_info
    staking_blocknum = msg.StakingBlockNum

    result = normal_aide.delegate.withdrew_delegate(private_key=delegate_prikey)
    # assert_code(result, 0)
    print(result)


@pytest.mark.P1
def test_ROE_002(normal_aide):
    """
    :param normal_aide_obj:
    :return:
    """
    value = normal_aide.delegate._economic.staking_limit
    address, prikey = generate_account(normal_aide, value * 3)
    normal_aide.staking.create_staking(amount=value, benifit_address=address, private_key=prikey)

    delegate_address, delegate_prikey = generate_account(normal_aide, normal_aide.delegate._economic.delegate_limit * 3)
    delegate_result = normal_aide.delegate.delegate(private_key=delegate_prikey)
    assert delegate_result['status'] == 1
    logger.info(delegate_result)

    msg = normal_aide.staking.staking_info
    staking_blocknum = msg.StakingBlockNum
    txn = {"gas": 1}
    status = 0
    try:
        result = normal_aide.delegate.withdrew_delegate(txn=txn, private_key=delegate_prikey)
    except BaseException:
        status = 1
    assert status == 1


@pytest.mark.P3
def test_ROE_003(normal_aide):
    """
    :param normal_aide_obj:
    :return:
    """
    value = normal_aide.delegate._economic.staking_limit
    address, prikey = generate_account(normal_aide, value * 3)
    normal_aide.staking.create_staking(amount=value, benifit_address=address, private_key=prikey)

    delegate_address, delegate_prikey = generate_account(normal_aide, normal_aide.delegate._economic.delegate_limit * 3)
    delegate_result = normal_aide.delegate.delegate(private_key=delegate_prikey)
    assert delegate_result['status'] == 1
    logger.info(delegate_result)

    # msg = normal_aide.staking.staking_info
    # staking_blocknum = msg.StakingBlockNum
    illegal_nodeID = "7ee3276fd6b9c7864eb896310b5393324b6db785a2528c00cc28ca8c" \
                     "3f86fc229a86f138b1f1c8e3a942204c03faeb40e3b22ab11b8983c35dc025de42865990"
    result = normal_aide.delegate.withdrew_delegate(node_id=illegal_nodeID, private_key=delegate_prikey)
    logger.info(result)
    # assert_code(result, 301109)


@pytest.mark.P1
def test_ROE_004(normal_aide):
    """
    :param normal_aide_obj:
    :return:
    """
    value = normal_aide.delegate._economic.staking_limit
    address, prikey = generate_account(normal_aide, value * 3)
    normal_aide.staking.create_staking(amount=value, benifit_address=address, private_key=prikey)

    delegate_address, delegate_prikey = generate_account(normal_aide, normal_aide.delegate._economic.delegate_limit * 3)
    delegate_result = normal_aide.delegate.delegate(private_key=delegate_prikey)
    assert delegate_result['status'] == 1
    logger.info(delegate_result)

    result = normal_aide.delegate.withdrew_delegate(amount=normal_aide.delegate._economic.delegate_limit + 1,
                                                    private_key=delegate_prikey)
    logger.info(result)


@pytest.mark.P1
def test_ROE_005_018(normal_aide):
    """
    :param normal_aide_obj:
    :return:
    """
    value = normal_aide.delegate._economic.staking_limit
    address, prikey = generate_account(normal_aide, value * 3)
    normal_aide.staking.create_staking(benifit_address=address, private_key=prikey)

    delegate_address, delegate_prikey = generate_account(normal_aide, normal_aide.delegate._economic.delegate_limit * 3)
    delegate_result = normal_aide.delegate.delegate(private_key=delegate_prikey)
    assert delegate_result['status'] == 1
    logger.info(delegate_result)
    # Return a pledge
    withdrew_staking_result = normal_aide.staking.withdrew_staking(private_key=prikey)
    print(f'withdrew_staking_result={withdrew_staking_result}')

    # The next two cycle
    wait_settlement(normal_aide, 2)
    amount = normal_aide.platon.get_balance(delegate_address)
    logger.info("The wallet balance:{}".format(amount))

    result = normal_aide.delegate.withdrew_delegate(private_key=delegate_prikey)
    logger.info(result)
    amount_after = normal_aide.platon.get_balance(delegate_address)
    logger.info("The wallet balance:{}".format(amount_after))
    delegate_limit = normal_aide.delegate._economic.delegate_limit
    assert delegate_limit - (amount_after - amount) < normal_aide.web3.toVon(1, 'lat')


@pytest.mark.P1
def test_ROE_006_008(normal_aide):
    """

    :param normal_aide_obj:
    :return:
    """
    address, prikey = generate_account(normal_aide, normal_aide.delegate._economic.staking_limit * 2)
    normal_aide.staking.create_staking(benifit_address=address, private_key=prikey)

    value = normal_aide.delegate._economic.delegate_limit
    delegate_address, delegate_prikey = generate_account(normal_aide, value * 4)
    delegate_result = normal_aide.delegate.delegate(amount=value * 3, private_key=delegate_prikey)
    assert delegate_result['status'] == 1
    logger.info(delegate_result)

    amount = normal_aide.platon.get_balance(delegate_address)
    logger.info("The wallet balance:{}".format(amount))
    result = normal_aide.delegate.withdrew_delegate(amount=value * 2, private_key=delegate_prikey)
    logger.info(result)
    amount_after = normal_aide.platon.get_balance(delegate_address)
    logger.info("The wallet balance:{}".format(amount_after))
    delegate_limit = normal_aide.delegate._economic.delegate_limit
    assert delegate_limit * 2 - (amount_after - amount) < normal_aide.web3.toVon(1, 'lat')


@pytest.mark.P1
def test_ROE_010(normal_aide):
    """
    :param normal_aide_obj:
    :return:
    """
    # client_new_node.economic.env.deploy_all()
    delegate_address, delegate_prikey = generate_account(normal_aide, normal_aide.delegate._economic.staking_limit)
    lockup_amount = normal_aide.web3.toVon(1000, 'lat')
    plan = [{'Epoch': 1, 'Amount': lockup_amount}]
    # Create a lock plan
    result = normal_aide.web3.restricting.create_restricting(release_address=delegate_address, plans=plan)
    logger.info(result)
    # assert_code(result, 0)
    msg = normal_aide.web3.restricting.get_restricting_info(delegate_address)
    logger.info(msg)
    # create staking
    staking_address, staking_prikey = generate_account(normal_aide, normal_aide.delegate._economic.staking_limit * 2)
    normal_aide.staking.create_staking(benifit_address=staking_address, private_key=staking_prikey)

    delegate_amount = normal_aide.web3.toVon(500, 'lat')
    # Lock account authorization
    delegate_result = normal_aide.delegate.delegate(amount=delegate_amount, balance_type=1, private_key=delegate_prikey)
    assert delegate_result['status'] == 1
    logger.info(delegate_result)
    # Own capital account entrustment
    result = normal_aide.delegate.delegate(amount=delegate_amount, balance_type=0, private_key=delegate_prikey)
    logger.info(result)

    undelegate_amount = normal_aide.web3.toVon(300, 'lat')
    logger.info("The amount of redemption is greater than the entrustment of the free account")
    amount = normal_aide.platon.get_balance(delegate_address)
    logger.info("The wallet balance:{}".format(amount))

    result = normal_aide.delegate.withdrew_delegate(amount=undelegate_amount, private_key=delegate_prikey)
    logger.info(result)

    msg = normal_aide.delegate.get_delegate_info(address=delegate_address)
    logger.info(msg)
    amount_after = normal_aide.platon.get_balance(delegate_address)
    logger.info("The wallet balance:{}".format(amount_after))
    assert undelegate_amount - (amount_after - amount) < normal_aide.web3.toVon(1, 'lat')



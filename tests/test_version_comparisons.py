import pytest

import semver


@pytest.mark.parametrize(
    'left,right, expected',
    (
        ('1.0.0', '1.0.0', 0),
        ('1.0.0', '1.1.0', -1),
        ('1.0.0', '1.0.1', -1),
        ('1.0.0', '2.0.0', -1),
        ('1.0.0', '2.0.0-beta', -1),
        ('1.9.9', '2.0.0', -1),
        ('1.0.0-alpha', '1.0.0-alpha.1', -1),
        ('1.0.0-alpha.1', '1.0.0-alpha.beta', -1),
        ('1.0.0-alpha.beta', '1.0.0-beta.2', -1),
        ('1.0.0-beta.2', '1.0.0-beta.11', -1),
        ('1.0.0-beta.11', '1.0.0-rc.1', -1),
        ('1.0.0-rc.1', '1.0.0', -1),
        ('1.0.0-a', '1.0.0-aa', -1),
        ('1.0.0-999', '1.0.0-1000', -1),
    ),
)
def test_semver_object_comparisons(chain, left, right, expected):
    test_semver_lib = chain.get_contract('TestSemVersion')

    left_ver = semver.parse_version_info(left)

    test_semver_lib.transact().setA(
        [left_ver.major, left_ver.minor, left_ver.patch],
        left_ver.prerelease or '',
    )

    right_ver = semver.parse_version_info(right)

    test_semver_lib.transact().setB(
        [right_ver.major, right_ver.minor, right_ver.patch],
        right_ver.prerelease or '',
    )

    is_eq = expected == 0
    is_gt = expected == 1
    is_ge = is_eq or is_gt
    is_lt = expected == -1
    is_le = is_eq or is_lt

    if left_ver.prerelease is None:
        expected_left_identifiers = []
    else:
        expected_left_identifiers = left_ver.prerelease.split('.')

    if right_ver.prerelease is None:
        expected_right_identifiers = []
    else:
        expected_right_identifiers = right_ver.prerelease.split('.')

    assert test_semver_lib.call().isEqual() is is_eq
    assert test_semver_lib.call().isGreater() is is_gt
    assert test_semver_lib.call().isGreaterOrEqual() is is_ge
    assert test_semver_lib.call().isLesser() is is_lt
    assert test_semver_lib.call().isLesserOrEqual() is is_le

    assert test_semver_lib.call().getANumIdentifiers() == len(expected_left_identifiers)

    for idx, identifier in enumerate(expected_left_identifiers):
        assert test_semver_lib.call().getAIdentifier(idx) == identifier

    assert test_semver_lib.call().getBNumIdentifiers() == len(expected_right_identifiers)

    for idx, identifier in enumerate(expected_right_identifiers):
        assert test_semver_lib.call().getBIdentifier(idx) == identifier

    eq_gas = test_semver_lib.estimateGas().isEqual()
    gt_gas = test_semver_lib.estimateGas().isGreater()
    ge_gas = test_semver_lib.estimateGas().isGreaterOrEqual()
    lt_gas = test_semver_lib.estimateGas().isLesser()
    le_gas = test_semver_lib.estimateGas().isLesserOrEqual()

    assert eq_gas < 40000
    assert gt_gas < 40000
    assert ge_gas < 40000
    assert lt_gas < 40000
    assert le_gas < 40000


@pytest.mark.parametrize(
    'left,right,expected',
    (
        ('1.0.0', '1.0.0', 0),
        ('1.0.0', '1.1.0', -1),
        ('1.0.0', '1.0.1', -1),
        ('1.0.0', '2.0.0', -1),
        ('1.0.0', '2.0.0-beta', -1),
        ('1.9.9', '2.0.0', -1),
        ('1.0.0-alpha', '1.0.0-alpha.1', -1),
        ('1.0.0-alpha.1', '1.0.0-alpha.beta', -1),
        ('1.0.0-alpha.beta', '1.0.0-beta.2', -1),
        ('1.0.0-beta.2', '1.0.0-beta.11', -1),
        ('1.0.0-beta.11', '1.0.0-rc.1', -1),
        ('1.0.0-rc.1', '1.0.0', -1),
        ('1.0.0-a', '1.0.0-aa', -1),
        ('1.0.0-999', '1.0.0-1000', -1),
    ),
)
def test_semver_direct_comparisons(chain, left, right, expected):
    semver_lib = chain.get_contract('SemVersionLib')

    left_ver = semver.parse_version_info(left)
    right_ver = semver.parse_version_info(right)

    cmp_args = (
        [left_ver.major, left_ver.minor, left_ver.patch],
        left_ver.prerelease or '',
        [right_ver.major, right_ver.minor, right_ver.patch],
        right_ver.prerelease or '',
    )

    is_eq = expected == 0
    is_gt = expected == 1
    is_ge = is_eq or is_gt
    is_lt = expected == -1
    is_le = is_eq or is_lt

    assert semver_lib.call().isEqual(*cmp_args) is is_eq
    assert semver_lib.call().isGreater(*cmp_args) is is_gt
    assert semver_lib.call().isGreaterOrEqual(*cmp_args) is is_ge
    assert semver_lib.call().isLesser(*cmp_args) is is_lt
    assert semver_lib.call().isLesserOrEqual(*cmp_args) is is_le

    eq_gas = semver_lib.estimateGas().isEqual(*cmp_args)
    gt_gas = semver_lib.estimateGas().isGreater(*cmp_args)
    ge_gas = semver_lib.estimateGas().isGreaterOrEqual(*cmp_args)
    lt_gas = semver_lib.estimateGas().isLesser(*cmp_args)
    le_gas = semver_lib.estimateGas().isLesserOrEqual(*cmp_args)

    assert eq_gas < 55000
    assert gt_gas < 55000
    assert ge_gas < 55000
    assert lt_gas < 55000
    assert le_gas < 55000

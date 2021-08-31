import pytest

from calculator import calculate_expression


def test_calculator():
    assert calculate_expression('1') == 1
    assert calculate_expression('1+1') == 2
    assert calculate_expression('(12+34)*(56-78)') == -1012
    assert calculate_expression('4/2/2') == 1
    assert calculate_expression('(((123+45/5)+(67*8))*9)') == 6012

def test_errors_calculator():
    assert calculate_expression('()') == 'Syntax error: incorret symbol'
    assert calculate_expression('1+') == 'Syntax error: incorret symbol'
    assert calculate_expression('1+a') == 'Syntax error: incorret symbol'
    assert calculate_expression('((1+2)+') == 'Syntax error: incorret symbol'
    assert calculate_expression('1/0') == 'Calculation error: zero division'

# test_tools.py
from app import Me

def test_the_tool():
    # test 1: specific day
    print("Test 1 (March 2):", Me().find_my_holiday(month="March", day="2"))

    # # test 2: lowercase month handling
    # print("Test 2 (june 10):", Me().find_my_holiday(month="june", day="10"))

    # # test 3: full month query
    # print("Test 3 (June Full Month):", Me().find_my_holiday(month="June", day="Full Month"))
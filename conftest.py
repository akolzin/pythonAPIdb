import pytest
#from api.client import RestfulBookerClient
from testdb.DB import DB


db = DB()

@pytest.fixture(scope="session")
def client():
    # client = RestfulBookerClient("https://restful-booker.herokuapp.com")
    # client.authorize("admin", "password123")
    return client

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call':
        db.insertTestResulr(report.nodeid, report.outcome == 'passed')
        print('eep!!', report.outcome)


# import pytest
# from selenium import webdriver
#
# @pytest.fixture(scope="function")
# # @pytest.mark.parametrize('language', ["en"])
# def browser():
#     print("\nstart browser for test..")
#     browser = webdriver.Chrome()
#     yield browser
#     print("\nquit browser..")
#     browser.quit()
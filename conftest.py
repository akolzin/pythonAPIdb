import pytest

from api.client import RestfulBookerClient


@pytest.fixture(scope="session")
def client():
    client = RestfulBookerClient("https://restful-booker.herokuapp.com")
    client.authorize("admin", "password123")
    return client


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
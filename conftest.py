#import allure
from playwright.sync_api import Page, sync_playwright, Playwright, APIRequestContext
from pages.table_page import TablePage
import pytest
import json


# @pytest.fixture(scope='function')
# def page():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         yield page
#         page.close()
#         browser.close()

@pytest.fixture(scope="function", autouse=True)
# navigate to base URL
def goto(page: Page):
    page.goto("")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }


@pytest.fixture(autouse=True)
# Performs tear down pages
def attach_playwright_results(page: Page, request):
    response_list = []
    page.on(
        "response",
        lambda response: response_list.extend(
            [response.all_headers(), response.status, response.url]
        ),
    )
    yield






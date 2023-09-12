import pytest
from playwright.sync_api import Page
from pages.footer_page import FooterPage
from pages.table_page import TablePage
from utils.utils import Utils


class TestFooter:

    @pytest.fixture(autouse=True)
    # Instantiates Page Objects
    def setup(self, page: Page):
        self.table_page = TablePage(page)
        self.footer_page = FooterPage(page)
        self.utils = Utils(page)



    def test_can_not_proceed_to_page_0(self):
        self.utils.wait_for_response(1)
        self.footer_page.move_page_backward()
        assert self.footer_page.get_current_page_number() == 1, "current page should be 1"


    def test_can_proceed_to_page_10(self):
        self.utils.wait_for_response(1)
        for page in range(1, 11):
            self.footer_page.move_page_forward()
            current_page = self.footer_page.get_current_page_number()
            assert current_page == page + 1, f"current page should be {page + 1} but it is {current_page}"


    def test_can_jump_tp_page(self, page: Page):
        jump_to = 5
        self.utils.wait_for_response(1)
        self.footer_page.go_to_page(page, str(jump_to))
        self.utils.wait_for_response(jump_to)


    @pytest.mark.parametrize("jump_to", ["000", "abc"])
    def test_invalid_params_in_the_page_field(self, page: Page, jump_to):
        self.utils.wait_for_response(1)
        self.footer_page.go_to_page(page, "5")
        self.footer_page.go_to_page(page, jump_to)
        self.utils.wait_for_response(5)  # for invalid params the page is not changed and the app does not crash


    @pytest.mark.parametrize("jump_to", ["001", "868657343"])
    def test_invalid_number_params_in_the_page_field(self, page: Page, jump_to):
        self.utils.wait_for_response(1)
        self.footer_page.go_to_page(page, "5")
        self.footer_page.go_to_page(page, jump_to)
        self.utils.wait_for_response(1)  #for invalid params the page dispalyed is page number 1






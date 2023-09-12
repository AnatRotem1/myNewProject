import pytest
import requests
from playwright.sync_api import sync_playwright, expect, Page
from pages.add_member_page import AddMemberPage
from pages.footer_page import FooterPage
from pages.table_page import TablePage
from utils.utils import Utils


class TestAddMember:

    @pytest.fixture(autouse=True)
    # Instantiates Page Objects
    def setup(self, page: Page):
        self.table_page = TablePage(page)
        self.footer_page = FooterPage(page)
        self.utils = Utils(page)
        self.add_member_page = AddMemberPage(page)

    def test_title_is_displayed(self):
        self.add_member_page.mainAddButton.click()
        expect(self.add_member_page.title).to_be_visible()

    def test_add_member(self, page: Page):
        name_to_add = "First_name"
        family_to_add = "Last_name"
        self.add_member(name_to_add, family_to_add)
        assert self.is_member_added_to_the_table(page, name_to_add, family_to_add), f"Member failed to be added, his name is {name_to_add} {family_to_add}"


    def test_the_add_member_response_in_network(self):
        name_to_add = "First_name_network"
        family_to_add = "Last_name_network"
        api_url = "http://localhost:5000/add"
        response = requests.post(api_url, json={"name": name_to_add, "family": family_to_add})
        assert response.status_code == 200, f"Expected 200 status code, but got {response.status_code}"
        assert response.text.__contains__("Added successfully"), f"Expected response message {'Added successfully'} , but got {response.text}"


    def test_added_members_get_unique_ids(self, page):
        members_dict = self.get_members_from_table(page)
        self.utils.verify_no_duplicate_ids(members_dict)

    @pytest.mark.parametrize("name_to_add, family_to_add",
                             [("", ""), ("123", "345"), ("!$%", "@(^"), ("same", "same"), ("First_name", "Last_name")])
    def test_add_member_with_invalid_parameters(self, page, name_to_add, family_to_add):
        self.add_member(name_to_add, family_to_add)
        assert not self.is_member_added_to_the_table(page, name_to_add,
                                                         family_to_add), f"Added invalid member name, with name: {name_to_add} and family: {family_to_add}"


    def is_member_added_to_the_table(self, page, expected_member_name, expected_member_family):
        members_dict = self.get_members_from_table(page)

        for member in members_dict.values():
            member_name = member["Name"]
            member_family = member["Family"]
            if member_name == expected_member_name and member_family == expected_member_family:
                return True
        return False

    def add_two_members(self, member1, family1, member2, family2):
        self.add_member(member1, family1)
        self.add_member(member2, family2)
    def add_member(self, name, family):
        self.add_member_page.mainAddButton.click()
        self.add_member_page.add_member(name, family)

    def get_members_from_table(self, page):
        members_dict = {}
        row_number = 1

        self.footer_page.go_to_page(page, "11")
        self.utils.wait_for_response(11)
        rows = self.table_page.get_rows()

        for row in rows:
            cells = row.locator("//td").all()

            member_id = cells[0].inner_text()
            member_name = cells[1].inner_text()
            member_family = cells[2].inner_text()

            members_dict[row_number] = {
                "Family": member_family,
                "id": member_id,
                "Name": member_name
            }
            row_number += 1
        return members_dict











from typing import Dict
import pytest
from playwright.sync_api import expect, Page
import re
from pages.footer_page import FooterPage
from pages.table_page import TablePage
from utils.utils import Utils


class TestTable:

    @pytest.fixture(autouse=True)
    # Instantiates Page Objects
    def setup(self, page: Page):
        self.table_page = TablePage(page)
        self.footer_page = FooterPage(page)
        self.utils = Utils(page)



    def test_each_page(self, page: Page):
        """
        iterates over the pages to test the validity of the data in the table
        """
        members_dict = {}
        row_number = 1

        for page_num in range(1, 11):
            self.utils.wait_for_response(page_num)
            self.verify_header()
            self.verify_body(members_dict, row_number)
            self.footer_page.go_to_page(page, f"{page_num + 1}")
            row_number += 10

        self.verify_no_duplicate_members(members_dict)
        self.utils.verify_no_duplicate_ids(members_dict)
        
    def verify_header(self):
        expected_texts = ["ID", "Name", "Family"]
        for i, text in enumerate(expected_texts, start=1):
            cell = self.table_page.get_header_cell(i)
            expect(cell).to_have_text(text)
            expect(cell).to_be_visible()

    def verify_body(self, members_dict, row_number):
        rows = self.table_page.get_rows()

        for row in rows:
            cells = row.locator("//td").all()

            member_id = cells[0].inner_text()
            member_name = cells[1].inner_text()
            member_family = cells[2].inner_text()

            self.assert_not_empty_or_none(member_family, member_id, member_name, row_number)
            self.assert_not_null(member_family, member_id, member_name, row_number)
            self.assert_is_valid(member_family, member_name, row_number, self.utils.valid_name_pattern)

            members_dict[row_number] = {
                "Family": member_family,
                "id": member_id,
                "Name": member_name
            }
            row_number += 1

    def verify_no_duplicate_members(self, members_dict):
        my_set = set()
        for entry in members_dict.values():
            name_value = entry['Name']
            family_value = entry['Family']
            member_tuple = (name_value, family_value)

            assert member_tuple not in my_set, f"Duplicate member found: {name_value} {family_value}"
            my_set.add(member_tuple)

 
    def assert_is_valid(self, member_family, member_name, row_number, valid_name_pattern):
        # Check if member_name and member_family do not contain numbers
        assert not re.search(r'\d', member_name), f"Member name is not valid: The member name in row {row_number} contains digits"
        assert not re.search(r'\d', member_family), f"Member name is not valid: The member family name in row {row_number} contains digits"
        # Check if member_name and member_family do not contain special characters
        assert (valid_name_pattern.match(
            member_name)), f"Member name is not valid: The member name in row {row_number} contains special characters"
        assert (valid_name_pattern.match(
            member_family)), f"Member name is not valid: The member family name in row {row_number} contains special characters"
        # Check if member_name is not equal to member_family
        assert member_name != member_family, f"Member name is not valid: The member is row {row_number} has the same private name and family name"

    def assert_not_null(self, member_family, member_id, member_name, row_number):
        # Check if any cell is empty or contains null
        assert member_id not in ["null", "Null"], f"Member name is not valid: The member Id in row {row_number} is null"
        assert member_name not in ["null", "Null"], f"Member name is not valid: The member name in row {row_number} is null"
        assert member_family not in ["null", "Null"], f"Member name is not valid: The member family name in row {row_number} is null"

    def assert_not_empty_or_none(self, member_family, member_id, member_name, row_number):
        assert member_id, f"Member name is not valid: The member Id in row {row_number} is None or empty"
        assert member_name, f"Member name is not valid: The member name in row {row_number} is None or empty"
        assert member_family, f"Member name is not valid: The member family name in row {row_number} is None or empty"



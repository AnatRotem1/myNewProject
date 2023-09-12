import re
from playwright.sync_api import Page


class AddMemberPage:

    def __init__(self, page: Page):
        self.page = page
        self.mainAddButton = page.locator('[data-testid="PersonAddIcon"]')
        self.title = page.get_by_role("heading", name="Add New Member")
        self.name_field = page.get_by_label("Name")
        self.family_field = page.get_by_label("Family")
        self.addButton = page.get_by_role("button", name=re.compile("ADD", re.IGNORECASE))


    def insert_name(self, str):
        self.name_field.fill(str)
    def insert_family(self, str):
        self.family_field.fill(str)
    def add_member(self, name, family):
        self.insert_name(name)
        self.insert_family(family)
        self.addButton.click()

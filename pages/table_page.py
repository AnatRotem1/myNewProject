from playwright.sync_api import Page


class TablePage:

    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator("//thead")
        self.table = page.locator("//table")
        self.rows = self.table.locator("//tr").all()[1:]

    def get_header_cell(self, i):
        return self.header.locator(f"th:nth-child({i})")
    def get_rows(self):
        return self.table.locator("//tr").all()[1:]

    def get_rows_count(self):
        return len(self.get_rows())
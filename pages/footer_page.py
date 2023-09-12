from playwright.sync_api import Page



class FooterPage:

    def __init__(self, page: Page):
        self.page = page
        self.page_field = page.locator('input[id=":r0:"]')
        self.arrow_right = page.locator('[data-testid="ArrowRightIcon"]')
        self.arrow_left = page.locator('[data-testid="ArrowLeftIcon"]')

    def move_page_forward(self):
        self.arrow_right.click()
    def move_page_backward(self):
        self.arrow_left.click()
    def get_current_page_number(self):
        return int(self.page_field.get_attribute("value"))
    def go_to_page(self, page: Page, go_to_page: str):
        self.page_field.fill(go_to_page)
        page.keyboard.press("Enter")
import re
import time
import requests
from playwright.sync_api import Page


class Utils:


    def __init__(self, page: Page):
        self.page = page
        # Define a.py regular expression pattern to match only letters and spaces
        self.valid_name_pattern = re.compile(r'^[A-Za-z\s]+$')

    def wait_for_response(self, page_num):
        start_time = time.time()
        api_url = f"http://0.0.0.0:5000/page?page={page_num}"
        response = requests.get(api_url)
        duration = time.time() - start_time
        assert response.status_code == 200, f"Expected 200 status code, but got {response.status_code}"
        assert duration < 1.0, f"Expected response time to be less than 1 second, but got {duration} seconds in page {page_num}"



    def verify_no_duplicate_ids(self, members_dict):
        my_set = set()
        for entry in members_dict.values():
            id_value = entry['id']
            assert id_value not in my_set, f"Duplicate id found: {id_value}"
            my_set.add(id_value)




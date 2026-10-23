from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost")

    # Test 1: page title
    assert "Task Manager" in driver.title
    print("PASS: page title is correct")

    # Test 2: heading element exists
    heading = driver.find_element(By.ID, "title")
    assert heading.text == "Task Manager"
    print("PASS: heading element found")

    # Test 3: add a task and verify it appears
    driver.find_element(By.ID, "task-input").send_keys("Selenium test task")
    driver.find_element(By.ID, "add-btn").click()
    time.sleep(1)
    tasks_list = driver.find_element(By.ID, "tasks-list").text
    assert "Selenium test task" in tasks_list
    print("PASS: new task appears in the list")

    print("ALL TESTS PASSED")
finally:
    driver.quit()

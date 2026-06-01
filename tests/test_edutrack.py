import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://edutrack-jenkins:3000"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

class EduTrackTests(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(BASE_URL)
        time.sleep(1)

    def tearDown(self):
        self.driver.quit()

    def test_01_page_title(self):
        self.assertIn("EduTrack", self.driver.title)

    def test_02_students_tab_active(self):
        active = self.driver.find_element(By.CSS_SELECTOR, ".tab.active")
        self.assertIn("Students", active.text)

    def test_03_add_student_form_visible(self):
        self.assertTrue(self.driver.find_element(By.ID, "s-name").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "s-email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "s-age").is_displayed())

    def test_04_add_student(self):
        self.driver.find_element(By.ID, "s-name").send_keys("Alice Khan")
        self.driver.find_element(By.ID, "s-email").send_keys("alice@test.com")
        self.driver.find_element(By.ID, "s-age").send_keys("21")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-students .btn").click()
        time.sleep(1)
        table = self.driver.find_element(By.ID, "students-table").text
        self.assertIn("Alice Khan", table)

    def test_05_student_email_in_table(self):
        self.driver.find_element(By.ID, "s-name").send_keys("Bob Ahmed")
        self.driver.find_element(By.ID, "s-email").send_keys("bob@test.com")
        self.driver.find_element(By.ID, "s-age").send_keys("22")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-students .btn").click()
        time.sleep(1)
        table = self.driver.find_element(By.ID, "students-table").text
        self.assertIn("bob@test.com", table)

    def test_06_fields_clear_after_add(self):
        self.driver.find_element(By.ID, "s-name").send_keys("Clear Test")
        self.driver.find_element(By.ID, "s-email").send_keys("clear@test.com")
        self.driver.find_element(By.ID, "s-age").send_keys("20")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-students .btn").click()
        time.sleep(1)
        self.assertEqual(self.driver.find_element(By.ID, "s-name").get_attribute("value"), "")
        self.assertEqual(self.driver.find_element(By.ID, "s-email").get_attribute("value"), "")

    def test_07_switch_to_courses_tab(self):
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Courses')]").click()
        time.sleep(0.5)
        active = self.driver.find_element(By.CSS_SELECTOR, ".tab.active")
        self.assertIn("Courses", active.text)

    def test_08_add_course(self):
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Courses')]").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "c-title").send_keys("DevOps 101")
        self.driver.find_element(By.ID, "c-desc").send_keys("CI/CD basics")
        self.driver.find_element(By.ID, "c-credits").send_keys("3")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-courses .btn").click()
        time.sleep(1)
        table = self.driver.find_element(By.ID, "courses-table").text
        self.assertIn("DevOps 101", table)

    def test_09_course_credits_in_table(self):
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Courses')]").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "c-title").send_keys("Cloud Computing")
        self.driver.find_element(By.ID, "c-desc").send_keys("AWS basics")
        self.driver.find_element(By.ID, "c-credits").send_keys("4")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-courses .btn").click()
        time.sleep(1)
        table = self.driver.find_element(By.ID, "courses-table").text
        self.assertIn("4 cr", table)

    def test_10_course_fields_clear(self):
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Courses')]").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "c-title").send_keys("Temp Course")
        self.driver.find_element(By.ID, "c-desc").send_keys("Temp desc")
        self.driver.find_element(By.ID, "c-credits").send_keys("2")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-courses .btn").click()
        time.sleep(1)
        self.assertEqual(self.driver.find_element(By.ID, "c-title").get_attribute("value"), "")

    def test_11_switch_to_enrollments_tab(self):
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Enrollments')]").click()
        time.sleep(0.5)
        active = self.driver.find_element(By.CSS_SELECTOR, ".tab.active")
        self.assertIn("Enrollments", active.text)

    def test_12_enrollment_dropdowns_populated(self):
        self.driver.find_element(By.ID, "s-name").send_keys("Dropdown Student")
        self.driver.find_element(By.ID, "s-email").send_keys("drop@test.com")
        self.driver.find_element(By.ID, "s-age").send_keys("23")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-students .btn").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Courses')]").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "c-title").send_keys("Drop Course")
        self.driver.find_element(By.ID, "c-credits").send_keys("3")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-courses .btn").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Enrollments')]").click()
        time.sleep(1)
        options = self.driver.find_element(By.ID, "e-student").find_elements(By.TAG_NAME, "option")
        self.assertGreater(len(options), 0)

    def test_13_add_enrollment(self):
        self.driver.find_element(By.ID, "s-name").send_keys("Enroll Student")
        self.driver.find_element(By.ID, "s-email").send_keys("enroll@test.com")
        self.driver.find_element(By.ID, "s-age").send_keys("24")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-students .btn").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Courses')]").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "c-title").send_keys("Enroll Course")
        self.driver.find_element(By.ID, "c-credits").send_keys("3")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-courses .btn").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Enrollments')]").click()
        time.sleep(1)
        Select(self.driver.find_element(By.ID, "e-student")).select_by_index(0)
        Select(self.driver.find_element(By.ID, "e-course")).select_by_index(0)
        self.driver.find_element(By.ID, "e-grade").send_keys("A")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-enrollments .btn").click()
        time.sleep(1)
        table = self.driver.find_element(By.ID, "enrollments-table").text
        self.assertNotIn("No enrollments yet", table)

    def test_14_delete_student(self):
        self.driver.find_element(By.ID, "s-name").send_keys("Delete Me")
        self.driver.find_element(By.ID, "s-email").send_keys("delete@test.com")
        self.driver.find_element(By.ID, "s-age").send_keys("25")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-students .btn").click()
        time.sleep(1)
        
        del_btn = self.driver.find_element(By.CSS_SELECTOR, "#students-table tr:last-child .del-btn")
        del_btn.click()
        
        self.wait.until(EC.staleness_of(del_btn))
        table = self.driver.find_element(By.ID, "students-table").text
        self.assertNotIn("Delete Me", table)

    def test_15_delete_course(self):
        self.driver.find_element(By.XPATH, "//div[@class='tab' and contains(text(),'Courses')]").click()
        time.sleep(0.5)
        self.driver.find_element(By.ID, "c-title").send_keys("Delete Course")
        self.driver.find_element(By.ID, "c-credits").send_keys("1")
        self.driver.find_element(By.CSS_SELECTOR, "#tab-courses .btn").click()
        time.sleep(1)
        
        del_btn = self.driver.find_element(By.CSS_SELECTOR, "#courses-table tr:last-child .del-btn")
        del_btn.click()
        
        self.wait.until(EC.staleness_of(del_btn))
        table = self.driver.find_element(By.ID, "courses-table").text
        self.assertNotIn("Delete Course", table)

if __name__ == "__main__":
    unittest.main(verbosity=2)

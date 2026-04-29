import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    WebDriverException
)

# Context manager for Selenium WebDriver
class WebDriverContext:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        try:
            self.driver = webdriver.Chrome()
            return self.driver
        except WebDriverException as e:
            print(f"WebDriver initialization failed: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

current_dir = os.getcwd()
file_path = os.path.join(current_dir, "report.html")
file_url = ''
try:
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    # Convert file path to URL format
    file_url = 'file:///' + os.path.abspath(file_path).replace('\\', '/')

except FileNotFoundError as fnf_error:
    print("File not found error:", fnf_error)
except Exception as e:
    print("An unexpected error occurred:", e)

# Prepare to store table data
table_data = []

if __name__ == "__main__":
    # Initialize WebDriver (example with Chrome)
    with WebDriverContext() as driver:
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "report.html")
        driver.get(file_url)
        time.sleep(5)

        try:
            # Wait for the table to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "table"))
            )

            # Get the table root element
            table = driver.find_element(By.XPATH,"//*[@id='2742bf19-7fb1-40ef-8b0e-fb51522276e9']/div/div/*[local-name()='svg'][1]/*[local-name()='g'][15]")

            # Get all columns
            columns = table.find_elements(By.CLASS_NAME, "y-column")

            for column in columns:
                # Get column header
                header = column.find_element(By.ID, "header").text.strip()

                # Get all data cells in column
                cells = column.find_elements(By.CLASS_NAME, "cell-text")

                # Filter out cell where cell.text == header
                data_cells = [cell.text.strip() for cell in cells if cell.text.strip() != header]

                # Store header and data
                table_data.append({
                    'header': header,
                    'data': data_cells
                })

            # Extract headers and rows
            headers = [item['header'] for item in table_data]
            rows = zip(*[item['data'] for item in table_data])

        except TimeoutException:
            print("There is some issue in reading data.")

        try:
            with open('table.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)
        except FileNotFoundError:
            print("Error: The specified file path does not exist.")
        except PermissionError:
            print("Error: You do not have permission to write to this location.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.save_screenshot("screenshot0.png")
        doughnut0_textdata = []
        try:
            cb2 = driver.find_element(By.XPATH,"//*[@id='2742bf19-7fb1-40ef-8b0e-fb51522276e9']/div/div/*[local-name()='svg'][2]/*[local-name()='g'][4]/*[local-name()='g'][1]/*[local-name()='g']/*[local-name()='g']/*[local-name()='g'][2]")
            cb2.click()
            time.sleep(5)
            cb3 = driver.find_element(By.XPATH, "//*[@id='2742bf19-7fb1-40ef-8b0e-fb51522276e9']/div/div/*[local-name()='svg'][2]/*[local-name()='g'][4]/*[local-name()='g'][1]/*[local-name()='g']/*[local-name()='g']/*[local-name()='g'][3]")
            cb3.click()
            time.sleep(5)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.save_screenshot("screenshot1.png")

            # Find all elements with class 'line'
            lines = driver.find_elements(By.CLASS_NAME, 'line')

            # Extract text from each element
            doughnut0_textdata = [line.text for line in lines]

        except TimeoutException:
            print("There is some issue in reading data.")

        try:
            with open('doughnut0.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Facility Type", "Min Average Time Spent"])
                writer.writerow(doughnut0_textdata)
        except FileNotFoundError:
            print("Error: The specified file path does not exist.")
        except PermissionError:
            print("Error: You do not have permission to write to this location.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        doughnut1_textdata = []
        try:
            cb1 = driver.find_element(By.XPATH,"//*[@id='2742bf19-7fb1-40ef-8b0e-fb51522276e9']/div/div/*[local-name()='svg'][2]/*[local-name()='g'][4]/*[local-name()='g'][1]/*[local-name()='g']/*[local-name()='g']/*[local-name()='g'][1]")
            cb1.click()
            time.sleep(5)
            cb2 = driver.find_element(By.XPATH,"//*[@id='2742bf19-7fb1-40ef-8b0e-fb51522276e9']/div/div/*[local-name()='svg'][2]/*[local-name()='g'][4]/*[local-name()='g'][1]/*[local-name()='g']/*[local-name()='g']/*[local-name()='g'][2]")
            cb2.click()
            time.sleep(5)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.save_screenshot("screenshot2.png")

            # Find all elements with class 'line'
            lines = driver.find_elements(By.CLASS_NAME, 'line')

            # Extract text from each element
            doughnut1_textdata = [line.text for line in lines]

        except TimeoutException:
            print("There is some issue in reading data.")

        try:
            with open('doughnut1.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Facility Type", "Min Average Time Spent"])
                writer.writerow(doughnut1_textdata)
        except FileNotFoundError:
            print("Error: The specified file path does not exist.")
        except PermissionError:
            print("Error: You do not have permission to write to this location.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        doughnut2_textdata = []
        try:
            cb2 = driver.find_element(By.XPATH,"//*[@id='2742bf19-7fb1-40ef-8b0e-fb51522276e9']/div/div/*[local-name()='svg'][2]/*[local-name()='g'][4]/*[local-name()='g'][1]/*[local-name()='g']/*[local-name()='g']/*[local-name()='g'][2]")
            cb2.click()
            time.sleep(5)
            cb3 = driver.find_element(By.XPATH,"//*[@id='2742bf19-7fb1-40ef-8b0e-fb51522276e9']/div/div/*[local-name()='svg'][2]/*[local-name()='g'][4]/*[local-name()='g'][1]/*[local-name()='g']/*[local-name()='g']/*[local-name()='g'][3]")
            cb3.click()
            time.sleep(5)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.save_screenshot("screenshot3.png")

            # Find all elements with class 'line'
            lines = driver.find_elements(By.CLASS_NAME, 'line')

            # Extract text from each element
            doughnut2_textdata = [line.text for line in lines]

        except TimeoutException:
            print("There is some issue in reading data.")

        try:
            with open('doughnut2.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Facility Type", "Min Average Time Spent"])
                writer.writerow(doughnut2_textdata)
        except FileNotFoundError:
            print("Error: The specified file path does not exist.")
        except PermissionError:
            print("Error: You do not have permission to write to this location.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


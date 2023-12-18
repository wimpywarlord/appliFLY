from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.options import Options

try:
  # ! Make sure you have installed all the dependencies:
  # Run : `pip install -r requirements.txt` to install all dependency.

  print("Dᴇᴠᴇʟᴏᴘᴇᴅ Bʏ Kꜱʜɪᴛɪᴊ Dʜʏᴀɴɪ");
  print("@https://github.com/wimpywarlord")

  print('\n')

  print('____________PRE-REQUISITES____________')
  print('1. Make sure have created a `.env` file in the same directory as this script.')
  print('2. Make sure have copied contents of the `env.txt` file into that `.env`.')
  print('3. Make sure have filled the `.env` file with your credentials and paths.')
  print('4. Make sure you installed all the dependencies: `pip install -r requirements.txt`')
  print('5. Make sure you have a good internet connection.')
  print('6. Make sure you have applied to atleast 1 job on the portal manually.')

  print('\n')

  print('____________NOTES____________')
  print("1. You will need to 1 time authenticate using DUO. Make sure you have your phone with you.")
  print("2. If the script crashes for any reason. Simply Restart It. It will work the next time, give it a few tries.")
  print("3. In case of errror, document the error and report to the github repository @https://github.com/wimpywarlord/appliFLY/issues")
  print("4. If you have already applied for a job, the script will skip it.")

  print('\n')

  # Load variables from .env into the environment
  load_dotenv()  

  # ! Program assumes you have applied to atleast one job before.
  # ! Hence this program does not fill all the fields. Instead only the ones that
  # ! are not prefilled while applying.

  # ! TODO: Sleep timers might indicate failure with slow internet connection.

  # The job posting URL look like so:
  # https://sjobs.brassring.com/TGnewUI/Search/Home/Home?partnerid=25620&siteid=5495&SID=%5E0H7sD8KSrU4EUv71HY1iNlPi%2FLOvg9dgktsvkP9lCLZISnp1wC3ZWGEynF16KAOw#jobDetails=4806069_5495
  # https://sjobs.brassring.com/TGnewUI/Search/Home/Home?partnerid=25620&siteid=5495&SID=%5ERgO0s1QqGFzWtDBhfI_slp_rhc_ezzW7oDCXSDQ7L1_slp_rhc_Ry7amPlixGPebB1JAnboIA3S1uZgn#jobDetails=4806064_5495
  # https://sjobs.brassring.com/TGnewUI/Search/Home/Home?partnerid=25620&siteid=5495&SID=%5ECzvGds%2FJVFYG8skdLcAm88wzj7UlqbGwag3xc9P9lL2C7cSK8ZkpIOI4IaXOtBEr#jobDetails=4806089_5495

  #  ? When we change jobDetails from the URL using siteid of some other job, it still loads up perfectly.

  # Create a new instance of the browser (make sure you have the appropriate driver installed)
  # You can use other drivers like Firefox, Edge, etc.

  # ____________ If Facing Jobs 0 Jobs found issue ________________
  # Absolute Path to Chrome Driver Example: C:\Users\ASUS\Downloads\chrome\chrome.exe
  # chromeDriver = webdriver.Chrome(executable_path=r"Absolute Path to the Chrome Driver")  # Uncomment this if facing 0 jobs found issue
  # ____________ No Erros ____________________
  chromeDriver = webdriver.Chrome()  # Comment this out if facing 0 jobs found issue
  
  chromeDriver.maximize_window()

  # Navigate to the website
  employmentHomePageUrl = 'https://students.asu.edu/employment/search'
  chromeDriver.get(employmentHomePageUrl)

  on_campus_job_button = chromeDriver.find_element(By.XPATH ,"/html/body/div/div/main/div[2]/article/div[2]/div/div/div/div/div/div[4]/div/a[1]")

  on_campus_job_button.click()

  # Find and Fill Id and Password
  username_field = chromeDriver.find_element(By.ID, "username")
  password_field = chromeDriver.find_element(By.ID, "password")
  login_button = chromeDriver.find_element(By.XPATH ,"/html/body/div/div/main/div/div/div/div/form/section[2]/div[1]/input")

  username_field.send_keys(os.getenv('ASUUSERNAME'))
  password_field.send_keys(os.getenv('ASUPASSWORD'))

  login_button.click()

  # Wait for DUO authentication.
  time.sleep(2)

  duo_security_iframe = chromeDriver.find_element(By.XPATH, "/html/body/div/div/main/div/form/div/iframe")
  chromeDriver.switch_to.frame(duo_security_iframe)

  wait_for_send_duo_push_button = WebDriverWait(chromeDriver, 10)
  wait_for_send_duo_push_button.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button")))

  send_duo_push_button = chromeDriver.find_element(By.XPATH, "/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button")

  # Click the send push button
  send_duo_push_button.click()

  # ! Please authenticate using your phone as soon as possible.

  # Wait for the search button to load on the job portal
  time.sleep(10)

  chromeDriver.switch_to.default_content()

  wait_for_search_button_job_portal = WebDriverWait(chromeDriver, 10)
  wait_for_search_button_job_portal.until(EC.element_to_be_clickable((By.ID, "searchControls_BUTTON_2")))
  job_portal_search_button = chromeDriver.find_element(By.ID, "searchControls_BUTTON_2")

  job_portal_search_button.click()

  # Wait for the search results to load
  # ! IMPORTANT - Possible point of failure, if wait time is not enough for slow internet connection.
  time.sleep(10)

  # Click Next button as many times as it is available
  while True:
      try:
          button = chromeDriver.find_element(By.ID, "showMoreJobs")
          button.click()
      except NoSuchElementException:
          print("All jobs staged for application.")
          break
      
  wait_for_job_title_links = WebDriverWait(chromeDriver, 10)
  wait_for_job_title_links.until(EC.presence_of_element_located((By.CLASS_NAME, "jobtitle")))
  job_title_links = chromeDriver.find_elements(By.CLASS_NAME, 'jobtitle')

  print("____________JOB LINKS FOUND____________");
  print("There are " + str(len(job_title_links)) + " jobs available for you to apply.");

  # Loop through the found links
  for link in job_title_links:
      time.sleep(2)
      print("Job Title:", link.text)
      print("URL:", link.get_attribute("href"))

      # Open a new tab using JavaScript
      chromeDriver.execute_script("window.open(arguments[0], '_blank');", link.get_attribute("href"))

      # Switch to the newly opened tab
      chromeDriver.switch_to.window(chromeDriver.window_handles[1])

      # ? If you have already applied for the job, then quit the window immidiately.
      text_to_find = "You have already applied for this job."
      if text_to_find in chromeDriver.page_source:
        # Close the new tab and switch back to the original tab
        chromeDriver.close()
        chromeDriver.switch_to.window(chromeDriver.window_handles[0])
        time.sleep(1)
        continue

      # * You are now in the new tab and can interact with its contents

      # Apply Button
      wait_for_apply_button_job_desc = WebDriverWait(chromeDriver, 30)
      wait_for_apply_button_job_desc.until(EC.element_to_be_clickable((By.ID, "applyFromDetailBtn")))
      job_desc_apply_button = chromeDriver.find_element(By.ID, "applyFromDetailBtn")

      job_desc_apply_button.click()
      
      # Lets get started Button
      wait_for_lets_get_started_button = WebDriverWait(chromeDriver, 30)
      wait_for_lets_get_started_button.until(EC.element_to_be_clickable((By.ID, "startapply")))
      lets_get_started_button = chromeDriver.find_element(By.ID, "startapply")

      lets_get_started_button.click()

      time.sleep(5)

      # Save and Continue Button 
      wait_for_save_and_continue_button = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_continue_button.until(EC.element_to_be_clickable((By.ID, "shownext")))
      save_and_continue_button = chromeDriver.find_element(By.ID, "shownext")

      save_and_continue_button.click()

      # SAVE AND CONTINUE BUTTON

      # YES - Are you currently eligible to work in the United States 
      # without ASU sponsorship?
      wait_for_sponsorship_radio_button = WebDriverWait(chromeDriver, 30)
      wait_for_sponsorship_radio_button.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[2]/fieldset/div/div[1]/input")))
      sponsorship_radio_button = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[2]/fieldset/div/div[1]/input")

      sponsorship_radio_button.click()

      # YES / NO - Are you eligible for Federal Work Study?
      if os.getenv('FEDERAL_WORK_STUDY').lower() == "true":
        # YES - Radio Button
        wait_for_federal_work_study_button = WebDriverWait(chromeDriver, 30)
        wait_for_federal_work_study_button.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[6]/fieldset/div/div[1]/input")))
        federal_work_study_button = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[6]/fieldset/div/div[1]/input")
        federal_work_study_button.click()
      else: 
        # NO - Radio Button
        wait_for_federal_work_study_button = WebDriverWait(chromeDriver, 30)
        wait_for_federal_work_study_button.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[6]/fieldset/div/div[1]/input")))
        federal_work_study_button = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[6]/fieldset/div/div[2]/input")
        federal_work_study_button.click()

      # How did you find out about this job?
      wait_for_where_you_found_the_job_drop_down = WebDriverWait(chromeDriver, 30)
      wait_for_where_you_found_the_job_drop_down.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[7]/span[2]/span[2]")))
      where_you_found_the_job_drop_down = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div/div/div[7]/span[2]/span[2]")

      where_you_found_the_job_drop_down.click()

      # How did you find out about this job?
      wait_for_where_you_found_the_job_drop_down_options = WebDriverWait(chromeDriver, 30)
      wait_for_where_you_found_the_job_drop_down_options.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[5]/div[1]/ul/li[4]/div")))
      where_you_found_the_job_drop_down_options = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[5]/div[1]/ul/li[4]/div")

      where_you_found_the_job_drop_down_options.click()

      # Save and Continue
      wait_for_save_and_next = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[4]/button")))
      save_and_next = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[4]/button")
      save_and_next.click()

      wait_for_save_and_next_part_2 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_2.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[4]/button")))
      save_and_next_part_2 = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[4]/button")
      save_and_next_part_2.click()

      # Find the file input element
      wait_for_resume_file_input = WebDriverWait(chromeDriver, 30)
      wait_for_resume_file_input.until(EC.element_to_be_clickable((By.ID, "AddResumeLink")))
      resume_file_input = chromeDriver.find_element(By.ID, "AddResumeLink")
      resume_file_input.click()
      
      # WAIT FOR MODAL TO APPEAR
      wait_for_resume_file_upload_modal = WebDriverWait(chromeDriver, 30)
      wait_for_resume_file_upload_modal.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]")))

      upload_resume_modal_iframe = chromeDriver.find_element(By.XPATH, "/html/body/div[3]/div[2]/iframe")
      chromeDriver.switch_to.frame(upload_resume_modal_iframe)

      browse_local_for_resume_button = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div[3]/label/input")

      # Set the file path to the input element
      browse_local_for_resume_button.send_keys(os.getenv('PATH_TO_RESUME'))

      chromeDriver.switch_to.default_content()

      # Find the file input element
      wait_for_cover_letter_file_input = WebDriverWait(chromeDriver, 30)
      wait_for_cover_letter_file_input.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div[2]/div/div[4]/div/div/div[3]/p/a")))
      cover_letter_file_input = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[7]/div[3]/form/div/div[1]/div[2]/div/div/div/div[2]/div/div[4]/div/div/div[3]/p/a")
      cover_letter_file_input.click()

      # WAIT FOR MODAL TO APPEAR
      wait_for_cover_letter_file_upload_modal = WebDriverWait(chromeDriver, 30)
      wait_for_cover_letter_file_upload_modal.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]")))

      upload_cover_letter_modal_iframe = chromeDriver.find_element(By.XPATH, "/html/body/div[3]/div[2]/iframe")
      chromeDriver.switch_to.frame(upload_cover_letter_modal_iframe)

      browse_local_for_cover_letter = chromeDriver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div[3]/label/input")

      # Set the file path to the input element
      browse_local_for_cover_letter.send_keys(os.getenv('PATH_TO_COVER_LETTER'))

      time.sleep(4)

      chromeDriver.switch_to.default_content()

      # Save and Continue
      wait_for_save_and_next_part_3 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_3.until(EC.element_to_be_clickable((By.ID, "shownext")))
      save_and_next_part_3 = chromeDriver.find_element(By.ID, "shownext")
      save_and_next_part_3.click()

      # TODO: CODE TO UPLOAD SUPPLEMENTAL FILES
      # CAN UPLOAD UPTO 25 FILES

      # Save and Continue
      wait_for_save_and_next_part_4 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_4.until(EC.element_to_be_clickable((By.ID, "shownext")))
      save_and_next_part_4 = chromeDriver.find_element(By.ID, "shownext")
      save_and_next_part_4.click()

      time.sleep(5)

      # Save and Continue
      wait_for_save_and_next_part_5 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_5.until(EC.element_to_be_clickable((By.ID, "shownext")))
      save_and_next_part_5 = chromeDriver.find_element(By.ID, "shownext")
      save_and_next_part_5.click()

      time.sleep(5)

      # Save and Continue
      wait_for_save_and_next_part_6 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_6.until(EC.element_to_be_clickable((By.ID, "shownext")))
      save_and_next_part_6 = chromeDriver.find_element(By.ID, "shownext")
      save_and_next_part_6.click()

      time.sleep(2)

      # Save and Continue
      wait_for_save_and_next_part_7 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_7.until(EC.element_to_be_clickable((By.ID, "shownext")))
      save_and_next_part_7 = chromeDriver.find_element(By.ID, "shownext")
      save_and_next_part_7.click()

      time.sleep(3)

      wait_for_save_and_next_part_8 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_8.until(EC.element_to_be_clickable((By.ID, "shownext")))
      save_and_next_part_8 = chromeDriver.find_element(By.ID, "shownext")
      save_and_next_part_8.click()

      time.sleep(3)

      # Send My Application
      wait_for_save_and_next_part_8 = WebDriverWait(chromeDriver, 30)
      wait_for_save_and_next_part_8.until(EC.element_to_be_clickable((By.ID, "save")))
      save_and_next_part_8 = chromeDriver.find_element(By.ID, "save")
      save_and_next_part_8.click()

      time.sleep(2)

      # Close the new tab and switch back to the original tab
      chromeDriver.close()
      chromeDriver.switch_to.window(chromeDriver.window_handles[0])

      time.sleep(2)

  print("Dᴇᴠᴇʟᴏᴘᴇᴅ Bʏ Kꜱʜɪᴛɪᴊ Dʜʏᴀɴɪ");
  print("Thanks for using. If this helped, be sure to star the project on Github @https://github.com/wimpywarlord/appliFLY/issues");

  # Close the browser
  chromeDriver.quit()
except Exception as e:
    print("An error occured. Please document & report it to the developer @https://github.com/wimpywarlord/appliFLY/issues")
    print(e)
    # Logs the error appropriately. 

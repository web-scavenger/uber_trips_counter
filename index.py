#! /usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time

# at first you must Sign in in current pc to Acc that you want to check.
# after that you can start use this script using comand line
# python ./index.py

user_name = 'user_login' # number template: 0645557788
user_pass = 'user_password'

base_link = 'https://riders.uber.com/trips?offset='
options = webdriver.ChromeOptions()

# WebDriver driver = new ChromeDriver(options)
driver = webdriver.Chrome(options=options)

# Search btn in current form and click submit btn
def submitCurrentForm(): 
  submit_form_btn = driver.execute_script("""
    var form = document.querySelector('form.push--top-small');
    var btn = form.querySelector('button')
    return btn
  """)
  # Click sumbit button
  submit_form_btn.click()
  return

# type user login to the field
def typeUser():
  time.sleep(3)
  login_box = driver.find_element_by_id('useridInput')
  login_box.send_keys(user_name)
  submitCurrentForm()

# type user password to the field
def typePass():
  time.sleep(2)
  pass_box = driver.find_element_by_name('password')
  pass_box.send_keys(user_pass)
  submitCurrentForm()

def typeUserInfo():
  typeUser()
  typePass()

# get all completed trips from the page and sum them up
# count just trips in Ukraine
def getTripsListFromCurrentPage():
  return driver.execute_script("""
    var testForTripsList = document.querySelector('div[data-identity="trip-list"]').innerHTML.length
    if(testForTripsList){
      var test = document.querySelectorAll('div[data-trip-status="COMPLETED"]');
      var result = 0;
      test.forEach(element => {
        var data = element.querySelector('div.bl.cg.av.aw.df.dg.dh.di.bx').innerText
        var price = data.slice(4)
        if(data.includes("UAH")) result+=Number(price)
      })
      return { result: result, count: test.length }
    } else { 
      return false
    }
  """)

# walking through the pages while we have trip`s data on them
def walkThroughThePages(offset, all_trips_result, trips_count):
  driver.get(base_link + str(offset))
  time.sleep(3)
  current_page_result = getTripsListFromCurrentPage()

  if current_page_result != False:
    all_trips_result += current_page_result["result"]
    trips_count += current_page_result["count"]
    offset += 10
    walkThroughThePages(offset, all_trips_result, trips_count)
  else: 
    print "Всього витратив:" + str(all_trips_result)
    print "Всього поїздок:" + str(trips_count)
    print "Середня ціна поїздки:" + str(all_trips_result / trips_count)

driver.get(base_link)

typeUserInfo()

time.sleep(1)

walkThroughThePages(0, 0, 0)

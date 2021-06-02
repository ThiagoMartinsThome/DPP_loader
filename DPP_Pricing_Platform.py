import streamlit as st
from time import sleep
from datetime import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

st.title('DPP Pricing Platform')

# Rate URL
user = st.sidebar.text_input('Input your user name:')
# Rate URL
pword = st.sidebar.text_input('Input your password:')

# Rate URL
dpp = st.text_input('Input Rate URL')

# File Name
file = st.file_uploader('File uploader')

# Sheet name
sheet_name = st.selectbox('Sheet Name', ['dpp_data1',
                                         'dpp_data2',
                                         'dpp_data3',
                                         'dpp_data4',
                                         'dpp_data5',
                                         'dpp_data6',
                                         'dpp_data7',
                                         ])
#For heroku
import os
GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_PATH

if st.button('Hit me'):
    # For heroku
    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    # chormedriver_path = 'chromedriver_win32/chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=chormedriver_path)
    sleep(2)

    # Initialize the website - First page
    driver.get(dpp)
    sleep(2)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(user)
    password.send_keys(pword)
    sleep(1)
    login_button_path = "/html/body/main/div/div/section/div/form/div[4]/button"
    WebDriverWait(driver, 240).until(EC.element_to_be_clickable((By.XPATH, login_button_path)))
    login_button = driver.find_element_by_xpath(login_button_path)
    login_button.click()
    sleep(2)

    # Read Excel file
    df = round(pd.read_excel(file, sheet_name=sheet_name, index_col='index', thousands="."), 2)
    df = df.replace(0, np.nan)
    df.dropna(inplace=True)
    st.dataframe(df.style.format("{:,.2f}", na_rep="-"))

    index = df.index
    cols = df.columns
    placeholder = st.empty()

    try:
        for c in range(0, len(cols)):
            for e, idx in enumerate(index):
                value = str(df.iloc[e, c])
                # print('idx: ', idx, 'col#: ', c, 'price: ', value)
                show = ('INDEX: ', idx, 'COLUMN NUMBER: ', c+1, 'PRICE: ', value)
                with placeholder:
                    st.write(show)
                # placeholder.empty()
                WebDriverWait(driver, 240).until(EC.element_to_be_clickable(
                    (By.NAME, "dynamicPrices.durations[{}].prices[{}].newPrice".format(c, idx - 1))))
                sleep(2)
                driver.find_element_by_name("dynamicPrices.durations[{}].prices[{}].newPrice".format(c, idx - 1))\
                    .clear()
                driver.find_element_by_name("dynamicPrices.durations[{}].prices[{}].newPrice".format(c, idx - 1))\
                    .send_keys(value)
    except Exception:
        st.error("FORMAT DO NOT MATCH. REVIEW EXCEL FILE FORMAT OR ENABLE THE DPP CANDLE ON: {}".format(show))

    else:
        st.success('Rate Loaded!!')

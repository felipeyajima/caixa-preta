import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import os

url_sandbox = os.environ['URL_SANDBOX']
username = os.environ['USERNAME']
passwordy = os.environ['PASSWORD']
tf_token = os.environ['TF_TOKEN']
tf_access_url = os.environ['TF_ACCESS_URL']
tf_access_id = os.environ['TF_ACCESS_ID']
tf_secret_url = os.environ['TF_SECRET_URL']
tf_secret_id = os.environ['TF_SECRET_ID']
qtd_servers = os.environ['QTD_SERVERS']

qtd_servers = int(qtd_servers)

def turn_on_environment(sandbox_url, e_mail, senha):
    from selenium.common.exceptions import NoSuchElementException

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.set_page_load_timeout(20)
    
    driver.get(sandbox_url)

    time.sleep(10)
 
 
    try:
        email = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "1-email")))
        email.send_keys(e_mail)
        print("encontrou e digitou o email")
    except: 
        try:
            email = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "1-email")))
            email.send_keys(e_mail)
            print("no catch encontrou e digitou o email")
        except: NoSuchElementException: print("nao encontrado o elemento campo email")

    try:
        password = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "1-password")))
        password.send_keys(senha)
        print("encontrou e digitou a senha")
    except:
        try:
            password = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "1-password")))
            password.send_keys(senha)
            print("no catch encontrou e digitou a senha")
        except: NoSuchElementException: print("nao encontrado o elemento campo senha")


    try:
        submit = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "1-submit")))
        submit.click()
        print("apertou o botao de logar")
    except:
        try:
            submit = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "1-submit")))
            submit.click()
            print("no catch passou pelo botao de logar")
        except NoSuchElementException: print("nao encontrado o elemento botao logar")



    ## open aws sandbox

    try:
        playground = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tabpanel-0"]/div[1]/div[2]/div/div[1]/div/button')))
        playground.click()
        print("criou o sandbox")
        time.sleep(10)
    except:
        try:
            playground = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tabpanel-0"]/div[1]/div[2]/div/div[1]/div/button')))
            playground.click()
            print("no catch conseguiu criar o sandbox")
            time.sleep(10)
        except NoSuchElementException: print("nao conseguiu criar sandbox")



    # copying credentials
    try:
        credential = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tabpanel-0"]/div/div[1]/div[2]/div[2]/div[4]/div[2]/input')))
        access_key = credential.get_attribute("value")
        #print(f'A access key é a seguinte: {access_key}')
    except:
        try:
            credential = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tabpanel-0"]/div/div[1]/div[2]/div[2]/div[4]/div[2]/input')))
            access_key = credential.get_attribute("value")
            #print(f'A access key é a seguinte: {access_key}')
        except NoSuchElementException: print("nao conseguido criar sandbox")


    try:
        credential = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tabpanel-0"]/div/div[1]/div[2]/div[2]/div[5]/div[2]/input')))
        secret_key = credential.get_attribute("value")
        #print(f'A secret key é a seguinte: {secret_key}')
    except:
        try:
            credential = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tabpanel-0"]/div/div[1]/div[2]/div[2]/div[5]/div[2]/input')))
            secret_key = credential.get_attribute("value")
            #print(f'A secret key é a seguinte: {secret_key}')
        except NoSuchElementException: print("nao conseguido criar sandbox")


    # ligando servidores
    try:
        servers = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tab-2"]')))
        servers.click()
        print("clicou servers")
        time.sleep(5)
    except:
        try:
            servers = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabs-:rh:--tab-2"]')))
            servers.click()
            print("no catch conseguiu acessar a aba servers")
            time.sleep(5)
        except NoSuchElementException: print("nao conseguido clicar em servers") 


    for x in range(0, qtd_servers):
        try:
            server1 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg' and @aria-label='play' and @width='24']")))
            server1.click()
            print("ligou servidor "+ str(x + 1))
        except:
            try:
                server1 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//*[local-name()='svg' and @aria-label='play' and @width='24']")))
                server1.click()
                print("ligou servidor "+ str(x + 1))               
            except NoSuchElementException: print("nao conseguido ligar server") 


    time.sleep(1)

    driver.quit()

    return [access_key, secret_key]



def send_to_tf(valor, token, terraform_url, var_id):

    x = "{ 'data': { 'id':'kakaka', 'attributes': { 'value':'hahaha' }, 'type':'vars' } }"
    b = x.replace("hahaha", valor)
    z = b.replace("kakaka", var_id)
    json_acceptable_string = z.replace("'", "\"")
    y = json.loads(json_acceptable_string)


    k = requests.patch(terraform_url, json = y, headers = {"Content-Type": "application/vnd.api+json","Authorization": token})

    print("enviada access key/secret key ao terraform cloud")



up = turn_on_environment(url_sandbox, username, passwordy)
send_to_tf(up[0],  tf_token, tf_access_url, tf_access_id)
send_to_tf(up[1],  tf_token, tf_secret_url, tf_secret_id)
import re
import os
import logging
import getpass
import string
from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# LOCAL IMPORTS
from modules.webhook import respond
from modules.convert import to_dict, to_file
from modules.utils import time_alive, do_sum, do_sub, do_multi, do_div, do_mod

VER = 1.31
BOT_NAME = 'jarvis'
DEBUGGING = True
LOGIN = getpass.getuser()
EMAIL = f'{LOGIN}@amazon.com'
ROOM = '' # CHATROOM NAME
HOOK = '' # WEBHOOK LINK
CREATION = datetime(2022, 8, 17)
MASTER = '' # OWNER NAME

class Main():
    def __init__(self):
        logging.basicConfig(filename='error.log', format='%(asctime)s - %(message)s', level=logging.WARNING)
        
        options = Options()
        options.add_argument("--headless")

        if not DEBUGGING:
            browser = webdriver.Firefox(options=options)
        else:
            browser = webdriver.Firefox()
            
        self.browser = browser
        self.browser.get('https://app.chime.aws/')
        self.learning = False
        self.answered = False
        self.teacher = ''
        
        self.responses = to_dict('data/responses.csv')
        
        self.browser.execute_script("window.open('');")
        self.browser.switch_to.window(self.browser.window_handles[0])
        
        self.launch()
        
    def launch(self):       
        # LOG IN
        try:
            wait = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#profile_primary_email')))
            
            emailInput = self.browser.find_element(By.CSS_SELECTOR, '#profile_primary_email')
            emailInput.send_keys(EMAIL)
            emailInput.send_keys(Keys.RETURN)
            
            sleep(0.5)
        except TimeoutException:
            logging.critical('Failed to log in.')
            self.browser.quit()
            
        # ACCEPT COOKIES
        try:
            wait = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#awsccc-cb-buttons > button:nth-child(2)')))
            
            cookieButton = self.browser.find_element(By.CSS_SELECTOR, '#awsccc-cb-buttons > button:nth-child(2)')
            cookieButton.click()
            
            sleep(0.5)
        except TimeoutException:
            logging.critical('Failed to find cookie button.')
            self.browser.quit()
            
        self.findRoom()
        self.monitor()
        
        
    def findRoom(self):
        try:
            wait = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.RoomList')))
            
            rooms = self.browser.find_elements(By.CLASS_NAME, 'RoomListItemContainer')
            for room in rooms:
                if room.text == ROOM:
                    room.click()
            
            sleep(0.5)
        except TimeoutException:
            logging.critical('Failed to find cookie button.')
            self.browser.quit()
            
            
    def monitor(self):
        output = []
        while True:
            try:
                wait = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ChatContainer__messages')))
                try:
                    msgs = self.browser.find_elements(By.CLASS_NAME, 'ChatMessageList__messageContainer')
                    if msgs:
                        lastMsg = len(msgs)-1
                        senders = self.browser.find_elements(By.CLASS_NAME, 'ChatMessage__sender')
                        lastSender = len(senders)-1
                                                
                        content = msgs[lastMsg].find_element(By.CLASS_NAME, 'Linkify').text
                        backup = content
                                                
                        if (self.learning and self.call != ''):
                            content = content
                        else:
                            content = re.sub(r'[^a-zA-Z0-9\s]','', content)
                            content = content.lower()
                        
                        sender = str(senders[len(senders)-1].text)
                        
                        # LEARNING MODULE
                        if senders[lastSender].text == self.teacher and self.learning:
                            name = self.teacher.replace(',', '').split()
                            if self.call == '':
                                self.call = content
                                respond(HOOK, f'OK, {name[1]}! Podaj odzew.')
                                
                                sleep(0.5)
                            else:
                                self.respond = content
                                output.append([self.call, self.respond])
                                to_file(output, 'data/responses.csv')
                                self.responses = to_dict('data/responses.csv')
                                self.learning = False
                                self.teacher = ''
                                output.clear()
                                respond(HOOK, f'OK, {name[1]}! Zapamietam!')
                        
                        # COMMANDS
                        if content.find(BOT_NAME)>=0:
                            if content.find('przeladuj')>=0:
                                self.responses = to_dict('data/responses.csv')
                                self.answered = True
                                respond(HOOK, f'Zrobione! 😊')
                            
                            # COMMANDS LIST
                            if content.find('lista')>=0:
                                nl = os.linesep
                                clist = ''
                                commands = ['/md ## Lista komend:',
                                            f'**zapamietaj** - *uczy slowa kluczowego i odpowiedzi*',
                                            f'**przeladuj** - *pobiera ponownie slownik reakcji*',
                                            f'**ile masz lat** - *oblicza wiek od stworzenia bota*',
                                            f'**ile to jest/ile jest** - *wykonuje proste obliczenia matematyczne na podanych liczbach*',
                                            f'**co to jest/kto to jest** - *szuka informacji o zadanym temacie/osobie*'
                                            ]
                                
                                for call in self.responses:
                                    commands.append(f'(slownik) **{call[0]}** - *{call[1]}*')
                                    
                                for command in commands:
                                    if clist == '':
                                        clist = command
                                    else:
                                        clist = clist + nl + command
                                    
                                self.answered = True
                                respond(HOOK, clist)
                            
                            # START LEARNING
                            if content.find('zapamietaj')>=0 and not self.learning:
                                self.teacher = sender
                                name = sender.replace(',', '').split()
                                if self.teacher == MASTER:
                                    self.learning = True
                                    self.call = ''
                                    self.respond = ''
                                    self.answered = True
                                    respond(HOOK, f'OK, {name[1]}! Podaj slowo kluczowe.')
                                    
                                    sleep(0.5)
                                else:
                                    self.answered = True
                                    respond(HOOK, f'Przepraszam, {name[1]}. Nie mozesz mnie uczyc.')
                            
                            # BOT AGE
                            if content.find('ile masz lat')>=0:
                                live = time_alive(CREATION)
                                self.answered = True
                                respond(HOOK, live)
                            
                            # BASIC MATH
                            if content.find('ile to jest')>=0 or content.find('ile jest')>=0:
                                search = str(backup.lower()).replace('ile to jest', '').replace('ile jest', '').replace('jarvis', '', 1).replace('?', '').replace(',', '').strip()

                                if search.find('+')>=0:
                                    equation = do_sum(search)
                                    
                                if search.find('-')>=0:
                                    equation = do_sub(search)
                                    
                                if search.find('*')>=0:
                                    equation = do_multi(search)
                                    
                                if search.find('/')>=0:
                                    equation = do_div(search)
                                    
                                if search.find('%')>=0:
                                    equation = do_mod(search)
                                    
                                self.answered = True    
                                respond(HOOK, equation)
                                
                            # WIKIPEDIA RESEARCH
                            if content.find('co to jest')>=0 or content.find('kto to jest')>=0:
                                answer = ''
                                name = sender.replace(',', '').split()
                                search = str(content.replace('co to jest', '')).replace('jarvis', '', 1).replace('kto to jest', '')
                                search = search.strip()
                                search = string.capwords(search)
                                splitSearch = search.split()
                                search = search.replace(' ', '_')
                                self.browser.switch_to.window(self.browser.window_handles[1])
                                self.browser.get(f'https://pl.wikipedia.org/wiki/{search}')
                                respond(HOOK, 'Pomyslmy... 🤔')
                                
                                sleep(0.5)
                                
                                try:
                                    wait = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'mw-parser-output')))
                                    try:
                                        body = self.browser.find_elements(By.CLASS_NAME, 'mw-parser-output')
                                        paragraphs = body[len(body)-1].find_elements(By.TAG_NAME, 'p')
                                        for paragraph in paragraphs:
                                            paragraph = str(paragraph.text)
                                            if re.search(search, paragraph, re.IGNORECASE):
                                                answer = str(paragraph)
                                                try:
                                                    for i in range(1,25):
                                                        answer = answer.replace(f'[{i}]', '')
                                                except:
                                                    pass
                                                break
                                            if len(splitSearch)>1:
                                                if re.search(splitSearch[0], paragraph, re.IGNORECASE):
                                                    if re.search(splitSearch[1], paragraph, re.IGNORECASE):
                                                        answer = str(paragraph)
                                                        try:
                                                            for i in range(1,25):
                                                                answer = answer.replace(f'[{i}]', '')
                                                        except:
                                                            pass
                                                        break
                                        if answer == '':
                                            raise ValueError
                                        else:
                                            respond(HOOK, answer)   
                                    except:
                                        respond(HOOK, f'Nie mam pojecia, {name[1]}. 😔')
                                except:
                                    respond(HOOK, f'Nie mam pojecia, {name[1]}. 😔')   
                                
                                self.browser.switch_to.window(self.browser.window_handles[0])
                                self.answered = True

                            
                            # DICTIONARY ANSWERS
                            if self.learning == False and self.answered == False: 
                                name = sender.replace(',', '').split()
                                self.analize(content, name[1])
                            
                            logging.info(f'{sender} napisal(a): "{content}"')
                            
                            
                            # IMMEDIATELY FLUSH INFORMATION
                            log = logging.getLogger()
                            handler = logging.FileHandler('error.log')
                            log.addHandler(handler)
                            
                            self.answered = False
                                
                except StaleElementReferenceException:
                    logging.warning('Failed to read message as it reloaded.')
                        
                        
                sleep(0.5)
            except TimeoutException:
                logging.critical('Failed to load list or parse response.')
                self.browser.quit()
                break
        
        
    def analize(self, content, name):
        dicted = str(content).split()
        for call in self.responses:
            if call[0] in dicted:
                answer = str(call[1]).replace('\n', os.linesep)
                respond(HOOK, answer)
                return
        respond(HOOK, f'Przepraszam, {name}. Nie rozumiem. 😔')
        
        
if __name__ == "__main__":
    Main()
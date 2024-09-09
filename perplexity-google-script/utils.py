import time, random, re, tldextract
from selenium.webdriver.common.by import By
from seleniumbase import Driver, SB

from sqlalchemy import create_engine, inspect, Table, MetaData, select, Column, String, ARRAY, func, Integer
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, Session


def create_selenium_driver(mode, proxy=None):
    '''
    Starts SeleniumBase and returns the driver.
    You can choose between wire mode to capture requests or uc mode for anti-bot-detection.
    :param str mode: either wire or uc
    '''
    if mode == 'wire':
        driver = Driver(wire=True, headed=False, proxy=proxy)
        driver.maximize_window()
        return driver
    elif mode == 'uc':
        driver = Driver(uc=True, headed=False, proxy=proxy)
        driver.maximize_window()
        return driver


def get_sources_google(driver, query):
    '''
    Returns a list of domains for Google's first-page search results for a given query.
    :param obj driver: The selenium driver
    :param str query: The query to use
    '''
    urls = []
    driver.get(f'https://www.google.de/search?q={query}')
    cookie_consent = driver.find_elements(By.XPATH, '//button/div[text()="Alle ablehnen"]')
    if cookie_consent:
        cookie_consent[0].click()
    for x in driver.find_elements(By.XPATH, '//cite[@role="text"]'):
        if x.text != '':
            if 'http' in x.text:
                urls.append(re.split(' › ', x.text)[0])
            elif 'Aufrufe' or 'Follower' in x.text:
                urls.append('youtube.com')
            else:
                continue
    return urls


def get_sources_perplexity(driver, query):
    '''
    Returns a list of sources used by perplexity.ai for a given query.
    :param obj driver: The selenium driver (needs to be seleniumbase with UC enabled)
    :param str query: The query to use
    '''
    driver.get('https://perplexity.ai')
    driver.find_element(By.XPATH, '//textarea[@placeholder="Ask anything..."]').send_keys(query)
    time.sleep(random.randint(0, 3))
    driver.find_element(By.XPATH, '//button[@aria-label="Submit"]').click()
    time.sleep(random.randint(5, 10))
    view_all_sources = driver.find_elements(By.XPATH, '//div[contains(@class, "grid-flow-col")]/div[contains(@class, "flex")]')
    if view_all_sources:
        driver.find_element(By.XPATH, '//div[contains(@class, "grid-flow-col")]/div[contains(@class, "flex")]').click()
        time.sleep(random.randint(0, 2))
        return [x.get_attribute('href') for x in driver.find_elements(By.XPATH, '//div[contains(@class, "gap-md")]//a')]
    else:
        return [x.get_attribute('href') for x in driver.find_elements(By.XPATH, '//div[contains(@class, "grid-flow-col")]/div/button/a')]


def compare_searches(queries):
    '''
    :param list queries: A list of lists with queries [category, subcategory0, subcategory1, query]
    '''
    results = []
    driver = create_selenium_driver('uc')
    for i, v in enumerate(queries):
        result = {}
        try:
            google_sources = [tldextract.extract(x).domain + '.' + tldextract.extract(x).suffix for x in get_sources_google(driver, v[3])]
        except Exception as e:
            google_sources = [None]
            print(e)
        try:
            perplexity_sources = [tldextract.extract(x).domain + '.' + tldextract.extract(x).suffix for x in get_sources_perplexity(driver, v[3])]
        except Exception as e:
            perplexity_sources = [None]
            print(e)
        result['category'] = v[0]
        result['subcategory0'] = v[1]
        result['subcategory1'] = v[2]
        result['query'] = v[3]
        result['google'] = google_sources
        result['perplexity'] = perplexity_sources
        results.append(result)
    driver.quit()
    return results


class DBConnection():
    '''
    Connection to a table in my Postgres database for news articles.
    '''
    def __init__(self, host, port, db_name, username, password, table_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self.engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}?sslmode=require')
        self.metadata = MetaData()
        self.table_name = table_name
        self.Base = declarative_base()
        self.TableClass = self.create_table_class()        
        self.Session = scoped_session(sessionmaker(bind=self.engine))


    def get_engine(self):
        '''
        Returns the engine
        '''
        return self.engine

    
    def create_table_class(self):
        '''
        Creates an SQLAlchemy table using the Base class.
        Uses the specified schema if tables does not yet exist.
        If it exists, it reads the table schema from the db.
        '''
        if not self.engine.dialect.has_table(self.engine.connect(), self.table_name):
            class TableClass(self.Base):
                __tablename__ = self.table_name
                id = Column(Integer, primary_key=True)
                category = Column(String)
                subcategory0 = Column(String)
                subcategory1 = Column(String)
                query = Column(String)
                google = Column(ARRAY(String))
                perplexity = Column(ARRAY(String))
            return TableClass
        else:
            class TableClass(self.Base):
                __table__ = Table(self.table_name, self.metadata, autoload_with=self.engine)
            return TableClass


    def create_table(self):
        '''
        Creates a new table if it does not yet exist.
        '''
        if not self.engine.dialect.has_table(self.engine.connect(), self.table_name):
            self.Base.metadata.create_all(self.engine)
            print(f'The following table has been created: {self.table_name}')


    def write_to_db(self, results):
        '''
        Takes a list of entries (dict) and writes it to the db.
        '''
        with self.Session() as session:
            objects = [self.TableClass(**entry) for entry in results]
            session.bulk_save_objects(objects)
            session.commit()
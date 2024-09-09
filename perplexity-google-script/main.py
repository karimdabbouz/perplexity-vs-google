from utils import create_selenium_driver, get_sources_google, get_sources_perplexity, compare_searches, DBConnection
import tldextract, os



if __name__ == '__main__':
    db = DBConnection(
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        db_name=os.environ.get('DB_NAME'),
        username=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'),
        table_name=os.environ.get('DB_TABLE_NAME')
    )
    with open('queries.txt', 'r') as file:
        queries = file.readlines()
        queries = [line.strip().split(',') for line in queries]
    results = compare_searches(queries)
    db.write_to_db(results)
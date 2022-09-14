__import__("dotenv").load_dotenv()
import os
import sys
import pandas as pd
from .util import WebDriver
from datetime import date, timedelta, datetime

days = os.environ.get('days', 1)

fechaInicio = date.today()-timedelta(days=days)

def main():
    if len(sys.argv) in 2:
        print("invalid number of arguments")
        exit(1)

    print("################################################")
    print(f"# Starting Script at {datetime.now().isoformat()}")
    print("################################################")

    cred_path = sys.argv[1]
    cred_df = pd.read_csv(cred_path)

    dfs = []

    driver = WebDriver()

    for _, cred in cred_df.iterrows():
        driver.login(cred)

        dfs.extend((
            driver.process_url(cred["rut"], x)
            for x in driver.get_urls(fechaInicio)
        ))

        driver.logout()

    driver.quit()

    df = pd.concat(dfs)

    df.to_excel("info.xlsx")

if __name__ == '__main__':
    main()

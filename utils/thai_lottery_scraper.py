import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from typing import Any
import numpy as np


class ThaiLotteryScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        self.base_url = "https://www.myhora.com/lottery/stats.aspx?mx=09&vx={year}"
        self.thai_month_map = {
            'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4,
            'พฤษภาคม': 5, 'มิถุนายน': 6, 'กรกฎาคม': 7, 'สิงหาคม': 8,
            'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12
        }

    def fetch_data(self, year: int) -> str:
        """Fetch HTML data from the lottery website"""
        assert isinstance(year, int), "Year must be an integer"
        assert year > 0, "Year must be a positive integer"
        # assert year <= 35, "Year must be less than or equal 35"

        url = self.base_url.format(year=year)
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_data(self, html_content: str) -> list[dict[str, Any]]:
        """Parse HTML content and extract lottery data"""
        data = []
        soup = BeautifulSoup(html_content, 'html.parser')
        lottery_table = soup.find('table', {'id': 'dl_lottery_stats_list'})

        if not lottery_table:
            return data

        rows = lottery_table.find_all('tr')
        for row in rows:
            td = row.find('td')
            if not td:
                continue

            rowx_div = td.find('div', class_='rowx')
            if not rowx_div:
                continue

            colx_divs = rowx_div.find_all('div', class_='colx')
            all_values = [div.text.strip() for div in colx_divs]

            if len(all_values) < 10:
                continue

            # print(all_values)  # Debugging line to check the values

            day = all_values[0]
            month = all_values[1]
            year = all_values[3]
            first_prize = all_values[5]
            last_two = all_values[6]
            top_three = all_values[7]
            bottom_two = all_values[8]
            front_last_three = all_values[9].split(' ')
            front_three = front_last_three[:2]
            last_three = front_last_three[2:]

            # Convert date
            gregorian_year = int(year) - 543
            month_num = self.thai_month_map.get(month, 1)
            date_obj = datetime(gregorian_year, month_num, int(day))

            data.append({
                'date': date_obj,
                'day': day,
                'th_month': month,
                'year': year,
                '1st_prize': np.array(first_prize.split()) if ' ' in first_prize else first_prize,
                '2digit_up': last_two,
                '3digit_up': top_three,
                '2digit_buttom': bottom_two,
                '3digit_front,3digit_bottom': np.array(front_last_three),
                '3digit_front': np.array(front_three),
                '3digit_bottom': np.array(last_three),
            })

        return data

    def data2df(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        """Convert data to DataFrame"""
        df = pd.DataFrame(data)

        return df

    def save_to_csv(self, data: list[dict[str, Any]], filename: str = 'lottery_results.csv'):
        """Save data to CSV file"""
        df = self.data2df(data)
        df.to_csv(filename, index=False)

    def save_to_parquet(self, data: list[dict[str, Any]], filename: str = 'lottery_results.parquet'):
        """Save data to Parquet file"""
        df = self.data2df(data)
        df.to_parquet(filename, index=False)

    def read_csv(self, filename: str = 'lottery_results.csv') -> pd.DataFrame:
        """Read data from CSV file"""
        return pd.read_csv(filename)

    def read_parquet(self, filename: str = 'lottery_results.parquet') -> pd.DataFrame:
        """Read data from Parquet file"""
        return pd.read_parquet(filename)

    def scrape(self, year: int, save: bool = False, output_file: str = 'lottery_results.csv') -> list[dict[str, Any]]:
        """Main method to scrape lottery data"""
        html_content = self.fetch_data(year)
        data = self.parse_data(html_content)

        # # Print for debugging
        # for item in data:
        #     print(item)

        if save:
            self.save_to_csv(data, output_file)
            self.save_to_parquet(data, output_file.replace('.csv', '.parquet'))

        return data

    def scrape_df(self, year: int, save: bool = False, output_file: str = 'lottery_results.csv') -> pd.DataFrame:
        """Scrape data and return as DataFrame"""
        data = self.scrape(year, save, output_file)
        df = self.data2df(data)

        return df


# Usage example
if __name__ == "__main__":
    scraper = ThaiLotteryScraper()
    scraper.scrape(35)  # Scrape year 35

#!/usr/bin/env python3
import os
from apiclient import discovery
from google.oauth2 import service_account
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime, Integer, Boolean, Date
from datetime import date
from datetime import datetime
from sqlalchemy.exc import IntegrityError, DataError

Base = declarative_base()

reference = ["S18 (4+64)", "A60 (2+32)", "A04 (2+32)", "A18 (1+32)", "Camon 20 (8+256)",
              "Camon 19 (4+128)", "Spark 10 (8+128)", "Spark 10C (8+128)", "Spark 10C (4+128)",
              "Spark 8C (2+64)", "Pop 7 pro (4+64)", "Pop 7 pro (3+64)", "Pop 7 (2+64)"
            ]

ref_codes = ["S18", "A60", "A04", "A18", "C20", "C19", "S10", "10C8G", '10C', "8C",
             'P7P4G', 'P7P3G', 'P7']

class MainStorage(Base):
    __tablename__ = 'cryptic_core_app_mainstorage'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    device_imei = Column(String(15), unique=True, nullable=False)
    phone_type = Column(String(25), nullable=False)
    in_stock = Column(Boolean, default=True)
    sales_type = Column(String(10), nullable=True, default="##")
    contract_no = Column(String(8), nullable=True, default='##')
    entry_date = Column(Date, default=date.today())
    stock_out_date = Column(Date, default=date.today())
    assigned = Column(Boolean, default=False)

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

file_scopes = ["https://www.googleapis.com/auth/spreadsheets"]
sheet_id = "1jjYkR-0OImQacljhO181Cj3PI7G5oUsd_Lk68V6_afE"
current_year = 2023
default_month = 7

def read_spread_sheet(sheetName, r_from, to):
    try:
        secret_file = os.path.join(os.getcwd(), 'credentials.json')
        credentials = service_account.Credentials.from_service_account_file(secret_file, scopes=file_scopes)
        service = discovery.build('sheets', 'v4', credentials=credentials)
        sheets = service.spreadsheets()
        data = sheets.values().get(spreadsheetId=sheet_id, range=f"{sheetName}!{r_from}:{to}").execute()
        values = data.get("values", [])
        for row in values:
            try:
                date_str = row[4].split("/")
                if len(date_str) == 1 and date_str != ['5,119,265']:
                    day = date_str[0].replace(',', '')
                    if '0' not in day and int(day) < 10:
                        day = '0'+day
                    date_f = "{}-0{}-{}".format(str(current_year), str(default_month), day)
                    formatted_date = date.fromisoformat(date_f).strftime('%d/%m/%y')
                    row[4] = formatted_date
                elif len(date_str) == 2 and date_str != ['5,119,265']:
                    day = date_str[0]
                    month = date_str[1]
                    date_f = "{}-{}-{}".format(current_year, month, day)
                    formatted_date = date.fromisoformat(date_f).strftime('%d/%m/%y')
                    row[4] = formatted_date
                if row[2] in ref_codes:
                    indx = ref_codes.index(row[2])
                    row[2] = reference[indx]
                try:
                    row[4] = datetime.strptime(row[4], "%d/%m/%y")
                    print(("*" * 20) + "Adding object" + "*" * 20)
                    print(row)
                    product = MainStorage(device_imei=row[0], phone_type=row[2], entry_date=row[4].date())
                    session.add(product)
                    session.commit()
                    print("Next.....")
                except (IntegrityError, ValueError, DataError):
                    session.rollback()
                    print("Already exist....next")
                    continue
            except IndexError:
                continue
        print("Done!!!")
    except OSError as err:
        print(err)


read_spread_sheet('NEW', 'A2', 'E596')

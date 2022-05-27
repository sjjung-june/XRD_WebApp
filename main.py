from flask import Flask, request, render_template
#import modules.inxrd_noqt, modules.outxrd_noqt
import os
import re
import numpy as np
import pandas as pd
from modules.calc import grain_size
from datetime import date

CURR_YEAR, CURR_MONTH, CURR_DATE = date.today().strftime('%Y-%m-%d').split('-')

#DEFAULT_PATH = rf"\\10.138.112.112\Analysis Results\XRD\1_XRD\{YEAR}\{MONTH:02}"
DEFAULT_PATH = rf"\\10.138.112.112\Analysis Results\XRD\1_XRD"
app = Flask("XRD Grain Size")

@app.route('/')
def root(Year_List = None, Month_List = None, SN_List = None):        
    Year_List = [Year for Year in os.listdir(DEFAULT_PATH) if os.path.isdir(os.path.join(DEFAULT_PATH,Year)) and 'JCPDS' not in Year]
    Month_List = [Month for Month in os.listdir(f'{DEFAULT_PATH}\{CURR_YEAR}')]
    SN_List = [SN for SN in os.listdir(f'{DEFAULT_PATH}\{CURR_YEAR}\{CURR_MONTH}')]
    return render_template('index.html', Year_List = Year_List, Month_List = Month_List, SN_List = SN_List)

@app.route('/main', methods=['POST'])
def main():    
    Year_Query = request.get_json()["YEAR"]
    Month_Query = request.get_json()["MONTH"]    
    Month_List = [Month for Month in os.listdir(f'{DEFAULT_PATH}\{Year_Query}')]
    SN_List = [SN for SN in os.listdir(f'{DEFAULT_PATH}\{Year_Query}\{Month_Query}')]
    return {"Month_List":Month_List, "SN_List":SN_List}

@app.route('/submit', methods=['POST'])
def login(File_List = None):
    SN_Query = request.get_json()["SN"]    
    Year_Query = request.get_json()["YEAR"]    
    Month_Query = request.get_json()["MONTH"]    
    File_List = os.listdir(f'{DEFAULT_PATH}\{Year_Query}\{Month_Query}\{SN_Query}')
    File_List = [x for x in File_List if ".txt" in x or ".TXT" in x]    
    File_List = [x for x in File_List if "2-ThetaChi_Phi" in x or "_Theta_2-Theta" in x]    
    Full_Dataset = {}
    Dataset = {}
    for file in File_List:
        data_path = f'{DEFAULT_PATH}\{Year_Query}\{Month_Query}\{SN_Query}\{file}'    
        df = pd.read_csv(data_path, header=2, sep="\t")    
        df.columns = ["Angle","Count"]
        Dataset[file] = {"Angle":df["Angle"].to_list(), "Count":df["Count"].to_list(), "Peaks_Pos":[], "Peaks_Height":[], "Peaks_Id":[]}        
    
    Full_Dataset[f'{SN_Query}'] = Dataset
    return Full_Dataset

@app.route('/plot', methods=['POST'])   
def plot():
    Plot_Query = request.get_json()
    data = Plot_Query["File"]
    sn = Plot_Query["SN"]
    data_path = f'{DEFAULT_PATH}\{sn}\{data}'    
    df = pd.read_csv(data_path, header=2, sep="\t")    
    df.columns = ["Angle","Count"]
    
    return {"SN":sn, "File": data, "Angle":df["Angle"].to_list(), "Count":df["Count"].to_list(), "Peaks":[]}

@app.route('/calc', methods=['POST'])   
def calc():
    calc_query = request.get_json()
    SN_Query = calc_query["SN"]        
    Year_Query = calc_query["YEAR"]        
    Month_Query = calc_query["MONTH"]        
    file_list = calc_query["File"]
    peak_pos = calc_query["Peaks_Pos"]
    peak_height = calc_query["Peaks_Height"]
    peak_id = calc_query["Peaks_Id"]
    
    Err_Return = ''
    for i in range(len(peak_id)):        
        if len(np.array(peak_id)[i][np.array(peak_id)[i]==True])<3:
            Err_Return += f'{file_list[i]} : Peak Count {len(np.array(peak_id)[i][np.array(peak_id)[i]==True])}'
        
    if Err_Return != "":
        return Err_Return 
    
    result = grain_size(SN_Query, Year_Query, Month_Query, file_list, peak_pos, peak_height, peak_id)
    result.to_csv(f'{DEFAULT_PATH}\{Year_Query}\{Month_Query}\{SN_Query}\Result\Grain_Size.csv',index=False)
    return "Grain Size 계산 완료" 
    
app.run(host="10.138.126.181")
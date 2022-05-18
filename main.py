from flask import Flask, request, render_template
#import modules.inxrd_noqt, modules.outxrd_noqt
import os
import re
import pandas as pd
from modules.calc import grain_size

YEAR = 2022
MONTH = 5
DEFAULT_PATH = rf"\\10.138.112.112\Analysis Results\XRD\1_XRD\{YEAR}\{MONTH:02}"
app = Flask("XRD Grain Size")

@app.route('/')
def root(SN_List = None):    
    SN_List = os.listdir(DEFAULT_PATH)        
    return render_template('index.html', SN_List=SN_List)

@app.route('/submit', methods=['POST'])
def login(File_List = None):
    SN_Query = request.get_json()["SN"]    
    File_List = os.listdir(f'{DEFAULT_PATH}\{SN_Query}')
    File_List = [x for x in File_List if ".txt" in x or ".TXT" in x]    
    Full_Dataset = {}
    Dataset = {}
    for file in File_List:
        data_path = f'{DEFAULT_PATH}\{SN_Query}\{file}'    
        df = pd.read_csv(data_path, header=2, sep="\t")    
        df.columns = ["Angle","Count"]
        Dataset[file] = {"Angle":df["Angle"].to_list(), "Count":df["Count"].to_list(), "Peaks_Pos":[], "Peaks_Height":[]}        
    
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
    sn = calc_query["SN"]        
    file_list = calc_query["File"]
    peak_pos = calc_query["Peaks_Pos"]
    peak_height = calc_query["Peaks_Height"]    
        
    result = {}
    for idx in range(len(file_list)):        
        result[f'{file_list[idx]}'] = grain_size(sn, file_list[idx], peak_pos[idx], peak_height[idx])
    
    df_result = pd.DataFrame(columns=["File","FWHM","Grain Size","Peak"])
    
    for key in result.keys():
        
        df = pd.DataFrame(result[key])
        df["File"] = key
        df = df[["File","FWHM","Grain Size","Peak"]]
        df_result = pd.concat([df_result,df])
    
    #df_result.to_csv(f'{DEFAULT_PATH}\{SN_Query})
    return "Done"
    
app.run(host="10.138.126.181")
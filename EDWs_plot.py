## import library
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import xlsxwriter
from io import BytesIO



# with open('template/style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def read_EDWs_data_csv(path1_input):
    df = pd.read_csv(path1_input)
    df.fillna('', inplace=True)
    for i in range(1, df.shape[0]):
        for j in range(1, df.shape[1]):
            if df.iloc[i,j].isnumeric()==True:
                df.iloc[i,j] = df.iloc[i,j].astype(float)

    df1 = df.iloc[:,:3]
    df2 = df.iloc[:,4:]

    for i in (df2.columns.to_list()):
        if 'Unnamed' in i:
            df2 = df2.drop(i, axis=1)
    df = pd.concat([df1, df2], axis=1)
    return df

def define_sheet_name(df, load_symbol):   
    load_id = []
    count = 0
    for i in range(df.shape[0]):
        loadi = df.iloc[i, 0]
        if load_symbol in loadi:
            load_id.append(int(i)+2)
    
    x = '=(main_plots!$A$'
    y_extreme = '=(main_plots!$B$'
    y_EDWs = '=(main_plots!$C$'
    for idi in load_id:
        if count!=(len(load_id)-1):
            x += str(idi)+',main_plots!$A$'
            y_extreme += str(idi)+',main_plots!$B$'
            y_EDWs += str(idi)+',main_plots!$C$'
            
        else:
            x += str(idi)+')'
            y_extreme += str(idi)+')'
            y_EDWs += str(idi)+')'
        count+=1
    return x, y_extreme, y_EDWs


def plot_envelop(x, y_extreme, y_EDWs):
    chart = workbook.add_chart({'type':'scatter', 'subtype':'straight_with_markers'})
    chart.add_series({'categories':x, 'values':y_extreme,'name':'Extreme',
                      'line':   {'color': 'blue'},
                       'marker': {'type': 'square','size,': 1,'border': {'color': 'blue'},
                                  'fill':   {'color': 'yellow'}}})
    chart.add_series({'categories':x, 'values':y_EDWs,'name':'EDWs-maxAmp',
                      'line':   {'none': True},
                       'marker': {'type': 'circle','size,': 3,'border': {'color': 'red'},
                                  'fill':   {'color': 'red'}}})

    chart.set_plotarea({
        'layout': {
            'x':      0.3,
            'y':      0.15,
            'width':  0.8,
            'height': 0.7,
        }
    })
    chart.set_legend({
        'layout': {
            'x':      0.70,
            'y':      0.12,
            'width':  0.3,
            'height': 0.25,
        }
    })
    return chart


def plot_envelop0(key_word, chart_loc,no_of_x_loc, worksheet):
    x, y_extreme, y_EDWs = define_sheet_name(df, key_word)
    chart = plot_envelop(x, y_extreme, y_EDWs)
    # Add a chart title and some axis labels. 
    chart.set_title({ 'name': key_word})
    chart.set_x_axis({'name': 'x/L*'+str(no_of_x_loc)+'+1'})
    chart.set_y_axis({'name': 'Response'})
    worksheet.insert_chart(chart_loc,chart)
    chart_loc = chart_loc[0]+str(int(chart_loc[1:])+16)
    return chart_loc


def plot_envelop_Ver_Ac(y_loc_list, key_word, chart_loc, worksheet):
    ## key_word = vcg or deck
    load_ids = []
    x_loc = []
    y_loc = []
    for i in range(df.shape[0]):
        loadi = df.iloc[i, 0]
        if ('Ver_Ac' in loadi) & (key_word in loadi):
            load_ids.append(i)
            x_loc.append(loadi[7:11])
            y_loc.append(loadi[13:17])

    locs = {'x_loc': x_loc, 'y_loc': y_loc, 'load_ids': load_ids}

    df_Ver_Ac = pd.DataFrame(locs)        
    for i in y_loc_list:
        idx = df_Ver_Ac.loc[df_Ver_Ac['y_loc'].astype(float)==i,'load_ids'] + 2

        x = '=(main_plots!$A$'
        y_extreme = '=(main_plots!$B$'
        y_EDWs = '=(main_plots!$C$'

        count = 0
        for idi in idx:
            if count!=(len(idx)-1):
                x += str(idi)+',main_plots!$A$'
                y_extreme += str(idi)+',main_plots!$B$'
                y_EDWs += str(idi)+',main_plots!$C$'

            else:
                x += str(idi)+')'
                y_extreme += str(idi)+')'
                y_EDWs += str(idi)+')'
            count+=1
        ### plot chart
        chart = plot_envelop(x, y_extreme, y_EDWs)
        # Add a chart title and some axis labels.
        chart_name = 'Ver_Ac'+'@y='+str(i)+'B,z='+key_word
        chart.set_title({ 'name': chart_name})
        chart.set_x_axis({'name': 'x/L*10+1'})
        chart.set_y_axis({'name': 'Response'})
        worksheet.insert_chart(chart_loc,chart)
        
        chart_loc = chart_loc[0]+str(int(chart_loc[1:])+16)
    return chart_loc


def plot_envelop_Lon_Ac(y_loc_list, z_loc_list, chart_loc, worksheet):
    chart_loc0 = chart_loc[0]+str(int(chart_loc[1:])+16)
    ## key_word = vcg or deck
    load_ids = []
    y_loc = []
    z_loc = []
    for i in range(df.shape[0]):
        loadi = df.iloc[i, 0]
        if ('Lon_Ac' in loadi):
            load_ids.append(i)
            y_loc.append(loadi[7:11])
            z_loc.append(loadi[13:17])

    locs = {'y_loc': y_loc, 'z_loc': z_loc, 'load_ids': load_ids}

    df_Ver_Ac = pd.DataFrame(locs)
    chart_locy = ['F', 'N', 'V', 'AD', 'AG']
    count0 = 0
    for i in y_loc_list:
        idx = df_Ver_Ac.loc[df_Ver_Ac['y_loc'].astype(float)==i,'load_ids'] + 2

        x = '=(main_plots!$A$'
        y_extreme = '=(main_plots!$B$'
        y_EDWs = '=(main_plots!$C$'

        count = 0
        for idi in idx:
            if count!=(len(idx)-1):
                x += str(idi)+',main_plots!$A$'
                y_extreme += str(idi)+',main_plots!$B$'
                y_EDWs += str(idi)+',main_plots!$C$'

            else:
                x += str(idi)+')'
                y_extreme += str(idi)+')'
                y_EDWs += str(idi)+')'
            count+=1
        ### plot chart
        chart = plot_envelop(x, y_extreme, y_EDWs)
        # Add a chart title and some axis labels.
        chart_name = 'Lon_Ac'+'@y='+str(i)+'B'
        chart.set_title({ 'name': chart_name})
        chart.set_x_axis({'name': 'x/L*10+1'})
        chart.set_y_axis({'name': 'Response'})
        worksheet.insert_chart(chart_loc,chart)
        
        chart_loc = chart_locy[count0]+str(int(chart_loc0[1:]))
        count0+=1
    chart_loc0 = chart_loc0[0]+str(int(chart_loc[1:])+16)
    return chart_loc0


def plot_envelop_Tran_Ac(z_loc_list, chart_loc, worksheet):
    load_ids = []
    x_loc = []
    z_loc = []
    for i in range(df.shape[0]):
        loadi = df.iloc[i, 0]
        if ('Tran_Ac' in loadi):
            load_ids.append(i)
            x_loc.append(loadi[8:12])
            z_loc.append(loadi[14:18])

    locs = {'x_loc': x_loc, 'z_loc': z_loc, 'load_ids': load_ids}

    df_Ver_Ac = pd.DataFrame(locs)        
    for i in z_loc_list:
        idx = df_Ver_Ac.loc[df_Ver_Ac['z_loc'].astype(float)==i,'load_ids'] + 2

        x = '=(main_plots!$A$'
        y_extreme = '=(main_plots!$B$'
        y_EDWs = '=(main_plots!$C$'

        count = 0
        for idi in idx:
            if count!=(len(idx)-1):
                x += str(idi)+',main_plots!$A$'
                y_extreme += str(idi)+',main_plots!$B$'
                y_EDWs += str(idi)+',main_plots!$C$'

            else:
                x += str(idi)+')'
                y_extreme += str(idi)+')'
                y_EDWs += str(idi)+')'
            count+=1
        ### plot chart
        chart = plot_envelop(x, y_extreme, y_EDWs)
        # Add a chart title and some axis labels.
        chart_name = 'Ver_Ac'+'@z='+str(i)+'D'
        chart.set_title({ 'name': chart_name})
        chart.set_x_axis({'name': 'x/L*10+1'})
        chart.set_y_axis({'name': 'Response'})
        worksheet.insert_chart(chart_loc,chart)
        
        chart_loc = chart_loc[0]+str(int(chart_loc[1:])+16)        
    return chart_loc

st.markdown(
  """
  <h1>RBA - EDWs Plot</h3>
  """
, unsafe_allow_html=True)


st.markdown(
  """
  <h3>How to use:</h3>
  
  <li>Define path to save the xlsx file containing EDW plots.</li>
  <li>Define file name. The file name should be in the format such as: file_name.xlsx </li>
  <li>Upload CSV file for EDWs summary.</li><br><br>

  <h3>Start auto-ploting EDWs</h3>
  """
, unsafe_allow_html=True)

# save_path0 = st.text_input('Step 1: Define path to save file', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)
# file_name = st.text_input('Step 2: Define file name', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False)
# path1_output = f"{save_path0}\{file_name}"

uploaded_file = st.file_uploader('Step 3: Upload CSV file for EDWs Summary Data', type=None, accept_multiple_files=False, disabled=False)

if uploaded_file is not None:
  df = read_EDWs_data_csv(uploaded_file)
  # if (save_path0 is not None) & (file_name is not None):
  output = BytesIO()

  alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

  workbook = xlsxwriter.Workbook(output, {'strings_to_numbers': True, 'in_memory': True})
  ### write sheet1: DB for database
  worksheet1 = workbook.add_worksheet('DB')

  for i, col_name in enumerate(df.columns):
      worksheet1.write(0, i, col_name)
      worksheet1.write_column(1, i, df[col_name])

  ##### sheet 2: main_plots for functions and plots
  worksheet2 = workbook.add_worksheet('main_plots')

  for i, col_name in enumerate(df.columns):
      worksheet2.write(0, i, col_name)
      worksheet2.write_column(1, i, df[col_name])

  ### function for Max Amplitude column B
  for i in range(8, df.shape[0]):
      col_max_amp = '$C$'+str(i+1)
      col_extr = '$B$'+str(i+1)

      max_amp_func = '=MAX(' + col_extr +'*$E$'+str(i+1)+':'

      j = df.shape[1]-1
      n_alphabet = j//len(alphabet)
      alphabeti = alphabet[j%len(alphabet)]
      if n_alphabet==0:
          end_col = '$'+ alphabeti + '&' + str(i+1)
      else:
          end_col = '$'+ alphabet[n_alphabet-1] + alphabeti + '$' + str(i+1)

      max_amp_func+= end_col + ')'

      worksheet2.write_array_formula(col_max_amp, max_amp_func)
      worksheet2.ignore_errors({'formula_range':col_max_amp})

  ### Amp/Extr as a function of wave amplitude
  for j in range(3, df.shape[1]):
      n_alphabet = j//len(alphabet)
      alphabeti = alphabet[j%len(alphabet)]
      if n_alphabet==0:
          col0 = alphabeti
      else:
          col0 = alphabet[n_alphabet-1] + alphabeti

      for i in range(8, df.shape[0]):
          coli = col0+str(i+1)
          func = '=DB!$' + col0 + '$'+ str(i+1)+'/DB!$'+col0+'$6*main_plots!$'+col0+'$6'
          worksheet2.write_array_formula(coli, func)

  ### Create graphs
  ### torion chart
  chart_loc = plot_envelop0('TOR', 'F9', 20, worksheet2)

  ### VBM chart
  chart_loc = plot_envelop0('VBM', chart_loc, 20, worksheet2)

  ### HBM chart
  chart_loc = plot_envelop0('HBM', chart_loc, 20, worksheet2)

  # ### HSF chart
  chart_loc = plot_envelop0('HSF', chart_loc, 20, worksheet2)

  # ### VSF chart
  chart_loc = plot_envelop0('VSF', chart_loc, 20, worksheet2)

  #### Ver_Ac_xxL_xxB_vcg
  y_loc_list = [0.0, 0.25, 0.50]
  chart_loc =  plot_envelop_Ver_Ac(y_loc_list, 'vcg', chart_loc, worksheet2)
  #### Ver_Ac_xxL_xxB_deck
  chart_loc =  plot_envelop_Ver_Ac(y_loc_list, 'deck', chart_loc, worksheet2)

  #### Lon_Ac_xxB_xxD
  y_loc_list = [0.00, 0.25, 0.50]
  z_loc_list = [0.00, 0.25, 0.50, 0.75, 1.00]
  chart_loc = plot_envelop_Lon_Ac(y_loc_list, z_loc_list, chart_loc, worksheet2)  

  #### Tran_Ac_xxL_xxD
  z_loc_list = [0.00, 0.25, 0.50, 0.75, 1.00]
  chart_loc = plot_envelop_Tran_Ac(z_loc_list, chart_loc, worksheet2)

  ### Bilge pressure chart
  chart_loc = plot_envelop0('Bilge', chart_loc, 10, worksheet2)

  ### Bottom pressure chart
  chart_loc = plot_envelop0('Bottom', chart_loc, 10, worksheet2)

  workbook.close()

  st.download_button(
    label="Download Excel File",
    data=output.getvalue(),
    file_name="EDW_plot.xlsx",
    mime="application/vnd.ms-excel"
  )

  # else:
  #   st.warning('Please define file path and file name.')

else:
  st.warning('Please upload csv files.')


st.info('Library used: streamlit, numpy, plotly, pandas, xlsxwriter. Author: Cong Nguyen')
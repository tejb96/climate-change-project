import pandas as pd
def parse_user_input():
    '''Stage 3'''
    pass

def dataframe_creation():
    '''Stage 1 and 2'''

    # For Temperature Data: 
    temp_data2 = pd.read_csv("Annual_Surface_Temperature_Change.csv", usecols = [1, 2, 3, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                                                51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                                                61, 62, 63, 64, 65, 66, 67, 68, 69])
    temp_data = temp_data2.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Temp')
    # print(temp_data)

    # For Land Data:
    land_data2 = pd.read_csv("Land_Cover_Accounts.csv", usecols = [1, 2, 3, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                                              21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                                                              31, 32, 33, 34, 35, 36, 37, 38, 39])

    land_data3 = land_data2.iloc[16:244,:]
    land_data = land_data3.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Land_Cover_Index')
    # print(land_data)

    # For Disaster Data:
    p = pd.read_csv("Climate-related_Disasters_Frequency.csv", usecols = [1, 2, 3, 4, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                                                                                  31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                                                                                  41, 42, 43, 44, 45, 46, 47, 48, 49, 50])

    dis_tot = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: TOTAL']
    dis_tot = dis_tot.drop('Indicator', axis = 1)
    d_total = dis_tot.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Total Disaster')

    dis_temp = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Extreme temperature']
    dis_temp = dis_temp.drop('Indicator', axis = 1)
    d_temp = dis_temp.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Extreme Temperature')

    dis_wildfire = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Wildfire']
    dis_wildfire = dis_wildfire.drop('Indicator', axis = 1)
    d_wildfire = dis_wildfire.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Wildfire')

    dis_drought = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Drought']
    dis_drought = dis_drought.drop('Indicator', axis = 1)
    d_drought = dis_drought.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Drought')

    dis_flood = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Flood']
    dis_flood = dis_flood.drop('Indicator', axis = 1)
    d_flood = dis_flood.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Flood')

    dis1 = pd.merge(d_temp, d_wildfire, on = ['Country', 'ISO2', 'ISO3', 'Year'], how = 'outer')
    dis2 = pd.merge(d_drought, d_flood, on = ['Country', 'ISO2', 'ISO3', 'Year'], how = 'outer')
    dis3 = pd.merge(dis1, dis2, on = ['Country', 'ISO2', 'ISO3', 'Year'], how = 'outer')
    disaster_data = pd.merge(dis3, d_total, on = ['Country', 'ISO2', 'ISO3', 'Year'], how = 'outer')

    # print(disaster_data)
    
    # TODO: merge temp_data, land_data, and disaster_data (preferably with years as columns)
    
    df1 = pd.merge(temp_data, land_data, on=['Country', 'ISO2', 'ISO3', 'Year'], how='inner')
    climate_data = pd.merge(df1, disaster_data, on=['Country', 'ISO2', 'ISO3', 'Year'], how='inner')

    print(climate_data) # [5771 Rows X 11 Columns]

def analysis_calculation():
    '''Stage 4'''
    pass

def export_data():
    '''Stage 5 a'''
    pass

def plot_data():
    '''Stage 5 b'''
    pass


def main():
    print("Climate Data")


if __name__ == '__main__':
    main()

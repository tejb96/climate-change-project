import pandas as pd
def parse_user_input():
    '''Stage 3'''
    pass

def dataframe_creation():
    '''Stage 1 and 2'''

    # Please ignore the variable names for now. I was just trying out things quicker. 

    # For Temperature Data: 
    x = pd.read_csv("Annual_Surface_Temperature_Change.csv", usecols = [1, 2, 3, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                                                51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                                                61, 62, 63, 64, 65, 66, 67, 68, 69])
    temp_data = x.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Temp')

    # For Land Data:
    y = pd.read_csv("Land_Cover_Accounts.csv", usecols = [1, 2, 3, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                                              21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                                                              31, 32, 33, 34, 35, 36, 37, 38, 39])

    z = y.iloc[16:244,:]
    land_data = z.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Land_Cover_Index')

    # For Disaster Data:
    p = pd.read_csv("Climate-related_Disasters_Frequency.csv", usecols = [1, 2, 3, 4, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                                                                                  31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                                                                                  41, 42, 43, 44, 45, 46, 47, 48, 49, 50])
    q = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: TOTAL']
    q = q.drop('Indicator', axis = 1)
    disaster_data = q.melt(id_vars=['Country','ISO2','ISO3'], var_name='Year', value_name='Total Disaster')
    
    # TODO: merge temp_data, land_data, and disaster_data (preferably with years as columns)
    


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

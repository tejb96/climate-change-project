import sys
import pandas as pd
import matplotlib.pyplot as plt 


def create_dataframe():
    '''Stage 1 and 2'''

    # For Temperature Data: 
    # The excel sheet containing the Annual Surface Temperature Change is read & manipulated to create a temperature change dataset. 
    temp_data1 = pd.read_csv("Annual_Surface_Temperature_Change.csv", usecols = [3, 1, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                                                51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                                                61, 62, 63, 64, 65, 66, 67, 68, 69])
    temp_data = temp_data1.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Temperature Change')
    
    # For Land Data:
    # The excel sheet containing the Land Cover Accounts is read & manipulated to create a land cover index dataset.
    land_data1 = pd.read_csv("Land_Cover_Accounts.csv", usecols = [3, 1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                                              21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                                                              31, 32, 33, 34, 35, 36, 37, 38, 39])

    land_data2 = land_data1.iloc[16:244,:]
    land_data = land_data2.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Land Cover Index')

    # For Disaster Data:
    # The excel sheet containing the Climate-related disaster frequency is read & manipulated to create a disaster dataset.
    p = pd.read_csv("Climate-related_Disasters_Frequency.csv", usecols = [3, 1, 4, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                                                                                  31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 
                                                                                  41, 42, 43, 44, 45, 46, 47, 48, 49, 50])

    dis_tot = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: TOTAL']
    dis_tot = dis_tot.drop('Indicator', axis = 1)
    d_total = dis_tot.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Total Disasters')

    dis_temp = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Extreme temperatures']
    dis_temp = dis_temp.drop('Indicator', axis = 1)
    d_temp = dis_temp.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Extreme Temperature')

    dis_wildfire = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Wildfires']
    dis_wildfire = dis_wildfire.drop('Indicator', axis = 1)
    d_wildfire = dis_wildfire.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Wildfires')

    dis_storm = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Storm']
    dis_storm = dis_storm.drop('Indicator', axis = 1)
    d_storm = dis_storm.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Storms')

    dis_landslide = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Landslide']
    dis_landslide = dis_landslide.drop('Indicator', axis = 1)
    d_landslide = dis_landslide.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Landslides')

    dis_drought = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Drought']
    dis_drought = dis_drought.drop('Indicator', axis = 1)
    d_drought = dis_drought.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Droughts')

    dis_flood = p.loc[p['Indicator'] == 'Climate related disasters frequency, Number of Disasters: Flood']
    dis_flood = dis_flood.drop('Indicator', axis = 1)
    d_flood = dis_flood.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Floods')

    # All the above sub datasets of disaster are joined to create a dataset of disasters. 
    dis1 = pd.merge(d_temp, d_wildfire, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis2 = pd.merge(d_storm, d_landslide, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis3 = pd.merge(d_drought, d_flood, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis4 = pd.merge(dis1, dis2, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis5 = pd.merge(dis4, dis3, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    disaster_data = pd.merge(dis5, d_total, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    
    # Merge operation is used to join the temperature dataset with the Land cover index dataset, 
    # and eventually with the disaster dataset. 
    # Climate data is the combined dataset containing [5771 rows X 12 columns]    
    df1 = pd.merge(temp_data, land_data, on=['ISO3', 'Country', 'Year'], how='inner')
    climate_data = pd.merge(df1, disaster_data, on=['ISO3', 'Country', 'Year'], how='inner')
    return climate_data


def analysis_part_1(climate_data):
    # Adding Column 1 of Fractional Total Disasters to the combined dataset of Climate Data. 
    total_disasters_yearly = climate_data.groupby('Year')['Total Disasters'].sum()
    country_yearly_disasters = climate_data.groupby(['ISO3', 'Country', 'Year'])['Total Disasters'].sum()
    fractional = (country_yearly_disasters.truediv(total_disasters_yearly, fill_value=0)) * 100
    combined1 = climate_data.merge(fractional, on = ['ISO3', 'Country', 'Year'])
    # print(combined1)
    
    # Adding Column 2 of Fractional land cover index to the combined dataset above. 
    land_cover_index_yearly = climate_data.groupby('Year')['Land Cover Index'].sum()
    country_yearly_land_cover_index = climate_data.groupby(['ISO3', 'Country', 'Year'])['Land Cover Index'].sum()
    fractional_land_cover_index = (country_yearly_land_cover_index.truediv(land_cover_index_yearly, fill_value=0)) * 100
    combined2 = combined1.merge(fractional_land_cover_index, on = ['ISO3', 'Country', 'Year'])
    # print(combined2)
    
    # Using a masking operation on a subset of the data
    more_disaster_countries = country_yearly_disasters[(country_yearly_disasters > 4.0)]
    high_disaster_countries = " ".join([str(country) for country in more_disaster_countries.index])
    # print(high_disaster_countries)
    
    # Indexed and sorted the combined dataset 
    climate_data_indexed = climate_data.set_index(['ISO3', 'Country', 'Year'])
    climate_data_indexed_sorted = climate_data_indexed.sort_index()
    return climate_data_indexed_sorted


def analysis_calculation(df, iso3_1, iso3_2, country_name, param):
    '''Stage 4'''


    # Used the describe method to print the aggregate stats for the entire dataset. 
    agg_stats = df.dropna().describe()
    # print(agg_stats)

    #......................Depends on user input.................................
    # Accessing a particular Country's Stats from the sorted dataset 
    country_stats = df.loc[iso3_1]
    stats = country_stats.mean()
    # print(stats) # Display the stats for the user to view 

    # For the second country choice used for comparison 
    comparison_country_stats = df.loc[iso3_2]
    two_country_stats = pd.concat([country_stats, comparison_country_stats])
    # print(two_country_stats)

    # Creation and printing of a pivot table 
    comparison_stats = two_country_stats.pivot_table(param, index='Year', columns = 'Country')
    # print(comparison_stats)
    
    # Used the groupby operation and aggregation computation for a subset of the data 
    each_country_yearly_temp = df.groupby(['Country', 'Year'])[param].sum()
    # print(each_country_yearly_temp)

    each_country_temp = each_country_yearly_temp[country_name]
    # print(each_country_temp)

    # Used an aggregation computation for a subset of the data. 
    each_country_temp_stats = each_country_temp.dropna().describe()
    # print(each_country_temp_stats)
    return comparison_stats

    


def export_data():
    '''Stage 5 a'''
    pass

def plot_data(comparison_stats, param, iso3_1, iso3_2):
    '''Stage 5 b'''
    
    ax = comparison_stats.plot.bar()
    ax.set_title(f"{param} comparison for 2 countries")
    ax.set_ylabel(f"{param}")
    ax.set_xlabel('Year')
    ax.legend([iso3_1, iso3_2])
    plt.show()

def is_valid_iso3(country, valid_iso3_list):
    return country in valid_iso3_list

def get_country_name_from_iso3(iso3_code, countries):
    return countries.get(iso3_code)


def get_valid_country_input_by_iso3(valid_iso3_list):
    '''Get ISO 3 code for country from user'''
    while True:
        try:
            country = input("Please enter the ISO 3 code of the country or enter 'exit' to exit the program: ")
            if country == "exit":
                sys.exit()
            elif is_valid_iso3(country, valid_iso3_list):
                return country
            else:
                raise ValueError("Invalid ISO 3 code.")
        except ValueError:
            print("The ISO 3 code was not valid. Please try again.")
            continue

def get_valid_parameter_input(valid_params):
    '''Get parameter from user'''
    while True:
        try:
            parameter_table = "\n".join([f"{k}: {v}" for k, v in valid_params.items()])
            param = input(f"Please enter the code for the parameter you want to choose from the list below or enter 'exit' to exit the program\n{parameter_table}\n")
            if param == "exit":
                sys.exit()
            if param.isdigit() and int(param) in valid_params.keys():
                return int(param)
            else:
                raise ValueError("Invalid parameter code.")
        except ValueError:
            print("The parameter you entered was not valid. Please try again.")
            continue


def get_iso3_countries_dict_from_df(climate_data):
    '''Get a dictionary of ISO 3 codes to Country Names'''
    df = climate_data.set_index(['ISO3'])
    unique_iso3_country_df = df.filter(items=['ISO3', 'Country']).drop_duplicates()
    return { i:row['Country'] for i, row in unique_iso3_country_df.iterrows() }


def main():
    print("Climate Data")
    
    # Create data frame
    climate_data = create_dataframe()
    
    # Create {ISO 3 Code: Country Name} dictionary to validate user input
    iso3_country_dict = get_iso3_countries_dict_from_df(climate_data)
    valid_iso3_list = iso3_country_dict.keys()
    
    # Create parameter dict to validate user input
    valid_params = {0: "Temperature Change", 1: "Land Cover Index", 3: "Total Disasters"}
    
    # Get the ISO 3 codes for the two countries from the user
    iso3_1 = get_valid_country_input_by_iso3(valid_iso3_list)
    country_1 = get_country_name_from_iso3(iso3_1, iso3_country_dict)
    print("Now pick a second country to compare with the first country.")
    iso3_2 = get_valid_country_input_by_iso3(valid_iso3_list)
    country_2 = get_country_name_from_iso3(iso3_2, iso3_country_dict)
    print(f"You chose the countries {country_1} and {country_2}")
    
    # Get the parameter that the user wants to compare
    print("Please select the parameter you want to compare from the list.")
    param = get_valid_parameter_input(valid_params)
    print(f"You picked paramter {valid_params[param]} to compare the two countries.")

    # analysis and calculation
    df1 = analysis_part_1(climate_data)
    comparison_stats = analysis_calculation(df1, iso3_1, iso3_2, country_1, valid_params[param])
    print(comparison_stats)

    # plot data
    plot_data(comparison_stats, valid_params[param], iso3_1, iso3_2)



if __name__ == '__main__':
    main()

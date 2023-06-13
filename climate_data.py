# climate_data.py
# AUTHORS: SOUMINI MOHANDAS and TEJPREET BAL
# The code was implemented by both the authors 
# A terminal-based application for computing and printing statistics based on given input.

import sys
import pandas as pd
import matplotlib.pyplot as plt 


def create_dataframe():
    """
    This function reads in 3 .csv files 
    3 separate .csv files were used to create this Climate Data dataset. 
    The 3 .csv files are: Annual Surface Temperature Change, Land Cover Accounts, and Climate related disasters frequency. 
    Returns
    -------
    a merged dataframe 
    """

    # For Temperature Data: 
    # The excel sheet containing the Annual Surface Temperature Change is read & manipulated to create a temperature change dataset. 
    temp_data_1 = pd.read_csv("Annual_Surface_Temperature_Change.csv", usecols = [3, 1, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 
                                                51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 
                                                61, 62, 63, 64, 65, 66, 67, 68, 69])
    temp_data = temp_data_1.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Temperature Change')
    
    # For Land Data:
    # The excel sheet containing the Land Cover Accounts is read & manipulated to create a land cover index dataset.
    land_data_1 = pd.read_csv("Land_Cover_Accounts.csv", usecols = [3, 1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                                              21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 
                                                              31, 32, 33, 34, 35, 36, 37, 38, 39])

    land_data_2 = land_data_1.iloc[16:244,:]
    land_data = land_data_2.melt(id_vars=['ISO3', 'Country'], var_name='Year', value_name='Land Cover Index')

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
    dis_1 = pd.merge(d_temp, d_wildfire, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis_2 = pd.merge(d_storm, d_landslide, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis_3 = pd.merge(d_drought, d_flood, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis_4 = pd.merge(dis_1, dis_2, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    dis_5 = pd.merge(dis_4, dis_3, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    disaster_data = pd.merge(dis_5, d_total, on = ['ISO3', 'Country', 'Year'], how = 'outer')
    
    # Merge operation is used to join the temperature dataset with the Land cover index dataset, 
    # and eventually with the disaster dataset. 
    # Climate data is the combined dataset containing [5771 rows X 12 columns]    
    df_1 = pd.merge(temp_data, land_data, on=['ISO3', 'Country', 'Year'], how='inner')
    climate_data = pd.merge(df_1, disaster_data, on=['ISO3', 'Country', 'Year'], how='inner')
    return climate_data

def masking_operation_subset_1(climate_data):
    """
    This function performs a pandas grouping operation
    Parameter
    ---------
    climate_data: dataframe 
    Returns
    -------
    a subset of the climate_data dataframe
    """
    total_disasters_yearly = climate_data.groupby('Year')['Total Disasters'].sum()
    return total_disasters_yearly

def masking_operation_subset_2(climate_data):
    """
    This function performs a pandas grouping operation 
    Parameter
    ---------
    climate_data: dataframe
    Returns
    -------
    a subset of the climate_data dataframe
    """
    country_yearly_disasters = climate_data.groupby(['ISO3', 'Country', 'Year'])['Total Disasters'].sum()
    return country_yearly_disasters
    
def analysis_part_1(climate_data, country_yearly_disasters, total_disasters_yearly):
    """
    This function performs a true division, groupby operation, hierarchical indexing and sorting 
    Parameters
    ----------
    climate_data: dataframe
    country_yearly_disasters: a subset of the dataframe
    total_disasters_yearly: a subset of the dataframe
    Returns
    -------
    climate_data:
        A hierarchically indexed and sorted dataframe 
    """
    # Adding a column of Fractional Total Disasters to the combined dataset of Climate Data. 
    fractional_total_disasters = (country_yearly_disasters.truediv(total_disasters_yearly, fill_value=0)) * 100
    combined_1 = climate_data.merge(fractional_total_disasters, on = ['ISO3', 'Country', 'Year'])
       
    # Adding another column of Fractional land cover index to the combined dataset above. 
    land_cover_index_yearly = climate_data.groupby('Year')['Land Cover Index'].sum()
    country_yearly_land_cover_index = climate_data.groupby(['ISO3', 'Country', 'Year'])['Land Cover Index'].sum()
    fractional_land_cover_index = (country_yearly_land_cover_index.truediv(land_cover_index_yearly, fill_value=0)) * 100
    combined_2 = combined_1.merge(fractional_land_cover_index, on = ['ISO3', 'Country', 'Year'])
    
    # The newly computed columns are assigned a column name
    combined_2.columns = ['ISO3', 'Country', 'Year', 'Temperature Change', 'Land Cover Index', 'Extreme Temperature', 'Wildfires', 
                     'Storms', 'Landslides', 'Droughts', 'Floods', 'Total Disasters', 'Fractional Total Disaster', 
                     'Fractional Land Cover Index']
    climate_data = combined_2

    # Indexed and sorted the combined dataset 
    # A hierarchical indexing is created 
    climate_data = climate_data.set_index(['ISO3', 'Country', 'Year'])
    climate_data = climate_data.sort_index()
    return climate_data

def export_data(climate_data):
    """
    This function exports the dataframe
    Parameter
    ---------
    climate_data: A hierarchically indexed and sorted: dataframe
    Returns
    -------
    ClimateDataExport.xlsx: 
        Excel file of the hierarchically indexed and sorted dataframe exported into the working directory 
    """
    climate_data.to_excel("ClimateDataExport.xlsx", index=True, header=True)

def masking_operation(country_yearly_disasters):
    """
    This function performs a masking operation fullfilling a certain condition (countries that experienced more than 20 disasters per year)
    Parameter
    ---------
    country_yearly_disasters: a subset of the dataframe
    Returns
    -------
    high_disaster_countries: 
        a tuple containing the ISO3 code, country name and the year 
    """
    more_disaster_countries = country_yearly_disasters[(country_yearly_disasters > 20.0)]
    high_disaster_countries = "\n".join([str(country) for country in more_disaster_countries.index])
    return high_disaster_countries

def overall_agg_stats(df):
    """
    This function evaluates the aggregate stats on the entire dataset using the pandas describe() method 
    Parameter
    ---------
    df: dataframe
    Returns
    -------
    agg_stats:
        the aggregate stats which includes the count, mean, std, min, 25%, 50%, 75% and max across the entire dataset 
    """
    agg_stats = df.dropna().describe()
    return agg_stats

def choice_country_1(df, iso3_1):
    """
    This function indexes the user's first country of choice
    Parameter
    ---------
    df: dataframe
    iso_1: ISO3 code of the user's first country of choice
    Returns
    -------
    country_stats:
    only the row values of that country from the dataframe
    """
    country_stats = df.loc[iso3_1]
    return country_stats

def country_1_agg_statistics(country_stats):
    """
    This function computes the mean aggregate stats of the user's first country of choice
    Parameter
    ---------
    country_stats:
        row values of the user's first country of choice from the dataset 
    Returns
    -------
    country_1_stats:
        mean stats across all values for that particular country 
    """
    country_1_stats = country_stats.mean()
    return country_1_stats

def choice_country_2(df, iso3_2):
    """
    This function indexes the user's second country of choice
    Parameter
    ---------
    df: dataframe
    iso3_2: ISO3 code of the user's second country of choice
    Returns
    -------
    comparison_country_stats:
        only the row values of that country from the dataframe
    """
    comparison_country_stats = df.loc[iso3_2]
    return comparison_country_stats

def country_2_agg_statistics(comparison_country_stats):
    """
    This function computes the mean aggregate stats of the user's second country of choice
    Parameter
    ---------
    comparison_country_stats:
        row values of the user's second country of choice from the dataset 
    Returns
    -------
    country_2_stats:
        mean stats across all values for that particular country 
    """
    country_2_stats = comparison_country_stats.mean()
    return country_2_stats 

def analysis_calculation(country_stats, comparison_country_stats, param):
    """
    This function concatenates or merges and creates a pivot table based on a climate change indicator or parameter
    Parameters
    ----------
    country_stats:
        First country stats: a subset of the dataframe
    comparison_country_stats:
        Second country stats: a subset of the dataframe
    param:
        a climate change indicator or parameter
    Returns
    -------
    comparison_stats:
        A pivot table of the comparison between 2 countries based on the climate change indicator or parameter
    """
    two_country_stats = pd.concat([country_stats, comparison_country_stats])
    # Creation and printing of a pivot table 
    comparison_stats = two_country_stats.pivot_table(param, index='Year', columns = 'Country')
    return comparison_stats
    
def plot_data(comparison_stats, param, iso3_1, iso3_2):
    """
    This function plots a bar graph using the matplotlib library 
    Parameters
    ----------
    comparison_stats:
        pivot table comparison dataframe
    param: 
        climate change indicator or parameter 
    iso3_1:
        ISO3 code of the user's first country
    iso3_2: 
        ISO3 code of the user's second country
    Returns
    -------
    Shows or displays a plot: 
        A bar graph showing the comparison between the 2 countries for the given climate change indicator or parameter 
    """
    ax = comparison_stats.plot.bar()
    ax.set_title(f"{param} comparison for 2 countries")
    ax.set_ylabel(f"{param}")
    ax.set_xlabel('Year')
    ax.legend([iso3_1, iso3_2])
    plt.show()

def get_valid_country_input_by_iso3(valid_iso3_list):
    """
    This function gets the ISO3 code for the country from the user
    Parameters
    ----------
    valid_iso3_list:
        List of valid ISO3 codes
    Returns
    -------
        Valid ISO3 code entered by the user
    """
    while True:
        try:
            country = input("Please enter the ISO3 code of the country (example: CAN, USA) or enter 'exit' to exit the program: ").upper()
            if country == "EXIT":
                sys.exit()
            elif country in valid_iso3_list:
                return country
            else:
                raise ValueError("Invalid ISO3 code.")
        except ValueError:
            print("The ISO3 code was not valid. Please try again.")
            continue

def get_valid_parameter_input(valid_params):
    """
    This function gets the parameter to compare the countries entered by the user
    Parameter
    ----------
    valid_params:
        Dictionary of int:string entries that represent user input and parameter name or climate change indicator 
    Returns
    -------
        Valid index for the parameter selected by the user
    """
    while True:
        try:
            parameter_table = "\n".join([f"{k}: {v}" for k, v in valid_params.items()])
            param = input(f"Please enter the code for the parameter you want to choose from the list below or enter 'exit' to exit the program\n{parameter_table}\n").upper()
            if param == "EXIT":
                sys.exit()
            if param.isdigit() and int(param) in valid_params.keys():
                return int(param)
            else:
                raise ValueError("Invalid parameter code.")
        except ValueError:
            print("The parameter you entered was not valid. Please try again.")
            continue

def get_iso3_countries_dict_from_df(climate_data):
    """
    This function creates a mapping of ISO3 codes to Country Names
    Parameter
    ----------
    climate_data:
        A dataframe of the climate data
    Returns
    -------
    A dictionary of unique ISO3:Country_name entries
    """
    df = climate_data.set_index(['ISO3'])
    unique_iso3_country_df = df.filter(items=['ISO3', 'Country']).drop_duplicates()
    return { i:row['Country'] for i, row in unique_iso3_country_df.iterrows() }


def main():
    print("ENSF592 Climate Data Statistics")
    print("Influence of climate change on various indicators for countries across several years\n")
    
    # Create data frame
    climate_data = create_dataframe()
    
    # Create {ISO3 Code: Country Name} dictionary to validate user input
    iso3_country_dict = get_iso3_countries_dict_from_df(climate_data)
    valid_iso3_list = iso3_country_dict.keys()
    
    # Create parameter dict to validate user input
    valid_params = {0: "Temperature Change", 1: "Land Cover Index", 2: "Total Disasters"}
    
    # Get the ISO3 codes for the two countries from the user
    iso3_1 = get_valid_country_input_by_iso3(valid_iso3_list)
    country_1 = iso3_country_dict.get(iso3_1)
    print("Now pick a second country to compare with the first country.")
    iso3_2 = get_valid_country_input_by_iso3(valid_iso3_list)
    while iso3_1 == iso3_2:
        print("\nYou selected the same country both times. Please pick the second country again.\n")
        iso3_2 = get_valid_country_input_by_iso3(valid_iso3_list)
    country_2 = iso3_country_dict.get(iso3_2)
    print(f"\nYou chose the countries {country_1} and {country_2}\n")

    # Aggregate stats for the 2 countries selected
    print(f"The mean aggregate statistics for the 2 countries over a period of 29 years is shown below: ")
    country_yearly_disasters = masking_operation_subset_2(climate_data)
    total_disasters_yearly = masking_operation_subset_1(climate_data)
    df = analysis_part_1(climate_data, country_yearly_disasters, total_disasters_yearly)
    country_stats = choice_country_1(df, iso3_1)
    country_1_stats = country_1_agg_statistics(country_stats)
    print(f"For {country_1}:\n{country_1_stats.to_string()}")

    comparison_country_stats = choice_country_2(df, iso3_2)
    country_2_stats = country_2_agg_statistics(comparison_country_stats)
    print(f"\nFor {country_2}:\n{country_2_stats.to_string()}")
    
    # Get the parameter that the user wants to compare
    print("\nPlease select the parameter or climate change indicator you want to compare from the list.")
    param = get_valid_parameter_input(valid_params)
    print(f"You picked the {valid_params[param]} parameter to compare the two countries.\n")

    # analysis and calculation
    comparison_stats = analysis_calculation(country_stats, comparison_country_stats, valid_params[param])
    print(f"A pivot table showing the {valid_params[param]} statistics for the 2 countries for the period from 1992 to 2020 is displayed below and a corresponding bar graph is generated as well showing the trend:\n{comparison_stats}")

    # plot data
    print("Plotting the data.")
    plot_data(comparison_stats, valid_params[param], iso3_1, iso3_2)

    # Print the aggregate stats for the entire dataset
    print("Would you be interested in knowing the aggregate statistics for the entire climate data dataset?")
    aggregate_input = input("Enter 'Y' for yes or enter any other key to skip this step and continue: ").upper()
    if aggregate_input == "Y":
        agg_stats = overall_agg_stats(df)
        print(f"\nThe aggregate stats for the entire Climate Data dataset is:\n{agg_stats}")
    # masking operation
    # TODO Uncomment this to obtain the result 
    print("Would you be interested in knowing how many countries experienced more than 20 climate-related disasters in a year?")
    high_disaster_input = input("Enter 'Y' for yes or enter any other key to skip this step and continue: ").upper()
    if high_disaster_input == "Y":
        country_yearly_disasters = masking_operation_subset_2(climate_data)
        high_disaster_countries = masking_operation(country_yearly_disasters)
        print(f"\nThe countries (along with their ISO3 codes and year) that experienced more than 20 climate-related disasters a year are:\n{high_disaster_countries}")
    # Export the entire merged, hierarchical dataset to an excel file in the working directory 
    print("Please wait. The program is exporting the dataframe to an excel file.")
    export_data(df)
    print("Exporting completed. Thank you for your patience.")
    
          

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@authors:   rivera
            Noa A.
"""
import pandas as pd # Pandas library for data frames
import yaml # Yaml library for reading yaml files
import argparse # Argparse library for getting command-line arguments
import matplotlib.pyplot as plt # Mathplotlib for generating plots


def main():

    # Code below is responsible for reading and storing
    # the input from the terminal.
    parser = argparse.ArgumentParser()

    parser.add_argument('--airlines' , '--AIRLINES=')
    parser.add_argument('--airports' , '--AIRPORTS=')
    parser.add_argument('--routes' , '--ROUTES=')
    parser.add_argument('--question' , '--QUESTION=')
    parser.add_argument('--graph' , '--GRAPH_TYPE=')

    args = parser.parse_args()


    """
    Below are lists storing information for the plots we will generate as part
    of our solution to the assignment. Each list consists of 5 strings - 
    1 - name of the output file for the plot (pdf)
    2 -name of the output file for the data (csv)
    3 - Title for the plot
    4 - Title for x-axis of bar plot
    5 - Title for y-axis of bar plot

    Finally we have a variable use_list which is used to store
    the correct list to send as an argument to the functions that 
    generate the plots. 
    """

    q1_graph_info = ['q1.pdf' , 'q1.csv' \
                ,"The Top 20 Airlines that Offer the Greatest Number of Routes with Destination Country as Canada:\n", \
                'Airline\n' , 'Number of Routes\n']

    q2_graph_info = ['q2.pdf' , 'q2.csv' \
                ,"The Top 30 Countries with Least Appearances as Destination Country on the Routes Data:\n", \
                'Country\n' , 'Number of Appearances\n']

    q3_graph_info = ['q3.pdf' , 'q3.csv' \
            ,"The Top 10 Destination Airports:\n", \
            'Airport\n' , 'Number of Appearances\n']

    q4_graph_info = ['q4.pdf' , 'q4.csv' \
            ,"The Top 15 Destination Cities:\n", \
            'City\n' , 'Number of Appearances\n']

    q5_graph_info = ['q5.pdf' , 'q5.csv' \
            ,"The Top 10 Canadian Routes with Greatest Altitude Distance:\n", \
            'Route\n' , 'Altitude Distance\n']

    use_list = []


    # We get the three data frames for all the input files:
    route_df , airport_df , airline_df = open_and_initilize(args.routes , args.airlines , args.airports)


    # Code below is responsible for callind the correct function to solve the 
    # question indicated by the user:

    if args.question == "q1":
        question_one(route_df , airline_df , airport_df)
        use_list = q1_graph_info

    elif args.question == "q2":
        question_two(route_df , airport_df)
        use_list = q2_graph_info

    elif args.question == "q3":
        question_three(route_df , airport_df)
        use_list = q3_graph_info

    elif args.question == "q4":
        question_four(route_df , airport_df)
        use_list = q4_graph_info

    else:
        question_five(route_df , airline_df , airport_df) 
        use_list = q5_graph_info


    # Code below is responsible for generating plots accroding to
    # command line arguments:
    if args.graph == "bar":
            generate_bar(use_list)
    else:
            generate_pie(use_list)

# End of main



def open_and_initilize(routes: str , airlines: str, airports: str) -> object:

    """

    Creates data frames for the data in given yaml files.

    The function reads the yaml files provided and "converts" them to
    data frames.
    
    Parameter routes: a string representing the name of the file containing
                      information about the routes. If it equals " ", then the 
                      calee does not need the information from this file in order
                      to answer the question. 
    Parameter airlines: a string representing the name of the file containing
                        information about the airlines. If it equals " ", then the 
                      calee does not need the information from this file in order
                      to answer the question. 
    Parameter airports: a string representing the name of the file containing
                        information about the airports. If it equals " ", then the 
                      calee does not need the information from this file in order
                      to answer the question. 

    returns the three data frames generated for the files. 

    """

    # Reading the file and storing info as a list
    with open(routes , 'r') as read_route:
        route = yaml.safe_load(read_route) # Different Loader!

    # "Converting" the list to a data frame using pandas
    route_df = pd.json_normalize(route , record_path=['routes'])

    with open(airlines , 'r') as read_airlines:
        lines = yaml.safe_load(read_airlines)

    airline_df = pd.json_normalize(lines , record_path=['airlines'])

    with open(airports , 'r') as read_airports:
        ports = yaml.safe_load(read_airports)

    airport_df = pd.json_normalize(ports , record_path=['airports'])


    # We need to make sure all the strings containing the name of the country are in the 
    # same format so that we can sort in alphabetical order without any special charaters
    # such as ' ' getting in the way:
    airport_df['airport_country'] = airport_df['airport_country'].apply( lambda x: x.lstrip(' ') ) 



    return route_df , airport_df , airline_df

    # End of open_and_initilize


def question_one(route_df: object , airline_df: object , airport_df: object):

    """

    Generates a csv file answering q1 of the assignment.

    The function uses the command-line input supplied by the 
    user to answer the following question: which are the top 20
    airlines that offer the greatest number of routes with destination 
    country as Canada?.
    This is done using the pandas library - merging and modifying the 
    data frames for a desired result. The desired result is then stored
    in a csv file.
    
    Parameter routes: a data frame of the input route.csv file
    Parameter airlines: a data frame of the input airlines.csv file
    Parameter airports: a data frame of the input airports.csv file

    """

    # Modifying data frames to only include columns of interest:
    airport_df.drop(columns = ['airport_name', 'airport_city' ,'airport_icao_unique_code' , 'airport_altitude'] , inplace = True)

    airline_df.drop(columns = ['airline_country'] , inplace = True)

    route_df.drop( columns = ['route_from_aiport_id'] , inplace = True)


    # Merge airport and route data to match the airline id to the dest. airport id and its country
    merged_airport_route_df = pd.merge(airport_df, route_df, left_on='airport_id' , right_on = 'route_to_airport_id',  how = 'right') 

    # Dropping unnecessary columns resulted by the merge
    merged_airport_route_df.drop(columns = ['route_to_airport_id' , 'airport_id'], inplace = True)

    # Filtering to keep only lines with dest. country as Canada:
    merged_airport_route_df= merged_airport_route_df[merged_airport_route_df['airport_country'] == 'Canada']
    
    # Merge merged_airport_route_df and airline_df to match the airline id to the airline name and code:
    merge_all_df = pd.merge(merged_airport_route_df, airline_df, left_on = 'route_airline_id' ,  right_on='airline_id' , how = 'left')
    
    
    # Get the final answer by grouping the lines with the same airline and get their size
    answer: pd.DataFrame = merge_all_df.groupby(['airline_name' , 'airline_icao_unique_code'],as_index=False).size()

    # Now sort in descending order so that the airlines with the most are at the top
    answer = answer.sort_values(by=['size', 'airline_name'], ascending=(False,True)).head(20)


    # Finally, generate the appropriate csv file for the answer:
    final_df = pd.DataFrame(columns=['subject' , 'statistic']) 
    final_df['subject']= answer['airline_name'] + ' (' + answer['airline_icao_unique_code'] + ')'
    final_df['statistic'] = answer['size']
    final_df.to_csv("q1.csv", index = False)

    # End of question_one


def question_two(route_df: object , airport_df: object):

    """

    Generates a csv file answering question 2 of the assignment.

    The function uses the command-line input supplied by the 
    user to answer the following question: What are the top 30 countries with least 
    appearances as destination country on the routes data?
    This is done using the pandas library - merging and modifying the 
    data frames for a desired result. The desired result is then stored
    in a csv file.
    
    Parameter routes: a data frame of the input route.csv file
    Parameter airports: a data frame of the input airports.csv file

    """

    # Modifying data frames to only include columns of interest:

    route_df.drop(['route_from_aiport_id' , 'route_airline_id'] , inplace = True , axis = 1)
    airport_df.drop(['airport_name', 'airport_city' ,'airport_icao_unique_code' , 'airport_altitude'] , inplace = True , axis = 1)


    # Merge airport and route data to match the dest. airport id to the dest. country:
    merged_airport_route_df = pd.merge(airport_df, route_df, left_on='airport_id' , right_on = 'route_to_airport_id' ,how = 'right') 


    # Get the final answer by grouping the lines with the same country and get their size
    answer: pd.DataFrame = merged_airport_route_df.groupby(['airport_country'],as_index=False).size()

    # Sort in both alphabetically and according to the size. Take only top 30 lines.
    answer = answer.sort_values(by=['size' , 'airport_country'], ascending=(True, True)).head(30)


    # # Generating the answer in a csv file:
    final_df = pd.DataFrame(columns=['subject' , 'statistic']) 
    final_df['subject']= answer['airport_country']
    final_df['statistic'] = answer['size']
    final_df.to_csv('q2.csv', index = False)

    # End of question_two

def question_three(route_df: object , airport_df: object):

    """

    Generates a csv file answering question 3 of the assignment.

    The function uses the command-line input supplied by the 
    user to answer the following question: What are the top 10 destination airports?
    This is done using the pandas library - merging and modifying the 
    data frames for a desired result. The desired result is then stored
    in a csv file.
    
    Parameter routes: a data frame of the input route.csv file
    Parameter airports: a data frame of the input airports.csv file

    """

    # Modifying data frames to only include columns of interest:
    airport_df.drop(columns = ['airport_altitude'] , inplace = True)

    route_df.drop(columns = ['route_airline_id','route_from_aiport_id'] , inplace = True)


    # Merge airport and route data to match the airline id to the rest of the information
    merged_airport_route_df = pd.merge(airport_df, route_df, left_on='airport_id' ,right_on = 'route_to_airport_id' , how = 'right') 

    

    # Get the final answer by concatanating the airport information into one column ('subject')
    # according to the specifications:
    answer: pd.DataFrame = pd.DataFrame(columns=['subject']) 
    answer['subject'] = merged_airport_route_df['airport_name'] + " (" + merged_airport_route_df['airport_icao_unique_code'] +'), '\
                        + merged_airport_route_df['airport_city'] + ', ' + merged_airport_route_df['airport_country']

    # Group by the airport info and get the size
    answer = answer.groupby(['subject'] , as_index=False).size()

    # Now sort in descending order so that the airports with the most appearances are at the top
    answer = answer.sort_values(by='size', ascending=False).head(10)


    # Finally, generate the appropriate csv file for the answer:
    final_df = pd.DataFrame(columns=['subject' , 'statistic']) 
    final_df['subject']= answer['subject']
    final_df['statistic'] = answer['size']
    final_df.to_csv('q3.csv', index = False)

    # End of question_three


def question_four(route_df: object , airport_df: object):

    """

    Generates a csv file answering question 4 of the assignment.

    The function uses the command-line input supplied by the 
    user to answer the following question:  What are the top 15 destination cities?
    This is done using the pandas library - merging and modifying the 
    data frames for a desired result. The desired result is then stored
    in a csv file.
    
    Parameter routes: a data frame of the input route.csv file
    Parameter airports: a data frame of the input airports.csv file

    """

    # Modifying data frames to only include columns of interest:
    airport_df.drop(columns = ['airport_name' , 'airport_icao_unique_code' ,'airport_altitude'] , inplace = True)
    route_df.drop(columns =['route_airline_id','route_from_aiport_id'] , inplace = True)


    # Merge airport and route data to match the airline id to the rest of the information
    merged_airport_route_df = pd.merge(airport_df, route_df, left_on='airport_id' , right_on = 'route_to_airport_id' , how = 'right') 

    

    # Get the final answer by concatanating the airport information into one column ('subject')
    # according to the specifications:
    answer: pd.DataFrame = pd.DataFrame(columns=['subject']) 
    answer['subject'] = merged_airport_route_df['airport_city'] + ', ' + merged_airport_route_df['airport_country']

    # Group by the airport info and get the size
    answer = answer.groupby(['subject'] , as_index=False).size()

    # Now sort in descending order so that the cities with the most appearances are at the top
    answer = answer.sort_values(by='size', ascending=False).head(15)


    # Finally, generate the appropriate csv file for the answer:
    final_df = pd.DataFrame(columns=['subject' , 'statistic']) 
    final_df['subject']= answer['subject']
    final_df['statistic'] = answer['size']
    final_df.to_csv('q4.csv', index = False)

    # End of question_four

def question_five(route_df: object , airline_df: object , airport_df: object):
    """

    Generates a csv file answering question 5 of the assignment.

    The function uses the command-line input supplied by the 
    user to answer the following question: What are the unique top 10 Canadian routes 
    with most difference between the destination altitude and the origin altitude?
    This is done using the pandas library - merging and modifying the 
    data frames for a desired result. The desired result is then stored
    in a csv file.
    
    Parameter routes: a data frame of the input route.csv file
    Parameter airlines: a data frame of the input airlines.csv file
    Parameter airports: a data frame of the input airports.csv file

    """

    # Modifying data frames to only include columns of interest:
    route_df.drop(columns = ['route_airline_id'] , inplace = True)
    airport_df.drop(columns = ['airport_city' , 'airport_name'] , inplace = True)

    # Merge airport and route data to match the airport id to the corresponding information:
    airline_route_from_airport_merged = pd.merge(route_df , airport_df , left_on = 'route_from_aiport_id', right_on = 'airport_id' , how = 'inner')    

    # Merge the data frame with the from airport info to the airport data frame again to match destination
    # airport code to the corresponding info:
    all_df = pd.merge(airline_route_from_airport_merged , airport_df , left_on = 'route_to_airport_id' , right_on = 'airport_id' , how = 'inner')


    # We now filter the data to only include lines with both destination and origin airports in Canada:
    all_df = all_df[all_df['airport_country_x'] == 'Canada']
    all_df = all_df[all_df['airport_country_y'] == 'Canada']


    # To maximize both space and runtime efficiency, we drop uneccssary columns:
    all_df.drop(columns = ['route_from_aiport_id' , 'route_to_airport_id' , 'airport_id_x' , 'airport_id_y' , 'airport_country_x' , 'airport_country_y'] , inplace = True)


    # We now convert the altitudes of the airports from strings to floats:
    all_df = all_df.astype({'airport_altitude_x' : 'float' , 'airport_altitude_y' : 'float'})

    # We concatenate the codes of the airports and format them to appear in one column as desired
    all_df['subject'] = all_df['airport_icao_unique_code_x'] +'-'+ all_df['airport_icao_unique_code_y']

    # We take the difference between all altitudes and take the absolute value.
    # The absolute value is taken so that we can eliminate equal routes.
    all_df['statistic'] = abs( all_df['airport_altitude_x'].sub(all_df['airport_altitude_y'], axis = 0) )

    # The lines with the same alitutde difference represent equal routes. Therefore, we group them together
    all_df = all_df.groupby(['statistic'] , group_keys = False).apply(lambda x: x)

    # Drop more unneeded coluns to increase efficiency
    all_df.drop(columns = {'airport_icao_unique_code_x' , 'airport_icao_unique_code_y' , 'airport_altitude_x' , 'airport_altitude_y'} , inplace = True)

    # Sort the data from highest to lowest alitutde difference 
    all_df = all_df.sort_values(by = 'statistic' , ascending = False).head(10)


    # Finally, generate the appropriate csv file for the answer:
    final_df = pd.DataFrame(columns=["subject" , "statistic"]) 
    final_df["subject"]= all_df['subject']
    final_df["statistic"] = all_df["statistic"]
    final_df.to_csv("q5.csv", index = False)

    # End of question_five


def generate_bar(info: list):

    """
    Generate a bar plot for the question.

    The function takes the csv answer file generated by the program in an
    earlier stage and generates an appropriate bar grpah. The bar graph is 
    stored in a pdf file. 
    
    Parameter output_file: a string that represents the name of the file to output
    Parameter data: a string representing the name of a csv file containing the answer 
            for the question (this is obtained earlier in the program)
    Parameter title: a string representing the title of the bar graph
    Parameter x_title: a string representing the title of the x-axis of the bar graph
    Parameter y_title: a string representing the title of the y-axis of the bar graph

    """
    
    # Reading the csv answer we generated for the question earlier.
    data_df = pd.read_csv(info[1])

    # Initilizing the plot
    fig = plt.figure()
    axes = fig.add_axes([0,0,1,1])
    f1 = axes.bar(data_df["subject"] , data_df["statistic"] )

    # Style Additions and readability improvements:
    plt.setp(axes.get_xticklabels(), rotation= - 60, horizontalalignment='left' , fontsize='small')
    axes.set_title(info[2])
    axes.set_xlabel(info[3])
    axes.set_ylabel(info[4])

    # Saving the plot as a pdf file:
    plt.savefig(info[0], format="pdf", bbox_inches="tight")


    # End of generate_bar



def generate_pie(info: list):

    """
    Generate a pie chart for the question.

    The function takes the csv answer file generated by the program in an
    earlier stage and generates an appropriate pie chart. The pie chart is 
    stored in a pdf file. 
    
    Parameter output_file: a string that represents the name of the file to output
    Parameter data: a string representing the name of a csv file containing the answer 
                    for the question (this is obtained earlier in the program)
    Parameter title: a string representing the title of the bar graph
    Parameter x_title: a string representing the title of the x-axis of the bar graph
    Parameter y_title: a string representing the title of the y-axis of the bar graph

    """
    # Reading the csv answer we generated for the question earlier.
    data_df = pd.read_csv(info[1])

    # Initilizing the plot
    fig = plt.figure()
    axes = fig.add_axes([0,0,1,1])
    f1 = axes.pie(data_df["statistic"] , labels = data_df["subject"] , textprops={'fontsize': 6})

    # Style Additions and readability improvements:
    axes.set_title(info[2])

    # Saving the plot as a pdf file:
    plt.savefig(info[0], format="pdf", bbox_inches="tight")


    # End of generate_pie



if __name__ == '__main__':
    main()


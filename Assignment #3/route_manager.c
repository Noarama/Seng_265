/** @file route_manager.c
 *  @brief A small program to analyze airline routes data.
 *  @author Mike Z.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author Noa A. 
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"

// TODO: Make sure to adjust this based on the input files given
#define MAX_LINE_LEN 120

/**
 * @brief Serves as an incremental counter for navigating the list.
 *
 * @param p The pointer of the node to print.
 * @param arg The pointer of the index.
 *
 */
void inccounter(node_t *p, void *arg)
{
    int *ip = (int *)arg;
    (*ip)++;
}

/**
 * @brief Allows to print out the content of a node.
 *
 * @param p The pointer of the node to print.
 * @param arg The format of the string.
 *
 */
void print_node(node_t *p, void *arg)
{
    char *fmt = (char *)arg;
    printf(fmt, p->word , p->stat);
}


/**
 * @brief Allows to print each node in the list.
 *
 * @param l The first node in the list
 *
 */
void analysis(node_t *l)
{
    int len = 0;

    apply(l, inccounter, &len);
    printf("Number of words: %d\n", len);

    apply(l, print_node, "%s, %d\n");
}

/*
 * free_list
 *
 * Purpose: This function frees the memory allocated for a linked list.
 *
 * Parameters: node_t* list - a pointer to the list we want to free.
 */

void free_list(node_t* to_free){
    // Releasing the space allocated for the list and other emalloc'ed elements
    node_t *temp_n = NULL;
    for (; to_free != NULL; to_free = temp_n)
    {
        temp_n = to_free->next;
        free(to_free->word);
        free(to_free);
    }
}

/*
 * change_stat_sign
 *
 * Purpose: This function changes the sign of the stat value of each node of a 
 *          list. 
 *
 * Parameters: node_t* list - a pointer to the list we want to update
 */

void change_stat_sign(node_t* list){
    node_t *temp_n = list;

    while(temp_n != NULL){
        if(temp_n->next == NULL)
            break;

        temp_n->stat *= -1;
        temp_n = temp_n->next;
        
    }

}

/*
 * generate_file
 *
 * Purpose: This function creates the output file and writes the contents
 *          of the given list to it.
 *
 * Parameters: node_t* list - a pointer to the list containing the information
 *             int num - the number of arguments the user wants to display. 
 */

void generate_file(node_t* final_list , int num){

    // Creating outputfile and printing title:
    FILE* out = fopen("output.csv" , "w+");
    fprintf(out, "subject,statistic\n");


    node_t* cur_n = final_list;
    int num_subjects = 0; // This will keep track of the number of subjects printed to the file

    while(cur_n != NULL){

        if(num_subjects == num) // If num_subjects equals the user provided number we are done.
            break;

        fprintf(out, "%s,%d\n" , cur_n->word , cur_n->stat);
        cur_n = cur_n->next;
        num_subjects++;
    }

    fclose(out);
}

/*
 * find_statistic
 *
 * Purpose: This function finds the number of occurences of the same element
 *          in a linked list.
 *
 * Parameters: node_t* list - a pointer to the list we want to check. 
               int q_num - the number of the question
 *
 * Returns: node_t* stat_list - a new list which includes the elements of the 
 *                              given list along with their statistics. 
 */
node_t* find_statistic(node_t* list , int q_num){

    node_t *temp_n = NULL;
    node_t* stat_list = NULL;
    int count = 2; // We initilize the count to 2 to account for the first element not being counted


    while(list != NULL && list->next != NULL){

        temp_n = list->next;

        while(temp_n != NULL && temp_n->next != NULL && strcmp(temp_n->word , temp_n->next->word) == 0){
            count++;
            temp_n = temp_n->next;
        }

        if(temp_n == NULL)
            break;

        switch(q_num){

            case 1:     stat_list = add_inorder_stat(stat_list , new_node(temp_n->word, count));
                        break;

            case 2:     // Multiply count bu -1 to make all stat values of the nodes 
                        // negative. Since we are interested in the countries that
                        // appear the least number of times, the negative values will result
                        // in the lowest statistic to appear on the top of the list. 
                        count *= -1;
                        stat_list = add_inorder_stat(stat_list , new_node(temp_n->word, count));
                        break;

            case 3:     stat_list = add_inorder_stat(stat_list , new_node(temp_n->word, count));
                        break;
        }

        count = 1;
        list = temp_n;
    }

    return stat_list;
}


/*
 * question_one_handler
 *
 * Purpose: This function answers the question What are the top N airlines 
 *          that offer the greatest number of routes with destination country 
 *          as Canada?
 *          The results are written to a csv file named output.csv
 *
 * Parameters: FILE* inp - A file pointer pointing to the input file provided 
 *                         by the user.
 *             int num - The number of subjects to be displayed
 */
void question_one_handler(FILE* inp , int num){

    char* airline_name = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    char* airline_code = (char *)malloc(sizeof(char) * 10);
    char* dest_country = (char *)malloc(sizeof(char) * MAX_LINE_LEN);


    // The format of the output requires the airline code to be 
    // enclosed in brackets. These two strings are concatenated with 
    // the string containing the airline code later in the function. 
    char* l_bracket = (char *)malloc(sizeof(char) * 10);
    char* r_bracket = (char *)malloc(sizeof(char) * 10);
    strcpy(l_bracket,  " (");
    strcpy(r_bracket , ")");


    node_t *list_airlines = NULL; 

    char* current_line = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    fgets(current_line , MAX_LINE_LEN , inp);
    int line = 1;

    while(fgets(current_line , MAX_LINE_LEN , inp) != NULL){

        if (line == 1){
            // If the line is 1, then we know the scanned value is the airline name. 
            // We need that info so store it. 
            sscanf(current_line , "-    airline_name: %[^\n]" , airline_name);
        }

        else if(line == 2){
            sscanf(current_line , "  airline_icao_unique_code: %[^\t\n']" , airline_code);

            // Adding the brackets:
            strcat(l_bracket,airline_code);
            strcat(l_bracket , r_bracket);
            strcpy(airline_code ,l_bracket);

            // Combining airline name nad code
            strcat(airline_name , airline_code);
        }
        
        else if(line == 11){
            // If the line is 11, then the scanned value is the dest. country.
            // We need that info so store it. 
            sscanf(current_line , "  to_airport_country: %[^\t\n]" , dest_country);

            // If block below removes leading spaces.
            if(*dest_country == '\'')
                sscanf(dest_country, "\' %[A-Za-z ]\'" , dest_country);

            // We compare the current dest. country to Canada. If equal, 
            // then we need to store that airline in a list. 
            if(strcmp(dest_country, "Canada") == 0)
                list_airlines = add_inorder(list_airlines , new_node(airline_name , -1));
        }

        else if(line == 13){
            line = 0;
            // Resetting the strings every time we get to a new route
            strcpy(l_bracket," (");
            strcpy(r_bracket,")");
        }

        line++;
    }

    // "Grouping" all duplicate nodes 
    node_t *stat_list = find_statistic(list_airlines , 1);

    // Generating the output file 
    generate_file(stat_list , num);


    // Freeing all allocated storage:
    free_list(stat_list);
    free_list(list_airlines);
    free(current_line);
    free(airline_name);
    free(airline_code);
    free(dest_country);
    free(l_bracket);
    free(r_bracket);
}



/*
 * question_two_handler
 *
 * Purpose: This function answers the question What are the top N countries with least 
 *          appearances as destination country on the routes data?
 *          The results are written to a csv file named output.csv
 *
 * Parameters: FILE* inp - A file pointer pointing to the input file provided 
 *                         by the user.
 *             int num - The number of subjects to be displayed.
 */
void question_two_handler(FILE* inp, int num){

    char* dest_country = (char *)malloc(sizeof(char) * MAX_LINE_LEN);

    node_t *list_dests = NULL; 

    char* current_line = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    fgets(current_line , MAX_LINE_LEN , inp);
    int line = 1;

    while(fgets(current_line , MAX_LINE_LEN , inp) != NULL){

        if(line == 11){
            // If the line is 11, then the scanned value is the dest. country.
            // We need that info so store it. 
            sscanf(current_line , "  to_airport_country: %[^\t\n]" , dest_country);

            // If block below removes leading spaces.
            if(*dest_country == '\'')
                sscanf(dest_country, "\' %[A-Za-z ]\'" , dest_country);

            list_dests = add_inorder(list_dests , new_node(dest_country, -1));
        }

        else if(line == 13){
            line = 0;
        }

        line++;
    }

    // "Grouping" all duplicate nodes
    node_t *stat_list = find_statistic(list_dests , 2);

    // Since the statistics of all nodes of the list returned by
    // find_statistic are negative (which made it easier to sort),
    // we now update them back to positive values.
    change_stat_sign(stat_list);

    // Generating output file
    generate_file(stat_list , num);

    // Freeing all allocated storage:
    free_list(stat_list);
    free_list(list_dests);
    free(current_line);
    free(dest_country);
}


/*
 * question_three_handler
 *
 * Purpose: This function answers the question What are the top N destination 
 *          airports? The results are written to a csv file named output.csv
 *
 * Parameters: FILE* inp - A file pointer pointing to the input file provided 
 *                         by the user.
  *            int num - The number of subjects to be displayed.
 */
void question_three_handler(FILE* inp, int num){

    char* airport_name = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    char* airport_code = (char *)malloc(sizeof(char) * 10);
    char* airport_country = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    char* airport_city = (char *)malloc(sizeof(char) * MAX_LINE_LEN);

    char* q_marks = (char *)malloc(sizeof(char) * 50);
    strcpy(q_marks, "\"");

    node_t *list_airports = NULL; 

    char* current_line = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    fgets(current_line , MAX_LINE_LEN , inp);

    int line = 1;

    while(fgets(current_line , MAX_LINE_LEN , inp) != NULL){

        switch(line){

            // If the line is 9, then the scanned value is the dest. airport name.
            // We need that info so store it. 
            case 9:     sscanf(current_line , "  to_airport_name: %[^\t\n]" , airport_name);
                        if(*airport_name == '\'')
                            sscanf(airport_name, "\' %[A-Za-z ]\'" , airport_name);
                        break;

            // If the line is 10, then the scanned value is the dest. airport city.
            // We need that info so store it. 
            case 10:    sscanf(current_line , "  to_airport_city: %[^\t\n]" , airport_city);
                        if(*airport_city == '\'')
                            sscanf(airport_city, "\' %[A-Za-z ]\'" , airport_city);
                        break;

            // If the line is 11, then the scanned value is the dest. airport country.
            // We need that info so store it. 
            case 11:    sscanf(current_line , "  to_airport_country: %[^\t\n]" , airport_country);
                        if(*airport_country == '\'')
                            sscanf(airport_country, "\' %[A-Za-z ]\'" , airport_country);
                        break;

            // If the line is 12, then the scanned value is the dest. airport code.
            // We need that info so store it. 
            case 12:    sscanf(current_line , "   to_airport_icao_unique_code: %[^\t\n]" , airport_code);
                        if(*airport_code == '\'')
                            sscanf(airport_code, "\' %[A-Za-z ]\'" , airport_code);
                        break;

            // If the line is 13, then we know we reached the last piece of info about
            // the specific route. So we have all the info we need. We combine it all to 
            // one string in the following format:
            // "-airport name- (-airport code-), -airport city-, -airport country-"
            case 13:    line = 0;
                        strcat(q_marks, airport_name);
                        strcpy(airport_name,q_marks);
                        strcat(airport_name , " (");
                        strcat(airport_name , airport_code);
                        strcat(airport_name, "), ");
                        strcat(airport_name , airport_city);
                        strcat(airport_name, ", ");
                        strcat(airport_name , airport_country);
                        strcat(airport_name, "\"");

                        // We must reassign " to the q_marks so that it is ready for
                        // the next iteration
                        strcpy(q_marks, "\"");

                        // Now add a new node to the list with that string
                        list_airports = add_inorder(list_airports , new_node(airport_name, -1));
                        break;
        }

        line++;
    }

    // // "Grouping" all duplicate nodes
    node_t *stat_list = find_statistic(list_airports , 3);

    // Generating output file
    generate_file(stat_list , num);

    // Freeing all allocated storage:
    free_list(stat_list);
    free_list(list_airports);
    free(current_line);
    free(airport_name);
    free(airport_code);
    free(airport_country);
    free(airport_city);
    free(q_marks);
}


/**
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */
int main(int argc, char *argv[])
{

    // Opening input file:
    char* inp_file_name = (char *)malloc(sizeof(char) * 30);;
    int num = 0;

    sscanf(argv[1] , "--DATA=%s" , inp_file_name);
    FILE* inp = fopen(inp_file_name , "r");

    sscanf(argv[3] , "--N=%d" , &num);

    // Getting number of question from command line arguments and calling
    // its corresponding handler.
    int q_num =0;

    sscanf(argv[2] , "--QUESTION=%d" , &q_num);
    switch(q_num){
        case 1:     question_one_handler(inp , num);
                    break;

        case 2:     question_two_handler(inp , num);
                    break;

        case 3:     question_three_handler(inp , num);
                    break;
    }

    // Closing the file
    fclose(inp);

    // Freeing all allocated memory:
    free(inp_file_name);

    exit(0);
}

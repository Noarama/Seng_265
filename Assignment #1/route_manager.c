/** @file route_manager.c
 *  @brief A pipes & filters program that uses conditionals, loops, and string processing tools in C to process airline routes.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author Noa A.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct conditions C;
struct conditions{

    int case_num;

    char data[50];

    char airline_name[50];
    char airline_code[10]; 

    char origin_airport[10];
    char origin_city[50];
    char origin_country[50];

    char dest_airport[10];
    char dest_city[50];
    char dest_country[50];
};

void seperate_words(C compare);
int case_one_handler(int status , char route_info[12][50] , C basis , FILE* fp);
int case_two_handler(int status , char route_info[12][50] , C basis , FILE* fp);
int case_three_handler(int status , char route_info[12][50] , C basis , FILE* fp);

/**
 * Function: main
 * --------------
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */
int main(int argc, char *argv[]){

    int args1 = atoi(argv[1]);

    C basis;
    
    // If block responsible for storing the input 
    // entered by the user in the terminal. 
    if(args1 >= 0){ 

        sscanf(argv[1] , "--DATA=%s" , basis.data);

        // Reading and storing the remaning
        // arguments passed by user in terminal:

        if(argc == 4){

            // Case 1:

            sscanf(argv[2] , "--AIRLINE=%s" , basis.airline_code);
            sscanf(argv[3] , "--DEST_COUNTRY=%[ A-Za-z]" , basis.dest_country);
            basis.case_num = 1;
        }

        else if(argc == 5){

            // Case 2:

            sscanf(argv[2] , "--SRC_COUNTRY=%s" , basis.origin_country);
            sscanf(argv[3] , "--DEST_CITY=%[ A-Za-z]" , basis.dest_city);
            sscanf(argv[4] , "--DEST_COUNTRY=%[ A-Za-z]" , basis.dest_country);
            basis.case_num = 2;
        }

        else if(argc == 6){

            // Case 3: 

            sscanf(argv[2] , "--SRC_CITY=%[ A-Za-z]" , basis.origin_city);
            sscanf(argv[3] , "--SRC_COUNTRY=%[ A-Za-z]" , basis.origin_country);
            sscanf(argv[4] , "--DEST_CITY=%[ A-Za-z]" , basis.dest_city);
            sscanf(argv[5] , "--DEST_COUNTRY=%[ A-Za-z]" , basis.dest_country);

            basis.case_num = 3;
        }

        seperate_words(basis);
    }
}


/*
 * Seperate_words
 *
 * Purpose: 
 * This function seperates the pieces of information included in 
 *          the scanned string from the command line. 
 *
 * Parameters: 
 * - C compare: a struct consisting of all scanned data from the command line.
 */
void seperate_words(C compare){

    FILE* data = fopen(compare.data , "r"); // Opening data file.
    FILE* out = fopen("output.txt" , "w"); // Creating output file.

    // Make sure files opened with no errors.
    if(data == NULL && out == NULL)
        printf("NO RESULTS FOUND.\n");

    // Declerations 
    char current_line[500];     // This string stores entire lines read from the file. 

    char route_info[12][50];   // An array of strings to store all individual 
                                //words of the current line.

    int status = 1;  // This int indicates if a title should be printed or not.

    /*
     * Idea: 
     * We read one line of the data file at a time. 
     * We then seperate the words (which are seperated
     * by commas in the file) and store them individually
     * in an array of strings. We do this so that we can have
     * easier access to the different pieces of information
     * that we need to comapre with the desired conditions 
     * and print to the output file.
    */

    while(fgets(current_line , 500 , data) != NULL){
    // This while loop iterates through the lines of the data file

        // Seperate the first word of the string and store in position 0.
        char* comma_pointer = strpbrk(current_line , ",");



        // This if statement deals with lines that do not contain
        // all the information. i.e, lines that look like ,,,%s,%s,...
        if(current_line[0] == ',')  
            strcpy(route_info[0] , "");

        else
            sscanf(current_line, "%[a-zA-z \0],%s" , route_info[0], comma_pointer);
        

        comma_pointer++; // Increase comma pointer by one to eliminate leading commas.
        int i = 1;



        // This while loop seperates the remaining words from the 
        // line and stores them in their corresponding position in 
        // the array. 
        while(comma_pointer !=  NULL && i < 12){

            if(*comma_pointer == ','){
                strcpy(route_info[0] , "");
                comma_pointer++;

            }else{
                sscanf(comma_pointer, "%[A-Za-z0-9.0-9 ],%[A-Za-z0-9.0-9 ,]" , route_info[i] , comma_pointer);

            }

            i++;
        }

        // At this point of the code we have all words
        // of a line stored in an array. So we need to
        // Compare and decide if the line should or shouldn't be 
        // printed to the output file, based on the corresponding case

        switch(compare.case_num){

            case 1:     status = case_one_handler(status , route_info , compare , out);
                        break;

            case 2:     status = case_two_handler(status , route_info , compare , out);
                        break;

            case 3:     status = case_three_handler(status , route_info , compare , out);
                        break;
        }
        
    }

    if(status == 1)
        fprintf(out , "NO RESULTS FOUND.");

    fclose(out);
    fclose(data);

}


/*
 * case_one_handler:
 * 
 * Purpose:
 * The function produces the corresponding output 
 * for the first case. 
 * 
 * Parameters: 
 * - int status: an integer indicating whether the title should 
 *               be printed.
 * - char route_info[12][100]: a 2d array holding all individual words 
 *                             seperated from the line.
 * - C basis: A struct holding all desired values as indicated by the user.
 * - FILE* fp: A file pointer pointing to the output file, where the lines
 *             satisfying the given conditions should be printed.
 *
 * Returns:
 * - int: an integer representing the current status after the function executes.
 */

int case_one_handler(int status , char route_info[12][50] , C basis , FILE* fp){



    if(!strcmp(route_info[1] , basis.airline_code )  && !strcmp(route_info[10] , basis.dest_country)){

        if(status){// If we get to here, it means a match was found so we can print the "title".
            fprintf(fp, "FLIGHTS TO %s BY %s (%s):\n" , basis.dest_country , route_info[0], basis.airline_code);
        }

        fprintf(fp, "FROM: %s, %s, %s " ,route_info[6], route_info[4], route_info[5]);
        fprintf(fp, "TO: %s (%s), %s\n", route_info[8], route_info[11], route_info[9]);

        status = 0;
    }

    return status;
}


/*
 * case_two_handler:
 * 
 * Purpose:
 * The function produces the corresponding output 
 * for the second case. 
 * 
 * Parameters: 
 * - int status: an integer indicating whether the title should 
 *               be printed.
 * - char route_info[12][100]: a 2d array holding all individual words 
 *                             seperated from the line.
 * - C basis: A struct holding all desired values as indicated by the user.
 * - FILE* fp: A file pointer pointing to the output file, where the lines
 *             satisfying the given conditions should be printed.
 *
 * Returns:
 * - int: an integer representing the current status after the function executes.
 */

int case_two_handler(int status , char route_info[12][50] , C basis , FILE* fp){

    if(!strcmp(route_info[5] , basis.origin_country )  && !strcmp(route_info[9] , basis.dest_city) && !strcmp(route_info[10] , basis.dest_country)){

        if(status){// If we get to here, it means a match was found so we can print the "title".
            fprintf(fp, "FLIGHTS FROM %s TO %s, %s:\n" , basis.origin_country , basis.dest_city, basis.dest_country);
        }

        fprintf(fp, "AIRLINE: %s (%s) " ,route_info[0], route_info[1]);
        fprintf(fp, "ORIGIN: %s (%s), %s\n", route_info[3], route_info[6], route_info[4]);

        status = 0;
    }

    return status;
}


/*
 * case_three_handler:
 * 
 * Purpose:
 * The function produces the corresponding output 
 * for the third case. 
 * 
 * Parameters: 
 * - int status: an integer indicating whether the title should 
 *               be printed.
 * - char route_info[12][100]: a 2d array holding all individual words 
 *                             seperated from the line.
 * - C basis: A struct holding all desired values as indicated by the user.
 * - FILE* fp: A file pointer pointing to the output file, where the lines
 *             satisfying the given conditions should be printed.
 *
 * Returns:
 * - int: an integer representing the current status after the function executes.
 */

int case_three_handler(int status , char route_info[12][50] , C basis , FILE* fp){

    if(!strcmp(route_info[4] , basis.origin_city) && !strcmp(route_info[5] , basis.origin_country )  && !strcmp(route_info[9] , basis.dest_city) && !strcmp(route_info[10] , basis.dest_country)){

        if(status){// If we get to here, it means a match was found so we can print the "title".
            fprintf(fp, "FLIGHTS FROM %s, %s TO %s, %s:\n" , basis.origin_city, basis.origin_country, basis.dest_city , basis.dest_country);
        }

        fprintf(fp, "AIRLINE: %s (%s) " ,route_info[0], route_info[1]);
        fprintf(fp, "ROUTE: %s-%s\n", route_info[6], route_info[11]);

        status = 0;
    }

    return status;
}







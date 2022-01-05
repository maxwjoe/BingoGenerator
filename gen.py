from fpdf import FPDF
import csv
import os
import random


# --- Global Variables
__OUTPUT__FOLDER__NAME = "pdfs"

# --- Functions

#Log Error : Logs an error to the console and terminates program
def __ERROR__(error_message):

    if type(error_message) != str:
        error_message = str(error_message)

    print("\nERROR : " + error_message + '\n')
    exit()


#getBingoNumbers : generates 5x10 array of random numbers (1-75)
def getBingoNumbers():
    random_numbers = []
    for i in range(0,50):
        random_numbers.append(random.randint(1,75))
    return random_numbers


#getGuests : gets guest list from spreadsheet
def getGuestsFromCSV(FILENAME):
    
    if type(FILENAME) != str or FILENAME.find(".csv") == -1:
        __ERROR__("Invalid Filename")

    names_full = None
    final_names = []

    #Get names from CSV
    with open(FILENAME, newline='') as file:
        file_read = csv.reader(file)
        names_full = list(file_read)

    #Filter Long Names
    for name in names_full:
        if len(name[0]) > 15:
            temp = name[0].split()
            final_names.append(temp[0])
            continue

        final_names.append(name[0])
    
    return final_names


#generatePDF : generates and save pdf
def generatePDF(guest_name_1, guest_name_2):

    #Handle Invalid Input
    if type(guest_name_1) != str or type(guest_name_2) != str:
        __ERROR__("Guest names must be a string type")

    #PDF Setup
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.add_font("PressStart2P","", "PressStart2P-Regular.ttf", uni=True)
    pdf.add_font("Nautical-Reg", "", "TheNautigal-Regular.ttf", uni=True)
    pdf.add_font("GreatVibes", '', 'GreatVibes-Regular.ttf', uni=True)

    pdf.set_font("helvetica")


    #Generate Bingo Boards
    bingo_nums = getBingoNumbers()
    for i in range(0,50):
        if i%5 == 0 :
            pdf.cell(40,20,"")

        if i == 22 or i == 27:
            pdf.cell(15,15,"UNMS",ln=((i + 1) % 10 == 0) ,border=True, align="C")
            continue

        pdf.cell(15,15,str(bingo_nums[i]),ln=((i + 1) % 10 == 0) ,border=True, align="C")
    

    #Spacing Vertical
    pdf.cell(0,50,"", ln=True)

    #Spacing Horizontal
    pdf.cell(25,1,"")

    #Print Guests
    __BORDER__ = False
    pdf.set_font("GreatVibes", size=50)
    pdf.cell(100,30,guest_name_1, align="C", border=__BORDER__)

    #Spacing Horizontal
    pdf.cell(25,1,"")
    pdf.cell(100,30,guest_name_2, align="C", border=__BORDER__)

    #Save PDF
    pdf.output(f'{__OUTPUT__FOLDER__NAME}/{guest_name_1}_AND_{guest_name_2}.pdf')


# --- Main Script
if __name__ == '__main__':
    
    #Check if output folder exists and create if it doesnt
    if os.path.isdir(__OUTPUT__FOLDER__NAME) == False :
        os.mkdir(__OUTPUT__FOLDER__NAME)


    #Get Guest List
    names = getGuestsFromCSV("names.csv")

    #Generate PDFS
    i = 0
    PDF_COUNT = 0
    while( i < len(names) ):

        guestA = names[i]

        if i + 1 >= len(names):
            guestB = "END"
        
        else :
            guestB = names[i + 1]
        
        generatePDF(guestA, guestB)

        PDF_COUNT += 1
        i += 2

    #Log Summary
    print("\n === SUMMARY ===\n")
    print(f" Guest Count : {len(names)}")
    print(f" PDFs Generated : {PDF_COUNT}")
    print(f" PDFs have been saved to the folder '{__OUTPUT__FOLDER__NAME}'.\n")
    print(" === END ===\n")

    



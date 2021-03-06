from fpdf import FPDF
import PyPDF2
import csv
import os
import random


# --- Global Variables
__OUTPUT__FOLDER__NAME__ = "pdfs"
__INPUT__CSV__ = "names.csv"
__BINGO__RANGE__ = (1,60)
__BINGO__NUMBERS__ = []

# --- Functions

#Log Error : Logs an error to the console and terminates program
def __ERROR__(error_message):

    if type(error_message) != str:
        error_message = str(error_message)

    print("\nERROR : " + error_message + '\n')
    exit()

#CheckForDuplicates : Checks for duplicates in an array
def checkForDuplicates(ARRAY_IN):
    
    if type(ARRAY_IN) != list:
        __ERROR__("checkForDuplicates() expects a list type")

    newlist = []

    if type(ARRAY_IN[0]) == list:
        seen = set()

        for item in ARRAY_IN :
            t = tuple(item)

            if t not in seen:
                newlist.append(item)
                seen.add(t)
        
    else :
        newlist = set(ARRAY_IN)
    
    if len(newlist) != len(ARRAY_IN):
            __ERROR__(f"Duplicate in array [TYPE = {type(ARRAY_IN[0])}]")



#getBingoNumbers : generates 5x5 array of random numbers (1-75)
def getBingoNumbers():

    bingo_numbers = []
    
    #Get Columns

    #B (1-15)
    B = [x for x in range(1, 16)]
    B = random.sample(B, 5)
    #I (16-30)
    I = [x for x in range(16, 31)]
    I = random.sample(I, 5)
    #N (31-45)
    N = [x for x in range(31, 46)]
    N = random.sample(N, 5)
    #G (46-60)
    G = [x for x in range(46, 61)]
    G = random.sample(G, 5)
    #O (61-75)
    O = [x for x in range(61, 76)]
    O = random.sample(O, 5)

    bingo_cols = [B, I, N, G, O]

    #check uniqueness (paranoid i know)
    checkForDuplicates(bingo_cols)
    for col in bingo_cols:
        checkForDuplicates(col)
    

    #Flatten
    for row in range(0,5):
        for col in range(0, 5):
            bingo_numbers.append(bingo_cols[col][row])
    
    #bc i am paranoid (even though its obvious)
    checkForDuplicates(bingo_numbers)

    return bingo_numbers


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
def generatePDF(guest_name_1, guest_name_2, PDF_COUNT):

    #Handle Invalid Input
    if type(guest_name_1) != str or type(guest_name_2) != str:
        __ERROR__("Guest names must be a string type")

    #PDF Setup
    pdf = FPDF('L', 'mm', 'A4')
    pdf.add_page()
    pdf.add_font("PressStart2P","", "PressStart2P-Regular.ttf", uni=True)
    pdf.add_font("Nautical-Reg", "", "TheNautigal-Regular.ttf", uni=True)
    pdf.add_font("GreatVibes", '', 'GreatVibes-Regular.ttf', uni=True)

    pdf.set_font("helvetica", size=25)


    #Generate Bingo Boards
    bingo_nums_1 = getBingoNumbers()
    bingo_nums_2 = getBingoNumbers()
    __BINGO__NUMBERS__.append(bingo_nums_1)
    __BINGO__NUMBERS__.append(bingo_nums_2)

    bingo_letters = ['B', 'I', 'N', 'G', 'O']
    
    pdf.cell(40,20,"")

    #First BINGO Letters
    for k in range(0,5):
        pdf.cell(15,15,bingo_letters[k], ln=False, border=False, align='C')
    
    #Horizontal Spacing
    pdf.cell(40,20,"")

    #Second BINGO Letters
    for k in range(0,5):
        pdf.cell(15,15,bingo_letters[k], ln=(k + 1 == 5), border=False, align='C')


    #BINGO NUMBERS
    pdf.set_font("helvetica", size=12)

    for row in range(0,5):

        pdf.cell(40,20,"")

        #First Guest
        for i in range(0 + (5*row), 5 + (5*row)):
            if i == 12 :
                pdf.cell(15,15,"UNMS",ln= (i == 5 + (5*row) - 1) ,border=True, align="C")
                continue 

            pdf.cell(15,15,str(bingo_nums_1[i]),ln=False ,border=True, align="C")

        #Horizontal Spacing
        pdf.cell(40,20,"")

        #Second Guest
        for i in range(0 + (5*row), 5 + (5*row)):
            if i == 12 :
                pdf.cell(15,15,"UNMS",ln= (i == 5 + (5*row) - 1) ,border=True, align="C")
                continue 

            pdf.cell(15,15,str(bingo_nums_2[i]),ln= (i == 5 + (5*row) - 1) ,border=True, align="C")


            
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
    #pdf.output(f'{__OUTPUT__FOLDER__NAME__}/{PDF_COUNT}.pdf')
    pdf.output(f'{PDF_COUNT}.pdf')



# --- Main Script
if __name__ == '__main__':
    
    #Check if output folder exists and create if it doesnt
    if os.path.isdir(__OUTPUT__FOLDER__NAME__) == False :
        os.mkdir(__OUTPUT__FOLDER__NAME__)


    #Get Guest List
    names = getGuestsFromCSV(__INPUT__CSV__)

    #Generate PDFS
    i = 0
    PDF_COUNT = 0
    while( i < len(names) ):

        guestA = names[i]

        if i + 1 >= len(names):
            guestB = "END"
        
        else :
            guestB = names[i + 1]
        
        generatePDF(guestA, guestB, PDF_COUNT)

        PDF_COUNT += 1
        i += 2

    
    #Check for duplicates in bingo and throw error if not unique
    checkForDuplicates(__BINGO__NUMBERS__)


    #MERGE PDFS
    MASTER_PDF_NAME = "merged"
    MASTER_PDF = PyPDF2.PdfFileMerger()

    for i in range(0, PDF_COUNT):
        MASTER_PDF.append(PyPDF2.PdfFileReader(f'{i}.pdf', 'rb'))
    
    MASTER_PDF.write(f"{MASTER_PDF_NAME}.pdf")


    #Log Summary
    print("\n === SUMMARY ===\n")
    print(f" Guest Count : {len(names)}")
    print(f" PDFs Generated : {PDF_COUNT}")
    print(f" Number of bingo sets generated : {len(__BINGO__NUMBERS__)}")
    print(f"\n Individual PDFs have been saved to the folder '{__OUTPUT__FOLDER__NAME__}'.\n")
    print(f" A PDF with all PDFs merged has been saved outside this folder with the name {MASTER_PDF_NAME}.\n")
    print(" === END ===\n")

    






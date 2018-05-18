#!/usr/bin/python



# karetka.py - application made for conversion of tablet weaving patterns in CSV format
# into instructions (which direction should be turned each tablet on each row and so on)
# in the HTML or TXT form

# license MIT
# Created by Martin Rybensky

__version__ = '0.01.01'
__author__ = 'Martin Rybensky'

import csv
import sys
import os.path

# summarization function

def summarize(numberlist):
        prev_number = min(numberlist) if numberlist else None
        pagelist = list()

        for number in sorted(numberlist):
            if number != prev_number+1:
                pagelist.append([number])
            elif len(pagelist[-1]) > 1:
                pagelist[-1][-1] = number
            else:
                pagelist[-1].append(number)
            prev_number = number

        return ','.join(['-'.join(map(str,page)) for page in pagelist])


# input filename is taken from the script's first argument

try:
    input_file = sys.argv[1]
except:
    print 'you must specify a filename of the csv file as a parameter'
    sys.exit(0)

if input_file is not "":
    if os.path.exists(input_file):
        print 'processed file: %s' % (input_file)
    else:
        print "requested file does not exist, exitting"
        sys.exit(0)
else:
    print "you must specify a filename of the csv file as a parameter"
    sys.exit(0)

# variables initialization
line = 0
backwards = []
forwards = []
reference = []
row = []
divided = []

css_class = ''


print 'h - HTML table with CSS'
print 't - TXT plain text without formatting'
while True: # infinite loop until pressed y/n
  user_input = raw_input('Please choose one of the options above (h / t)\n')
  if user_input == 'h':
    result = input_file.rsplit('.',1)[0] + '.html'

    # create output html file
    html_file = open(result, "w+")
    html_file.write('<html>\n')
    html_file.write('<style>\n')
    html_file.write('body { font-family: Sans-Serif; font-size: 10pt; }\n') 
    html_file.write('table { border-collapse: collapse; border: 1px solid #000; font-size: 10pt; }\n') 
    html_file.write('.header { background-color: #000; color: #FFF; padding-top: 2px; padding-bottom: 2px; font-weight: bold; text-align: center; }\n') 
    html_file.write('td { padding-right: 3px; padding-left: 6px; font-size: 10pt; border: 1px solid #000; }\n') 
    html_file.write('#frame { border: 0px; padding: 0px; margin: 0px auto; border-spacing: 0px; }\n') 
    html_file.write('.light { background-color: FAFAFA; }\n') 
    html_file.write('.dark { background-color: F1F1F1; }\n') 
    html_file.write('.selected { background-color: #A1A1A1; color: #F1F1F1; }\n') 
    html_file.write('</style>\n\n')   
    
    html_file.write('<center>\n<div id="frame">\n<table>\n')
    html_file.write('<tr class="header"><td>step</td><td>forwards</td><td>backwards</td></tr>\n')          
    html_file.close()
    
  elif user_input == 't':
    # filename of the output file is created by replacing .csv extension with .txt
    result = input_file.rsplit('.',1)[0] + '.txt'

    # create output txt file
    text_file = open(result, "w+")








  # parse the input csv file
  with open(input_file, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ', quotechar=';')

    for row in csvreader:
        
        print row[0]
        if ';' in row[0]:
          delimiter = ';'
        else:
          delimiter = ','          
    
        line += 1 # row count, +1 for each loop
        step = line - 2

        # save the column count into variable
        if line == 1:
            columncount = row[0]
            columncount = columncount.rsplit(delimiter, 1)[1]
            columncount = int(columncount)

        # save the first row as a reference to compare with following lines
        # 
        elif line == 2:
            reference = row[0].split(delimiter,columncount)
        else:
            # split values in the current row
            divided = row[0].split(delimiter,columncount)

            for i, elem in enumerate(divided):
                if reference[i] == divided[i]:
                    g = i + 1
                    forwards.append(g)
                else:
                    g = i + 1
                    backwards.append(g)

            # write row to file
            if user_input == 'h':
            
              if step % 2 == 0:
                css_class = 'light'
              else:
                css_class = 'dark'
                
              html_file = open(result,"a")
              html_file.write('<tr class="' + css_class + '" onclick="this.className=\'selected\'"><td><b>' + str(step) + '</b></td><td>' + str(summarize(forwards)) + '</td><td>' + str(summarize(backwards)) + '</td></tr>\n')
              html_file.close()              
            elif user_input == 't':
              text_file = open(result, "a")
              text_file.write('step ' + str(step) + '\n' +'forwards: ' + str(summarize(forwards)) + '\n' + 'backwards: ' + str(summarize(backwards)) + '\n' + '\n')
              text_file.close()

            # reset variables before next loop
            g = 0
            i = 0
            del forwards[:]
            del backwards[:]

    lastrow = step
    
    if user_input == 'h':
        html_file = open(result,"a")
        html_file.write('</table></div>')        
        html_file.close()      

    print 'column count: ' + str(columncount)
    print 'row count (steps): ' + str(lastrow)
    print 'result has been saved to file ' + result
    sys.exit(0)

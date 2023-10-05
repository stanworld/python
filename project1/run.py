import pandas as pd
 
# read by default 1st sheet of an excel file
inputfile = input("Enter the full name of input file: ")
outputfile = input("Enter the full name of output file: ")
inputsheet = input("Enter the name of input sheet: ")
outputsheet = input("Enter the name of output sheet: ")
df1 = pd.read_excel(inputfile, sheet_name=inputsheet)

print("Before processing: number of rows:" + str(len(df1)))
df2 = df1[df1["Sample Status"] != "Abandoned" ]
df2 = df2[df2["PF Bases (BC)"]/pow(10,9) > 9.5 ]
df2 = df2[df2["Target Bases @ 10X % (HS)"] > 85 ]
print("After processing: number of rows:"+ str(len(df2)))
print("Selecting columns to generate new sheet")
selected_columns = df2[['Project', 'Collaborator Sample ID']]
selected_columns.to_excel(outputfile, sheet_name=outputsheet, index=False)
print("Job Done!")






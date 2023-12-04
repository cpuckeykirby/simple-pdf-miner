import re
import pandas as pd
from pdfminer.high_level import extract_pages, extract_text

pdf_list = ['<insert pdf path>',
            '<insert pdf path>',
            '<insert pdf path>'
            '<etc>'            ]
dict = ['shell','account','office','burger','etc']


report_id = []
for pdf_path in pdf_list:
    report_id.append(pdf_path.replace('<insert pdf path without pdf name>','')) #removes extra path to just get the file name, used when producing table of the results, make sure all pdf's are in the same file

df = pd.DataFrame()
dict_counter = {}
index_counter = -1

#dictionary 1 counts
for pdf_path in pdf_list:
    index_counter = index_counter+1
    report_name = pdf_path.replace('<insert pdf path without pdf name>','')
    print(f"PDF #{index_counter}: Extracting Text from {report_name}...")
    text = extract_text(pdf_path)
    dict1_count=0
    print(f"Counting Dictionary Words in {pdf_path.replace('<insert pdf path without pdf name>','')}:")
    for word in dict:
        word_count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), text))
        dict1_count = dict1_count + word_count
        print(f"'{word}' occurs {word_count} times")
        dict_counter.update({word:word_count})
    df = pd.concat([df, pd.DataFrame([dict_counter])])

df.reset_index()
df['report name']=report_id
report_name = df.pop('report name')
df.insert(0, 'report name', report_name) #adding report names and dropping them into the first column
print(df)

df.to_csv('<insert path for output dataframe>', index=False) #outputting to .csv file

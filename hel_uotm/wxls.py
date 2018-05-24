import re, os
import xlrd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

gen_path = input("Enter the path: ")
define_file = open(gen_path , "r", encoding='ANSI')

def write_cells(row,column,write_list):
    for w in range(5):
        worksheet.write(row, column+w , write_list[w])

def write_formulas(row, column, offset):
    cell_val = xl_rowcol_to_cell(row, column)
    cell_val1 = xl_rowcol_to_cell(row, column-2-offset)
    cell_val2 = xl_rowcol_to_cell(row, column-1-offset)
    worksheet.write_formula(cell_val, '=SQRT(('+cell_val1+'*'+cell_val1+')+('+cell_val2+'*' + cell_val2 +'))', cell_format1)

def write_last_part(row, column):
    write_formulas(row, column, 0)
    write_formulas(row, column+1, 3)
    i = 0
    for d in hel_check_list[row-2]:
        worksheet.write(row, column+2 + i , float(d))
        i += 1
for ll in define_file:
    check_d = False
    ll_list = re.split(r'\t+', ll)

    file_pth = ll_list[0]
    file_ext = ll_list[1]

    check = False
    file_pth_list = list()
    for r, d, f in os.walk(file_pth):
        if d and not check:
            for file in d:
                if file != "conv":
                    file_pth_list.append(file)
            check = True
            break

    for f_elem in file_pth_list:
        s_inverted = []
        ele_list = []
        f_check = re.findall(r'(.*)\n+?', file_ext)
        if f_check:
            file_ext = f_check[0]
        workbook = xlsxwriter.Workbook(file_pth+"\\conv\\"+file_ext +"_"+ f_elem +".xlsx")
        worksheet = workbook.add_worksheet('Data')
        cell_format1 = workbook.add_format()
        cell_format1.set_align('center')

        ele_path = os.path.join(r, f_elem ,"UOTM.SON")
        file_study  = open(ele_path , "r", encoding='ANSI')

        ele_path_hel = os.path.join(r, f_elem ,"HEL.DAT")
        file_study_hel  = open(ele_path_hel , "r", encoding='ANSI')

        hel_check = False
        hel_check_list = list()
        for line in file_study_hel:
            if hel_check:
                f_check = re.findall(r'BLOK', line)
                if f_check:
                    break
                line_list = line.split()
                hel_check_list.append([line_list[1],line_list[2],line_list[3]])
            else:
                f_check = re.findall(r'IBIT', line)
                if f_check:
                    hel_check = True

        file_check = False
        row = 0
        for line in file_study:
            if file_check:
                line_list = line.split()
                column = 0
                for l in line_list:
                    worksheet.write(row, column ,float(l))
                    column += 1
                write_last_part(row, column)
                row += 1
            elif re.findall(r'\d', line):
                file_check = True
                line_list = line.split()
                column = 0
                for l in line_list:
                    worksheet.write(row, column , float(l))
                    column += 1
                write_last_part(row, column)
                row += 1
            elif re.findall(r'NOD', line):
                line_list = line.split()
                column = 0
                for l in line_list:
                    worksheet.write(row, column , l)
                    column += 1
                write_list = ["T","M","X","Y","Z"]
                write_cells(row, column,write_list)
                row += 1
            elif re.findall(r'rad', line):
                line_list = line.split()
                column = 1
                unit_list = list()
                for l in line_list:
                    unit_list.append(l)
                    worksheet.write(row, column , l)
                    column += 1
                write_list = [unit_list[7],unit_list[10],unit_list[1],unit_list[1],unit_list[1]]
                write_cells(row, column,write_list)
                row += 1
        print(file_ext +"_"+ f_elem +".xlsx is written")
        workbook.close()

import re, os
import xlrd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

gen_path = input("Enter the path: ")
define_file = open(gen_path , "r", encoding='ANSI')

def write_cells(row,column,write_list):
    for w in range(len(write_list)):
        worksheet.write(row, column+w , write_list[w],cell_format1)

def write_formulas(row, column, offset):
    cell_val = xl_rowcol_to_cell(row, column)
    cell_val1 = xl_rowcol_to_cell(row, column-offset-3)
    cell_val2 = xl_rowcol_to_cell(row, column-offset)
    worksheet.write_formula(cell_val, '='+ cell_val1 +'+'+ cell_val2, cell_format1)

def write_last_part(row):
    column = 7
    for i in range(3):
        write_formulas(row, column+i, 3)

for ll in define_file:
    check_d = False
    ll_list = re.split(r'\t+', ll)

    file_pth = ll_list[0]
    file_ext = ll_list[1]

    file_pth_list = list()
    for r, d, f in os.walk(file_pth):
        if d:
            for file in d:
                if file != "conv" and file != "grf":
                    file_pth_list.append(file)
            os.makedirs(r+"\\grf", exist_ok=True)
            break

    f_check = re.findall(r'(.*)\n+?', file_ext)
    if f_check:
        file_ext = f_check[0]

    for f_elem in file_pth_list:
        ele_list = []
        rmin_path = os.path.join(file_pth, f_elem )
        for r, d, f in os.walk(rmin_path):
            if d:
                for file in d:
                    in_path = os.path.join(rmin_path, file)
                    ele_list.append(in_path)
                break
        for current_path in ele_list:
            son_path = os.path.join(current_path, "HEL.SON")
            file_son  = open(son_path , "r", encoding='ANSI')

            dat_path = os.path.join(current_path, "HEL.DAT")
            file_dat  = open(dat_path , "r", encoding='ANSI')

            hel_check = False
            hel_dat_list = list()
            count = 0
            for line in file_dat:
                if hel_check:
                    f_check = re.findall(r'BLOK', line)
                    if f_check:
                        break
                    line_list = line.split()
                    count = int(re.findall(r'\d+',line_list[0])[0])
                    hel_dat_list.append([count,float(line_list[1]),float(line_list[2]),float(line_list[3])])
                else:
                    f_check = re.findall(r'IBIT', line)
                    if f_check:
                        hel_check = True

            hel_check = False
            hel_son_list = [[0,0,0]]
            for line in file_son:
                if hel_check:
                    if len(line.strip()) == 0:
                        break
                    line_list = line.split()
                    hel_son_list.append([float(line_list[0]),float(line_list[1]),float(line_list[2])])
                else:
                    f_check = re.findall(r'EIGENVECTOR', line)
                    if f_check:
                        hel_check = True

            list_number = re.findall(r'\d+', dat_path)
            list_number = list_number[len(list_number)-1]
            xls_path = os.path.join(file_pth,"grf",file_ext +"_"+f_elem + "_" +list_number +".xlsx")
            workbook = xlsxwriter.Workbook(xls_path)
            worksheet = workbook.add_worksheet('Data')
            cell_format1 = workbook.add_format()
            cell_format1.set_align('center')
            row = 0
            write_list = ["NOD","X","Y","Z", "Delta_X", "Delta_Y", "Delta_Z","Son_X","Son_Y","Son_Z"]
            write_cells(row, 0,write_list)
            row += 1

            for a in range(len(hel_son_list)):
                write_list = hel_dat_list[a] + hel_son_list[a]
                write_cells(row, 0 , write_list)
                write_last_part(row)
                row+=1

            write_list = []
            length_dat = len(hel_dat_list)
            length_data = length_dat-row+1
            for i in range(length_data):
                write_list = hel_dat_list[length_dat-length_data+i] + [0,0,0]
                write_cells(row,0 ,write_list)
                write_last_part(row)
                row += 1
            workbook.close()
            print(xls_path + " is written")

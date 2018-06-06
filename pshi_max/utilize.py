import re, os
import xlrd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.utility import xl_col_to_name

def read_def(ll):
    ll_list = re.split(r'\t+', ll)

    file_pth = ll_list[0]
    file_ext = ll_list[1]

    file_pth_list = list()
    for r, d, f in os.walk(file_pth):
        if d:
            for file in d:
                if not re.findall(r'(?:conv|grf|geom)', file):
                    file_pth_list.append(file)
            os.makedirs(r+"\\geom", exist_ok=True)
            break

    f_check = re.findall(r'(.*)\n+?', file_ext)
    if f_check:
        file_ext = f_check[0]
    return file_pth, file_ext, file_pth_list

def open_xls(xls_path):
    workbook = xlsxwriter.Workbook(xls_path)
    worksheet = workbook.add_worksheet('Data')
    cell_format1 = workbook.add_format()
    cell_format1.set_align('center')
    return workbook, worksheet, cell_format1

def write_cells(row,column,write_list, worksheet, cell_format1):
    for w in range(len(write_list)):
        worksheet.write(row, column+w , write_list[w],cell_format1)

def write_to_col(row,column,write_list, worksheet, cell_format1 ):
    for w in range(len(write_list)):
        worksheet.write(row+w, column, write_list[w],cell_format1)

def write_formulas(row, column, offset,start, worksheet, cell_format1):
    cell_val = xl_rowcol_to_cell(row, column)
    letter = xl_col_to_name(start)
    form_str = letter+'2:'+ letter + str(offset+1) +')'
    worksheet.write_formula(cell_val, '=MAX('+ form_str, cell_format1)
    cell_val = xl_rowcol_to_cell(row, column+1)
    worksheet.write_formula(cell_val, '=MIN('+ form_str, cell_format1)

def write_last_part(offset, worksheet, cell_format1):
    for i in range(6):
        write_formulas(1+i, 12, offset, 5+i, worksheet, cell_format1)

def read_file(current_path, file_ext):
    data_path = os.path.join(current_path, file_ext)
    file_data = open(data_path , "r", encoding='ANSI')
    return data_path, file_data

def extract_data(str_find, str_end, file_son):
    graf_check = False
    graf_son_list = list()
    for line in file_son:
        if graf_check:
            if re.findall(r''+str(str_end), line) or len(line.strip()) == 0:
                break
            line_list = line.split()
            line_list = [float(i) for i in line_list]
            graf_son_list.append(line_list)
        else:
            f_check = re.findall(r''+str(str_find), line)
            if f_check:
                graf_check = True
    return graf_son_list

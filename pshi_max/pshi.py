import re, os
from utilize import write_cells,write_to_col,write_formulas,write_last_part,read_file,extract_data, open_xls, read_def
import xlrd
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.utility import xl_col_to_name

gen_path = input("Enter the path: ")
define_file = open(gen_path , "r", encoding='ANSI')

for ll in define_file:
    file_pth, file_ext, file_pth_list = read_def(ll)
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
            son_path, file_son = read_file(current_path, "GRAFIK.SON")
            graf_son_list = extract_data('PSHI','end_length', file_son)

            dat_path, file_dat = read_file(current_path, "HEL.DAT")
            hel_dat_list =  extract_data('IBIT','BLOK',file_dat)
            hel_dat_list = [i[3] for i in hel_dat_list]

            list_number = re.findall(r'\d+', son_path)
            list_number = list_number[len(list_number)-1]
            xls_path = os.path.join(file_pth,"geom",file_ext +"_"+f_elem + "_" +list_number +".xlsx")
            workbook, worksheet, cell_format1 = open_xls(xls_path)
            row = 0
            start_column = 1
            write_list = ["Z","NOD","ACI(RAD)","ACI(DERECE)","TUR", "R", "C", "K","T","ETA","PSHI", " ", "MAX", "MIN"]
            write_list2 = ["R", "C", "K","T","ETA","PSHI"]
            write_to_col(1,0,hel_dat_list, worksheet, cell_format1)
            column = len(write_list)-3
            write_to_col(1,column,write_list2, worksheet, cell_format1)
            write_cells(row, start_column-1,write_list, worksheet, cell_format1)
            row += 1

            for son_data in graf_son_list:
                write_cells(row, start_column , son_data, worksheet, cell_format1)
                row+=1
            write_last_part(len(graf_son_list), worksheet, cell_format1)
            workbook.close()
            print(xls_path + " is written")

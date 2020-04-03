

def write_cse_file(cse_filename, res_filename, csv_filename):
    cse_file = open(cse_filename, "w")
	
    # read and write the header
    #
    temp_file = open("csefile_data_part1.dat", "r")
    for line in temp_file:
        cse_file.write(line)
    temp_file.close()
    
    # write the command for loading the results file
    cse_file.write("\n")
    cse_file.write(">load filename=" + res_filename + ", force_reload=true")
    cse_file.write("\n")
    cse_file.write("")

    temp_file = open("csefile_data_part2.dat", "r")
    for line in temp_file:
        cse_file.write(line)
    temp_file.close()

    # write the csv file name
    cse_file.write("")
    cse_file.write("  Export File = " + csv_filename)
    cse_file.write("\n")

    temp_file = open("csefile_data_part3.dat", "r")
    for line in temp_file:
        cse_file.write(line)

    temp_file.close()
    cse_file.close()
	
    return


#class CSEfile:
#    res_file = ""
#    csv_file = ""

#    set_result_filename(fname1):
#        res_file = fname1

#    set_csv_filename(fname1):
#        csv_file = fname1

#    write_file():
		

#if __name__ == '__main__':
#write_cse_file("cse_filename", "res_filename", "csv_filename")
		
		
		
		
		
		
		
		
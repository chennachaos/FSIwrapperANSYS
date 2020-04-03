

def write_ccl_file(ccl_filename, disp=0.0, velo=0.0):
    ccl_file = open(ccl_filename, "w")

    # read and write the header
    #
    temp_file = open("cclfile_data_part1.dat", "r")
    for line in temp_file:
        ccl_file.write(line)
    temp_file.close()
    
    # write the command for loading the results file
    ccl_file.write("       CylinDisp = %f  [cm]   \n"  % (disp) )
    ccl_file.write("       CylinVelo = %f  [cm/s] \n"  % (velo) )
    ccl_file.write("")

    temp_file = open("cclfile_data_part2.dat", "r")
    for line in temp_file:
        ccl_file.write(line)
    temp_file.close()

    temp_file.close()
    ccl_file.close()
	
    return

#if __name__ == '__main__':
#    write_ccl_file("ccl_filename", disp=1.0, velo=2.0)
		
		
		
		
		
		
		
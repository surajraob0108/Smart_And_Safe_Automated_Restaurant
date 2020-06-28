# -*- coding: utf-8 -*-
import csv
# the a is for append, if w for write is used then it overwrites the file
def write_to_csv():

    with open("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/Hospital_DataBase.csv","w") as log:
        patient_details_write = csv.writer(log, delimiter=",")
        patient_details_write.writerow(["Insurance number" , "Name" , "   Place"])
        patient_details_write.writerow(["717839425354","Mary Julia","Stuttgart"])
        #patient_details_write.writerow(["980018342470","James Anderson","Berlin"])
        patient_details_write.writerow(["80430249112","Jonathan Andrews","Munich"])
        patient_details_write.writerow(["1042928448371","Payal Singh","Ingolstadt"])
        #patient_details_write.writerow(["520994865728","Parmesh Kulkarni","HeidelBerg"])

def append_to_csv():

    with open("/home/pi/Public/Team16_Project/Sensors_Interface/Programs/Hospital_DataBase.csv","a") as log:
        patient_details_write = csv.writer(log, delimiter=",") #quotechar="”", quoting=csv.QUOTE_MINIMAL)
        patient_details_write.writerow(["520994865728","Parmesh Kulkarni","HeidelBerg"])

write_to_csv()
append_to_csv()
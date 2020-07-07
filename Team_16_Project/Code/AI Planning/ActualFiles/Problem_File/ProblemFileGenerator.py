import requests
import sys

MaskSensor = True
IDSensor = True
TempSensor  = True

def GenerateProblemPDDLFile(MaskSensor, IDSensor, TempSensor):
	ProbFile = open("D:\Rox stuff\Materials\Smart Cities and IoT\Exercise\SSSR_Repository\Team_16_Project\Code\AI Planning\ActualFiles\Problem_File\SSSR_ProblemFile.pddl","w+")
	ProbFile.write("(define\n\n(problem SSSR_CustomerAcceptance)\n\n(:domain SSSR)\n\n(:objects\tMask - mask\n\t\tID - RFID\n\t\tTemperature - temp\n\t\tMainDoor - door\n\t\tCustomer Manager - person\n)\n\n")
	ProbFile.write("(:init\t(IsCustomer Customer)\n\t\t(IsManager Manager)\n\t\t(IsDoor MainDoor)\n")
	if(MaskSensor == True):
		ProbFile.write("\t\t(MaskOkay Mask)\n")
	if(IDSensor == True):
		ProbFile.write("\t\t(HealthOkay ID)\n")
	if(TempSensor == True):
		ProbFile.write("\t\t(TempOkay Temperature)\n")
	ProbFile.write(")\n\n")
	ProbFile.write("(:goal\t(and (JudgeCustomer Customer)(not (IsDoorOpen MainDoor))(not (ManagerAlert Manager)) )\n) \n\n)")

def GetAIPlan():
	data = {'domain': open("D:\Rox stuff\Materials\Smart Cities and IoT\Exercise\SSSR_Repository\Team_16_Project\Code\AI Planning\ActualFiles\Domain_File\SSSR_DomainFile.pddl", 'r').read(),
    'problem' : open("D:\Rox stuff\Materials\Smart Cities and IoT\Exercise\SSSR_Repository\Team_16_Project\Code\AI Planning\ActualFiles\Problem_File\SSSR_ProblemFile.pddl", 'r').read()}
	
	response = requests.post('http://solver.planning.domains/solve', json = data).json()
	with open("D:\Rox stuff\Materials\Smart Cities and IoT\Exercise\SSSR_Repository\Team_16_Project\Code\AI Planning\ActualFiles\AI_Plans\AIPlan.txt", 'w') as f:
		for act in response['result']['plan']:
			f.write(str(act['name']))
			f.write('\n')
            
GenerateProblemPDDLFile(MaskSensor, IDSensor, TempSensor)
GetAIPlan()
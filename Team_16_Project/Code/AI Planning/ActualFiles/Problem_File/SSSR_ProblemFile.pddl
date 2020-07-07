(define

(problem SSSR_CustomerAcceptance)

(:domain SSSR)

(:objects	Mask - mask
		ID - RFID
		Temperature - temp
		MainDoor - door
		Customer Manager - person
)

(:init	(IsCustomer Customer)
		(IsManager Manager)
		(IsDoor MainDoor)
		(HealthOkay ID)
		(TempOkay Temperature)
)

(:goal	(and (JudgeCustomer Customer)(not (IsDoorOpen MainDoor))(not (ManagerAlert Manager)) )
) 

)
(define 

(problem SSSR_AllSensorsConfigured_Allow)

(:domain SSSR)

(:objects   Mask - mask 
            ID -RFID 
            Temperature - temp
            MainDoor - door
            Customer Manager - person
)

(:init      (IsCustomer Customer)
            (IsDoor MainDoor)
            (IsManager Manager)
            (MaskOkay Mask) 
            (HealthOkay ID) 
            (TempOkay Temperature)
)

(:goal      (and (JudgeCustomer Customer) (not (IsDoorOpen MainDoor)) (not (ManagerAlert Manager))  )
)

)
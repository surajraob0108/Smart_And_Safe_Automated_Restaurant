(define 

(problem SSSR_AllSensorsConfigured_Reject)

(:domain SSSR)

(:objects   Mask - mask 
            ID - RFID
            Temperature - temp
            MainDoor - door
            Customer Manager - person
)

(:init      (IsCustomer Customer)
            (IsManager Manager)
            (IsDoor MainDoor)
            (MaskOkay Mask)
            (HealthOkay ID)
)

(:goal      (and (JudgeCustomer Customer) (not (IsDoorOpen MainDoor)) (not (ManagerAlert Manager))  )
)

)
(define 
(domain SSSR)

(:requirements  [:adl][:strips][:typing])

(:types person sensor door - object
        Mask RFID Temp - sensor
)

(:predicates    (IsCustomer ?x - person)
                (IsManager ?x - person)
                (IsDoor ?x - door)
                (TempOkay ?x - temp)
                (MaskOkay ?x - mask)
                (HealthOkay ?x - RFID)
                (IsDoorOpen ?x - door)
                (JudgeCustomer ?x - person)
                (ManagerAlert ?x - person)
)

(:action Allow
    :parameters     (?v - mask ?w - RFID ?x - temp ?y - person ?z - door)
    :precondition   (and (IsCustomer ?y) (IsDoor ?z) (MaskOkay ?v) (HealthOkay ?w) (TempOkay ?x) (not (IsDoorOpen ?z)) (not (JudgeCustomer ?y))    )
    :effect         (IsDoorOpen ?z) 
)

(:action CloseDoor 
    :parameters     (?x - door ?y - person)
    :precondition   (IsDoorOpen ?x)
    :effect         (and (not (IsDoorOpen ?x)) (JudgeCustomer ?y)   ) 
)

(:action RejectID
    :parameters     (?u - mask ?v - RFID ?w - temp ?x ?y - person ?z - door)
    :precondition   (and (IsCustomer ?x) (IsManager ?y) (IsDoor ?z) (MaskOkay ?u) (not (HealthOkay ?v)) (TempOkay ?w) (not (IsDoorOpen ?z)) (not (ManagerAlert ?y)) (not (JudgeCustomer ?x))    )
    :effect         (ManagerAlert ?y)   
)

(:action RejectTemp
    :parameters     (?u - mask ?v - RFID ?w - temp ?x ?y - person ?z - door)
    :precondition   (and (IsCustomer ?x) (IsManager ?y) (IsDoor ?z) (MaskOkay ?u) (HealthOkay ?v) (not (TempOkay ?w)) (not (IsDoorOpen ?z)) (not (ManagerAlert ?y)) (not (JudgeCustomer ?x))    )
    :effect         (ManagerAlert ?y)   
)

(:action RejectMask
    :parameters     (?u - mask ?v - RFID ?w - temp ?x ?y - person ?z - door)
    :precondition   (and (IsCustomer ?x) (IsManager ?y) (IsDoor ?z) (not (MaskOkay ?u)) (HealthOkay ?v) (TempOkay ?w) (not (IsDoorOpen ?z)) (not (ManagerAlert ?y)) (not (JudgeCustomer ?x))    )
    :effect         (ManagerAlert ?y)   
)

(:action RejectIDandTemp
    :parameters     (?u - mask ?v - RFID ?w - temp ?x ?y - person ?z - door)
    :precondition   (and (IsCustomer ?x) (IsManager ?y) (IsDoor ?z) (MaskOkay ?u) (not (HealthOkay ?v)) (not (TempOkay ?w)) (not (IsDoorOpen ?z)) (not (ManagerAlert ?y)) (not (JudgeCustomer ?x))    )
    :effect         (ManagerAlert ?y)   
)

(:action RejectIDandMask
    :parameters     (?u - mask ?v - RFID ?w - temp ?x ?y - person ?z - door)
    :precondition   (and (IsCustomer ?x) (IsManager ?y) (IsDoor ?z) (not (MaskOkay ?u)) (not (HealthOkay ?v)) (TempOkay ?w) (not (IsDoorOpen ?z)) (not (ManagerAlert ?y)) (not (JudgeCustomer ?x))    )
    :effect         (ManagerAlert ?y)   
)

(:action RejectTempandMask
    :parameters     (?u - mask ?v - RFID ?w - temp ?x ?y - person ?z - door)
    :precondition   (and (IsCustomer ?x) (IsManager ?y) (IsDoor ?z) (not (MaskOkay ?u)) (HealthOkay ?v) (not (TempOkay ?w)) (not (IsDoorOpen ?z)) (not (ManagerAlert ?y)) (not (JudgeCustomer ?x))    )
    :effect         (ManagerAlert ?y)   
)

(:action RejectAll
    :parameters     (?u - mask ?v - RFID ?w - temp ?x ?y - person ?z - door)
    :precondition   (and (IsCustomer ?x) (IsManager ?y) (IsDoor ?z) (not (MaskOkay ?u)) (not (HealthOkay ?v)) (not (TempOkay ?w)) (not (IsDoorOpen ?z)) (not (ManagerAlert ?y)) (not (JudgeCustomer ?x))    )
    :effect         (ManagerAlert ?y)   
)

(:action Alert
    :parameters     (?x ?y - person)
    :precondition   (ManagerAlert ?x)
    :effect         (and (not (ManagerAlert ?x)) (JudgeCustomer ?y)    )
)

)
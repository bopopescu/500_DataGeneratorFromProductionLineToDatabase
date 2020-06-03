import mysql.connector
import datetime
import random

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="pilzdb"
)

mycursor = mydb.cursor()


###########################################################################

class ProductionLine:
    # Data for operators

    # operatorx = [name, PITmodeID, shift, levelTrain, nrOperator, correctWork(1 - correct, 0 - incorrect)]
    # operator0 = ["Nowak", "4005678", 0, 2, 0, 1]
    # operator1 = ["Pawlak", "4008221", 1, 1, 1, 1]
    # operator2 = ["Zieliński", "4003753", 2, 0, 2, 1]

    operator0 = ["Wójcik", "4001678", 0, 2, 0, 1]
    operator1 = ["Kowalski", "4001221", 1, 2, 1, 1]
    operator2 = ["Gańczak", "4001753", 2, 2, 2, 1]

    # operator0 = ["Bednarski", "4002678", 0, 2, 0, 1]
    # operator1 = ["Wiśniewski", "4002221", 1, 1, 1, 1]
    # operator2 = ["Czarnecki", "4002753", 2, 0, 2, 1]

    listOfOperators = [operator0, operator1, operator2]
    currentOperator = listOfOperators[0][2]

    # Data for Date
    myYear = 2020
    myMonth = 4
    myDay = 6
    myHour = 6
    myMinute = 0
    mySecond = 0
    startTime = datetime.datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond)
    endTime = datetime.datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond)
    currentTime = startTime
    currentShift = 0

    # Data for machine
    PILZ_PITmodeID = 0
    PILZ_PITmodeMode = 0
    PILZ_ESTOPStatus = 1
    PILZ_STOPButtonStatus = 0
    PILZ_STARTButtonStatus = 0
    PILZ_RESETButtonStatus = 0
    PILZ_PSENmlock1Status = 1
    PILZ_PSENmlock2Status = 1
    PILZ_MachineStatus = 0
    PILZ_ElementStatus = 0
    PILZ_PSENopt1 = 1
    PILZ_PSENopt2 = 1
    PILZ_PSENsgate = 1

    # Machine1_Probability = [ProbabilityOfCorrentPutElement, ProbabilityOfDropElement, ProbabilityOfDangerous, ProbabilityOfFaultSituation, SumOfProbabilities]
    # Machine1_Probability = [9499, 500, 5, 0, 0]
    Machine1_Probability = [9499, 500, 0, 0, 0]
    # Machine1_Probability = [9899, 100, 5, 0, 0]

    Machine1_Probability[4] = Machine1_Probability[0] + Machine1_Probability[1] + Machine1_Probability[2] + Machine1_Probability[3]
    Machine1_RandomValue = 0

    # Delays in seconds related with work shift
    # Delay_workShift = [firstShift, secondShift, thirdShift]
    Delay_workShift = [6, 2, 11]

    # Delays in seconds related with level of operator training
    # Delay_levelTraining = [level0, level1, level2] level 2 means that the operator has full skils
    Delay_levelTraining = [10, 6, 1]
    Delay_levelTrainingService = [60 * 10, 60 * 5, 60]

    # Delay when machine put element correctly
    Delay_machinePutElementCorrectly = 60 * 1
    # Delay when machine drop element
    Delay_machineDropElement = 60 * 4
    # Delay when machine is reparing
    Delay_serviceMachine = 60 * 60 * 3
    # Delay when occur dangerous situation
    Delay_machineDangerousSituation = 60 * 20
    # Delay preparing to work
    Delay_preparingToWOrk = 60 * 10
    # Delay related with end work
    Delay_endWork = 60 * 10
    # Delay test function
    Delay_testFunctions = 60 * 2
    # Delay when material is supplementing
    Delay_materialSupplement = 60 * 10

    stack_raw_material = 50

    # General statistic
    numberOfGoodElements = 0
    numberOfDropedElements = 0
    numberOfDangerousSituation = 0
    numberOfServiceWork = 0

    numberOfGoodElementsArray = [0, 0, 0]
    numberOfDropedElementsArray = [0, 0, 0]
    numberOfDangerousSituationArray = [0, 0, 0]
    numberOfServiceWorkArray = [0, 0, 0]

    numberOfGoodElementsArray2 = [0, 0, 0]
    numberOfDropedElementsArray2 = [0, 0, 0]
    numberOfDangerousSituationArray2 = [0, 0, 0]
    numberOfServiceWorkArray2 = [0, 0, 0]

    numberOfUseEmergencyStop = [0, 0, 0]

    numberOfRowInDatabase = 0

    def putDataToTheDatabase(self):
        txt = "INSERT INTO linia3 (id, date, time, machine_run, pitmode_id, pitmode_mode, estop, stop_button, start_button, reset_button, mlock_1, mlock_2) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
        print(txt.format("NULL", self.currentTime.strftime("%Y-%m-%d"), self.currentTime.strftime("%H:%M:%S"),
                         self.PILZ_MachineStatus, self.PILZ_PITmodeID, self.PILZ_PITmodeMode, self.PILZ_ESTOPStatus,
                         self.PILZ_STOPButtonStatus, self.PILZ_STARTButtonStatus, self.PILZ_RESETButtonStatus,
                         self.PILZ_PSENmlock1Status, self.PILZ_PSENmlock2Status))
        # mycursor.execute(txt.format("NULL", self.currentTime.strftime("%Y-%m-%d"), self.currentTime.strftime("%H:%M:%S"), self.PILZ_MachineStatus, self.PILZ_PITmodeID, self.PILZ_PITmodeMode, self.PILZ_ESTOPStatus, self.PILZ_STOPButtonStatus, self.PILZ_STARTButtonStatus, self.PILZ_RESETButtonStatus, self.PILZ_PSENmlock1Status, self.PILZ_PSENmlock2Status))
        # mydb.commit()
        # txt = "Zapisanie w bazie danych: id {}; date {}; time {};  machinerun {}; pitmodeid {}; pitmodemode {}; estop {}; stopbutton {}; startbutton {}; resetbutton {}; mlock1 {}; mlock2 {}"
        # print(txt.format("NULL", self.currentTime.strftime("%Y-%m-%d"), self.currentTime.strftime("%H:%M:%S"), self.PILZ_MachineStatus, self.PILZ_PITmodeID, self.PILZ_PITmodeMode, self.PILZ_ESTOPStatus, self.PILZ_STOPButtonStatus, self.PILZ_STARTButtonStatus, self.PILZ_RESETButtonStatus, self.PILZ_PSENmlock1Status, self.PILZ_PSENmlock2Status))
        self.numberOfRowInDatabase += 1

    def changeMachine1Status(self):
        if self.PILZ_MachineStatus == 0:
            self.PILZ_MachineStatus = 1
        elif self.PILZ_MachineStatus == 1:
            self.PILZ_MachineStatus = 0
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_machine_run", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_MachineStatus))
        # mycursor.execute(txt.format("line3_machine_run", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_MachineStatus))
        # mydb.commit()

    def changePITmodeID(self, operator):
        if self.PILZ_PITmodeID == operator[1]:
            self.PILZ_PITmodeID = 0
        else:
            self.PILZ_PITmodeID = operator[1]
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_pitmode_id", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_PITmodeID))
        # mycursor.execute(txt.format("line3_pitmode_id", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_PITmodeID))
        # mydb.commit()

    def changePITmodeMode(self, mode):
        self.PILZ_PITmodeMode = mode
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_pitmode_mode", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_PITmodeMode))
        # mycursor.execute(txt.format("line3_pitmode_mode", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_PITmodeMode))
        # mydb.commit()

    def changeESTOPStatus(self):
        if self.PILZ_ESTOPStatus == 0:
            self.PILZ_ESTOPStatus = 1
            self.statisticUseOfEmergencyStop()
        elif self.PILZ_ESTOPStatus == 1:
            self.PILZ_ESTOPStatus = 0
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_estop", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_ESTOPStatus))
        # mycursor.execute(txt.format("line3_estop", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_ESTOPStatus))
        # mydb.commit()

    def changeSTOPButtonStatus(self):
        self.PILZ_STOPButtonStatus = 1
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_stop_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_ESTOPStatus))
        # mycursor.execute(txt.format("line3_stop_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_ESTOPStatus))
        # mydb.commit()
        self.addConstantTime(1)
        self.PILZ_STOPButtonStatus = 0
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_stop_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_ESTOPStatus))
        # mycursor.execute(txt.format("line3_stop_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_ESTOPStatus))
        # mydb.commit()

    def changeSTARTButtonStatus(self):
        self.PILZ_STARTButtonStatus = 1
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_start_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_STARTButtonStatus))
        # mycursor.execute(txt.format("line3_start_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_STARTButtonStatus))
        # mydb.commit()
        self.PILZ_STARTButtonStatus = 0
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_start_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_STARTButtonStatus))
        # mycursor.execute(txt.format("line3_start_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_STARTButtonStatus))
        # mydb.commit()

    def changeRESETButtonStatus(self):
        self.PILZ_RESETButtonStatus = 1
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_reset_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_RESETButtonStatus))
        # mycursor.execute(txt.format("line3_reset_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_RESETButtonStatus))
        # mydb.commit()
        self.PILZ_RESETButtonStatus = 0
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_reset_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_RESETButtonStatus))
        # mycursor.execute(txt.format("line3_reset_button", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_RESETButtonStatus))
        # mydb.commit()

    def changePSENmlock1Status(self):
        if self.PILZ_PSENmlock1Status == 0:
            self.PILZ_PSENmlock1Status = 1
        elif self.PILZ_PSENmlock1Status == 1:
            self.PILZ_PSENmlock1Status = 0
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_mlock_1", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_PSENmlock1Status))
        # mycursor.execute(txt.format("line3_mlock_1", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_PSENmlock1Status))
        # mydb.commit()

    def changePSENmlock2Status(self):
        if self.PILZ_PSENmlock2Status == 0:
            self.PILZ_PSENmlock2Status = 1
        elif self.PILZ_PSENmlock2Status == 1:
            self.PILZ_PSENmlock2Status = 0
        self.addConstantTime(1)
        # self.putDataToTheDatabase()
        txt = "INSERT INTO {} (id, date_time, value) VALUES ('{}', '{}', '{}');"
        print(txt.format("line3_mlock_2", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                         self.PILZ_PSENmlock2Status))
        # mycursor.execute(txt.format("line3_mlock_2", "NULL", self.currentTime.strftime("%Y-%m-%d %H:%M:%S"),
                                    # self.PILZ_PSENmlock2Status))
        # mydb.commit()

    def addRandomTime(self, rangeDelayTime):
        delta_time = datetime.timedelta(seconds=random.randint(0, rangeDelayTime))
        self.currentTime = self.currentTime + delta_time

    def addConstantTime(self, constantTime):
        delta_time = datetime.timedelta(seconds=constantTime)
        self.currentTime = self.currentTime + delta_time

    def addRCTime(self, consDelay, alterDelay):
        self.addConstantTime(consDelay)
        self.addRandomTime(alterDelay)

    def setStartDateAndTime(self, myYear, myMonth, myDay, myHour, myMinute, mySecond):
        self.startTime = datetime.datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond)

    def setEndDateAndTime(self, myYear, myMonth, myDay, myHour, myMinute, mySecond):
        self.endTime = datetime.datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond)

    def receivingElement(self):
        self.addConstantTime(self.Delay_machinePutElementCorrectly)
        self.addRandomTime(self.Delay_levelTraining[self.currentOperator[3]])
        self.addRandomTime(self.Delay_workShift[self.currentShift])

    def receivingElementIncorrect(self):
        self.addConstantTime(self.Delay_machinePutElementCorrectly / 2)
        self.addRandomTime(self.Delay_levelTraining[self.currentOperator[3]])
        self.addRandomTime(self.Delay_workShift[self.currentShift])

    def dropWork(self):
        self.addConstantTime(self.Delay_machineDropElement)
        self.addRandomTime(self.Delay_levelTraining[self.currentOperator[3]])
        self.addRandomTime(self.Delay_workShift[self.currentShift])

    def serviceWork(self):
        self.addConstantTime(self.Delay_serviceMachine)
        self.addRandomTime(self.Delay_levelTraining[self.currentOperator[3]])
        self.addRandomTime(self.Delay_workShift[self.currentShift])

    def occurDangerousSituation(self):
        self.addConstantTime(self.Delay_machineDangerousSituation)

    def delayTestFunction(self):
        self.addConstantTime(self.Delay_testFunctions)

    def delayMaterialSupplement(self):
        self.addConstantTime(self.Delay_materialSupplement)
        self.addRandomTime(self.Delay_levelTraining[self.currentOperator[3]])
        self.addRandomTime(self.Delay_workShift[self.currentShift])

    def delayMaterialSupplementIncorrect(self):
        self.addConstantTime(self.Delay_materialSupplement / 2)
        self.addRandomTime(self.Delay_levelTraining[self.currentOperator[3]])
        self.addRandomTime(self.Delay_workShift[self.currentShift])


    def setShift(self):
        timeStart1Shift = (6 * 60 * 60)
        timeStart2Shift = (14 * 60 * 60)
        timeStart3Shift = (22 * 60 * 60)
        myShiftTime = (int(self.currentTime.strftime("%H")) * 60 * 60) + (int(self.currentTime.strftime("%M")) * 60) + (
            int(self.currentTime.strftime("%S")))
        if ((myShiftTime >= timeStart1Shift) and (myShiftTime < timeStart2Shift)):
            # print("Shift 1")
            self.currentShift = 0
        elif ((myShiftTime >= timeStart2Shift) and (myShiftTime < timeStart3Shift)):
            # print("Shift 2")
            self.currentShift = 1
        elif ((myShiftTime >= timeStart3Shift) or (myShiftTime < timeStart1Shift)):
            # print("Shift 3")
            self.currentShift = 2

    def setCurrentOperator(self):
        for i in self.listOfOperators:
            if i[2] == self.currentShift:
                self.currentOperator = i

    def resetParameters(self):
        self.currentTime = self.startTime
        self.setShift()
        self.setCurrentOperator()

    def operatorStartWork(self):
        self.addConstantTime(self.Delay_preparingToWOrk)

    def operatorEndWork(self):
        self.addConstantTime(self.Delay_endWork)

    def setRandomValueForMachine(self):
        self.Machine1_RandomValue = random.randint(0, self.Machine1_Probability[4])
        print(self.Machine1_RandomValue)

    def procedureOfCorrectWork(self):
        self.changeSTOPButtonStatus()
        self.changeMachine1Status()
        self.changePSENmlock1Status()
        self.receivingElement()
        self.changeSTARTButtonStatus()
        self.changePSENmlock1Status()
        self.changeMachine1Status()

    def procedureOfIncorrectWork(self):
        self.changeESTOPStatus()
        self.changeMachine1Status()
        self.changePSENmlock1Status()
        self.changePSENmlock2Status()
        self.receivingElementIncorrect()
        self.changeESTOPStatus()
        self.changeRESETButtonStatus()
        self.changePSENmlock1Status()
        self.changePSENmlock2Status()
        self.changeSTARTButtonStatus()
        self.changeMachine1Status()

    def procedureOfServiceWork(self):
        self.changeSTOPButtonStatus()
        self.changeMachine1Status()
        self.changePSENmlock1Status()
        self.changePITmodeMode(2)
        self.changePSENmlock2Status()
        self.serviceWork()
        self.changePITmodeMode(1)
        self.changePSENmlock2Status()
        self.changeRESETButtonStatus()
        self.changeSTARTButtonStatus()
        self.changePSENmlock1Status()
        self.changeMachine1Status()

    def procedureOfEmergencyWork(self):
        self.changeESTOPStatus()
        self.changeMachine1Status()
        self.changePSENmlock1Status()
        self.changePSENmlock2Status()
        self.occurDangerousSituation()
        self.changeESTOPStatus()
        self.changeRESETButtonStatus()
        self.changePSENmlock1Status()
        self.changePSENmlock2Status()
        self.changeSTARTButtonStatus()
        self.changeMachine1Status()

    def procedureOfTestEmergencyStop(self):
        self.changeESTOPStatus()
        self.changeMachine1Status()
        self.changePSENmlock1Status()
        self.changePSENmlock2Status()
        self.changeESTOPStatus()
        self.changeRESETButtonStatus()
        self.changePSENmlock1Status()
        self.changePSENmlock2Status()
        self.changeSTARTButtonStatus()
        self.changeMachine1Status()

    def procedureOfStartWork(self):
        self.operatorStartWork()
        self.changePITmodeID(self.currentOperator)
        self.changePITmodeMode(1)
        self.changeRESETButtonStatus()
        self.changeSTARTButtonStatus()
        self.changeMachine1Status()

    def procedureOfEndWork(self):
        self.changeSTOPButtonStatus()
        self.changeMachine1Status()
        self.changePITmodeID(self.currentOperator)
        self.operatorEndWork()





    #################################################################

    def putDataInDatabasev2(self):
        txt = "INSERT INTO `v5_line1` (`id`, `date_time`, `date`, `time`, `pitmode_id`, `pitmode_mode`, `operator_name`, `training_level`, `Estop`, `Lbarier1`, `Lbarier2`, `Machine_run`, `button_stop`, `button_start`, `button_reset`, `sgate`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');"
        print(txt.format(self.currentTime.strftime("%Y-%m-%d %H:%M:%S"), self.currentTime.strftime("%Y-%m-%d"), self.currentTime.strftime("%H:%M:%S"), self.PILZ_PITmodeID, self.PILZ_PITmodeMode, self.currentOperator[0], self.currentOperator[3], self.PILZ_ESTOPStatus, self.PILZ_PSENopt1, self.PILZ_PSENopt2, self.PILZ_MachineStatus, self.PILZ_STOPButtonStatus, self.PILZ_STARTButtonStatus, self.PILZ_RESETButtonStatus, self.PILZ_PSENsgate))
        mycursor.execute(txt.format(self.currentTime.strftime("%Y-%m-%d %H:%M:%S"), self.currentTime.strftime("%Y-%m-%d"), self.currentTime.strftime("%H:%M:%S"), self.PILZ_PITmodeID, self.PILZ_PITmodeMode, self.currentOperator[0], self.currentOperator[3], self.PILZ_ESTOPStatus, self.PILZ_PSENopt1, self.PILZ_PSENopt2, self.PILZ_MachineStatus, self.PILZ_STOPButtonStatus, self.PILZ_STARTButtonStatus, self.PILZ_RESETButtonStatus, self.PILZ_PSENsgate))
        mydb.commit()
        self.numberOfRowInDatabase += 1

    def setupRESETButtonStatus(self, status):
        self.PILZ_RESETButtonStatus = status
        if status == 1:
            self.putDataInDatabasev2()
        else:
            nic = 1
        self.PILZ_RESETButtonStatus = 0
        self.addConstantTime(1)

    def setupSTARTButtonStatus(self, status):
        self.PILZ_STARTButtonStatus = status
        if status == 1:
            self.putDataInDatabasev2()
        else:
            nic = 1
        self.PILZ_STARTButtonStatus = 0
        self.addConstantTime(1)

    def setupSTOPButtonStatus(self, status):
        self.PILZ_STOPButtonStatus = status
        if status == 1:
            self.putDataInDatabasev2()
        else:
            nic = 1
        self.PILZ_STOPButtonStatus = 0
        self.addConstantTime(1)

    def setupMachineStatus(self, status):
        self.PILZ_MachineStatus = status
        if status == 1:
            self.putDataInDatabasev2()
        else:
            self.putDataInDatabasev2()
        self.addConstantTime(1)

    def setupLightCurtain1Status(self, status):
        self.PILZ_PSENopt1 = status
        if status == 1:
            nic = 0
        else:
            self.putDataInDatabasev2()
        self.PILZ_PSENopt1 = 1
        self.addConstantTime(1)

    def setupLightCurtain2Status(self, status):
        self.PILZ_PSENopt2 = status
        if status == 1:
            nic = 0
        else:
            self.putDataInDatabasev2()
        self.PILZ_PSENopt2 = 1
        self.addConstantTime(1)

    def setupSgateStatus(self, status):
        self.PILZ_PSENsgate = status
        if status == 1:
            nic = 0
        else:
            self.putDataInDatabasev2()
        self.PILZ_PSENsgate = 1
        self.addConstantTime(1)

    def setupESTOPStatus(self, status):
        self.PILZ_ESTOPStatus = status
        self.statisticUseOfEmergencyStop()
        if status == 1:
            nic = 0
        else:
            self.putDataInDatabasev2()
        self.PILZ_ESTOPStatus = 1
        self.addConstantTime(1)

    def setupPITmodeMode(self, status):
        self.PILZ_PITmodeMode = status
        self.putDataInDatabasev2()
        self.addConstantTime(1)

    def setupPITmodeID(self, operator):
        self.PILZ_PITmodeID = operator[1]
        self.putDataInDatabasev2()
        self.addConstantTime(1)



    def procedureOfStartWorkv2(self):
        self.operatorStartWork()
        self.setupPITmodeID(self.currentOperator)
        self.setupPITmodeMode(1)
        if self.currentOperator[3] == 3:
            self.procedureOfTestESTOPv2()
            self.procedureOfTestLightCurtain1v2()
            self.procedureOfTestLightCurtain2v2()
            self.procedureOfTestSgatev2()
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

    def procedureOfNormalWorkv2(self):
        self.setupLightCurtain1Status(1)
        self.setupLightCurtain1Status(0)
        self.receivingElement()
        self.setupLightCurtain2Status(1)
        self.setupLightCurtain2Status(0)

        self.stack_raw_material = self.stack_raw_material - 1
        self.statisticOfCorrectWork()

    def procedureOfDropElementCorrectWorkv2(self):
        self.setupLightCurtain1Status(0)
        self.setupLightCurtain1Status(1)
        self.setupSTOPButtonStatus(1)
        self.setupMachineStatus(0)
        self.setupPITmodeMode(2)
        self.setupSgateStatus(0)
        self.dropWork()
        self.setupPITmodeMode(1)
        self.setupSgateStatus(1)
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

        self.statisticOfServiceWork()

    def procedureOfDropElementIncorrectWorkv2(self):
        self.setupLightCurtain1Status(0)
        self.setupLightCurtain1Status(1)
        self.setupSTOPButtonStatus(1)
        self.setupMachineStatus(0)
        self.setupESTOPStatus(0)
        self.setupPITmodeMode(2)
        self.setupSgateStatus(0)
        self.dropWork()
        self.setupPITmodeMode(1)
        self.setupSgateStatus(1)
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

        self.statisticOfServiceWork()

    def procedureOfDangerousSituationv2(self):
        self.setupESTOPStatus(0)
        self.setupMachineStatus(0)
        self.setupSgateStatus(0)
        self.setupPITmodeMode(4)
        self.occurDangerousSituation()
        self.setupPITmodeMode(1)
        self.setupESTOPStatus(1)
        self.setupRESETButtonStatus(1)
        self.setupSgateStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

        self.Machine1_Probability[3] = self.Machine1_Probability[3] + 10
        self.Machine1_Probability[4] = self.Machine1_Probability[0] + self.Machine1_Probability[1] + self.Machine1_Probability[2] + self.Machine1_Probability[3]

        self.statisticOfEmergencyWork()

    def procedureOfFaultOccurev2(self):
        self.setupPITmodeMode(3)
        self.setupMachineStatus(0)
        self.serviceWork()
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)
        self.procedureOfTestESTOPv2()
        self.procedureOfTestLightCurtain1v2()
        self.procedureOfTestLightCurtain2v2()
        self.procedureOfTestSgatev2()
        self.setupPITmodeMode(1)
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

        self.Machine1_Probability[3] = 0
        self.Machine1_Probability[4] = self.Machine1_Probability[0] + self.Machine1_Probability[1] + \
                                       self.Machine1_Probability[2] + self.Machine1_Probability[3]

        self.statisticOfRepairWork()

    def procedureOfMaterialSupplementCorrectWorkv2(self):
        self.setupSTOPButtonStatus(0)
        self.setupMachineStatus(0)
        self.delayMaterialSupplement()
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)
        self.stack_raw_material = 50

    def procedureOfMaterialSupplementIncorrectWorkv2(self):
        self.setupESTOPStatus(0)
        self.setupMachineStatus(0)
        self.setupSgateStatus(0)
        self.delayMaterialSupplementIncorrect()
        self.setupESTOPStatus(1)
        self.setupRESETButtonStatus(1)
        self.setupSgateStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

        self.stack_raw_material = 50
        self.Machine1_Probability[3] = self.Machine1_Probability[3] + 100
        self.Machine1_Probability[4] = self.Machine1_Probability[0] + self.Machine1_Probability[1] + \
                                       self.Machine1_Probability[2] + self.Machine1_Probability[3]

    def procedureOfEndWorkv2(self):
        self.setupSTOPButtonStatus(1)
        self.setupMachineStatus(0)
        self.setupPITmodeMode(0)
        self.setupPITmodeID(-1)
        self.operatorEndWork()

    def procedureOfTestESTOPv2(self):
        self.setupSTOPButtonStatus(1)
        self.setupMachineStatus(0)
        self.setupESTOPStatus(0)
        self.setupSgateStatus(0)
        self.delayTestFunction()
        self.setupESTOPStatus(1)
        self.setupRESETButtonStatus(1)
        self.setupSgateStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

    def procedureOfTestLightCurtain1v2(self):
        self.setupLightCurtain1Status(0)
        self.setupLightCurtain1Status(1)
        self.setupMachineStatus(0)
        self.delayTestFunction()
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

    def procedureOfTestLightCurtain2v2(self):
        self.setupLightCurtain2Status(0)
        self.setupLightCurtain2Status(1)
        self.setupMachineStatus(0)
        self.delayTestFunction()
        self.setupRESETButtonStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)

    def procedureOfTestSgatev2(self):
        self.setupSgateStatus(0)
        self.setupMachineStatus(0)
        self.delayTestFunction()
        self.setupRESETButtonStatus(1)
        self.setupSgateStatus(1)
        self.setupSTARTButtonStatus(1)
        self.setupMachineStatus(1)




    def statisticOfCorrectWork(self):
        self.numberOfGoodElements += 1
        if self.currentShift == 0:
            self.numberOfGoodElementsArray[self.currentShift] += 1
        elif self.currentShift == 1:
            self.numberOfGoodElementsArray[self.currentShift] += 1
        elif self.currentShift == 2:
            self.numberOfGoodElementsArray[self.currentShift] += 1

        if self.currentOperator[4] == 0:
            self.numberOfGoodElementsArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 1:
            self.numberOfGoodElementsArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 2:
            self.numberOfGoodElementsArray2[self.currentOperator[4]] += 1

    def statisticOfServiceWork(self):
        self.numberOfDropedElements += 1
        if self.currentShift == 0:
            self.numberOfDropedElementsArray[self.currentShift] += 1
        elif self.currentShift == 1:
            self.numberOfDropedElementsArray[self.currentShift] += 1
        elif self.currentShift == 2:
            self.numberOfDropedElementsArray[self.currentShift] += 1

        if self.currentOperator[4] == 0:
            self.numberOfDropedElementsArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 1:
            self.numberOfDropedElementsArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 2:
            self.numberOfDropedElementsArray2[self.currentOperator[4]] += 1

    def statisticOfEmergencyWork(self):
        self.numberOfDangerousSituation += 1
        if self.currentShift == 0:
            self.numberOfDangerousSituationArray[self.currentShift] += 1
        elif self.currentShift == 1:
            self.numberOfDangerousSituationArray[self.currentShift] += 1
        elif self.currentShift == 2:
            self.numberOfDangerousSituationArray[self.currentShift] += 1

        if self.currentOperator[4] == 0:
            self.numberOfDangerousSituationArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 1:
            self.numberOfDangerousSituationArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 2:
            self.numberOfDangerousSituationArray2[self.currentOperator[4]] += 1

    def statisticUseOfEmergencyStop(self):
        if self.currentOperator[4] == 0:
            self.numberOfUseEmergencyStop[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 1:
            self.numberOfUseEmergencyStop[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 2:
            self.numberOfUseEmergencyStop[self.currentOperator[4]] += 1

    def statisticOfRepairWork(self):
        self.numberOfServiceWork += 1
        if self.currentShift == 0:
            self.numberOfServiceWorkArray[self.currentShift] += 1
        elif self.currentShift == 1:
            self.numberOfServiceWorkArray[self.currentShift] += 1
        elif self.currentShift == 2:
            self.numberOfServiceWorkArray[self.currentShift] += 1

        if self.currentOperator[4] == 0:
            self.numberOfServiceWorkArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 1:
            self.numberOfServiceWorkArray2[self.currentOperator[4]] += 1
        elif self.currentOperator[4] == 2:
            self.numberOfServiceWorkArray2[self.currentOperator[4]] += 1


productionLine1 = ProductionLine()

# initial parameters
productionLine1.setStartDateAndTime(2020, 4, 6, 6, 0, 0)
productionLine1.setEndDateAndTime(2020, 4, 11, 6, 0, 0)
productionLine1.operator0[2] = 0  # zmiana I
productionLine1.operator1[2] = 1  # zmiana II
productionLine1.operator2[2] = 2  # zmiana III
productionLine1.resetParameters()

while productionLine1.currentTime < productionLine1.endTime:
    productionLine1.setShift()
    productionLine1.setCurrentOperator()
    productionLine1.procedureOfStartWorkv2()
    while 1:
        oldShift = productionLine1.currentShift
        productionLine1.setShift()
        if oldShift != productionLine1.currentShift:
            productionLine1.procedureOfEndWork()
            break
        else:
            if productionLine1.stack_raw_material <= 0:
                # procedura napełniania
                if productionLine1.currentOperator[3] >= 1:
                    # napełnianie prawidłowe
                    productionLine1.procedureOfMaterialSupplementCorrectWorkv2()
                else:
                    # napełnianie nieprawidłowe
                    productionLine1.procedureOfMaterialSupplementIncorrectWorkv2()
            else:
                productionLine1.setRandomValueForMachine()
                if productionLine1.Machine1_RandomValue <= productionLine1.Machine1_Probability[0]:
                    # Normalna praca
                    productionLine1.procedureOfNormalWorkv2()
                elif productionLine1.Machine1_RandomValue > productionLine1.Machine1_Probability[0] and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1]):
                    # Upadek detalu w strefie
                    if productionLine1.currentOperator[3] > 1:
                        # prawidłowa praca
                        productionLine1.procedureOfDropElementCorrectWorkv2()
                    else:
                        # nieprawidłowa praca
                        productionLine1.procedureOfDropElementIncorrectWorkv2()
                elif productionLine1.Machine1_RandomValue > (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1]) and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2]):
                    # niebezpieczna sytuacja
                    productionLine1.procedureOfDangerousSituationv2()
                elif productionLine1.Machine1_RandomValue > (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2]) and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2] + productionLine1.Machine1_Probability[3]):
                    # Ustarka
                    productionLine1.procedureOfFaultOccurev2()




# initial parameters
productionLine1.setStartDateAndTime(2020, 4, 13, 6, 0, 0)
productionLine1.setEndDateAndTime(2020, 4, 18, 6, 0, 0)
productionLine1.operator0[2] = 1
productionLine1.operator1[2] = 2
productionLine1.operator2[2] = 0
productionLine1.resetParameters()

while productionLine1.currentTime < productionLine1.endTime:
    productionLine1.setShift()
    productionLine1.setCurrentOperator()
    productionLine1.procedureOfStartWorkv2()
    while 1:
        oldShift = productionLine1.currentShift
        productionLine1.setShift()
        if oldShift != productionLine1.currentShift:
            productionLine1.procedureOfEndWork()
            break
        else:
            if productionLine1.stack_raw_material <= 0:
                # procedura napełniania
                if productionLine1.currentOperator[3] >= 1:
                    # napełnianie prawidłowe
                    productionLine1.procedureOfMaterialSupplementCorrectWorkv2()
                else:
                    # napełnianie nieprawidłowe
                    productionLine1.procedureOfMaterialSupplementIncorrectWorkv2()
            else:
                productionLine1.setRandomValueForMachine()
                if productionLine1.Machine1_RandomValue <= productionLine1.Machine1_Probability[0]:
                    # Normalna praca
                    productionLine1.procedureOfNormalWorkv2()
                elif productionLine1.Machine1_RandomValue > productionLine1.Machine1_Probability[0] and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1]):
                    # Upadek detalu w strefie
                    if productionLine1.currentOperator[3] > 1:
                        # prawidłowa praca
                        productionLine1.procedureOfDropElementCorrectWorkv2()
                    else:
                        # nieprawidłowa praca
                        productionLine1.procedureOfDropElementIncorrectWorkv2()
                elif productionLine1.Machine1_RandomValue > (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1]) and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2]):
                    # niebezpieczna sytuacja
                    productionLine1.procedureOfDangerousSituationv2()
                elif productionLine1.Machine1_RandomValue > (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2]) and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2] + productionLine1.Machine1_Probability[3]):
                    # Ustarka
                    productionLine1.procedureOfFaultOccurev2()

# initial parameters
productionLine1.setStartDateAndTime(2020, 4, 20, 6, 0, 0)
productionLine1.setEndDateAndTime(2020, 4, 25, 6, 0, 0)
productionLine1.operator0[2] = 2
productionLine1.operator1[2] = 0
productionLine1.operator2[2] = 1
productionLine1.resetParameters()

while productionLine1.currentTime < productionLine1.endTime:
    productionLine1.setShift()
    productionLine1.setCurrentOperator()
    productionLine1.procedureOfStartWorkv2()
    while 1:
        oldShift = productionLine1.currentShift
        productionLine1.setShift()
        if oldShift != productionLine1.currentShift:
            productionLine1.procedureOfEndWork()
            break
        else:
            if productionLine1.stack_raw_material <= 0:
                # procedura napełniania
                if productionLine1.currentOperator[3] >= 1:
                    # napełnianie prawidłowe
                    productionLine1.procedureOfMaterialSupplementCorrectWorkv2()
                else:
                    # napełnianie nieprawidłowe
                    productionLine1.procedureOfMaterialSupplementIncorrectWorkv2()
            else:
                productionLine1.setRandomValueForMachine()
                if productionLine1.Machine1_RandomValue <= productionLine1.Machine1_Probability[0]:
                    # Normalna praca
                    productionLine1.procedureOfNormalWorkv2()
                elif productionLine1.Machine1_RandomValue > productionLine1.Machine1_Probability[0] and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1]):
                    # Upadek detalu w strefie
                    if productionLine1.currentOperator[3] > 1:
                        # prawidłowa praca
                        productionLine1.procedureOfDropElementCorrectWorkv2()
                    else:
                        # nieprawidłowa praca
                        productionLine1.procedureOfDropElementIncorrectWorkv2()
                elif productionLine1.Machine1_RandomValue > (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1]) and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2]):
                    # niebezpieczna sytuacja
                    productionLine1.procedureOfDangerousSituationv2()
                elif productionLine1.Machine1_RandomValue > (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2]) and productionLine1.Machine1_RandomValue <= (productionLine1.Machine1_Probability[0] + productionLine1.Machine1_Probability[1] + productionLine1.Machine1_Probability[2] + productionLine1.Machine1_Probability[3]):
                    # Ustarka
                    productionLine1.procedureOfFaultOccurev2()

# mydb.commit()

txt = "Sumarycznie: Dobre elementy {}, Upadek detalu {}, Sytuacje awaryjne {}, serwis {}"
print(txt.format(productionLine1.numberOfGoodElements, productionLine1.numberOfDropedElements,
                 productionLine1.numberOfDangerousSituation, productionLine1.numberOfServiceWork))

txt = "Zmiana I: Dobre elementy {}, Upadek detalu {}, Sytuacje awaryjne {}, serwis {}"
print(txt.format(productionLine1.numberOfGoodElementsArray[0], productionLine1.numberOfDropedElementsArray[0],
                 productionLine1.numberOfDangerousSituationArray[0], productionLine1.numberOfServiceWorkArray[0]))

txt = "Zmiana II: Dobre elementy {}, Upadek detalu {}, Sytuacje awaryjne {}, serwis {}"
print(txt.format(productionLine1.numberOfGoodElementsArray[1], productionLine1.numberOfDropedElementsArray[1],
                 productionLine1.numberOfDangerousSituationArray[1], productionLine1.numberOfServiceWorkArray[1]))

txt = "Zmiana III: Dobre elementy {}, Upadek detalu {}, Sytuacje awaryjne {}, serwis {}"
print(txt.format(productionLine1.numberOfGoodElementsArray[2], productionLine1.numberOfDropedElementsArray[2],
                 productionLine1.numberOfDangerousSituationArray[2], productionLine1.numberOfServiceWorkArray[2]))

txt = "Operator I: Dobre elementy {}, Upadek detalu {}, Sytuacje awaryjne {}, serwis {}"
print(txt.format(productionLine1.numberOfGoodElementsArray2[0], productionLine1.numberOfDropedElementsArray2[0],
                 productionLine1.numberOfDangerousSituationArray2[0], productionLine1.numberOfServiceWorkArray2[0]))

txt = "Operator II: Dobre elementy {}, Upadek detalu {}, Sytuacje awaryjne {}, serwis {}"
print(txt.format(productionLine1.numberOfGoodElementsArray2[1], productionLine1.numberOfDropedElementsArray2[1],
                 productionLine1.numberOfDangerousSituationArray2[1], productionLine1.numberOfServiceWorkArray2[1]))

txt = "Operator III: Dobre elementy {}, Upadek detalu {}, Sytuacje awaryjne {}, serwis {}"
print(txt.format(productionLine1.numberOfGoodElementsArray2[2], productionLine1.numberOfDropedElementsArray2[2],
                 productionLine1.numberOfDangerousSituationArray2[2], productionLine1.numberOfServiceWorkArray2[2]))

txt = "Emergency STOP: Operator I - {}, Operator II - {}, Operator III - {}"
print(txt.format(productionLine1.numberOfUseEmergencyStop[0], productionLine1.numberOfUseEmergencyStop[1],
                 productionLine1.numberOfUseEmergencyStop[2]))

txt = "Liczba rekordów: {}"
print(txt.format(productionLine1.numberOfRowInDatabase))

# Requirements
    # pricing 
    # quantity
    # due date
    # process
    # material
    # Ship to and from or just to
    # QC + tolerances
    # CO2
    # Certifications

# Constraints
    # Hard
        # Boolean
    # Soft
        # Cost
            # Less than or equal to
        # Benefit
            # more than or equal to 
    # Interval
        # Minimum
        # Optimal
        # Maximum

# Objective
    # maximise satisfaction
        # Sum of weights * decision variable values

# Weights for soft and interval constraints

# Penalties
    # Late 
    # Cancellation
    # Poor quality


class Requirement():

    def __init__(self,requirementName,requirementType,weight,constraint):
        self.requirementName = requirementName
        self.requirementType = requirementType
        self.weight = weight
        self.constraint = constraint

    def __str__(self):
        return "Name {} - Type {} - Weight {} - Constraint {}".format(self.requirementName,self.requirementName,self.weight,self.constraint)

    def weightedScore(self,value,min,max):
        return self.score(value,min,max)*self.weight
    

    def score(self,value,min,max):
        if(self.requirementType == 'hard'):
            return self.hardScore(value,self.constraint)
        elif(self.requirementType == 'interval'):
            return self.intervalScore(value,self.constraint[0],self.constraint[1],self.constraint[2],self.constraint[3])
        elif(self.requirementType == 'soft_cost'):
            return self.softCostScore(value,min,max,self.constraint)
        elif(self.requirementType == 'soft_benefit'):
            return self.softBenefitScore(value,min,max,self.constraint)
        elif(self.requirementType == 'any'):
            return 0

    
    def hardScore(self,value,constraint):
        if(value == constraint):
            return 0
        else:
            return -1


    def intervalScore(self,value,min,optimalLowerBound,optimalHigherBound,max):
        
        if( optimalLowerBound <= value <= optimalHigherBound ):
            return 1

        elif(min <= value < optimalLowerBound):
            return (value - min)/(optimalLowerBound - min)

        elif (optimalHigherBound < value <= max):
            return (max - value)/(max - optimalHigherBound)

        else:
            return -1


    def softBenefitScore(self,value,min,max,constraint):

        if(value >= constraint):
            return ((value - min + min/2)/(max -min + min/2))**(constraint/min)
        else:
            return -1


    def softCostScore(self,value,min,max,constraint):
        if(value <= constraint):
            return ((max - value + min/2)/(max -min + min/2))**(min/constraint)
        else:
            return -1
        

class Bid():
    
    score = 0

    def __init__(self,entries,factoryId,machineId):
        self.entries = entries
        self.factoryId = factoryId
        self.machineId = machineId

    def __str__(self):
        return "FactoryId {} - MachineId {} - Entries {} - Score {}".format(self.factoryId,self.machineId,self.entries,self.score)
        

        

# bids = [
# Bid({'price':1000,'dueDate':1,'quality':6},1),
# Bid({'price':500,'dueDate':3,'quality':6},2),
# Bid({'price':1000,'dueDate':3,'quality':9},3)
# ]

# # Cares most about price
# companyA = [
# Requirement('price','soft_cost',0.7,1000),
# Requirement('dueDate','interval',0.2,[1,2,3,4]),
# Requirement('quality','soft_benefit',0.1,5)
# ]

# # Cares most about due date
# companyB = [
# Requirement('price','soft_cost',0.2,1000),
# Requirement('dueDate','soft_cost',0.7,3),
# Requirement('quality','soft_benefit',0.1,5)
# ]

# # Cares most about quality
# companyC = [
# Requirement('price','soft_cost',0.1,1000),
# Requirement('dueDate','interval',0.2,[1,2,3,4]),
# Requirement('quality','soft_benefit',0.7,5)
# ]

# companies = [companyA,companyB,companyC]
 
# allBidValues = {'price':[],'dueDate':[],'quality':[]}
# for bid in bids:
#     # Find min and max for each entry 
#     allBidValues['price'].append(bid.entries['price'])
#     allBidValues['dueDate'].append(bid.entries['dueDate'])
#     allBidValues['quality'].append(bid.entries['quality'])


# scores = {}
# for company in companies:
#     for bid in bids:
#         bidScore = 0
#         for requirement in company:
#             # Evaluate the score for each requirement Type 
#             score = requirement.weightedScore(bid.entries[requirement.requirementName],min(allBidValues[requirement.requirementName]),max(allBidValues[requirement.requirementName]))
#             print('Requirement {} - Score {}'.format(requirement.requirementName,score))
#             bidScore += score

#         # Return score 
#         scores[bid.number] = bidScore

#     print(scores)
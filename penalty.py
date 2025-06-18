def total_debt(outstandingdebt):
    if outstandingdebt<=50000:
        return 0
    elif outstandingdebt<=100000:
        return 10
    elif outstandingdebt<=150000:
        return 25
    elif outstandingdebt<=200000:
        return 50
    else:
        return 80

def apply_penalties(score,numofdelayedpayments,numofcreditinquiry,delayfromduedate,numofcreditcard,outstandingdebt):
    if numofcreditcard>3:
        score -=30
    score-=numofdelayedpayments*10
    if numofcreditinquiry>2:
        score -=20
    score -=delayfromduedate*10
    score-=total_debt(outstandingdebt)
    return score

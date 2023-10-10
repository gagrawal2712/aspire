PDG = 'PDG'
AVD = 'AVD'
RJD = 'RJD'
PAID = 'PAID'

LOAN_STATUS = (
    (PDG, 'Pending'),
    (AVD, 'Approved'),
    (RJD, 'Rejected'),
    (PAID, 'Paid')
)

PMT_STATUS = (
    (PDG, 'Pending'),
    (PAID, 'Paid')
)

REPAYMENT_FREQ = 7  # Currently set to weekly, can be changed later on

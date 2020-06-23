from models import opr as opr_model


def search(SQL_Read):
    year = 2019
    events = sorted(SQL_Read.getEvents(year=year))
    for event in events:
        print(event)
        oprs = opr_model.get_ixOPR(event)
        print(oprs)

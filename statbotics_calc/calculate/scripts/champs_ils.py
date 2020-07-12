from helper import setup

start_year = 2002
end_year = 2020
clean = False

TBA, SQL, SQL_Read, SQL_Write = setup.setup(clean)

for year in range(2016, 2020):
    events = SQL_Read.getEvents_year(year=year)
    rp1_acc, rp1_mse, rp2_acc, rp2_mse, count = 0, 0, 0, 0, 0
    for event in events:
        if event.type == 3:
            for match in event.matches:
                if match.playoff == 0:
                    if match.red_rp_1 == int(match.red_rp_1_prob + 0.5):
                        rp1_acc += 1
                    if match.blue_rp_1 == int(match.blue_rp_1_prob + 0.5):
                        rp1_acc += 1
                    if match.red_rp_2 == int(match.red_rp_2_prob + 0.5):
                        rp2_acc += 1
                    if match.blue_rp_2 == int(match.blue_rp_2_prob + 0.5):
                        rp2_acc += 1
                    rp1_mse += (match.red_rp_1-match.red_rp_1_prob)**2
                    rp1_mse += (match.blue_rp_1-match.blue_rp_1_prob)**2
                    rp2_mse += (match.red_rp_2-match.red_rp_2_prob)**2
                    rp2_mse += (match.blue_rp_2-match.blue_rp_2_prob)**2
                    count += 2
    rp1_acc = round(rp1_acc/count, 4)
    rp1_mse = round(rp1_mse/count, 4)
    rp2_acc = round(rp2_acc/count, 4)
    rp2_mse = round(rp2_mse/count, 4)
    print(year, rp1_acc, rp1_mse, rp2_acc, rp2_mse)

import sys
import api
import graph


def main():
    print("Check Data on:")
    print("1. Single Day")
    print("2. Multiple Days")
    print("3. 26-01-2020 to 26-01-2021")
    choice = int(input("Choice: "))
    res = None
    if choice == 1:
        checkSingleDay()
    elif choice == 2:
        checkMultipleDays()
    elif choice == 3:
        checkMultipleDays(ffrom_date="26-01-2020", tto_date= "26-01-2021")
    else:
        print("Invalid Choice")
        sys.exit(-1)    

def checkSingleDay():
    chk_date = input("Enter data as 26-01-2021: ")
    res = api.fetchEquityDataForSingleDay(on_date=chk_date, useCache=True)
    if res is None:
        print("Error API broke or No results")
    else:
        graph.plotCompanyConsolidated(res, f"Insider Trading: {chk_date}", saveImage=True)

def checkMultipleDays(ffrom_date=None, tto_date=None):
    if ffrom_date is None or tto_date is None:
        print("Enter date range (inclusive)")
        ffrom_date = input("Enter FROM data as 26-01-2021: ")
        tto_date = input("Enter TO data as 26-01-2021: ")
    res = api.fetchEquityData(from_date=ffrom_date,to_date=tto_date,useCache=True)
    if res is None:
        print("Error API broke or No results")
    else:
        print("\nAnalyze:")
        print("1. All companies consolidated")
        print("2. Single Company over this Time")
        choice = int(input("Choice: "))
        if choice==1:
            graph.plotCompanyConsolidated(res, f"Insider Trading: {ffrom_date} to {tto_date}", saveImage=True)
        elif choice==2:
            sym = input("Enter symbol: ")
            graph.plotTargetCompanyByDate(res,sym,f"Insider Trading at {sym}: {ffrom_date} to {tto_date}",saveImage=True)


if __name__ == "__main__":
    main()
from datetime import date
import holidays

def get_nsw_holidays(year=2025):
    nsw_holidays = holidays.AU(prov='NSW', years=year)
    
    # get weekday holidays (skip sat/sun)
    weekday_holidays = [
        (date.strftime(d, "%Y-%m-%d"), str(name))
        for d, name in nsw_holidays.items() 
        if date.weekday(d) < 5  # 0-4 is Mon-Fri
    ]
    
    # sort chronologically
    weekday_holidays.sort(key=lambda x: x[0])
    
    return weekday_holidays

if __name__ == "__main__":
    holidays_2025 = get_nsw_holidays(2025)
    print("NSW Public Holidays 2025 (weekdays only):")
    # correct way to print tuples
    for holiday_date, holiday_name in holidays_2025:
        print(f"{holiday_date}: {holiday_name}")
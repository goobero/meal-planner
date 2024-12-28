from datetime import date, timedelta, datetime
import calendar
import random
from holiday_helper import get_nsw_holidays
from meals import MEALS, SIDES

def get_weekdays_in_month(year, month):
    # gets all weekdays in month
    cal = calendar.monthcalendar(year, month)
    weekdays = []
    for week in cal:
        for day_idx, day in enumerate(week):
            if day != 0 and day_idx < 5:
                current_date = date(year, month, day)
                weekdays.append(current_date.strftime("%Y-%m-%d"))
    return weekdays

def select_meal(available_meals, previous_category=None):
    # picks a meal avoiding same category as yesterday
    valid_categories = [cat for cat in available_meals.keys() 
                       if cat != previous_category and available_meals[cat]]
    
    if not valid_categories:
        return None, None
        
    category = random.choice(valid_categories)
    meal = random.choice(available_meals[category])
    
    return category, meal

def create_monthly_menu(year, month):
    weekdays = get_weekdays_in_month(year, month)
    holidays = get_nsw_holidays(year)
    holiday_dates = [h[0] for h in holidays]
    
    # copy meals so we can remove used ones
    available_meals = {
        category: meals[:] for category, meals in MEALS.items()
    }
    
    menu = {}
    previous_category = None
    
    for day in weekdays:
        if day in holiday_dates:
            menu[day] = "Public Holiday"
        else:
            category, meal = select_meal(available_meals, previous_category)
            if meal:
                menu[day] = meal
                available_meals[category].remove(meal)
                previous_category = category
    
    return menu

def format_menu_for_pdf(menu, language='zh'):
    """
    Formats menu for either Chinese or English PDF
    """
    formatted_menu = {}
    for date, entry in menu.items():
        if entry == "Public Holiday":
            formatted_menu[date] = "Public Holiday"
        else:
            # get right language + add sides
            meal_name = entry[language]  # 'zh' or 'en'
            sides = SIDES[language]
            formatted_menu[date] = f"{meal_name} + {sides}"
    
    return formatted_menu

def group_by_week(menu):
    """
    Groups menu items by week for better display
    """
    weeks = {}
    for date, meal in menu.items():
        # get week number
        week_num = datetime.strptime(date, "%Y-%m-%d").isocalendar()[1]
        if week_num not in weeks:
            weeks[week_num] = {}
        weeks[week_num][date] = meal
    
    return weeks


# test it
if __name__ == "__main__":
    # generate basic menu
    menu = create_monthly_menu(2025, 1)
    
    print("\nRAW MENU:")
    for date, entry in menu.items():
        print(f"{date}: {entry}")
        
    print("\nCHINESE MENU:")
    chinese_menu = format_menu_for_pdf(menu, 'zh')
    for date, entry in chinese_menu.items():
        print(f"{date}: {entry}")
        
    print("\nENGLISH MENU:")
    english_menu = format_menu_for_pdf(menu, 'en')
    for date, entry in english_menu.items():
        print(f"{date}: {entry}")
        
    print("\nBY WEEK:")
    weekly = group_by_week(menu)
    for week_num, days in weekly.items():
        print(f"\nWeek {week_num}:")
        for date, entry in days.items():
            if entry == "Public Holiday":
                print(f"{date}: {entry}")
            else:
                print(f"{date}: {entry['zh']} / {entry['en']}")
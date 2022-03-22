def get_country_confirmed_infected(country, start_date = None, end_date = None):
    from datetime import datetime, timedelta
    import requests
    if(end_date is None):
        end_date = datetime.now().date()
    if(start_date is None):
        start_date = end_date - timedelta(days=7)
    
    resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed",
                        params={"from": start_date,
                                "to": end_date})
    return resp.json()

def getMessage(country):
    from dateutil.parser import parse
    cases = get_country_confirmed_infected(country )
    latest_day = cases[-1]
    earliest_day = cases[0]
    percentage_increase = (latest_day['Cases'] - earliest_day['Cases']) / (earliest_day['Cases'] / 100)
    msg = f"There were {latest_day['Cases']} confirmed COVID cases in {country} " \
          f"on {parse(latest_day['Date']).date()}\n"

    msg += f"This is {round(abs(percentage_increase), 4)}% increase over the last week. " \
                   f"Travel is not recommended."
    return msg
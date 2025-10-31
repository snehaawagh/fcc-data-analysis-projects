import pandas as pd

def demographic_data_analyzer(print_data=True):
    # Assign column names per UCI Adult Data set
    column_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
        'occupation', 'relationship', 'race', 'sex', 'hours-per-week', 'native-country', 'salary'
    ]
    df = pd.read_csv('adult.data.csv', names=column_names, skipinitialspace=True)

    # Remove rows with missing values encoded as '?'
    df = df.replace('?', pd.NA).dropna()

    # Strip whitespace for important categorical columns
    for col in ['race', 'sex', 'education', 'salary', 'native-country', 'occupation']:
        df[col] = df[col].str.strip()

    # 1. Race count
    race_count = df['race'].value_counts()

    # 2. Average age of men
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Percentage with Bachelors degrees
    percentage_bachelors = round(
        (df['education'] == 'Bachelors').sum() / len(df) * 100, 1)

    # 4/5. Higher/lower education rich
    higher_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    lower_education = ~higher_education
    
    higher_education_rich = round(
        (df[higher_education]['salary'] == '>50K').sum() / higher_education.sum() * 100, 1)
    lower_education_rich = round(
        (df[lower_education]['salary'] == '>50K').sum() / lower_education.sum() * 100, 1)

    # 6. Min work hours
    min_hours = df['hours-per-week'].min()

    # 7. % min-hours workers rich
    min_workers = df[df['hours-per-week'] == min_hours]
    if len(min_workers) == 0:
        rich_min_workers = 0
    else:
        rich_min_workers = round((min_workers['salary'] == '>50K').sum() / len(min_workers) * 100, 1)

    # 8. Country with highest % rich
    country_counts = df['native-country'].value_counts()
    rich_country_counts = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_percentages = (rich_country_counts / country_counts * 100).dropna()
    highest_earning_country = country_percentages.idxmax()
    highest_earning_country_percentage = round(country_percentages.max(), 1)

    # 9. Most popular occupation for >50K earners in India
    india_occupations = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]['occupation']
    if len(india_occupations) > 0:
        top_in_occupation = india_occupations.value_counts().idxmax()
    else:
        top_in_occupation = None

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_min_workers}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print("Highest percentage of rich people in country:", highest_earning_country_percentage)
        print("Top occupations in India for those who earn >50K:", top_in_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_hours': min_hours,
        'rich_min_workers': rich_min_workers,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_in_occupation': top_in_occupation
    }

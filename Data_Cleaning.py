import pandas as pd
import re

df = pd.read_csv('Non_Cleaned_Indeed_Jobs.csv')

def clean_rating(rating):
    try:
        return float(str(rating)[:3])
    except ValueError:
        return None  # Return None for non-numeric values
    
def clean_benefits(benefit):
    if str(benefit).startswith("Benefits"):
        return str(benefit)[45:-16].strip().replace("\n", ",")
    else:
        return benefit
        

def clean_salary(salary):
    if pd.isna(salary):
        return pd.Series([None, None, None])
    
    salary = salary.replace(",", "")
    salary_range = re.findall(r'\d+[,.]*\d*', salary)
    
    if len(salary_range) == 1:  # If there's only one number, put it in both start and end
        start_salary = salary_range[0]
        end_salary = salary_range[0]
    elif len(salary_range) == 2:
        start_salary, end_salary = salary_range
    else:
        start_salary, end_salary = None, None
    
    # Extract the type (year, month, week, day, hour)
    salary_type = None
    salary_lower = salary.lower()  # Lowercase salary for case-insensitive matching
    if 'year' in salary_lower:
        salary_type = 'year'
    elif 'month' in salary_lower:
        salary_type = 'month'
    elif 'week' in salary_lower:
        salary_type = 'week'
    elif 'day' in salary_lower:
        salary_type = 'day'
    elif 'hour' in salary_lower:
        salary_type = 'hour'
    
    return pd.Series([start_salary, end_salary, salary_type])

def clean_job_titles(title):
    if not isinstance(title, str):
        return 'Unknown', 'Unknown'
    
    lower_title = title.lower()
    
    # Define job titles and patterns
    job_patterns = {
        'IT Project Manager': r'\b(it project|project) (manager|management|coordinator)\b',
        'Project Manager': r'\bproject (manager|management|coordinator)\b',
        'Accountant': r'\baccountant\b',
        'Business Analyst': r'\bbusiness analyst\b',
        'Cyber Security Specialist': r'\b(cyber\s*security|cybersecurity|information\s*security|infosec)\b',
        'Data Analyst': r'\bdata analyst\b',
        'DevOps Engineer': r'\bdevops\b',
        'Financial Analyst': r'\bfinancial analyst\b',
        'HR Assistant': r'\b(hr\s*assistant|human\s*resources\s*assistant|hr\s*admin|hr\s*coordinator)\b',
        'Machine Learning Engineer': r'\b(machine learning|ml)\b',
        'QA Engineer': r'\b(q[a-z]?|quality|test)\s*engineer\b',
        'Software Engineer': r'\bsoftware engineer\b',
        'System Administrator': r'\b(system\s*administrator|sysadmin|system\s*admin|it administrator)\b',
        'Data Scientist': r'\b(data\s*science|data\s*scientist)\b'
    }
    
    # Default to Unknown for both title and level
    cleaned_title = 'Unknown'
    level = 'Unknown'
    
    # Check for job titles and assign levels
    for title_key, pattern in job_patterns.items():
        if re.search(pattern, lower_title):
            cleaned_title = title_key
            
            if re.search(r'\bsr|senior\b', lower_title):
                level = 'Senior'
            elif re.search(r'\b(middle|mid|mid-level)\b', lower_title):
                level = 'Middle'
            elif re.search(r'\b(junior|jr)\b', lower_title):
                level = 'Junior'
            break

    return cleaned_title, level



df.drop_duplicates(inplace = True)
df["company_rating"] = df["company_rating"].apply(clean_rating).astype(float)
df["benefits"] = df["benefits"].apply(clean_benefits)
df['title'], df['level'] = zip(*df['job_title'].apply(clean_job_titles))
df[['start_salary', 'end_salary', 'salary_type']] = df['salary'].apply(clean_salary)
df.drop(df[df['title'] == 'Unknown'].index, inplace=True)

df.to_csv('Indeed_Jobs.csv',index=False)
import pandas as pd
import re
import openai

# Set your OpenAI API key
openai.api_key = ""

# Function to generate skill recommendations using LLM
def generate_skill_recommendations(job_description):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Tell about the skill in general and based on the following job description suggest what else skills are needed with it? \n\n{job_description}"}
        ]
    )
    return response['choices'][0]['message']['content']

# Function to extract skills from description using regular expressions
def extract_skills(description):
    skills_pattern = r"(?:skills|proficiency|expertise|experience) in ([\w\s,]+)"
    skills_match = re.search(skills_pattern, description, re.IGNORECASE)
    if skills_match:
        skills = skills_match.group(1)
        return [skill.strip() for skill in skills.split(',')]  # Return as a list of skills
    return []

# Function to read data from a CSV file
def read_csv(file_path):
    return pd.read_csv(file_path)

# Function to filter job titles based on the inputted skills
def filter_jobs_by_skills(df, skills):
    # Create a regex pattern from the skills list for matching
    pattern = '|'.join(map(re.escape, skills))  # Join skills with OR operator
    filtered_df = df[df['description'].str.contains(pattern, case=False, na=False)]
    return filtered_df[['url', 'job_title', 'salary', 'company_name', 'company_rating','description']]

# Function to write DataFrame to a CSV file (optional if you want to save results)
def write_csv(file_path, df):
    df.to_csv(file_path, index=False)

# Main interaction loop
def main():
    # Read job descriptions from CSV
    df = read_csv('Indeed_Jobs.csv')  # Adjust file path accordingly
    
    # Input job description from user
    job_description = input("Enter a skill(skills) for getting job recommendations: ").strip()
    
    if not job_description:
        print("No skill entered, exiting.")
        return
        
    # Generate skills using the LLM
    recommended_skills = generate_skill_recommendations(job_description)
    print(f"The skill description: {recommended_skills}")

    # Optionally, filter job titles based on entered skills
    input_skills = input("Would you like to filter jobs based on the skills? (yes/no): ").strip().lower()
    if input_skills == 'yes':
        # Split recommended skills into a list
        skills_list = extract_skills(recommended_skills)  # Extract skills from the generated response
        if skills_list:
            filtered_jobs = filter_jobs_by_skills(df, skills_list)
            if not filtered_jobs.empty:
                print(f"\nJobs available for the recommended skills ({', '.join(skills_list)}):\n")
                # Save the filtered jobs to a CSV file
                filtered_jobs.to_csv("output_LLM.csv", index=False)
                print("Filtered jobs saved to 'output_LLM.csv'.")
            else:
                print(f"No job titles found for the skills: {', '.join(skills_list)}")
        else:
            print("No skills found in the recommendations.")
        
      

# Corrected line: using double underscores
if __name__ == "__main__":
    main()

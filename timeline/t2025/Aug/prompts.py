job_summarization = """
Given below is the job description
{job_description}

Give a summary of the job description (skills, experience, etc things that are relevant to job application)
"""

cv_maker = """
Given below is the summary of job description
{job_summarization}

Here is also candidate profile content
{candidate_profile_info}

make a CV for the candidate. Just make it a list of bullet points instead of markdown
"""


motivation_writer = """
Given below is the summary of job description
{job_summarization}

Here is also candidate profile content
{candidate_profile_info}

Write a motivation letter for the candidate (from the perspective of the candidate)
"""
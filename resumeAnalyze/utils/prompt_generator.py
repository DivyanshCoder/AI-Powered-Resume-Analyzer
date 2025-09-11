def create_hf_resume_analysis_prompt(resume_text, job_description=None):
    """Optimized prompts for Hugging Face models"""
    
    if job_description:
        prompt = f"""<s>[INST] You are an expert HR professional. Analyze this resume against the job description.

        Job Description: {job_description[:800]}...

        Resume: {resume_text[:1200]}...

        Provide analysis in this format:
        1. Match Score: [0-100%]
        2. Key Strengths: [bullet points]
        3. Missing Skills: [list]
        4. Recommendations: [actionable advice]
        [/INST]"""

    else:
        prompt = f"""<s>[INST] You are an expert career advisor. Analyze this resume comprehensively.

        Resume: {resume_text[:1500]}...

        Provide analysis in this format:
        1. Overall Quality Score: [0-100%]
        2. Key Skills Identified: [list]
        3. Experience Level: [junior/mid/senior]
        4. Strengths: [bullet points]
        5. Improvement Areas: [specific suggestions]
        [/INST]"""
            
    return prompt

def create_ats_optimization_prompt(resume_text, job_description):
    """ATS-focused prompt for Hugging Face"""
    prompt = f"""<s>[INST] Help optimize this resume for ATS systems.

    Job Requirements: {job_description[:600]}...
    Current Resume: {resume_text[:800]}...

    Provide:
    1. ATS Score: [0-100%]
    2. Missing Keywords: [list]
    3. Formatting Issues: [list]
    4. Optimization Tips: [specific advice]
    [/INST]"""
    
    return prompt

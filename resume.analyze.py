
"""
AI Resume Analyzer - Parse, analyze & score resumes
Author: Maheen | AI & ML Engineer
"""

import re
import json
from collections import Counter


class ResumeAnalyzer:
    def __init__(self):
        self.tech_skills = [
            "python", "javascript", "java", "c++", "react", "node.js",
            "sql", "mongodb", "aws", "docker", "kubernetes", "git",
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "pandas", "numpy", "flask", "django", "fastapi", "html",
            "css", "typescript", "rust", "go", "php", "ruby", "swift"
        ]
        self.soft_skills = [
            "leadership", "communication", "teamwork", "problem solving",
            "critical thinking", "time management", "creativity",
            "adaptability", "collaboration", "project management"
        ]
    
    def extract_email(self, text):
        """Extract email addresses"""
        emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
        return emails
    
    def extract_phone(self, text):
        """Extract phone numbers"""
        phones = re.findall(r"[\+\(]?[0-9][0-9 .\-\(\)]{8,}[0-9]", text)
        return phones
    
    def extract_skills(self, text):
        """Extract technical and soft skills"""
        text_lower = text.lower()
        found_tech = [s for s in self.tech_skills if s in text_lower]
        found_soft = [s for s in self.soft_skills if s in text_lower]
        return {"technical": found_tech, "soft": found_soft}
    
    def extract_education(self, text):
        """Extract education keywords"""
        degrees = ["bachelor", "master", "phd", "bsc", "msc", "mba",
                   "b.tech", "m.tech", "diploma", "certification"]
        text_lower = text.lower()
        found = [d for d in degrees if d in text_lower]
        return found
    
    def extract_experience_years(self, text):
        """Extract years of experience"""
        patterns = re.findall(r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience", text.lower())
        return [int(y) for y in patterns]
    
    def calculate_score(self, skills, education, experience):
        """Score resume out of 100"""
        score = 0
        
        # Technical skills (max 40)
        score += min(len(skills["technical"]) * 5, 40)
        
        # Soft skills (max 20)
        score += min(len(skills["soft"]) * 4, 20)
        
        # Education (max 20)
        score += min(len(education) * 10, 20)
        
        # Experience (max 20)
        if experience:
            years = max(experience)
            score += min(years * 4, 20)
        
        return min(score, 100)
    
    def analyze(self, resume_text):
        """Full resume analysis"""
        results = {
            "contact": {
                "emails": self.extract_email(resume_text),
                "phones": self.extract_phone(resume_text)
            },
            "skills": self.extract_skills(resume_text),
            "education": self.extract_education(resume_text),
            "experience_years": self.extract_experience_years(resume_text),
            "word_count": len(resume_text.split()),
            "score": 0
        }
        
        results["score"] = self.calculate_score(
            results["skills"],
            results["education"],
            results["experience_years"]
        )
        
        return results
    
    def print_report(self, results):
        """Print formatted analysis report"""
        print(f"\n{'='*50}")
        print(f"  RESUME ANALYSIS REPORT")
        print(f"{'='*50}")
        
        print(f"\n📧 Emails: {', '.join(results['contact']['emails']) or 'None found'}")
        print(f"📱 Phone: {', '.join(results['contact']['phones']) or 'None found'}")
        
        print(f"\n💻 Technical Skills ({len(results['skills']['technical'])}):")
        for s in results["skills"]["technical"]:
            print(f"   ✅ {s}")
        
        print(f"\n🤝 Soft Skills ({len(results['skills']['soft'])}):")
        for s in results["skills"]["soft"]:
            print(f"   ✅ {s}")
        
        print(f"\n🎓 Education: {', '.join(results['education']) or 'None found'}")
        print(f"📅 Experience: {results['experience_years'] or 'Not specified'}")
        print(f"📝 Word Count: {results['word_count']}")
        
        print(f"\n⭐ RESUME SCORE: {results['score']}/100")
        print(f"{'='*50}")


if __name__ == "__main__":
    print("AI Resume Analyzer")
    print("Paste resume text (type 'DONE' on new line when finished):\n")
    
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "DONE":
            break
        lines.append(line)
    
    resume_text = "\n".join(lines)
    
    analyzer = ResumeAnalyzer()
    results = analyzer.analyze(resume_text)
    analyzer.print_report(results)
    
    # Save report
    with open("report.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nReport saved to report.json!")

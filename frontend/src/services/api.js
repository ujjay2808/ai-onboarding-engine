export const analyzeData = async (formData) => {
  // MOCK RESPONSE — swap this for real API once Vansh's backend is ready
  // Just uncomment the lines below and delete the mock:
  // const res = await fetch('http://localhost:5000/analyze', { method: 'POST', body: formData })
  // return res.json()

  await new Promise(r => setTimeout(r, 2000)) // simulate loading
  return {
    match_score: 65,
    resume_skills: ["Python", "HTML", "CSS", "Git"],
    jd_skills: ["Python", "React", "SQL", "HTML", "CSS", "Git", "Docker"],
    missing_skills: ["React", "SQL", "Docker"],
    roadmap: [
      {
        skill: "SQL",
        week: 1,
        difficulty: "Beginner",
        reason: "SQL recommended because: (1) Required in JD. (2) Not found in your resume. (3) No prerequisites needed. Confidence: High.",
        resources: [
          { title: "SQL Full Course", url: "https://www.youtube.com/watch?v=HXV3zeQKqGY", platform: "YouTube", duration: "4 hours" },
          { title: "SQL for Beginners", url: "https://www.coursera.org/learn/sql-for-data-science", platform: "Coursera", duration: "1 week" }
        ]
      },
      {
        skill: "React",
        week: 2,
        difficulty: "Intermediate",
        reason: "React recommended because: (1) Required in JD. (2) Not found in your resume. (3) You already know JavaScript basics. Confidence: High.",
        resources: [
          { title: "React Crash Course", url: "https://www.youtube.com/watch?v=w7ejDZ8SWv8", platform: "YouTube", duration: "2 hours" },
          { title: "React - The Complete Guide", url: "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", platform: "Udemy", duration: "2 weeks" }
        ]
      },
      {
        skill: "Docker",
        week: 3,
        difficulty: "Intermediate",
        reason: "Docker recommended because: (1) Required in JD. (2) Not found in your resume. (3) Best learned after core skills are solid. Confidence: High.",
        resources: [
          { title: "Docker Tutorial for Beginners", url: "https://www.youtube.com/watch?v=fqMOX6JJhGo", platform: "YouTube", duration: "2 hours" }
        ]
      }
    ]
  }
}
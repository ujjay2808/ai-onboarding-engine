import { useLocation, useNavigate } from 'react-router-dom'

function ResultPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const result = location.state?.result

  if (!result) {
    return (
      <div className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-400 mb-4">No results found.</p>
          <button onClick={() => navigate('/upload')} className="bg-blue-600 px-6 py-3 rounded-xl">
            Go Back
          </button>
        </div>
      </div>
    )
  }

  const { match_score, resume_skills, jd_skills, missing_skills, roadmap } = result

  const scoreColor = match_score >= 70 ? 'text-green-400' : match_score >= 40 ? 'text-yellow-400' : 'text-red-400'
  const barColor = match_score >= 70 ? 'bg-green-500' : match_score >= 40 ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <div className="min-h-screen bg-gray-950 text-white px-4 py-12">
      <div className="max-w-3xl mx-auto">

        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-blue-400 mb-2">Your Skill Analysis</h1>
          <p className="text-gray-400">Here's your personalised learning roadmap</p>
        </div>

        {/* Match Score */}
        <div className="bg-gray-900 rounded-2xl p-6 mb-6 text-center">
          <p className="text-gray-400 text-sm mb-1">Job Match Score</p>
          <p className={`text-6xl font-bold mb-4 ${scoreColor}`}>{match_score}%</p>
          <div className="w-full bg-gray-700 rounded-full h-3">
            <div className={`${barColor} h-3 rounded-full transition-all`} style={{ width: `${match_score}%` }}></div>
          </div>
        </div>

        {/* Skills Grid */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-900 rounded-2xl p-5">
            <h3 className="text-green-400 font-semibold mb-3">✅ Your Skills</h3>
            <div className="flex flex-wrap gap-2">
              {resume_skills.map(skill => (
                <span key={skill} className="bg-green-900 text-green-300 text-xs px-3 py-1 rounded-full">{skill}</span>
              ))}
            </div>
          </div>
          <div className="bg-gray-900 rounded-2xl p-5">
            <h3 className="text-red-400 font-semibold mb-3">❌ Missing Skills</h3>
            <div className="flex flex-wrap gap-2">
              {missing_skills.map(skill => (
                <span key={skill} className="bg-red-900 text-red-300 text-xs px-3 py-1 rounded-full">{skill}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Roadmap */}
        <div className="bg-gray-900 rounded-2xl p-6 mb-6">
          <h3 className="text-blue-400 font-bold text-xl mb-6">🗺️ Your Learning Roadmap</h3>
          <div className="space-y-6">
            {roadmap.map((item, index) => (
              <div key={item.skill} className="border border-gray-700 rounded-xl p-5">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-white font-bold text-lg">Week {item.week} — {item.skill}</h4>
                  <span className={`text-xs px-3 py-1 rounded-full ${item.difficulty === 'Beginner' ? 'bg-green-900 text-green-300' : 'bg-yellow-900 text-yellow-300'}`}>
                    {item.difficulty}
                  </span>
                </div>
                <p className="text-gray-400 text-sm mb-4 italic">💡 {item.reason}</p>
                <div className="space-y-2">
                  {item.resources.map(r => (
                    <a key={r.url} href={r.url} target="_blank" rel="noreferrer"
                      className="flex items-center justify-between bg-gray-800 hover:bg-gray-700 rounded-lg px-4 py-2 transition-all">
                      <span className="text-blue-300 text-sm">{r.title}</span>
                      <span className="text-gray-500 text-xs">{r.platform} · {r.duration}</span>
                    </a>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Back Button */}
        <button onClick={() => navigate('/upload')}
          className="w-full border border-gray-600 hover:border-blue-500 text-gray-400 hover:text-blue-400 py-3 rounded-xl transition-all">
          ← Analyse Another Resume
        </button>

      </div>
    </div>
  )
}

export default ResultPage
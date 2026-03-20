import { useNavigate } from 'react-router-dom'

function Home() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center px-4">
      <div className="max-w-2xl text-center">
        <div className="mb-6 text-5xl">🧠</div>
        <h1 className="text-4xl font-bold mb-4 text-blue-400">
          AI-Adaptive Onboarding Engine
        </h1>
        <p className="text-gray-400 text-lg mb-4">
          Upload your resume and a job description.
        </p>
        <p className="text-gray-400 text-lg mb-10">
          Our AI finds your skill gaps and builds a personalized learning roadmap — just for you.
        </p>
        <button
          onClick={() => navigate('/upload')}
          className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-8 py-4 rounded-xl text-lg transition-all"
        >
          Get Started →
        </button>
      </div>
    </div>
  )
}

export default Home
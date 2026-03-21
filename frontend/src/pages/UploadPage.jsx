import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeData } from '../services/api'

function UploadPage() {
  const navigate = useNavigate()
  const [resume, setResume] = useState(null)
  const [jd, setJd] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    if (!resume || !jd) {
      setError('Please upload both files before submitting.')
      return
    }
    setError('')
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('resume', resume)
      formData.append('jd', jd)
      const result = await analyzeData(formData)
      navigate('/result', { state: { result } })
    } catch (err) {
      setError('Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center px-4">
      <div className="w-full max-w-xl">
        <h2 className="text-3xl font-bold text-blue-400 mb-2 text-center">Upload Your Documents</h2>
        <p className="text-gray-400 text-center mb-8">We'll analyse your skills and build your roadmap</p>

        {/* Resume Upload */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-300 mb-2">📄 Resume (PDF)</label>
          <div className="border-2 border-dashed border-gray-600 rounded-xl p-6 text-center hover:border-blue-500 transition-all">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setResume(e.target.files[0])}
              className="hidden"
              id="resume-input"
            />
            <label htmlFor="resume-input" className="cursor-pointer">
              {resume ? (
                <p className="text-green-400 font-medium">✅ {resume.name}</p>
              ) : (
                <p className="text-gray-400">Click to upload your resume <span className="text-blue-400">(PDF only)</span></p>
              )}
            </label>
          </div>
        </div>

        {/* JD Upload */}
        <div className="mb-8">
          <label className="block text-sm font-semibold text-gray-300 mb-2">📋 Job Description (PDF or TXT)</label>
          <div className="border-2 border-dashed border-gray-600 rounded-xl p-6 text-center hover:border-blue-500 transition-all">
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setJd(e.target.files[0])}
              className="hidden"
              id="jd-input"
            />
            <label htmlFor="jd-input" className="cursor-pointer">
              {jd ? (
                <p className="text-green-400 font-medium">✅ {jd.name}</p>
              ) : (
                <p className="text-gray-400">Click to upload job description <span className="text-blue-400">(PDF or TXT)</span></p>
              )}
            </label>
          </div>
        </div>

        {/* Error */}
        {error && <p className="text-red-400 text-sm text-center mb-4">{error}</p>}

        {/* Submit */}
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-white font-semibold py-4 rounded-xl text-lg transition-all"
        >
          {loading ? '⏳ Analysing...' : 'Analyse My Skills →'}
        </button>
      </div>
    </div>
  )
}

export default UploadPage
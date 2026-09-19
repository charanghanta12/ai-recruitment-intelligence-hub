export type Candidate = {
  id: string
  name: string
  role?: string
  location?: string
  experience?: number
  skills?: string[]
  status?: string
  email?: string
  phone?: string
  experience_years?: number
  education?: string
}

export type Job = { id: string; title: string; description?: string; required_skills?: string; experience_required?: number; department?: string; location?: string; status?: string; requiredSkills?: string[]; candidateCount?: number }
export type Screening = { screening_id: string; candidate_id?: string; job_id?: string; status: 'queued' | 'processing' | 'completed' | 'failed'; result?: { summary?: string; matching_skills?: string[]; missing_skills?: string[]; experience_analysis?: string; strengths?: string[]; areas_to_explore?: string[]; interview_questions?: string[] }; error?: string }
export type Resume = { id: string; candidate_id: string; filename: string; content_text?: string; uploaded_at: string }

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { Accept: 'application/json', ...init?.headers },
  })
  if (!response.ok) throw new Error(`RecruitFlow API error: ${response.status}`)
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export const candidateApi = {
  list: () => request<Candidate[]>('/api/candidates'),
  create: (payload: { name: string; email: string }) => request<Candidate>('/api/candidates', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  get: (id: string) => request<Candidate>(`/api/candidates/${encodeURIComponent(id)}`),
  uploadResume: (file: File, candidateId: string) => {
    const body = new FormData(); body.append('file', file)
    return request<Candidate>(`/api/resumes/upload?candidate_id=${encodeURIComponent(candidateId)}`, { method: 'POST', body })
  },
}

export const jobApi = {
  list: () => request<Job[]>('/api/jobs'),
  get: (id: string) => request<Job>(`/api/jobs/${encodeURIComponent(id)}`),
  create: (payload: { title: string; description?: string; location?: string; required_skills?: string; requiredSkills?: string[] }) => request<Job>('/api/jobs', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
}

export const resumeApi = { getForCandidate: (candidateId: string) => request<Resume>(`/api/resumes/candidate/${encodeURIComponent(candidateId)}`) }

export const screeningApi = {
  list: () => request<Screening[]>('/api/screenings'),
  run: (candidateId: string, jobId: string) => request<Screening>('/api/screenings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ candidate_id: candidateId, job_id: jobId }) }),
  get: (id: string) => request<Screening>(`/api/screenings/${encodeURIComponent(id)}`),
}

export const assistantApi = { chat: (question: string) => request<{ answer: string }>('/api/assistant/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question }) }) }

export const applicationApi = { list: () => request('/api/applications') }
export type Interview = { id: string; candidate_id: string; job_id: string; scheduled_at: string; interview_type: string; status: string; feedback?: string }
export const interviewApi = { list: () => request<Interview[]>('/api/interviews'), create: (payload: { candidate_id: string; job_id: string; scheduled_at: string; interview_type: string }) => request<Interview>('/api/interviews', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }) }
export const agentApi = { list: () => request('/api/agents'), runs: () => request('/api/agents/runs'), activity: (runId: string) => request(`/api/agents/runs/${encodeURIComponent(runId)}`) }
export const knowledgeApi = { list: () => request('/api/knowledge'), search: (query: string) => request(`/api/knowledge/search?q=${encodeURIComponent(query)}`) }

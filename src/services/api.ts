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
}

export type Job = { id: string; title: string; department?: string; location?: string; status?: string; requiredSkills?: string[]; candidateCount?: number }
export type Screening = { id: string; status: 'queued' | 'processing' | 'completed' | 'failed'; result?: unknown; error?: string }

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? ''

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
  get: (id: string) => request<Candidate>(`/api/candidates/${encodeURIComponent(id)}`),
  uploadResume: (file: File, jobId?: string) => {
    const body = new FormData(); body.append('file', file); if (jobId) body.append('job_id', jobId)
    return request<Candidate>('/api/resumes/upload', { method: 'POST', body })
  },
}

export const jobApi = {
  list: () => request<Job[]>('/api/jobs'),
  get: (id: string) => request<Job>(`/api/jobs/${encodeURIComponent(id)}`),
  create: (payload: Omit<Job, 'id'>) => request<Job>('/api/jobs', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
}

export const screeningApi = {
  run: (candidateId: string, jobId: string) => request<Screening>('/api/screening/run', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ candidate_id: candidateId, job_id: jobId }) }),
  get: (id: string) => request<Screening>(`/api/screening/${encodeURIComponent(id)}`),
}

export const applicationApi = { list: () => request('/api/applications') }
export const interviewApi = { list: () => request('/api/interviews'), create: (payload: unknown) => request('/api/interviews', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }) }
export const agentApi = { list: () => request('/api/agents'), runs: () => request('/api/agents/runs'), activity: (runId: string) => request(`/api/agents/runs/${encodeURIComponent(runId)}`) }
export const knowledgeApi = { list: () => request('/api/knowledge'), search: (query: string) => request(`/api/knowledge/search?q=${encodeURIComponent(query)}`) }

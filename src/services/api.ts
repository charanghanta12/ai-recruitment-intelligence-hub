export type Candidate = {
  id: string
  name: string
  role: string
  location: string
  experience: number
  skills: string[]
  status: string
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? ''

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  if (!response.ok) throw new Error(`RecruitFlow API error: ${response.status}`)
  return response.json() as Promise<T>
}

export const candidateApi = {
  list: () => request<Candidate[]>('/api/candidates'),
  get: (id: string) => request<Candidate>(`/api/candidates/${encodeURIComponent(id)}`),
}

export const jobApi = {
  list: () => request('/api/jobs'),
  get: (id: string) => request(`/api/jobs/${encodeURIComponent(id)}`),
}

export const applicationApi = { list: () => request('/api/applications') }
export const interviewApi = { list: () => request('/api/interviews') }
export const agentApi = {
  list: () => request('/api/agents'),
  activity: (runId: string) => request(`/api/agents/runs/${encodeURIComponent(runId)}`),
}
export const knowledgeApi = { search: (query: string) => request(`/api/knowledge/search?q=${encodeURIComponent(query)}`) }

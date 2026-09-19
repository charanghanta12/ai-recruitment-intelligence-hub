'use client'

import { useState } from 'react'
import { Activity, ArrowUpRight, BookOpen, BriefcaseBusiness, CalendarDays, Check, Command, MessageSquareText, Settings, Sparkles, Users, X, Zap } from 'lucide-react'

type Section = 'Home' | 'Candidates' | 'Jobs' | 'Interviews' | 'AI Assistant' | 'Knowledge Base' | 'AI Agents' | 'Activity' | 'Settings'

const destinations: { label: Exclude<Section, 'Home'>; icon: typeof Users; detail: string }[] = [
  { label: 'Candidates', icon: Users, detail: 'Review talent and signals' },
  { label: 'Jobs', icon: BriefcaseBusiness, detail: 'Shape your open roles' },
  { label: 'Interviews', icon: CalendarDays, detail: 'Prepare better conversations' },
  { label: 'AI Assistant', icon: MessageSquareText, detail: 'Ask your hiring copilot' },
  { label: 'Knowledge Base', icon: BookOpen, detail: 'Keep your hiring context' },
  { label: 'AI Agents', icon: Zap, detail: 'Automate the busywork' },
  { label: 'Activity', icon: Activity, detail: 'Follow every decision' },
  { label: 'Settings', icon: Settings, detail: 'Tune your workspace' },
]

function Brand({ onClick }: { onClick: () => void }) {
  return <button className="rf-brand" onClick={onClick} aria-label="Go to RecruitFlow home"><span className="rf-brand-symbol"><Sparkles /></span><span>RecruitFlow <b>AI</b></span></button>
}

function Home({ onOpen }: { onOpen: (section: Section) => void }) {
  return <section className="rf-home rf-enter">
    <div className="rf-home-copy">
      <p className="rf-kicker"><span className="rf-pulse" /> A calmer way to hire</p>
      <h1>Make the <i>right</i><br />people decision.</h1>
      <p className="rf-lede">RecruitFlow brings signal, context and momentum together so every hire feels clear, considered and human.</p>
      <div className="rf-actions"><button className="rf-primary" onClick={() => onOpen('Candidates')}>Enter your workspace <ArrowUpRight /></button><button className="rf-command" onClick={() => onOpen('AI Assistant')}><Command /> Ask RecruitFlow <kbd>⌘ K</kbd></button></div>
      <div className="rf-proof"><span><Check /> Evidence, not noise</span><span><Check /> Built for humans</span></div>
    </div>
    <div className="rf-constellation" aria-label="Explore workspace areas">
      <div className="rf-ring rf-ring-one" /><div className="rf-ring rf-ring-two" /><div className="rf-core"><Sparkles /><small>YOUR<br />WORKSPACE</small></div>
      {destinations.slice(0, 6).map(({ label, icon: Icon }, index) => <button key={label} className={`rf-node rf-node-${index + 1}`} onClick={() => onOpen(label)} aria-label={`Open ${label}`}><Icon /><span>{label}</span></button>)}
      <div className="rf-constellation-note">Move through your hiring<br /><strong>with intention.</strong></div>
    </div>
  </section>
}

function Workspace({ section, onOpen }: { section: Exclude<Section, 'Home'>; onOpen: (section: Section) => void }) {
  const item = destinations.find((entry) => entry.label === section) ?? destinations[0]
  const Icon = item.icon
  return <section className="rf-workspace rf-enter"><button className="rf-back" onClick={() => onOpen('Home')}>Back to home <span>↗</span></button><div className="rf-workspace-intro"><div className="rf-section-icon"><Icon /></div><p className="rf-kicker">RecruitFlow workspace</p><h1>{section}</h1><p className="rf-lede">{item.detail}. Everything you need, arranged with less noise and more intention.</p></div><div className="rf-action-panel"><div><span className="rf-panel-label">Ready when you are</span><h2>Let&apos;s make progress.</h2><p>Your workspace is connected and waiting for your next thoughtful decision.</p></div><button className="rf-primary" onClick={() => onOpen(section)}>Open {section} <ArrowUpRight /></button></div><div className="rf-explore"><span>Explore another area</span>{destinations.filter(({ label }) => label !== section).slice(0, 4).map(({ label }) => <button key={label} onClick={() => onOpen(label)}>{label}</button>)}</div></section>
}

export default function Page() {
  const [section, setSection] = useState<Section>('Home')
  const [menuOpen, setMenuOpen] = useState(false)
  const open = (next: Section) => { setSection(next); setMenuOpen(false) }
  return <div className="rf-app"><header className="rf-header"><Brand onClick={() => open('Home')} /><button className="rf-menu-trigger" onClick={() => setMenuOpen(true)} aria-expanded={menuOpen}><span>Explore</span><span className="rf-menu-dots"><i /><i /><i /></span></button></header><main>{section === 'Home' ? <Home onOpen={open} /> : <Workspace section={section} onOpen={open} />}</main><footer className="rf-footer"><span>RecruitFlow <b>AI</b></span><span>Thoughtful hiring, amplified.</span><button onClick={() => setMenuOpen(true)}>All areas <ArrowUpRight /></button></footer>{menuOpen && <div className="rf-overlay" role="dialog" aria-modal="true" aria-label="Explore RecruitFlow"><div className="rf-menu-card"><div className="rf-menu-head"><div><span className="rf-panel-label">The workspace</span><h2>Where would you like to go?</h2></div><button className="rf-close" onClick={() => setMenuOpen(false)} aria-label="Close menu"><X /></button></div><div className="rf-menu-grid">{destinations.map(({ label, icon: Icon, detail }) => <button key={label} onClick={() => open(label)}><span className="rf-menu-icon"><Icon /></span><span><strong>{label}</strong><small>{detail}</small></span><ArrowUpRight /></button>)}</div></div></div>}</div>
}

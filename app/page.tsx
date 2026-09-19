'use client'

import { useState } from 'react'
import { ArrowRight, Activity, BookOpen, BriefcaseBusiness, CalendarDays, Check, ChevronRight, MessageSquareText, Settings, Sparkles, Users, Zap } from 'lucide-react'

type Section = 'Home' | 'Candidates' | 'Jobs' | 'Interviews' | 'AI Assistant' | 'Knowledge Base' | 'AI Agents' | 'Activity' | 'Settings'

const nav: { label: Section; icon: typeof Users }[] = [
  { label: 'Candidates', icon: Users },
  { label: 'Jobs', icon: BriefcaseBusiness },
  { label: 'Interviews', icon: CalendarDays },
  { label: 'AI Assistant', icon: MessageSquareText },
  { label: 'Knowledge Base', icon: BookOpen },
  { label: 'AI Agents', icon: Zap },
  { label: 'Activity', icon: Activity },
  { label: 'Settings', icon: Settings },
]

function Brand({ onClick }: { onClick: () => void }) {
  return <button onClick={onClick} className="rf-brand" aria-label="Go to home"><span className="rf-brand-mark"><Sparkles /></span><span>RecruitFlow <b>AI</b></span></button>
}

function Home({ onStart }: { onStart: () => void }) {
  return <section className="rf-home rf-section-enter">
    <div className="rf-hero-copy">
      <p className="rf-eyebrow"><span className="rf-live-dot" /> The intelligent hiring workspace</p>
      <h1>Hire with more <em>clarity.</em></h1>
      <p className="rf-hero-text">RecruitFlow turns every candidate signal into a confident decision. Simple tools, thoughtful intelligence, better teams.</p>
      <div className="rf-hero-actions"><button className="rf-primary-button" onClick={onStart}>Start screening <ArrowRight /></button><button className="rf-text-button">Explore workspace <ChevronRight /></button></div>
      <div className="rf-trust"><span><Check /> Evidence-backed insights</span><span><Check /> Built for human decisions</span></div>
    </div>
    <div className="rf-hero-art" aria-hidden="true"><div className="rf-art-halo" /><div className="rf-art-orbit orbit-one" /><div className="rf-art-orbit orbit-two" /><div className="rf-hero-orb"><Sparkles /></div><div className="rf-floating-card rf-floating-top"><span className="rf-mini-icon"><Users /></span><div><strong>Candidate signal</strong><small>Strong alignment</small></div><span className="rf-score">94</span></div><div className="rf-floating-card rf-floating-bottom"><span className="rf-mini-icon blue"><Activity /></span><div><strong>Hiring momentum</strong><small>+24% this week</small></div></div></div>
  </section>
}

function Workspace({ section }: { section: Exclude<Section, 'Home'> }) {
  const copy: Record<Exclude<Section, 'Home'>, [string, string, string]> = { Candidates: ['Candidates', 'Your talent, thoughtfully organized.', 'Review candidate profiles, signals and progress in one calm workspace.'], Jobs: ['Open roles', 'The right role starts here.', 'Create, refine and share roles that attract your next great teammate.'], Interviews: ['Interviews', 'Better conversations, better decisions.', 'Keep every interview focused, fair and easy to follow.'], 'AI Assistant': ['AI Assistant', 'Ask better hiring questions.', 'Get grounded answers about candidates, roles and your hiring process.'], 'Knowledge Base': ['Knowledge Base', 'Your hiring intelligence, together.', 'Keep guidelines, principles and context close to every decision.'], 'AI Agents': ['AI Agents', 'Let the busywork disappear.', 'Configure thoughtful agents for screening, scheduling and evaluation.'], Activity: ['Activity', 'Everything in motion.', 'See the latest progress across your recruitment workspace.'], Settings: ['Settings', 'Make RecruitFlow yours.', 'Manage your workspace preferences and API connection.'] }
  const [title, lead, text] = copy[section]
  return <section className="rf-workspace rf-section-enter"><div className="rf-workspace-heading"><p className="rf-eyebrow">RecruitFlow workspace</p><h1>{title}</h1><p>{lead}</p></div><div className="rf-workspace-card"><div className="rf-card-glow" /><div className="rf-card-icon"><Sparkles /></div><h2>{title} is ready when you are.</h2><p>{text}</p><button className="rf-primary-button">Open {title} <ArrowRight /></button></div></section>
}

export default function Page() {
  const [section, setSection] = useState<Section>('Home')
  const go = (next: Section) => setSection(next)
  return <div className="rf-app min-h-screen"><header className="rf-header"><div className="rf-header-inner"><Brand onClick={() => go('Home')} /><nav className="rf-top-nav" aria-label="Main navigation"><button className={section === 'Home' ? 'active' : ''} onClick={() => go('Home')}>Home</button>{nav.slice(0, 4).map(({ label }) => <button key={label} className={section === label ? 'active' : ''} onClick={() => go(label)}>{label}</button>)}<button className="rf-more-link" onClick={() => go('Settings')}>More <ChevronRight /></button></nav><button className="rf-header-cta" onClick={() => go('AI Assistant')}>Ask AI <Sparkles /></button></div></header><main className="rf-main">{section === 'Home' ? <Home onStart={() => go('Candidates')} /> : <Workspace section={section} />}</main><footer className="rf-footer"><span>RecruitFlow <b>AI</b></span><span>AI insights, human decisions.</span><div>{nav.slice(4).map(({ label }) => <button key={label} onClick={() => go(label)}>{label}</button>)}</div></footer></div>
}

import React, { useState, useRef } from "react";
import { useLocation, Link } from "react-router-dom";
import html2pdf from "html2pdf.js";
import { motion } from "framer-motion";
import MainLayout from "../layouts/MainLayout";
import Card from "../components/Card";
import Badge from "../components/Badge";
import Button from "../components/Button";
import { 
  TrendingUp, 
  Target, 
  Award, 
  ListCheck, 
  Milestone, 
  ArrowRight,
  ChevronRight,
  Download,
  Share2,
  AlertTriangle,
  Briefcase,
  RefreshCw,
  Sparkles,
  CheckCircle2,
  XCircle
} from "lucide-react";

/* ───────── helpers ───────── */
const getScoreColor = (score) => {
  if (score >= 80) return { ring: "stroke-emerald-500", bg: "bg-emerald-50", text: "text-emerald-600", label: "Excellent Match" };
  if (score >= 60) return { ring: "stroke-accent",      bg: "bg-indigo-50",  text: "text-accent",      label: "Strong Potential" };
  if (score >= 40) return { ring: "stroke-amber-500",   bg: "bg-amber-50",   text: "text-amber-600",   label: "Room to Grow" };
  return              { ring: "stroke-red-500",    bg: "bg-red-50",     text: "text-red-600",     label: "Needs Development" };
};

const fadeUp = {
  hidden:  { opacity: 0, y: 24 },
  visible: (i = 0) => ({ opacity: 1, y: 0, transition: { delay: i * 0.08, duration: 0.45, ease: "easeOut" } })
};

/* ───────── component ───────── */
const ResultsPage = () => {
  const location = useLocation();
  const rawResults = location.state?.results || {
    match_score: 85,
    missing_skills: [
      { skill: "Cloud Architecture", importance: "high" },
      { skill: "Docker", importance: "medium" },
      { skill: "Advanced SQL", importance: "medium" },
      { skill: "Kubernetes", importance: "low" }
    ],
    strengths: [
      { skill: "React.js", proficiency: "expert" },
      { skill: "UI/UX Design", proficiency: "advanced" },
      { skill: "Leadership", proficiency: "advanced" },
      { skill: "Product Strategy", proficiency: "intermediate" }
    ],
    recommendations: "Complete a certification in AWS Solutions Architect.\nContribute to open-source projects using Kubernetes.\nStrengthen data modeling skills.",
    roadmap: "Weeks 1-4: Master Docker and Containerization Fundamentals\nMonths 2-3: AWS Certified Solutions Architect Associate Prep & Exam\nMonths 4-6: Build Portfolio Projects with Microservices Architecture\nGoal: Apply for Senior Full-Stack / Cloud Engineer Roles",
    key_gaps: ["No direct experience with AWS", "Missing Docker certification", "Limited cloud deployment experience"],
    suitable_roles: ["Senior Frontend Developer", "Technical Lead", "Full-Stack Engineer"]
  };

  // Normalize backend results
  const results = {
    score: rawResults.match_score !== undefined ? rawResults.match_score : (rawResults.score || 0),
    strengths: (rawResults.strengths || []).map(s => typeof s === 'string' ? s : (s.skill || s)),
    skillGaps: (rawResults.missing_skills || rawResults.skillGaps || []).map(s => typeof s === 'string' ? s : (s.skill || s)),
    recommendations: Array.isArray(rawResults.recommendations) 
      ? rawResults.recommendations 
      : (rawResults.recommendations || "").split("\n").filter(r => r.trim()),
    roadmap: (() => {
      const roadmapData = rawResults.roadmap;
      
      // If roadmap is already an array, use it
      if (Array.isArray(roadmapData)) {
        return roadmapData.filter(r => r).map(r => typeof r === 'string' ? { step: "Step", task: r } : r);
      }
      
      // If roadmap is a string, try to parse as JSON first
      if (typeof roadmapData === 'string' && roadmapData.trim()) {
        try {
          const parsed = JSON.parse(roadmapData);
          
          // If it's an error response, return empty array
          if (parsed.error) {
            return [];
          }
          
          // Extract milestones if available
          if (parsed.milestones && Array.isArray(parsed.milestones)) {
            return parsed.milestones
              .filter(m => m && m.milestone)
              .map(m => ({ 
                step: m.milestone || "Milestone", 
                task: m.target_date ? `${m.milestone} (Target: ${m.target_date})` : m.milestone 
              }));
          }
          
          // Extract from short_term_goals, medium_term_goals, long_term_goals
          const goals = [];
          if (parsed.short_term_goals) {
            goals.push({ step: "Short Term (3-6 months)", task: JSON.stringify(parsed.short_term_goals, null, 2) });
          }
          if (parsed.medium_term_goals) {
            goals.push({ step: "Medium Term (6-12 months)", task: JSON.stringify(parsed.medium_term_goals, null, 2) });
          }
          if (parsed.long_term_goals) {
            goals.push({ step: "Long Term (1-2 years)", task: JSON.stringify(parsed.long_term_goals, null, 2) });
          }
          
          if (goals.length > 0) {
            return goals;
          }
          
          // If no structured data found, return empty (don't show raw JSON)
          return [];
        } catch (e) {
          // If JSON parsing fails, try to split by newlines
          const lines = roadmapData.split("\n").filter(r => r.trim());
          if (lines.length > 0) {
            return lines.map((r, i) => {
              const colonIdx = r.indexOf(":");
              if (colonIdx > -1) {
                return { step: r.slice(0, colonIdx).trim(), task: r.slice(colonIdx + 1).trim() };
              }
              return { step: `Step ${i + 1}`, task: r.trim() };
            });
          }
          return [];
        }
      }
      
      // If roadmap is an object, extract milestones
      if (typeof roadmapData === 'object' && roadmapData !== null) {
        // Check for error
        if (roadmapData.error) {
          return [];
        }
        
        if (roadmapData.milestones && Array.isArray(roadmapData.milestones)) {
          return roadmapData.milestones
            .filter(m => m && m.milestone)
            .map(m => ({ 
              step: m.milestone || "Milestone", 
              task: m.target_date ? `${m.milestone} (Target: ${m.target_date})` : m.milestone 
            }));
        }
        
        // Extract from goal fields
        const goals = [];
        if (roadmapData.short_term_goals) {
          goals.push({ step: "Short Term (3-6 months)", task: JSON.stringify(roadmapData.short_term_goals, null, 2) });
        }
        if (roadmapData.medium_term_goals) {
          goals.push({ step: "Medium Term (6-12 months)", task: JSON.stringify(roadmapData.medium_term_goals, null, 2) });
        }
        if (roadmapData.long_term_goals) {
          goals.push({ step: "Long Term (1-2 years)", task: JSON.stringify(roadmapData.long_term_goals, null, 2) });
        }
        
        return goals;
      }
      
      return [];
    })(),
    keyGaps: rawResults.key_gaps || [],
    suitableRoles: rawResults.suitable_roles || []
  };

  const scoreInfo = getScoreColor(results.score);
  const [isExporting, setIsExporting] = useState(false);
  const pdfRef = useRef(null);

  const handleExportPDF = () => {
    if (!pdfRef.current) return;
    setIsExporting(true);
    
    const opt = {
      margin:       10,
      filename:     'career-match-analysis.pdf',
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { 
        scale: 2, 
        useCORS: true, 
        logging: true, 
        onclone: (document) => {
          // Unhide the static circle fallback specifically for html2canvas
          const fallbacks = document.querySelectorAll('[data-html2canvas-fallback]');
          fallbacks.forEach(el => el.style.display = 'block');
        }
      },
      jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };
    
    // Safety timeout in case html2canvas hangs silently on animated SVGs
    const fallbackTimeout = setTimeout(() => {
      if (isExporting) {
        setIsExporting(false);
        console.warn("PDF generation timed out (html2canvas hang)");
        alert("PDF generation took too long. The document might be too complex. Please try the native browser print function (Ctrl+P / Cmd+P).");
      }
    }, 15000);

    html2pdf().set(opt).from(pdfRef.current).save()
      .then(() => {
        clearTimeout(fallbackTimeout);
        setIsExporting(false);
      })
      .catch((err) => {
        clearTimeout(fallbackTimeout);
        console.error("PDF generation failed:", err);
        alert("Failed to generate PDF. Please try again or use your browser's print function (Ctrl+P).");
        setIsExporting(false);
      });
  };

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'My Career Match Analysis',
          text: `I just scored a ${results.score}% match for a role on the Job Intelligence Platform!`,
          url: window.location.href,
        });
      } catch (error) {
        console.log('Error sharing:', error);
      }
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  return (
    <MainLayout>
      <div ref={pdfRef} className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 pb-24 bg-white relative z-0">
        {/* ── Header ── */}
        <motion.div 
          initial="hidden" animate="visible" variants={fadeUp}
          className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10"
        >
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-accent" />
              <span className="text-sm font-semibold text-accent uppercase tracking-wider">AI-Powered Insights</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 leading-tight">Career Match Analysis</h1>
            <p className="text-gray-500 mt-1">Analysis based on your profile and target role</p>
          </div>
          <div className="flex items-center gap-3" data-html2canvas-ignore>
            <Button variant="secondary" size="sm" onClick={handleExportPDF} disabled={isExporting}>
              <Download className={`w-4 h-4 mr-2 ${isExporting ? 'animate-pulse' : ''}`} /> 
              {isExporting ? 'Exporting...' : 'Export PDF'}
            </Button>
            <Button variant="secondary" size="sm" onClick={handleShare}>
              <Share2 className="w-4 h-4 mr-2" /> Share
            </Button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* ════════════ Main Column ════════════ */}
          <div className="lg:col-span-2 space-y-8">

            {/* ── Score Hero Card ── */}
            <motion.div initial="hidden" animate="visible" custom={1} variants={fadeUp}>
              <Card className={`p-8 border-0 shadow-md ${scoreInfo.bg}`}>
                <div className="flex flex-col md:flex-row items-center gap-10">
                  {/* Animated Score Ring */}
                  <div className="relative flex items-center justify-center shrink-0">
                    <svg className="w-44 h-44" viewBox="0 0 160 160">
                      <circle cx="80" cy="80" r="70" className="stroke-gray-200/60 fill-none" strokeWidth="10" />
                      {/* Static circle for PDF export fallback */}
                      <circle 
                        cx="80" cy="80" r="70"
                        className={`${scoreInfo.ring} fill-none`}
                        strokeWidth="10"
                        strokeDasharray="440"
                        strokeDashoffset={440 - (440 * results.score) / 100}
                        strokeLinecap="round"
                        style={{ transform: "rotate(-90deg)", transformOrigin: "center", display: "none" }}
                        data-html2canvas-fallback
                      />
                      <motion.circle 
                        cx="80" cy="80" r="70"
                        className={`${scoreInfo.ring} fill-none`}
                        strokeWidth="10"
                        strokeDasharray="440"
                        initial={{ strokeDashoffset: 440 }}
                        animate={{ strokeDashoffset: 440 - (440 * results.score) / 100 }}
                        transition={{ duration: 1.6, ease: "easeOut", delay: 0.3 }}
                        strokeLinecap="round"
                        style={{ transform: "rotate(-90deg)", transformOrigin: "center" }}
                        data-html2canvas-ignore
                      />
                    </svg>
                    <div className="absolute text-center">
                      <motion.span 
                        className={`text-5xl font-black ${scoreInfo.text}`}
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5, delay: 0.8 }}
                      >
                        {results.score}
                      </motion.span>
                      <p className={`text-xs font-bold uppercase tracking-wider mt-0.5 ${scoreInfo.text}`}>/ 100</p>
                    </div>
                  </div>

                  {/* Score Context */}
                  <div className="flex-1 space-y-3 text-center md:text-left">
                    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-semibold ${scoreInfo.bg} ${scoreInfo.text}`}>
                      <Target className="w-4 h-4" />
                      {scoreInfo.label}
                    </div>
                    <p className="text-gray-600 leading-relaxed text-sm">
                      {results.score >= 60
                        ? "Your profile shows strong alignment with this role. Focus on bridging the identified skill gaps to become an elite candidate."
                        : "There is meaningful distance between your current profile and this role. The roadmap below outlines a clear path to get there."}
                    </p>
                    <div className="flex flex-wrap gap-2 justify-center md:justify-start">
                      {results.strengths.slice(0, 3).map(s => (
                        <Badge key={s} variant="success">{s}</Badge>
                      ))}
                      {results.strengths.length > 3 && (
                        <Badge variant="gray">+{results.strengths.length - 3} more</Badge>
                      )}
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>

            {/* ── AI Recommendations ── */}
            {results.recommendations.length > 0 && (
              <motion.section initial="hidden" animate="visible" custom={2} variants={fadeUp} className="space-y-4">
                <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-accent" /> AI Recommendations
                </h3>
                <div className="grid grid-cols-1 gap-3">
                  {results.recommendations.map((rec, i) => (
                    <motion.div key={i} initial="hidden" animate="visible" custom={2 + i * 0.5} variants={fadeUp}>
                      <Card className="p-5 flex items-start gap-4 border-l-4 border-l-accent/80 hover:shadow-md hover:translate-x-0.5 transition-all duration-200">
                        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-accent/10 shrink-0 mt-0.5">
                          <span className="text-sm font-bold text-accent">{i + 1}</span>
                        </div>
                        <p className="text-gray-700 leading-relaxed text-sm">{rec}</p>
                      </Card>
                    </motion.div>
                  ))}
                </div>
              </motion.section>
            )}

            {/* ── Career Roadmap ── */}
            {results.roadmap.length > 0 && (
              <motion.section initial="hidden" animate="visible" custom={4} variants={fadeUp} className="space-y-4">
                <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <Milestone className="w-5 h-5 text-accent" /> Your Career Roadmap
                </h3>
                <Card className="p-8">
                  <div className="relative">
                    {/* Vertical timeline line */}
                    <div className="absolute left-[11px] top-2 bottom-2 w-0.5 bg-gradient-to-b from-accent via-accent/40 to-emerald-400 rounded-full" />
                    <div className="space-y-8">
                      {results.roadmap.map((item, i) => {
                        const isLast = i === results.roadmap.length - 1;
                        return (
                          <motion.div 
                            key={i} 
                            className="flex items-start gap-6 relative"
                            initial="hidden" animate="visible" custom={4 + i * 0.6} variants={fadeUp}
                          >
                            <div className={`w-6 h-6 rounded-full border-[3px] border-white shadow-md shrink-0 z-10 ${isLast ? 'bg-emerald-500 ring-2 ring-emerald-100' : 'bg-accent ring-2 ring-accent/10'}`} />
                            <div className="pb-1">
                              <span className={`text-xs font-bold uppercase tracking-wider ${isLast ? 'text-emerald-600' : 'text-accent'}`}>{item.step}</span>
                              <h4 className="text-base font-semibold text-gray-900 mt-0.5 leading-snug">{item.task}</h4>
                            </div>
                          </motion.div>
                        );
                      })}
                    </div>
                  </div>
                </Card>
              </motion.section>
            )}

            {/* ── Key Gaps ── */}
            {results.keyGaps.length > 0 && (
              <motion.section initial="hidden" animate="visible" custom={6} variants={fadeUp} className="space-y-4">
                <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-500" /> Key Gaps to Address
                </h3>
                <Card className="p-6">
                  <div className="space-y-3">
                    {results.keyGaps.map((gap, i) => (
                      <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-amber-50/60 border border-amber-100/80">
                        <XCircle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
                        <p className="text-sm text-gray-700 leading-relaxed">{gap}</p>
                      </div>
                    ))}
                  </div>
                </Card>
              </motion.section>
            )}
          </div>

          {/* ════════════ Sidebar ════════════ */}
          <div className="space-y-6">

            {/* ── Key Strengths ── */}
            <motion.div initial="hidden" animate="visible" custom={1.5} variants={fadeUp}>
              <Card className="p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <Award className="w-5 h-5 text-emerald-500" /> Key Strengths
                </h3>
                <div className="space-y-2.5">
                  {results.strengths.map(s => (
                    <div key={s} className="flex items-center gap-2.5 p-2 rounded-lg hover:bg-green-50/60 transition-colors">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                      <span className="text-sm font-medium text-gray-700">{s}</span>
                    </div>
                  ))}
                  {results.strengths.length === 0 && (
                    <p className="text-sm text-gray-400 italic">No strengths identified yet.</p>
                  )}
                </div>
              </Card>
            </motion.div>

            {/* ── Skill Gaps ── */}
            <motion.div initial="hidden" animate="visible" custom={2.5} variants={fadeUp}>
              <Card className="p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-red-500 rotate-180" /> Skill Gaps
                </h3>
                <div className="space-y-2.5">
                  {results.skillGaps.map(gap => (
                    <div key={gap} className="flex items-center justify-between group p-2 rounded-lg hover:bg-red-50/40 transition-colors">
                      <span className="text-sm font-medium text-gray-600">{gap}</span>
                      <ChevronRight className="w-4 h-4 text-gray-300 group-hover:text-accent transition-colors" />
                    </div>
                  ))}
                  {results.skillGaps.length === 0 && (
                    <p className="text-sm text-gray-400 italic">No skill gaps identified.</p>
                  )}
                </div>
              </Card>
            </motion.div>

            {/* ── Suitable Roles ── */}
            {results.suitableRoles.length > 0 && (
              <motion.div initial="hidden" animate="visible" custom={3.5} variants={fadeUp}>
                <Card className="p-6">
                  <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <Briefcase className="w-5 h-5 text-accent" /> Suitable Roles
                  </h3>
                  <div className="space-y-2.5">
                    {results.suitableRoles.map(role => (
                      <div key={role} className="flex items-center gap-2.5 p-2.5 rounded-lg bg-accent/5 border border-accent/10">
                        <ArrowRight className="w-4 h-4 text-accent shrink-0" />
                        <span className="text-sm font-semibold text-gray-800">{role}</span>
                      </div>
                    ))}
                  </div>
                </Card>
              </motion.div>
            )}

            {/* ── Start New Analysis CTA ── */}
            <motion.div initial="hidden" animate="visible" custom={4.5} variants={fadeUp}>
              <Card className="p-6 bg-gradient-to-br from-accent to-indigo-700 text-white border-none shadow-lg shadow-accent/20 relative overflow-hidden">
                <div className="absolute -top-10 -right-10 w-36 h-36 bg-white/5 rounded-full blur-2xl" data-html2canvas-ignore />
                <div className="absolute -bottom-6 -left-6 w-24 h-24 bg-white/5 rounded-full blur-xl" data-html2canvas-ignore />
                <div className="relative z-10">
                  <RefreshCw className="w-8 h-8 mb-3 opacity-80" />
                  <h4 className="font-bold text-lg mb-2">Try Another Match</h4>
                  <p className="text-sm text-indigo-100 mb-5 leading-relaxed">
                    Upload a different CV or refine your target role for a new analysis.
                  </p>
                  <Link to="/">
                    <Button className="w-full bg-white text-accent hover:bg-gray-50 border-none font-semibold">
                      Start New Analysis <ArrowRight className="ml-2 w-4 h-4" />
                    </Button>
                  </Link>
                </div>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default ResultsPage;

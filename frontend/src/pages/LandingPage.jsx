import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowRight, Zap, TrendingUp, Search, BrainCircuit, Sparkles, Target, FileText, Compass, ChevronRight } from "lucide-react";
import Button from "../components/Button";
import Card from "../components/Card";
import MainLayout from "../layouts/MainLayout";

const LandingPage = () => {
  // Animation Variants
  const fadeUp = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: "easeOut" } },
  };

  const staggerContainer = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 },
    },
  };

  const features = [
    {
      title: "Deep Context Analysis",
      description: "Our AI doesn't just scan for keywords. It understands the context, impact, and seniority of your experience.",
      icon: BrainCircuit,
      color: "from-blue-500 to-indigo-500",
      bg: "bg-blue-500/10"
    },
    {
      title: "Precision Skill Matching",
      description: "Instantly compare your actual skills against any job description to reveal exactly what hiring managers want.",
      icon: Target,
      color: "from-accent to-purple-500",
      bg: "bg-accent/10"
    },
    {
      title: "Actionable Career Roadmaps",
      description: "Get a step-by-step, personalized timeline detailing certifications, projects, and skills needed to land the role.",
      icon: Compass,
      color: "from-emerald-400 to-teal-500",
      bg: "bg-emerald-500/10"
    }
  ];

  const steps = [
    {
      step: "01",
      title: "Upload your CV",
      description: "Securely upload your resume in PDF format. Our AI instantly parses and structures your experience.",
      icon: FileText
    },
    {
      step: "02",
      title: "Define Target Role",
      description: "Paste a specific job description or simply enter your desired job title to set the benchmark.",
      icon: Search
    },
    {
      step: "03",
      title: "Get AI Insights",
      description: "Receive a comprehensive diagnostic report, complete with a match score, missing skills, and a growth roadmap.",
      icon: Sparkles
    }
  ];

  return (
    <MainLayout>
      {/* ── Background Elements ── */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10 bg-gray-50/50">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-accent/15 blur-[120px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-indigo-500/10 blur-[120px]" />
      </div>

      {/* ════════════ Hero Section ════════════ */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-gray-200 shadow-sm mb-8"
          >
            <Sparkles className="w-4 h-4 text-accent" />
            <span className="text-sm font-semibold text-gray-800 tracking-wide">Next-Gen Career Intelligence</span>
          </motion.div>

          <motion.h1 
            initial="hidden" animate="visible" variants={fadeUp}
            className="text-5xl md:text-7xl font-black tracking-tight text-gray-900 mb-8 leading-[1.1]"
          >
            Unlock Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent to-indigo-600">Dream Career</span> with AI
          </motion.h1>

          <motion.p 
            initial="hidden" animate="visible" variants={fadeUp} transition={{ delay: 0.1 }}
            className="text-xl md:text-2xl text-gray-600 mb-10 leading-relaxed max-w-3xl mx-auto"
          >
            Stop guessing what hiring managers want. Upload your CV, analyze skill gaps, and get a personalized roadmap to land your next big role.
          </motion.p>

          <motion.div 
            initial="hidden" animate="visible" variants={fadeUp} transition={{ delay: 0.2 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <Link to="/upload" className="w-full sm:w-auto">
              <Button size="lg" className="w-full sm:w-auto h-14 px-8 text-lg group shadow-lg shadow-accent/25 hover:shadow-accent/40 hover:-translate-y-0.5 transition-all">
                Analyze My CV <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
            </Link>
          </motion.div>
        </div>

      </section>

      {/* ════════════ Features Section ════════════ */}
      <section id="features" className="py-24 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20 max-w-3xl mx-auto">
            <h2 className="text-4xl font-bold text-gray-900 mb-6 tracking-tight">Everything you need to level up</h2>
            <p className="text-xl text-gray-600">Powerful, context-aware AI tools designed to give you a definitive competitive edge in the job market.</p>
          </div>
          
          <motion.div 
            variants={staggerContainer} initial="hidden" whileInView="visible" viewport={{ once: true, margin: "-100px" }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {features.map((feature, i) => (
              <motion.div key={i} variants={fadeUp} className="group h-full">
                <Card className="p-8 h-full bg-white/60 backdrop-blur-sm border-gray-200/60 hover:border-transparent hover:shadow-2xl hover:shadow-accent/10 transition-all duration-300 relative overflow-hidden">
                  <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300`} />
                  
                  <div className={`p-4 ${feature.bg} rounded-2xl w-fit mb-8 group-hover:scale-110 transition-transform duration-300`}>
                    <feature.icon className="w-7 h-7 text-gray-900" style={{ stroke: "url(#gradient-accent)" }} />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed text-lg">{feature.description}</p>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </div>
        
        {/* SVG Definition for gradient icons */}
        <svg width="0" height="0">
          <linearGradient id="gradient-accent" x1="100%" y1="100%" x2="0%" y2="0%">
            <stop stopColor="#4f46e5" offset="0%" />
            <stop stopColor="#6366f1" offset="100%" />
          </linearGradient>
        </svg>
      </section>

      {/* ════════════ How it Works ════════════ */}
      <section className="py-24 bg-white border-y border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            
            <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={staggerContainer}>
              <h2 className="text-4xl font-bold text-gray-900 mb-12 tracking-tight">How it works</h2>
              
              <div className="space-y-12 relative">
                <div className="absolute left-[27px] top-8 bottom-8 w-0.5 bg-gray-100 -z-10" />
                
                {steps.map((item, i) => (
                  <motion.div key={i} variants={fadeUp} className="flex gap-8 group">
                    <div className="flex flex-col items-center">
                      <div className="w-14 h-14 rounded-full bg-white border-4 border-gray-50 shadow-sm flex items-center justify-center shrink-0 group-hover:border-accent/20 group-hover:shadow-accent/10 transition-all duration-300">
                        <item.icon className="w-6 h-6 text-accent" />
                      </div>
                    </div>
                    <div className="pt-2">
                      <span className="text-sm font-bold text-accent tracking-widest uppercase mb-1 block">Step {item.step}</span>
                      <h3 className="text-2xl font-bold text-gray-900 mb-3">{item.title}</h3>
                      <p className="text-lg text-gray-600 leading-relaxed">{item.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
   
          </div>
        </div>
      </section>

      {/* ════════════ CTA Section ════════════ */}
      <section className="py-24 relative overflow-hidden">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <Card className="bg-gray-900 text-white p-12 md:p-16 text-center rounded-[2.5rem] overflow-hidden relative shadow-2xl border-none">
            {/* CTA Background Effects */}
            <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/3 w-[500px] h-[500px] bg-accent/40 rounded-full blur-[100px]" />
            <div className="absolute bottom-0 left-0 translate-y-1/2 -translate-x-1/3 w-[400px] h-[400px] bg-purple-500/30 rounded-full blur-[100px]" />
            
            <div className="relative z-10 max-w-3xl mx-auto">
              <h2 className="text-4xl md:text-6xl font-black mb-6 tracking-tight text-white leading-tight">
                Stop guessing. <br/>Start growing.
              </h2>
              <p className="text-gray-300 text-xl mb-12 leading-relaxed">
                Join professionals using AI to pinpoint exactly what hiring managers are looking for and land their dream jobs.
              </p>
              <Link to="/upload">
                <Button size="lg" className="px-12 h-16 text-lg font-bold bg-white text-gray-900 hover:bg-gray-50 hover:scale-105 transition-all shadow-xl shadow-white/10 group">
                  Analyze Your CV Now <ChevronRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </section>
    </MainLayout>
  );
};

export default LandingPage;

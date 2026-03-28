import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import MainLayout from "../layouts/MainLayout";
import Loader from "../components/Loader";
import Card from "../components/Card";
import { Sparkles, Brain, Search, CheckCircle2 } from "lucide-react";

const LoadingPage = () => {
  const [currentStep, setCurrentStep] = useState(0);
  
  const steps = [
    { icon: Search, message: "Analyzing CV content..." },
    { icon: Brain, message: "Matching skills with job requirements..." },
    { icon: Sparkles, message: "Generating personalized recommendations..." },
    { icon: CheckCircle2, message: "Finalizing your career roadmap..." },
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <MainLayout>
      <div className="max-w-xl mx-auto px-4 pt-24 text-center">
        <div className="relative inline-block mb-12">
          <div className="absolute inset-0 bg-accent/20 rounded-full blur-2xl animate-pulse" />
          <div className="relative p-6 bg-white rounded-full shadow-xl">
            <Loader size="lg" className="w-16 h-16" />
          </div>
        </div>

        <h1 className="text-3xl font-bold text-gray-900 mb-8">AI at Work</h1>
        
        <div className="space-y-6">
          {steps.map((step, index) => {
            const Icon = step.icon;
            const isActive = index === currentStep;
            const isCompleted = index < currentStep;

            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ 
                  opacity: isActive || isCompleted ? 1 : 0.3,
                  x: 0,
                  scale: isActive ? 1.05 : 1
                }}
                className={`flex items-center p-4 rounded-xl border transition-all ${
                  isActive 
                    ? "bg-white border-accent shadow-sm" 
                    : isCompleted 
                      ? "bg-gray-50 border-gray-100" 
                      : "bg-transparent border-transparent"
                }`}
              >
                <div className={`p-2 rounded-lg mr-4 ${
                  isActive ? "bg-accent/10 text-accent" : isCompleted ? "bg-green-100 text-green-600" : "text-gray-400"
                }`}>
                  <Icon className="w-5 h-5" />
                </div>
                <p className={`text-lg font-medium ${isActive ? "text-gray-900" : "text-gray-500"}`}>
                  {step.message}
                </p>
                {isCompleted && <CheckCircle2 className="ml-auto w-5 h-5 text-green-500" />}
              </motion.div>
            );
          })}
        </div>
      </div>
    </MainLayout>
  );
};

export default LoadingPage;

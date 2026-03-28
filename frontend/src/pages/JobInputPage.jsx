import React, { useState } from "react";
import { useAnalysis } from "../hooks/useAnalysis";
import MainLayout from "../layouts/MainLayout";
import Card from "../components/Card";
import Button from "../components/Button";
import Textarea from "../components/Textarea";
import { Search, Briefcase } from "lucide-react";

const JobInputPage = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const { submitJob, loading, error } = useAnalysis();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (title.trim().length < 2 || description.trim().length < 50) return;
    submitJob({ title, description });
  };

  return (
    <MainLayout>
      <div className="max-w-3xl mx-auto px-4 pt-12 text-zinc-950">
        <div className="text-center mb-12">
          <div className="inline-flex p-3 bg-accent/10 rounded-xl mb-6">
            <Briefcase className="w-8 h-8 text-accent" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">What's your target role?</h1>
          <p className="text-gray-600">
            Provide the job title and description to see how well you match.
          </p>
        </div>

        <Card className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label className="block text-sm font-semibold text-gray-700">Job Title</label>
              <input
                type="text"
                placeholder="e.g. Senior Software Engineer"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-3 rounded-lg border border-gray-200 focus:ring-2 focus:ring-accent focus:border-transparent outline-none transition-all"
                required
              />
            </div>

            <Textarea
              label="Job Description"
              placeholder="Paste the full job description here..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="min-h-[200px]"
              error={description && description.length < 50 ? "Please provide a more detailed description (min 50 characters)" : null}
            />

            {error && (
              <div className="p-4 bg-red-50 border border-red-100 rounded-lg text-sm text-red-600">
                {error}
              </div>
            )}

            <Button
              type="submit"
              size="lg"
              className="w-full"
              disabled={loading || description.length < 50 || title.length < 2}
            >
              {loading ? "Processing..." : "Continue to Analysis"}
            </Button>
          </form>
        </Card>
        
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
          <button 
            type="button"
            className="p-4 bg-white border border-gray-200 rounded-xl hover:border-accent hover:bg-accent/5 transition-all text-left group"
            onClick={() => {
              setTitle("Senior Frontend Developer");
              setDescription("Senior Frontend Developer with experience in modern JavaScript frameworks, responsive design, and state management.");
            }}
          >
            <p className="text-sm font-bold text-gray-900 mb-1 group-hover:text-accent">Try Example: Frontend dev</p>
            <p className="text-xs text-gray-500">Fast-track with a sample role</p>
          </button>
          <button 
            type="button"
            className="p-4 bg-white border border-gray-200 rounded-xl hover:border-accent hover:bg-accent/5 transition-all text-left group"
            onClick={() => {
              setTitle("Backend Engineer");
              setDescription("Backend Engineer specializing in Python, FastAPI, and Cloud infrastructure. Experience with distributed systems and SQL.");
            }}
          >
            <p className="text-sm font-bold text-gray-900 mb-1 group-hover:text-accent">Try Example: Backend dev</p>
            <p className="text-xs text-gray-500">Fast-track with a sample role</p>
          </button>
        </div>
      </div>
    </MainLayout>
  );
};

export default JobInputPage;

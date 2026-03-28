import React from "react";
import { useAnalysis } from "../hooks/useAnalysis";
import FileUpload from "../components/FileUpload";
import MainLayout from "../layouts/MainLayout";
import Card from "../components/Card";
import Loader from "../components/Loader";

const UploadPage = () => {
  const { upload, loading, error } = useAnalysis();

  return (
    <MainLayout>
      <div className="max-w-3xl mx-auto px-4 pt-12">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Upload your CV</h1>
          <p className="text-gray-600">
            Let's start by analyzing your current profile. Upload your resume in PDF format.
          </p>
        </div>

        <Card className="p-8 md:p-12 relative overflow-hidden">
          {loading && (
            <div className="absolute inset-0 bg-white/80 backdrop-blur-[2px] z-50 flex flex-col items-center justify-center p-6 text-center animate-in fade-in duration-300">
              <Loader size="lg" className="mb-4" />
              <p className="text-gray-900 font-bold text-lg">Analyzing Document</p>
              <p className="text-gray-500 text-sm">Extracting skills and professional history...</p>
            </div>
          )}

          <div className="space-y-6">
            <FileUpload 
              onFileSelect={(file) => file && upload(file)} 
              disabled={loading}
            />
            
            {error && (
              <div className="p-4 bg-red-50 border border-red-100 rounded-lg text-sm text-red-600 animate-in shake-in">
                {error}
              </div>
            )}

            <div className="bg-blue-50/50 p-4 rounded-lg border border-blue-100 translate-y-6">
              <p className="text-sm text-blue-700 leading-relaxed font-medium">
                Privacy Note: Your CV is processed securely and only used for your professional analysis. We don't share your personal data with third parties.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </MainLayout>
  );
};

export default UploadPage;

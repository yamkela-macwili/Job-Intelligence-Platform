import React, { useState, useRef } from "react";
import { Upload, X, FileText, CheckCircle2 } from "lucide-react";
import { cn } from "../services/utils";
import Button from "./Button";

const FileUpload = ({ onFileSelect, accept = ".pdf", maxSize = 10 * 1024 * 1024 }) => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFile = (selectedFile) => {
    setError(null);
    if (!selectedFile) return;

    if (accept && !selectedFile.name.endsWith(".pdf")) {
      setError("Please upload a PDF file.");
      return;
    }

    if (selectedFile.size > maxSize) {
      setError("File size exceeds 10MB limit.");
      return;
    }

    setFile(selectedFile);
    onFileSelect(selectedFile);
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  const onDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => {
    setIsDragging(false);
  };

  const removeFile = () => {
    setFile(null);
    onFileSelect(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="w-full">
      {!file ? (
        <div
          onDrop={onDrop}
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onClick={() => fileInputRef.current?.click()}
          className={cn(
            "relative group cursor-pointer border-2 border-dashed rounded-xl p-12 transition-all flex flex-col items-center justify-center space-y-4",
            isDragging
              ? "border-accent bg-accent/5"
              : "border-gray-200 hover:border-accent hover:bg-gray-50"
          )}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => handleFile(e.target.files[0])}
            accept={accept}
            className="hidden"
          />
          <div className="p-4 bg-accent/5 rounded-full group-hover:scale-110 transition-transform">
            <Upload className="w-8 h-8 text-accent" />
          </div>
          <div className="text-center">
            <p className="text-lg font-medium text-gray-900">
              Click or drag and drop to upload
            </p>
            <p className="text-sm text-gray-500">Only PDF files are supported</p>
          </div>
        </div>
      ) : (
        <div className="p-4 border border-gray-200 rounded-xl bg-white flex items-center justify-between animate-in fade-in slide-in-from-bottom-2">
          <div className="flex items-center space-x-4">
            <div className="p-2 bg-accent/10 rounded-lg">
              <FileText className="w-6 h-6 text-accent" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900 truncate max-w-[200px]">
                {file.name}
              </p>
              <p className="text-xs text-gray-500">
                {(file.size / (1024 * 1024)).toFixed(2)} MB
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-5 h-5 text-green-500" />
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                removeFile();
              }}
              className="text-gray-400 hover:text-red-500 p-1 h-auto"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>
        </div>
      )}
      {error && <p className="mt-2 text-sm text-red-500">{error}</p>}
    </div>
  );
};

export default FileUpload;

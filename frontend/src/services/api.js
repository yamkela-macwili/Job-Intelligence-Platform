import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const uploadCV = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/api/v1/cv/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const submitJobDescription = (data) => {
  return api.post("/api/v1/jobs", data);
};

export const startAnalysis = (cvId, jobId) => {
  return api.post("/api/v1/analysis", { cv_id: cvId, job_id: jobId });
};

export const getAnalysisResults = (id) => {
  return api.get(`/api/v1/analysis/${id}`);
};

export default api;

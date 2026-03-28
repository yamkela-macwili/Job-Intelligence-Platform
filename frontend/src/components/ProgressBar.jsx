import React from "react";
import { motion } from "framer-motion";
import { cn } from "../services/utils";

const ProgressBar = ({ progress, className, ...props }) => {
  return (
    <div
      className={cn("w-full h-2 bg-gray-100 rounded-full overflow-hidden", className)}
      {...props}
    >
      <motion.div
        className="h-full bg-accent"
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.5, ease: "easeOut" }}
      />
    </div>
  );
};

export default ProgressBar;

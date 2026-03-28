import React from "react";
import { cn } from "../services/utils";

const Loader = ({ className, size = "md", ...props }) => {
  const sizes = {
    sm: "w-4 h-4 border-2",
    md: "w-8 h-8 border-3",
    lg: "w-12 h-12 border-4",
  };

  return (
    <div
      className={cn(
        "rounded-full border-accent border-t-transparent animate-spin",
        sizes[size],
        className
      )}
      {...props}
    />
  );
};

export default Loader;

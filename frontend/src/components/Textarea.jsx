import React from "react";
import { cn } from "../services/utils";

const Textarea = React.forwardRef(({ className, label, error, ...props }, ref) => {
  return (
    <div className="w-full space-y-1.5">
      {label && (
        <label className="text-sm font-medium text-gray-700 block">
          {label}
        </label>
      )}
      <textarea
        ref={ref}
        className={cn(
          "w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm transition-all focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent disabled:opacity-50 min-h-[120px]",
          error && "border-red-500 focus:ring-red-500/50 focus:border-red-500",
          className
        )}
        {...props}
      />
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  );
});

Textarea.displayName = "Textarea";

export default Textarea;

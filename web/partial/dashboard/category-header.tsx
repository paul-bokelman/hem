import { Button } from "@/components/ui/button";
import { IconDownload, IconFingerprint, IconRefresh } from "@tabler/icons-react";

export const CategoryHeader = () => {
  return (
    <div className="flex flex-col gap-2">
      <div className="w-full flex items-center justify-between">
        <h2 className="text-2xl font-medium flex items-center gap-2">
          Classical <span className="text-muted-foreground">(BSPR Classical)</span>
        </h2>
        <Button variant="outline">
          <IconDownload /> Download Data
        </Button>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <IconFingerprint className="size-4 text-muted-foreground" />
          <span>518272dee1c8d089c6eecbcc</span>
        </div>
        <div className="flex items-center gap-2">
          <IconRefresh className="size-4 text-muted-foreground" />
          <span>4/2/25 @ 3:02pm</span>
        </div>
      </div>
    </div>
  );
};

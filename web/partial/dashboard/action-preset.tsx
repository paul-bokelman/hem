import { Wrench } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface ActionPresetProps {
  name: string;
  description: string;
}

export const ActionPreset = ({ name, description }: ActionPresetProps) => {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <Badge variant="outline" className="py-2 cursor-default">
            <div className="flex items-center gap-2">
              <Wrench className="text-muted-foreground size-4" /> {name}
            </div>
          </Badge>
        </TooltipTrigger>
        <TooltipContent>
          <p>{description}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
};

import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { ChevronsUpDown } from "lucide-react";
import { IconClipboard } from "@tabler/icons-react";

const formats = ["RT", "RT+", "PSD"];

export const CategoryDataDisplay = () => {
  const [activeFormat, setActiveFormat] = React.useState<string>("RT");

  if (!activeFormat) {
    return null;
  }
  return (
    <div className="w-full flex flex-col gap-4">
      <div className="w-full justify-between flex items-center">
        <h2 className="text-base font-medium">Formatted Data</h2>
      </div>
      <div className="flex items-center gap-2">
        <Input
          type="text"
          value="10s:Classical: C24 playing \+01Dances of Galanta\- by \+04\- /10s:on BSPR Classical"
          disabled
        />
        <Button variant="outline">
          <IconClipboard />
        </Button>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="outline"
              className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
            >
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate text-xs">{activeFormat}</span>
              </div>
              <ChevronsUpDown className="ml-auto" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
            align="end"
            side="bottom"
            sideOffset={4}
          >
            <DropdownMenuLabel className="text-xs text-muted-foreground">Formats</DropdownMenuLabel>
            {formats.map((format) => (
              <DropdownMenuItem key={format} onClick={() => setActiveFormat(format)} className="gap-2 p-2">
                {format}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      {activeFormat === "RT" && <RTCard />}
      {activeFormat === "RT+" && <RTPlusCard />}
      {activeFormat === "PSD" && <PSDCard />}
    </div>
  );
};

const PSDCard = () => {
  return (
    <Card>
      <CardContent>psd</CardContent>
    </Card>
  );
};

const RTCard = () => {
  return (
    <Card>
      <CardContent>rt</CardContent>
    </Card>
  );
};

const RTPlusCard = () => {
  return (
    <Card>
      <CardContent>rt+</CardContent>
    </Card>
  );
};

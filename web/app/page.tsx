"use client";

import React from "react";
import dynamic from "next/dynamic";
import Link from "next/link";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { CircleHelp } from "lucide-react";

const AudioRecorderComponent = dynamic(() => import("@/components/audio-recorder"), {
  ssr: false,
});

const Index = () => {
  return (
    <div className="-mt-6 flex flex-col w-full h-screen items-center justify-center ">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold">Hem</h1>

          <Dialog>
            <DialogTrigger asChild>
              <CircleHelp className="text-muted-foreground size-4 hover:text-white cursor-pointer" />
            </DialogTrigger>
            <DialogContent className="max-w-full">
              <DialogHeader>
                <DialogTitle>What is Hem?</DialogTitle>
                <DialogDescription className="text-sm text-muted-foreground">
                  Hem is your ultimate home assistant, designed to simplify your life. Effortlessly control smart home
                  devices, automate tasks, and create powerful workflows—all with your voice. With a growing plugin
                  ecosystem, Hem empowers developers to expand its capabilities, seamlessly integrating with countless
                  services and devices to make your home truly smart.
                </DialogDescription>
              </DialogHeader>
            </DialogContent>
          </Dialog>
        </div>
        <p className="text-muted-foreground">Effortless Control, Infinite Possibility — Your Home, Your Way.</p>
        <div className="flex items-center justify-between">
          <AudioRecorderComponent />
          <Link href="/dashboard" className="text-sm text-muted-foreground underline hover:text-white">
            Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Index;

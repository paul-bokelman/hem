"use client";

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTrigger } from "@/components/ui/dialog";
import { ActionPreset, Macro, MacroDialogContent } from "@/partial/dashboard";
import { DialogDescription, DialogTitle } from "@radix-ui/react-dialog";
import { CircleHelp, Fingerprint, Plus } from "lucide-react";
import Link from "next/link";

const Dashboard = () => {
  const presetActions = [
    {
      name: "Weather",
      description: "Get the current condition and forecast for a location.",
    },
    {
      name: "Time",
      description: "Retrieve the current time for a specific timezone.",
    },
    {
      name: "Date",
      description: "Retrieve today's date in a specific format.",
    },
    {
      name: "Stock Prices",
      description: "Fetch the latest stock prices for a given company.",
    },
    {
      name: "Crypto Prices",
      description: "Retrieve the current prices of popular cryptocurrencies.",
    },
    {
      name: "Sports Scores",
      description: "Get the latest scores and updates for your favorite sports.",
    },
    {
      name: "Exchange Rates",
      description: "Fetch the latest currency exchange rates.",
    },
  ];

  const macros = [
    {
      name: "Morning",
      prompt: "Give me a morning info summary for today.",
      requiredActions: ["Weather", "Time", "Date"],
      allowOtherActions: false,
    },
    {
      name: "Assets and Portfolio",
      prompt:
        "Tell me about the state of the stock and crypto market. Additionally, tell me if my portfolio is doing well.",
      requiredActions: ["Stock Prices", "Crypto Prices"],
      allowOtherActions: true,
    },
  ];

  return (
    <div className="flex flex-col pt-32 pb-16">
      <Breadcrumb className="mb-4">
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink href="/" asChild>
              <Link href="/">Hem</Link>
            </BreadcrumbLink>
          </BreadcrumbItem>
          <BreadcrumbSeparator />
          <BreadcrumbItem>
            <BreadcrumbPage>Dashboard</BreadcrumbPage>
          </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
      <div className="flex flex-col gap-4">
        <div className="flex items-center gap-2">
          <Fingerprint className="text-muted-foreground size-4" />
          <span className="text-muted-foreground text-sm">3e82de6a-234c-4cd2-a687-1537ef659273</span>
        </div>
        <div className="flex flex-col gap-2 mt-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Actions</h2>
            <Dialog>
              <DialogTrigger asChild>
                <CircleHelp className="text-muted-foreground size-4 hover:text-white cursor-pointer" />
              </DialogTrigger>
              <DialogContent className="max-w-full">
                <DialogHeader>
                  <DialogTitle>What are Actions?</DialogTitle>
                  <DialogDescription className="text-sm text-muted-foreground">
                    Actions are predefined functionalities available by default. They allow you to perform specific
                    tasks involving data retrieval, processing, and interaction with various services. You can use these
                    actions to create macros or trigger them directly through voice commands.
                  </DialogDescription>
                </DialogHeader>
              </DialogContent>
            </Dialog>
          </div>
          <p className="text-muted-foreground text-sm">Built-in actions we provide to build your own macros.</p>
          <div className="flex items-center gap-2 flex-wrap border border-dashed rounded-md p-2 bg-background">
            {presetActions.map((action) => (
              <ActionPreset key={action.name} name={action.name} description={action.description} />
            ))}
          </div>
        </div>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" className="mt-2 w-fit">
              <Plus />
              Create Custom Action
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-full">
            <DialogHeader>
              <DialogTitle>Coming Soon...</DialogTitle>
              <DialogDescription className="text-sm text-muted-foreground">
                In the near future, you will have the capability to create and publish custom actions to our
                marketplace, enabling integration with your own APIs or datasets. These custom actions will be
                accessible within macros and can be triggered through voice commands, offering enhanced flexibility and
                functionality.
              </DialogDescription>
            </DialogHeader>
          </DialogContent>
        </Dialog>
        <div className="border w-full rounded-full my-4" />
        <div className="flex flex-col gap-2 mt-2">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Macros</h2>
            <Dialog>
              <DialogTrigger asChild>
                <CircleHelp className="text-muted-foreground size-4 hover:text-white cursor-pointer" />
              </DialogTrigger>
              <DialogContent className="max-w-full">
                <DialogHeader>
                  <DialogTitle>What are Macros?</DialogTitle>
                  <DialogDescription className="text-sm text-muted-foreground">
                    Macros are chains of actions that allow you to define multi-stage workflows. They enable quick and
                    complex interactions by combining multiple actions into a single command. A macro consists of
                    required actions and optional actions, allowing you to customize the flow of information and
                    responses. You can create macros using built-in actions or your own custom actions, providing
                    flexibility in how you interact with your home assistant.
                  </DialogDescription>
                </DialogHeader>
              </DialogContent>
            </Dialog>
          </div>
          <p className="text-muted-foreground text-sm">
            Define your own pipelines and multi-stage actions for quick and complex interaction
          </p>
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" className="mt-2 w-fit">
                <Plus />
                Create Macro
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-full">
              <MacroDialogContent />
            </DialogContent>
          </Dialog>
          <div className="mt-2 flex flex-col gap-4">
            {macros.map((macro) => (
              <Macro key={macro.name} {...macro} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

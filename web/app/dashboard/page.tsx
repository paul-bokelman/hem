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
import { ActionPreset, Macro, MacroDialogContent } from "@/partials/dashboard";
import { DialogDescription, DialogTitle } from "@radix-ui/react-dialog";
import { CircleHelp, Fingerprint, Loader, Plus } from "lucide-react";
import Link from "next/link";
import { useUser } from "@/partials/user-context";
import { useUserMacros, useActions } from "@/hooks/api";

const Dashboard = () => {
  const { user } = useUser();
  const { data: actions, isLoading: actionsLoading, isError: actionsError } = useActions();
  const { data: macros, isLoading: macrosLoading, isError: macrosError } = useUserMacros(user?.id || "");

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
          <span className="text-muted-foreground text-sm">{user?.id || "unknown"}</span>
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
            {actionsLoading ? (
              <div className="text-muted-foreground text-sm flex items-center gap-2">
                <Loader className="animate-spin size-4" />
                Loading actions...
              </div>
            ) : actionsError ? (
              <div className="text-red-500 text-sm">Failed to load actions. Please try again later.</div>
            ) : (
              actions?.map((action) => (
                <ActionPreset key={action.name} name={action.name} description={action.description} />
              ))
            )}
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
            {macrosLoading ? (
              <div className="text-muted-foreground text-sm flex items-center gap-2">
                <Loader className="animate-spin size-4" />
                Loading macros...
              </div>
            ) : macrosError ? (
              <div className="text-red-500 text-sm">Failed to load macros. Please try again later.</div>
            ) : macros?.length === 0 ? (
              <div className="text-muted-foreground text-sm">
                No macros found. Create your first macro to get started!
              </div>
            ) : (
              macros?.map((macro) => <Macro key={macro.name} {...macro} />)
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

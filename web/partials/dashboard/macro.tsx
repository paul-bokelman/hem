import React from "react";
import type { Macro as MacroProps } from "@/hooks/api";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { DialogClose, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { IconCircleCheckFilled, IconXboxXFilled } from "@tabler/icons-react";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useUser } from "@/partials/user-context";
import { useCreateMacro, useActions, useDeleteMacro } from "@/hooks/api";
import { Loader, Trash2 } from "lucide-react";
import { toast } from "sonner";

export const Macro = ({ id, name, prompt, required_actions, allow_other_actions }: MacroProps) => {
  const { user } = useUser();
  const { mutate } = useDeleteMacro();

  const handleDelete = () => {
    if (!user) {
      console.error("No user found. Cannot delete macro.");
      return;
    }

    mutate(
      { macro_id: id, user_id: user.id },
      {
        onSuccess: () => {
          toast.success("Macro deleted successfully!");
        },
        onError: (error) => {
          console.error("Error deleting macro:", error);
          toast.error("Failed to delete macro. Please try again.");
        },
      }
    );
  };

  return (
    <div className="flex flex-col gap-2">
      <h3 className="font-semibold">{name}</h3>
      <div className="flex flex-col gap-2 rounded-md border p-4 bg-muted-foreground/5">
        <div className="flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <h4 className="italic text-muted-foreground text-sm">Prompt</h4>
            <Trash2 onClick={handleDelete} className="text-red-500 size-4 hover:text-red-600" />
          </div>
          <p className="">{prompt}</p>
        </div>
        <div className="flex flex-col gap-2 mt-2">
          <h4 className="text-sm text-muted-foreground italic">Required Actions</h4>
          <div className="flex items-center gap-2 flex-wrap">
            {required_actions.map((action) => (
              <Badge key={action.id} variant="outline" className="text-sm">
                {action.name}
              </Badge>
            ))}
          </div>
        </div>
        <div className="flex flex-row items-center gap-2 mt-2">
          <h4 className="text-sm">Allow Other Actions:</h4>
          {allow_other_actions ? (
            <IconCircleCheckFilled className="text-green-400 size-4" />
          ) : (
            <IconXboxXFilled className="text-red-400 size-4" />
          )}
        </div>
      </div>
    </div>
  );
};

const macroFormSchema = z.object({
  name: z.string().min(1, { message: "Name is required" }).max(50, { message: "Name must be less than 50 characters" }),
  prompt: z
    .string()
    .min(20, { message: "Prompt must be at least 20 characters" })
    .max(500, { message: "Prompt must be less than 500 characters" }),
  required_actions: z.array(z.string()),
  allow_other_actions: z.boolean(),
});

export const MacroDialogContent = () => {
  const { user } = useUser();
  const createMacro = useCreateMacro(user?.id || "");
  const { data: actions, isLoading: actionsLoading, isError: actionsError } = useActions(); // Fetch actions dynamically

  const form = useForm({
    resolver: zodResolver(macroFormSchema),
    defaultValues: {
      name: "",
      prompt: "",
      required_actions: [],
      allow_other_actions: false,
    },
  });

  const handleSubmission = (data: z.infer<typeof macroFormSchema>) => {
    if (!user) {
      console.error("No user found. Cannot create macro.");
      return;
    }

    createMacro.mutate(
      {
        name: data.name,
        prompt: data.prompt,
        allow_other_actions: data.allow_other_actions,
        required_actions: data.required_actions,
      },
      {
        onSuccess: () => {
          toast.success("Macro created successfully!");
          form.reset();
          document.getElementById("dialog-close-button")?.click();
        },
        onError: (error) => {
          console.error("Error creating macro:", error);
          toast.error("Failed to create macro. Please try again.");
        },
      }
    );
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmission)} className="space-y-4">
        <DialogHeader>
          <DialogTitle>Create Macro</DialogTitle>
          <DialogDescription>Create a customized macro from a prompt and actions</DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-4 py-2">
          <FormField
            control={form.control}
            name="name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Name</FormLabel>
                <FormControl>
                  <Input placeholder="A name for your macro. Ex: 'Asset Prices'" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="prompt"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Prompt</FormLabel>
                <FormControl>
                  <Textarea
                    placeholder="A prompt explaining what you want the macro to do. Ex: 'Tell me about crypto and stock prices and add the data to my google spreadsheet.'"
                    className="min-h-32"
                    {...field}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="required_actions"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Required Actions</FormLabel>
                <div className="flex flex-col gap-2">
                  {actionsLoading ? (
                    <div className="text-muted-foreground text-sm flex items-center gap-2">
                      <Loader className="animate-spin size-4" />
                      Loading actions...
                    </div>
                  ) : actionsError ? (
                    <div className="text-red-500 text-sm">Failed to load actions. Please try again later.</div>
                  ) : (
                    <>
                      <div className="flex items-center gap-2 flex-wrap border border-dashed rounded-md p-2 bg-muted-foreground/5">
                        {field.value.length !== 0 ? (
                          field.value.map((action: string) => (
                            <Badge
                              key={action}
                              variant="default"
                              className="cursor-pointer"
                              onClick={() => field.onChange(field.value.filter((a: string) => a !== action))}
                            >
                              {actions?.find((a) => a.id.toString() === action)?.name || action}
                            </Badge>
                          ))
                        ) : (
                          <p className="text-muted-foreground text-sm">
                            No actions selected, click an action to add it.
                          </p>
                        )}
                      </div>
                      <div className="flex items-center gap-2 flex-wrap">
                        {actions
                          ?.filter((action) => !field.value.includes(action.id.toString()))
                          .map((action) => (
                            <Badge
                              key={action.id}
                              variant="outline"
                              className="cursor-pointer"
                              onClick={() => field.onChange([...field.value, action.id.toString()])}
                            >
                              {action.name}
                            </Badge>
                          ))}
                      </div>
                    </>
                  )}
                </div>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="allow_other_actions"
            render={({ field }) => (
              <FormItem className="flex items-center space-x-2">
                <FormControl>
                  <Switch id="allow_other_actions" checked={field.value} onCheckedChange={field.onChange} />
                </FormControl>
                <FormLabel htmlFor="allow_other_actions">Allow Other Actions</FormLabel>
              </FormItem>
            )}
          />
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button id="dialog-close-button" variant="outline">
              Cancel
            </Button>
          </DialogClose>
          <Button type="submit" disabled={createMacro.isLoading}>
            {createMacro.isLoading ? "Saving..." : "Save"}
          </Button>
        </DialogFooter>
      </form>
    </Form>
  );
};

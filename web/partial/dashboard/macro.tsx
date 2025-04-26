import React from "react";
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

interface MacroProps {
  name: string;
  prompt: string;
  requiredActions: string[];
  allowOtherActions: boolean;
}

export const Macro = ({ name, prompt, requiredActions, allowOtherActions }: MacroProps) => {
  return (
    <div className="flex flex-col gap-2">
      <h3 className="font-semibold">{name}</h3>
      <div className="flex flex-col gap-2 rounded-md border p-4 bg-muted-foreground/5">
        <div className="flex flex-col gap-2">
          <h4 className="italic text-muted-foreground text-sm">Prompt</h4>
          <p className="">{prompt}</p>
        </div>
        <div className="flex flex-col gap-2 mt-2">
          <h4 className="text-sm text-muted-foreground italic">Required Actions</h4>
          <div className="flex items-center gap-2 flex-wrap">
            {requiredActions.map((action) => (
              <Badge key={action} variant="outline" className="text-sm">
                {action}
              </Badge>
            ))}
          </div>
        </div>
        <div className="flex flex-row items-center gap-2 mt-2">
          <h4 className="text-sm">Allow Other Actions:</h4>
          {allowOtherActions ? (
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
  requiredActions: z.array(z.string()),
  allowOtherActions: z.boolean(),
});

export const MacroDialogContent = () => {
  const allActions = ["Weather", "Stock Prices", "Crypto Prices"];

  const form = useForm({
    resolver: zodResolver(macroFormSchema),
    defaultValues: {
      name: "",
      prompt: "",
      requiredActions: [],
      allowOtherActions: false,
    },
  });

  const handleSubmission = (data: z.infer<typeof macroFormSchema>) => {
    console.log(data);
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
            name="requiredActions"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Required Actions</FormLabel>
                <div className="flex flex-col gap-2">
                  <div className="flex items-center gap-2 flex-wrap border border-dashed rounded-md p-2 bg-muted-foreground/5">
                    {field.value.length !== 0 ? (
                      field.value.map((action: string) => (
                        <Badge
                          key={action}
                          variant="default"
                          className="cursor-pointer"
                          onClick={() => field.onChange(field.value.filter((a: string) => a !== action))}
                        >
                          {action}
                        </Badge>
                      ))
                    ) : (
                      <p className="text-muted-foreground text-sm">No actions selected, click an action to add it.</p>
                    )}
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    {allActions
                      .filter((action) => !field.value.includes(action))
                      .map((action) => (
                        <Badge
                          key={action}
                          variant="outline"
                          className="cursor-pointer"
                          onClick={() => field.onChange([...field.value, action])}
                        >
                          {action}
                        </Badge>
                      ))}
                  </div>
                </div>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="allowOtherActions"
            render={({ field }) => (
              <FormItem className="flex items-center space-x-2">
                <FormControl>
                  <Switch id="allowOtherActions" checked={field.value} onCheckedChange={field.onChange} />
                </FormControl>
                <FormLabel htmlFor="allowOtherActions">Allow Other Actions</FormLabel>
              </FormItem>
            )}
          />
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button type="submit">Save</Button>
        </DialogFooter>
      </form>
    </Form>
  );
};

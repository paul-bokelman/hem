"use client";

import * as React from "react";
import { ColumnDef, flexRender, getCoreRowModel, getPaginationRowModel, useReactTable } from "@tanstack/react-table";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { IconDotsVertical, IconPlus } from "@tabler/icons-react";
import { Badge } from "../../components/ui/badge";

const data: Destination[] = [
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
  {
    id: "m5gr84i9",
    callsign: "HERCULES",
    format: "RT",
    "ip:port": "192.168.104.144:10001",
    status: "online",
  },
];

export type Destination = {
  id: string;
  callsign: string;
  format: string;
  "ip:port": string;
  status: string;
};

export const columns: ColumnDef<Destination>[] = [
  {
    accessorKey: "callsign",
    header: () => <div className="ml-1">Callsign</div>,
    cell: ({ row }) => <div className="ml-1">{row.getValue("callsign")}</div>,
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => (
      <Badge variant="outline" className="text-muted-foreground px-1.5 flex items-center">
        <div
          className={`rounded-full ${
            row.original.status === "online"
              ? "bg-green-400"
              : row.original.status === "error"
              ? "bg-red-400"
              : "bg-muted-foreground"
          } size-2`}
        />
        {row.original.status}
      </Badge>
    ),
  },
  {
    accessorKey: "format",
    header: "Format",
    cell: ({ row }) => <div className="capitalize">{row.getValue("format")}</div>,
  },
  {
    accessorKey: "ip:port",
    header: "IP:Port",
    cell: ({ row }) => (
      <a
        className="hover:underline"
        href={`http://${row.getValue("ip:port")}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        {row.getValue("ip:port")}
      </a>
    ),
  },
  {
    id: "actions",
    cell: () => (
      <DropdownMenu>
        <div className="w-full flex justify-end">
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className="data-[state=open]:bg-muted text-muted-foreground flex size-8"
              size="icon"
            >
              <IconDotsVertical />
              <span className="sr-only">Open menu</span>
            </Button>
          </DropdownMenuTrigger>
        </div>
        <DropdownMenuContent align="end" className="w-32">
          <DropdownMenuItem>Edit</DropdownMenuItem>
          <DropdownMenuItem>Enable</DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem variant="destructive">Delete</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    ),
  },
];

export const CategoryDestinationTable = () => {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <div className="w-full">
      <div className="w-full justify-between flex items-center mb-4">
        <h2 className="text-base font-medium">Destinations</h2>
        <Button variant="outline" size="sm">
          <IconPlus />
          <span className="hidden lg:inline">Add Destination</span>
        </Button>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center">
                  No destinations found.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="flex-1 text-sm text-muted-foreground">
          Showing {table.getRowModel().rows.length} of {table.getCoreRowModel().rows.length} total destinations
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button variant="outline" size="sm" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>
            Next
          </Button>
        </div>
      </div>
    </div>
  );
};

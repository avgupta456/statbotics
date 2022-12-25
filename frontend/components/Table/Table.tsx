"use client";

import React, { useState } from "react";

import {
  ColumnDef,
  SortingState,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";

const Table = (
  data: any[],
  columns: ColumnDef<any, any>[],
  paginate: boolean,
  headerClassName: (header: any) => string,
  rowClassName: (row: any) => string,
  cellClassName: (cell: any) => string
) => {
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useReactTable({
    data: data,
    columns,
    state: {
      sorting,
      pagination: paginate ? { pageIndex: 0, pageSize: 50 } : undefined,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  const pageIndex = table.getState().pagination.pageIndex;
  const pageSize = table.getState().pagination.pageSize;
  const numRows = data.length;

  return (
    <div className="p-2 text-xs text-sm">
      <table>
        <thead className="border-b-2">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <th key={header.id} colSpan={header.colSpan} className={headerClassName(header)}>
                    {header.isPlaceholder ? null : (
                      <div
                        {...{
                          className: header.column.getCanSort() ? "cursor-pointer select-none" : "",
                          onClick: header.column.getToggleSortingHandler(),
                        }}
                      >
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {{
                          asc: " 🔼",
                          desc: " 🔽",
                        }[header.column.getIsSorted() as string] ?? null}
                      </div>
                    )}
                  </th>
                );
              })}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id} className={rowClassName(row)}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className={cellClassName(cell)}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {paginate && (
        <div className="w-full flex justify-center gap-8 mt-2">
          <div className="flex gap-2">
            <div className="flex items-center">Rows per page:</div>
            <select
              value={table.getState().pagination.pageSize}
              onChange={(e) => {
                table.setPageSize(Number(e.target.value));
              }}
            >
              {[
                { dispSize: 10, pageSize: 10 },
                { dispSize: 25, pageSize: 25 },
                { dispSize: 50, pageSize: 50 },
                { dispSize: 100, pageSize: 100 },
                { dispSize: "All", pageSize: data.length },
              ].map((x) => (
                <option key={x.pageSize} value={x.pageSize}>
                  {x.dispSize}
                </option>
              ))}
            </select>
          </div>
          <span className="flex items-center gap-1">
            <div>{`${pageIndex * pageSize + 1} - ${Math.min(
              (pageIndex + 1) * pageSize,
              numRows
            )} of ${numRows}`}</div>
          </span>
          <div>
            <button
              className="border rounded p-1"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              {"<"}
            </button>
            <button
              className="border rounded p-1"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              {">"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Table;

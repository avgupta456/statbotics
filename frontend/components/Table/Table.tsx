"use client";

import React, { useState } from "react";
import Select from "react-select";

import {
  ColumnDef,
  SortingState,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";

import { classnames } from "../../utils";

const Table = ({
  data,
  columns,
  paginate,
  headerClassName,
  headerCellClassName,
  rowClassName,
  cellClassName,
}: {
  data: any[];
  columns: ColumnDef<any, any>[];
  paginate: boolean;
  headerClassName: () => string;
  headerCellClassName: (header: any) => string;
  rowClassName: (row: any) => string;
  cellClassName: (cell: any) => string;
}) => {
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useReactTable({
    data: data,
    columns,
    initialState: {
      pagination: {
        pageSize: 10,
      },
    },
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  const pageIndex = table.getState().pagination.pageIndex;
  const pageSize = table.getState().pagination.pageSize;
  const numRows = data.length;

  const pageOptions: any = [
    { value: 10, label: 10 },
    { value: 25, label: 25 },
    { value: 50, label: 50 },
    { value: 100, label: 100 },
  ];

  const colSpans = table.getHeaderGroups()[0].headers.map((header) => header.colSpan);
  const cumColSpans = colSpans
    .reduce((acc, curr) => [...acc, curr + (acc[acc.length - 1] ?? 0)], [])
    .slice(0, -1);

  const showColDividers = table.getHeaderGroups().length > 1;

  return (
    <div className="text-sm">
      <table>
        <thead className={headerClassName()}>
          {table.getHeaderGroups().map((headerGroup, i) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header, j) => {
                return (
                  <th
                    key={header.id}
                    colSpan={header.colSpan}
                    className={classnames(
                      headerCellClassName(header),
                      showColDividers &&
                        i === 0 &&
                        j !== cumColSpans.length &&
                        "border-r-2 border-double border-gray-300",
                      showColDividers &&
                        i !== 0 &&
                        cumColSpans.includes(j + 1) &&
                        "border-r-2 border-double border-gray-300"
                    )}
                  >
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
              {row.getVisibleCells().map((cell, j) => (
                <td
                  key={cell.id}
                  className={classnames(
                    cellClassName(cell),
                    showColDividers &&
                      cumColSpans.includes(j + 1) &&
                      "border-r-2 border-double border-gray-300"
                  )}
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {paginate && numRows > 10 && (
        <div className="w-full h-10 flex items-center justify-center gap-2 mt-4 text-xs">
          <div className="flex gap-2">
            <div className="flex items-center">Rows / Page:</div>
            <Select
              instanceId="paginate-select"
              menuPlacement="top"
              className="w-20"
              styles={{
                menu: (provided) => ({ ...provided, zIndex: 9999 }),
              }}
              options={pageOptions}
              onChange={(e) => table.setPageSize(Number((e as any).value))}
              value={{
                value: table.getState().pagination.pageSize,
                label: table.getState().pagination.pageSize,
              }}
            />
          </div>
          <span className="w-24 flex items-center gap-1">
            <div>{`${pageIndex * pageSize + 1} - ${Math.min(
              (pageIndex + 1) * pageSize,
              numRows
            )} of ${numRows}`}</div>
          </span>
          <div>
            <button
              className={classnames(
                "border rounded py-1 px-2 mr-2",
                !table.getCanPreviousPage() ? "opacity-50" : ""
              )}
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              {"<"}
            </button>
            <button
              className={classnames(
                "border rounded py-1 px-2",
                !table.getCanNextPage() ? "opacity-50" : ""
              )}
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

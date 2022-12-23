import React from "react";

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  ColumnDef,
} from "@tanstack/react-table";

const Table = (
  data: any[],
  columns: ColumnDef<any, any>[],
  headerClassName: (header: any) => string,
  rowClassName: (row: any) => string,
  cellClassName: (cell: any) => string
) => {
  const cleanData = data.map((row) => {
    // replace null with "N/A"
    Object.keys(row).forEach((key) => {
      if (row[key] === null) {
        row[key] = "N/A";
      }
    });
    return row;
  });

  const table = useReactTable({
    data: cleanData,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="p-2 text-xxs lg:text-xs">
      <table>
        <thead className="border-b-2">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id} className="lg:text-sm">
              {headerGroup.headers.map((header) => {
                return (
                  <th
                    key={header.id}
                    colSpan={header.colSpan}
                    className={headerClassName(header)}
                  >
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
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
        <tfoot>
          {table.getFooterGroups().map((footerGroup) => (
            <tr key={footerGroup.id}>
              {footerGroup.headers.map((header) => (
                <th key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.footer,
                        header.getContext()
                      )}
                </th>
              ))}
            </tr>
          ))}
        </tfoot>
      </table>
    </div>
  );
};

export default Table;

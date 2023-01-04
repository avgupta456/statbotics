"use client";

import React, { useState } from "react";
import { CSVLink } from "react-csv";
import { DebounceInput } from "react-debounce-input";
import { MdClose, MdCloudDownload, MdColorLens, MdSearch } from "react-icons/md";

import { ColumnDef } from "@tanstack/react-table";

import { classnames } from "../../utils";
import Table from "./Table";
import { TableKey } from "./shared";

const InsightsTable = ({
  data,
  columns,
  leftCol,
  rightCol,
  searchCols,
  csvFilename,
  toggleDisableHighlight,
}: {
  data: any[];
  columns: ColumnDef<any, any>[];
  leftCol: string;
  rightCol: string;
  searchCols: string[];
  csvFilename: string;
  toggleDisableHighlight: () => void;
}) => {
  const [showSearch, setShowSearch] = useState(false);
  const [search, setSearch] = useState("");

  const filteredData = data.filter((row) =>
    searchCols.some((col) => row[col].toString().toLowerCase().includes(search.toLowerCase()))
  );

  const headerClassName = () => "border-b-2 border-gray-800";

  const headerCellClassName = (header: any) =>
    classnames(
      "w-28 px-4 py-2",
      header.id === leftCol ? "rounded-tl-lg" : "",
      header.id === rightCol ? "rounded-tr-lg" : ""
    );

  const rowClassName = (row: any) => classnames("text-center h-full hover:bg-blue-100");

  const cellClassName = (cell: any) =>
    classnames(
      cell.column.id === "team" ? "w-40 py-2 truncate" : "w-28 py-2",
      cell.row.index === data.length - 1 && cell.column.id === leftCol ? "rounded-bl-lg" : "",
      cell.row.index === data.length - 1 && cell.column.id === rightCol ? "rounded-br-lg" : ""
    );

  return (
    <div className="text-sm">
      <div className="w-full px-2 py-1 flex items-center justify-center">
        <div className="flex-grow">
          {showSearch ? (
            <div className="flex">
              <DebounceInput
                minLength={2}
                debounceTimeout={300}
                className="max-w-60 p-2 relative rounded text-sm border-[2px] border-inputBlue focus:outline-none"
                placeholder="Search"
                onChange={(e) => setSearch(e.target.value)}
              />
              <MdClose
                className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer"
                onClick={() => {
                  setSearch("");
                  setShowSearch(!showSearch);
                }}
              />
            </div>
          ) : (
            <div className="text-lg text-gray-800">Team Insights</div>
          )}
        </div>
        <div className="tooltip" data-tip="Search">
          <MdSearch
            className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer"
            onClick={() => setShowSearch(!showSearch)}
          />
        </div>
        <div className="tooltip" data-tip="Toggle Highlight">
          <MdColorLens
            className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer"
            onClick={toggleDisableHighlight}
          />
        </div>
        <div className="tooltip" data-tip="Download CSV">
          <CSVLink data={data} filename={csvFilename}>
            <MdCloudDownload className="w-10 h-10 p-2 ml-2 rounded-lg hover:bg-gray-100 text-gray-500 hover:text-blue-600 text-2xl cursor-pointer" />
          </CSVLink>
        </div>
      </div>
      <div className="h-2" />
      <Table
        data={filteredData}
        columns={columns}
        paginate={true}
        headerClassName={headerClassName}
        headerCellClassName={headerCellClassName}
        rowClassName={rowClassName}
        cellClassName={cellClassName}
      />
      <TableKey />
    </div>
  );
};

export default InsightsTable;

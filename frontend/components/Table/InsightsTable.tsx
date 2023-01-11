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
  includeKey = true,
}: {
  data: any[];
  columns: ColumnDef<any, any>[];
  leftCol: string;
  rightCol: string;
  searchCols: string[];
  csvFilename: string;
  toggleDisableHighlight?: () => void;
  includeKey?: boolean;
}) => {
  const [showSearch, setShowSearch] = useState(false);
  const [search, setSearch] = useState("");

  const filteredData = data.filter((row) =>
    searchCols.some((col) => row[col].toString().toLowerCase().includes(search.toLowerCase()))
  );

  const headerClassName = () => "border-b-2 border-gray-800";

  const headerCellClassName = (header: any) =>
    classnames(
      "px-4 py-2",
      header.id === leftCol ? "rounded-tl-lg" : "",
      header.id === rightCol ? "rounded-tr-lg" : ""
    );

  const rowClassName = (row: any) =>
    classnames(
      "text-center h-full hover:bg-blue-100",
      row?.original?.record === "0-0-0" ? "bg-yellow-50" : ""
    );

  const cellClassName = (cell: any) =>
    classnames(
      "py-2",
      cell.row.index === data.length - 1 && cell.column.id === leftCol ? "rounded-bl-lg" : "",
      cell.row.index === data.length - 1 && cell.column.id === rightCol ? "rounded-br-lg" : ""
    );

  return (
    <div className="w-full lg:w-fit lg:max-w-full text-sm mb-4">
      <div className="w-full px-2 py-1 flex items-center justify-center">
        <div className="flex-grow">
          {showSearch ? (
            <div className="flex">
              <DebounceInput
                minLength={2}
                debounceTimeout={300}
                className="w-36 md:w-60 p-2 relative rounded text-sm border-[2px] border-inputBlue focus:outline-none"
                placeholder="Search"
                onChange={(e) => setSearch(e.target.value)}
              />
              <MdClose
                className="hover_icon ml-2"
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
          <MdSearch className="hover_icon ml-2" onClick={() => setShowSearch(!showSearch)} />
        </div>
        {toggleDisableHighlight && (
          <div className="tooltip" data-tip="Toggle Highlight">
            <MdColorLens className="hover_icon ml-2" onClick={toggleDisableHighlight} />
          </div>
        )}
        <div className="tooltip" data-tip="Download CSV">
          <CSVLink data={filteredData} filename={csvFilename}>
            <MdCloudDownload className="hover_icon ml-2" />
          </CSVLink>
        </div>
      </div>
      <div className="h-2" />
      <div className="overflow-x-scroll overflow-y-hidden scrollbar-hide">
        <Table
          data={filteredData}
          columns={columns}
          paginate={true}
          headerClassName={headerClassName}
          headerCellClassName={headerCellClassName}
          rowClassName={rowClassName}
          cellClassName={cellClassName}
        />
      </div>
      {includeKey && <TableKey />}
    </div>
  );
};

export default InsightsTable;

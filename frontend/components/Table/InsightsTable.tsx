"use client";

import React, { useState } from "react";
import { CSVLink } from "react-csv";
import { DebounceInput } from "react-debounce-input";
import { MdAdd, MdClose, MdCloudDownload, MdColorLens, MdRemove, MdSearch } from "react-icons/md";

import { ColumnDef } from "@tanstack/react-table";

import { classnames } from "../../utils";
import Table from "./Table";
import { TableKey } from "./shared";

const InsightsTable = ({
  title,
  data,
  columns,
  detailedData = [],
  detailedColumns = [],
  searchCols,
  csvFilename,
  toggleDisableHighlight,
  includeKey = true,
}: {
  title: string;
  data: any[];
  columns: ColumnDef<any, any>[];
  detailedData?: any[];
  detailedColumns?: ColumnDef<any, any>[];
  searchCols: string[];
  csvFilename: string;
  toggleDisableHighlight?: () => void;
  includeKey?: boolean;
}) => {
  const [showSearch, setShowSearch] = useState(false);
  const [search, setSearch] = useState("");

  const [expanded, setExpanded] = useState(false);

  const expandable = detailedData?.length > 0;
  const currData = expanded ? detailedData : data;
  const currColumns = expanded ? detailedColumns : columns;

  const filteredData = currData.filter((row) =>
    searchCols.some((col) => row[col].toString().toLowerCase().includes(search.toLowerCase()))
  );

  const headerClassName = () => "border-b-2 border-gray-800";

  const headerCellClassName = (header: any) => classnames("px-1 md:px-2 py-2");

  const rowClassName = (row: any) =>
    classnames(
      "text-center h-14 md:hover:bg-blue-100",
      row?.original?.record === "0-0-0" ? "bg-yellow-50" : ""
    );

  const cellClassName = (cell: any) => classnames("py-2");

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
            <div className="text-lg text-gray-800">{title}</div>
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
        {expandable && (
          <div className="tooltip" data-tip={expanded ? "Shrink" : "Expand"}>
            <MdAdd
              className="hover_icon ml-2"
              onClick={() => setExpanded(!expanded)}
              style={{ display: expanded ? "none" : "block" }}
            />
            <MdRemove
              className="hover_icon ml-2"
              onClick={() => setExpanded(!expanded)}
              style={{ display: expanded ? "block" : "none" }}
            />
          </div>
        )}
      </div>
      <div className="h-2" />
      <div className="overflow-x-scroll overflow-y-hidden scrollbar-hide">
        <Table
          data={filteredData}
          columns={currColumns}
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

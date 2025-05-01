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
  title = null,
  data,
  columns,
  detailedData = [],
  detailedColumns = [],
  searchCols = [],
  toggleDisableHighlight = undefined,
}: {
  title?: string | null | undefined;
  data: any[];
  columns: ColumnDef<any, any>[];
  detailedData?: any[];
  detailedColumns?: ColumnDef<any, any>[];
  searchCols?: string[];
  toggleDisableHighlight?: () => void;
}) => {
  const [showSearch, setShowSearch] = useState(false);
  const [search, setSearch] = useState("");

  const [expanded, setExpanded] = useState(false);

  const hasTitle = title !== undefined && title !== null && title !== "";
  const expandable = detailedData?.length > 0;
  const searchable = searchCols?.length > 0;
  const currData = expanded ? detailedData : data;
  const currColumns = expanded ? detailedColumns : columns;

  const filteredData = searchable
    ? currData.filter((row) =>
      searchCols.some((col) => row[col].toString().toLowerCase().includes(search.toLowerCase()))
    )
    : currData.filter((row) =>
      Object.values(row).some((value) => value.toString().toLowerCase().includes(search.toLowerCase()))
    );

  const headerClassName = () => "border-b-2 border-gray-800";

  const headerCellClassName = (header: any) => classnames("px-1 md:px-2 py-2");

  const rowClassName = (row: any) =>
    classnames(
      "text-center h-14 md:hover:bg-blue-100",
      row?.original?.next_event_key && row?.original?.record === "0-0-0" && "bg-yellow-50", // teams page
      row?.original?.first_event && row?.original?.rank === -1 && "bg-yellow-50" // event page
    );

  const cellClassName = (cell: any) => classnames("py-2");

  return (
    <div className="w-full md:w-fit md:max-w-full text-sm mb-4">
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
            hasTitle && (
              <div className="text-lg text-gray-800 font-bold">{title}</div>
            )
          )}
        </div>
        {searchable && (<div className="tooltip" data-tip="Search">
          <MdSearch className="hover_icon ml-2" onClick={() => setShowSearch(!showSearch)} />
        </div>)
        }
        {toggleDisableHighlight && (
          <div className="tooltip" data-tip="Toggle Highlight">
            <MdColorLens className="hover_icon ml-2" onClick={toggleDisableHighlight} />
          </div>
        )}
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
      {toggleDisableHighlight && <TableKey />}
    </div>
  );
};

export default InsightsTable;

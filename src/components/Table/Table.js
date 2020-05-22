import React from 'react';
import MUIDataTable from "mui-datatables";

export default function ReactTable({data}) {

  const options = {
  filterType: 'checkbox',
  resizeableColumns: true
  };

  const columns = [
    {
      name: "Number",
      label: "number",
      options: {
        filter: false,
        sort: true,
      }
    },
    {
      name: "Name",
      label: "name",
      options: {
        filter: false,
        sort: true,
      }
    },
    {
      name: "ELO",
      label: "elo",
      options: {
        filter: false,
        sort: true,
      }
    },
    {
      name: "ELO Recent",
      label: "elo_recent",
      options: {
        filter: false,
        sort: true,
      }
    },
    {
      name: "ELO Mean",
      label: "elo_mean",
      options: {
        filter: false,
        sort: true,
      }
    },
    {
      name: "ELO Max",
      label: "elo_max",
      options: {
        filter: false,
        sort: true,
      }
    },
  ]

  console.log(data)
  return (
    <MUIDataTable
      title={"Team List"}
      data={data}
      columns={columns}
      options={options}
    />
  )
}

import React from 'react';
import MUIDataTable from "mui-datatables";

export default function ReactTable({columns, data}) {

  const options = {
  filterType: 'multiselect',
  responsive: 'scrollMaxHeight',
  rowsPerPageOptions: [10, 20, 50],

  };

  return (
    <MUIDataTable
      title={"Team List"}
      data={data}
      columns={columns}
      options={options}
    />
  )
}

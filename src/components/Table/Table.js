import React from 'react';
import MUIDataTable from "mui-datatables";
import createMuiTheme from '@material-ui/core/styles/createMuiTheme';
import {ThemeProvider as MuiThemeProvider} from '@material-ui/core/styles';

const getMuiTheme = () => createMuiTheme({
  overrides: {
    MuiTableCell: {
      root: {
        width: "200px",
        padding: "10px 16px",
        textAlign: "center",
        '@media (max-width: 700px)': {
          padding: "5px 8px",
        }
      }
    },
    MUIDataTableHeadCell: {
      fixedHeaderCommon: {
        backgroundColor: "#3f51b5",
      },

      sortAction: {
        margin: "auto",
        marginTop: "6px",
        color: "white",
        '& path': {  color: "white" },
      },

      sortActive: {
        color: "white",
      },

      data: {
        color: "white",
      },

      hintIconAlone: {
        marginTop: "6px",
        color: "white"
      },

      hintIconWithSortIcon: {
        marginTop: "6px",
         color: "white"
       },
    },
  },
});

export default function ReactTable({title, columns, data}) {
  const theme = getMuiTheme();

  const options = {
    filter: false,
    print: false,
    responsive: 'scrollFullHeight',
    rowsPerPageOptions: [10, 20, 50],
    selectableRows: "none",
    fixedHeaderOptions: {
      xAxis: false,
      yAxis: true
    },
    elevation: 1,
  };

  const new_columns = columns.map(
    function([name, searchable, visible, filterable, hint]) {
      return {
        label: `${name}`,
        options: {
          sort: true,
          filter: `${filterable}`==="true",
          searchable: `${searchable}`==="true",
          display: `${visible}`==="true",
          hint: hint
        },
      }
    }
  );

  return (
    <MuiThemeProvider theme={theme}>
      <MUIDataTable
        title={title}
        data={data}
        columns={new_columns}
        options={options}
      />
    </MuiThemeProvider>
  )
}

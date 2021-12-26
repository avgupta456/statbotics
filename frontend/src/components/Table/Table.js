import React from "react";
import MUIDataTable from "mui-datatables";
import createMuiTheme from "@material-ui/core/styles/createMuiTheme";
import { ThemeProvider as MuiThemeProvider } from "@material-ui/core/styles";

import styles from "./Table.module.css";

const getMuiTheme = () =>
  createMuiTheme({
    overrides: {
      MuiTableCell: {
        root: {
          width: "200px",
          padding: "10px 16px",
          textAlign: "center",
          "@media (max-width: 700px)": {
            padding: "10px 8px",
          },
        },
      },
      MUIDataTable: {
        paper: {
          minHeight: "375px",
        },
      },
      MUIDataTableHeadCell: {
        fixedHeader: {
          backgroundColor: "#3f51b5",
        },

        sortAction: {
          margin: "auto",
          marginTop: "6px",
          color: "white",
          "& path": { color: "white" },
        },

        sortActive: {
          color: "white",
        },

        data: {
          color: "white",
        },

        hintIconAlone: {
          marginTop: "6px",
          color: "white",
        },

        hintIconWithSortIcon: {
          marginTop: "6px",
          color: "white",
        },
      },
    },
  });

export default function ReactTable({ title, columns, data }) {
  const theme = getMuiTheme();
  const options = {
    filter: false,
    print: false,
    responsive: "ScrollFullHeight",
    rowsPerPageOptions: [10, 20, 50],
    selectableRows: "none",
    fixedHeaderOptions: {
      xAxis: false,
      yAxis: true,
    },
    elevation: 0,
    textLabels: {
      body: {
        noMatch: "Data on the way, hang tight!",
      },
    },
  };

  const new_columns = columns.map(function ([
    name,
    searchable,
    visible,
    link,
    hint,
  ]) {
    var dict = {
      name: `${name}`,
      label: `${name}`,
      options: {
        sort: true,
        filter: "false",
        searchable: `${searchable}` === "true",
        display: `${visible}` === "true",
        viewColumns: `${visible}` === "true",
        hint: hint,
      },
    };

    if (link) {
      dict["options"]["customBodyRender"] = (value, tableMeta, updateValue) => {
        const link = value.split("|")[0].trim();
        const display = value.split("|")[1].trim();
        return <a href={`${link}`}>{display}</a>;
      };
    }

    return dict;
  });

  const newData = data.map((row) => row.map((value) => value || -1));

  return (
    <MuiThemeProvider theme={theme}>
      <div className={styles.table}>
        <MUIDataTable
          title={title}
          data={newData}
          columns={new_columns}
          options={options}
        />
      </div>
    </MuiThemeProvider>
  );
}

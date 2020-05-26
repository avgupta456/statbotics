import React from 'react';
import MUIDataTable from "mui-datatables";
import createMuiTheme from '@material-ui/core/styles/createMuiTheme';
import {ThemeProvider as MuiThemeProvider} from '@material-ui/core/styles';

class ReactTable extends React.Component {

  getMuiTheme = () => createMuiTheme({
    overrides: {
      MUIDataTableFilterList: {
        root: {
          marginBottom: "10px",
        },
      },
      MuiTableCell: {
        root: {
          width: "200px",
          padding: "10px 16px",
          textAlign: "center",
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

  render() {
    const options = {
      filter: false,
      responsive: 'scrollMaxHeight',
      rowsPerPageOptions: [10, 20, 50],
      selectableRows: "none",
      fixedHeaderOptions: {
        xAxis: false,
        yAxis: true
      },
      elevation: 1,
    };

    const new_columns = this.props.columns.map(
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
      <MuiThemeProvider theme={this.getMuiTheme()}>
        <MUIDataTable
          title={this.props.title}
          data={this.props.data}
          columns={new_columns}
          options={options}
        />
      </MuiThemeProvider>
    )
  }
}

export default ReactTable;

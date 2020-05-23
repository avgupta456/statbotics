import React from 'react';
import MUIDataTable from "mui-datatables";
import createMuiTheme from '@material-ui/core/styles/createMuiTheme';
import {ThemeProvider as MuiThemeProvider} from '@material-ui/core/styles';

class ReactTable extends React.Component {

  getMuiTheme = () => createMuiTheme({
    overrides: {
      MuiTableCell: {
        root: {
          width: "200px",
          padding: "10px 16px",
        }
      },
      MUIDataTableHeadCell: {
        fixedHeaderCommon: {
          backgroundColor: "#3f51b5",
        },

        sortAction: {
          marginTop: "6px",
          color: "white",
          '& path': {  color: "white" }
        },
        sortActive: { color: "white", },
        data: { color: "white", },
      },
    },
  });

  render() {
    const options = {
      filterType: 'multiselect',
      responsive: 'scrollMaxHeight',
      rowsPerPageOptions: [10, 20, 50],
      selectableRows: "none",
      fixedHeaderOptions: {
        xAxis: false,
        yAxis: true
      },
    };

    const new_columns = this.props.columns.map(
      function([name, searchable, visible, filterable]) {
        return {
          label: `${name}`,
          options: {
            sort: true,
            filter: `${filterable}`==="true",
            searchable: `${searchable}`,
            display: `${visible}`,
          },
        }
      }
    );
    
    return (
      <MuiThemeProvider theme={this.getMuiTheme()}>
        <MUIDataTable
          title={"Team List"}
          data={this.props.data}
          columns={new_columns}
          options={options}
        />
      </MuiThemeProvider>
    )
  }
}

export default ReactTable;

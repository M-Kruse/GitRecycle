import React, { Component } from "react";
import { Table } from "reactstrap";
import { Button } from "reactstrap";
import { Badge } from "reactstrap";
import { Header } from "reactstrap";
import BootstrapTable from 'react-bootstrap-table-next';

import axios from "axios";

import { API_URL_BASE } from "../constants";

const endpoint_query = `${API_URL_BASE}/api/query/`

const token = process.env.REACT_APP_GITRECYCLE_AUTH_TOKEN;

class QueryList extends Component {
  state = {
    queries: [],
    
  };

  componentDidMount() {
    this.resetState();
  }

  getQueries = () => {
      axios.get(endpoint_query, { headers: {authorization : `Token ${token}`}}).then(res => this.setState({ queries: res.data }));
  };

  resetState = () => {
    this.getQueries();
  };

  render() {
    const queries = this.state.queries;
    
    return (
      <Table size="sm">
        <thead>
          <tr>
            <th>String</th>
            <th>Language</th>
            <th>Time Limit</th>
          </tr>
        </thead>
        <tbody>
          {!queries || queries.length <= 0 ? (
            <tr>
              <td colSpan="1" align="center">
                <b>No Query Data Found</b>
              </td>
            </tr>
          ) : (
            queries.results.map(query => (
              <tr key={query.pk}>
                <td>{query.string}</td>
                <td>{query.language  ? query.language : 'Any'}</td>
                <td>{query.time_limit ? query.time_limit : 'None'}</td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default QueryList;

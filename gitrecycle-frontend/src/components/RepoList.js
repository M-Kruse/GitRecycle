import React, { Component } from "react";
import { Table } from "reactstrap";
import { Button } from "reactstrap";
import { Badge } from "reactstrap";
import { Header } from "reactstrap";
import BootstrapTable from 'react-bootstrap-table-next';
  
class RepoList extends Component {
  render() {
    const repos = this.props.repos;
    return (
      <Table size="sm">
        <thead>
          <tr>
            <th>URL</th>
            <th>Create Date</th>
            <th>Last Checked</th>
            <th>Archived</th>
            <th>Missing</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!repos || repos.length <= 0 ? (
            <tr>
              <td colSpan="1" align="center">
                <b>No Repo Data Found</b>
              </td>
            </tr>
          ) : (
            repos.results.map(repo => (
              <tr key={repo.pk}>
                <td>{repo.url}</td>
                <td>{repo.create_date}</td>
                <td>{repo.last_checked}</td>
                <td><Badge href="#" color={repo.archived ? 'success' : 'warning'}> {String(repo.archived)} </Badge> </td>
                <td><Badge href="#" color={repo.missing ? 'success' : 'warning'}> {String(repo.missing)} </Badge> </td>
                <td><Button color="primary" size="sm">Detail</Button>{' '}</td>
                <td></td>

              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default RepoList;

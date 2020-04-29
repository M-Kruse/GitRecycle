import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import RepoList from "./RepoList";

import axios from "axios";

import { API_URL_MISSING } from "../constants";

const token = process.env.REACT_APP_GITRECYCLE_AUTH_TOKEN;

class Home extends Component {
  state = {
    repos: []
  };

  componentDidMount() {
    this.resetState();
  }

  getRepos = () => {
    axios.get(API_URL_MISSING, { headers: {authorization : `Token ${token}`}}).then(res => this.setState({ repos: res.data }));
  };

  resetState = () => {
    this.getRepos();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <RepoList
              repos={this.state.repos}
              resetState={this.resetState}
            />
          </Col>
        </Row>

      </Container>
    );
  }
}

export default Home;
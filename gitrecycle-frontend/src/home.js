import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import RepoList from "./RepoList";

import axios from "axios";

import { API_URL } from "../constants";

class Home extends Component {
  state = {
    repos: []
  };

  componentDidMount() {
    this.resetState();
  }

  getStudents = () => {
    axios.get(API_URL).then(res => this.setState({ repos: res.data }));
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
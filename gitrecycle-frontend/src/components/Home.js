import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import RepoList from "./RepoList";
import Header from "./Header";

class Home extends Component {

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Header />
      </Container>
    );
  }
}

export default Home;
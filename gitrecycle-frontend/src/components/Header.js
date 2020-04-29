import React, { Component } from "react";
import { Col, Container, Row, Jumbotron, Button } from "reactstrap";

import logo from '../assets/img/GitRecycle-Logo.png'; // with import

class Header extends Component {
  render() {
    return (
      <div className="text-center">
    
            <div>
      <Jumbotron>
        <img
          alt="GitRecycleLogo"
          src={logo}
          width="300"
          className="img-thumbnail"
          style={{ marginTop: "20px" }}
        />
        <h1 className="display-3">GitRecycle</h1>
        <p className="lead"> This is a project to monitor Github for repos that go from public to being missing in a period of time.</p>
        <hr className="my-2" />
        <p> Keywords are used as queries to search Github and results are saved. A time limit is set. If the repo goes missing within the timeframe, it is flagged for review. If not, it is deleted.</p>
        <p className="lead">
          <Button href="https://github.com/M-Kruse/GitRecycle" color="primary">Learn More</Button>
        </p>
      </Jumbotron>
    </div>
      </div>
    );
  }
}

export default Header;